import streamlit as st
import json
import re
import time
from urllib.parse import urljoin

import httpx

from backend.scanner.request_engine import (
    send_request,
    set_base_url,
    get_base_url
)

from backend.models.finding import Finding

from backend.results.scan_results import (
    get_findings,
    clear_findings,
    add_finding
)




st.set_page_config(
    page_title="SentinelAPI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.markdown(
    """
    <style>
    .stApp {
        background: #ffffff !important;
        color: #172033;
    }

    /* Clean white workspace while keeping colorful cards */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #ffffff !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,.92) !important;
        border-bottom: 1px solid #e8edf5;
    }

    /* Main text outside the designed cards */
    .stMarkdown, .stCaption, label {
        color: #172033;
    }
    [data-testid="stHeader"] { background: rgba(255,255,255,.92) !important; border-bottom: 1px solid #e8edf5; }
    [data-testid="stMainBlockContainer"] {
        max-width: 1480px;
        padding-top: 1.1rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#111936 0%,#0b1830 55%,#091526 100%);
        border-right: 1px solid #30446d;
    }
    [data-testid="stSidebar"] * { color: #edf4ff; }
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {
        color:#b8c7dc !important;
    }
    [data-testid="stSidebar"] label {
        color:#f1f5f9 !important;
        font-weight:650;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background: #091427 !important;
        border: 1px solid #3b5280 !important;
        border-radius: 12px !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 30px 32px;
        border-radius: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(96,165,250,.32);
        background: linear-gradient(135deg,#1d285d,#092e4b 55%,#261747);
        box-shadow: 0 20px 55px rgba(0,0,0,.28);
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 240px; height: 240px;
        right: -70px; top: -90px;
        border-radius: 50%;
        background: radial-gradient(circle,rgba(34,211,238,.28),transparent 68%);
    }
    .hero-badge {
        display: inline-flex;
        padding: 7px 12px;
        border-radius: 999px;
        color: #bbf7d0;
        background: rgba(34,197,94,.12);
        border: 1px solid rgba(74,222,128,.32);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: .8px;
        margin-bottom: 12px;
    }
    .main-title {
        font-size: clamp(34px,4vw,52px);
        line-height: 1;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;
        background: linear-gradient(90deg,#fff,#67e8f9 45%,#a78bfa 80%,#f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle { font-size:15px;color:#b5c8e2;margin:10px 0 20px; }
    .info-box {
        padding:13px 16px;
        border-radius:13px;
        background:rgba(6,182,212,.09);
        border:1px solid rgba(34,211,238,.28);
        color:#d9f7ff;
    }

    .step-row {
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:12px;
        margin:0 0 24px;
    }
    .step {
        padding:15px 16px;
        border-radius:15px;
        border:1px solid #d7deea;
        background:linear-gradient(145deg,#ffffff,#f8fbff);
        box-shadow:0 8px 22px rgba(31,41,55,.08);
        transition:.18s ease;
    }
    .step:hover { transform:translateY(-3px); box-shadow:0 14px 28px rgba(31,41,55,.13); }
    .step-num {
        display:inline-flex;
        width:29px;height:29px;
        align-items:center;justify-content:center;
        border-radius:50%;
        color:white;font-weight:900;margin-right:8px;
    }
    .s1 .step-num { background:linear-gradient(135deg,#06b6d4,#2563eb); }
    .s2 .step-num { background:linear-gradient(135deg,#8b5cf6,#ec4899); }
    .s3 .step-num { background:linear-gradient(135deg,#f59e0b,#ef4444); }
    .s4 .step-num { background:linear-gradient(135deg,#22c55e,#14b8a6); }
    .step-title { color:#172033;font-weight:850;font-size:14px; }
    .step-text { color:#52627a;font-size:11px;margin-top:7px;line-height:1.4; }
    .s1 { border-top:4px solid #06b6d4; }
    .s2 { border-top:4px solid #8b5cf6; }
    .s3 { border-top:4px solid #f59e0b; }
    .s4 { border-top:4px solid #22c55e; }

    .section-title {
        font-size:23px;
        font-weight:900;
        color:#172033;
        margin:8px 0 5px;
        letter-spacing:-.3px;
    }
    .section-caption {
        color:#52627a;
        font-size:13px;
        margin-bottom:14px;
    }
    .section-bar {
        height:4px;width:70px;border-radius:999px;margin:5px 0 15px;
        background:linear-gradient(90deg,#22d3ee,#6366f1,#ec4899);
    }

    .process-card {
        padding:20px 21px;
        border-radius:18px;
        margin-bottom:15px;
        border:1px solid #dbe4ef;
        background:linear-gradient(145deg,#ffffff,#f8fbff);
        box-shadow:0 11px 28px rgba(31,41,55,.10);
    }
    .process-icon { font-size:27px;margin-bottom:8px; }
    .process-card h3 { color:#172033;margin:0 0 5px;font-size:17px; }
    .process-card p { color:#52627a;margin:0;font-size:12px;line-height:1.55; }
    .process-icon { filter:saturate(1.25); }
    .upload-card { border-top:4px solid #06b6d4; background:linear-gradient(135deg,#ecfeff,#ffffff); }
    .scan-card { border-top:4px solid #f59e0b; background:linear-gradient(135deg,#fff7ed,#ffffff); }
    .findings-card { border-top:4px solid #ef4444; background:linear-gradient(135deg,#fff1f2,#ffffff); }
    .export-card { border-top:4px solid #22c55e; background:linear-gradient(135deg,#f0fdf4,#ffffff); }

    .metric-card {
        min-height:125px;
        padding:19px;
        border-radius:17px;
        border:1px solid #dbe4ef;
        box-shadow:0 8px 22px rgba(15,23,42,.08);
        transition:.18s ease;
        position:relative; overflow:hidden;
    }
    .metric-card:hover { transform:translateY(-3px); box-shadow:0 14px 30px rgba(15,23,42,.13); }
    .metric-card:after { content:""; position:absolute; width:80px; height:80px; right:-22px; top:-25px; border-radius:50%; background:rgba(255,255,255,.65); }
    .metric-blue {
        background:linear-gradient(135deg,#ecfeff,#eff6ff);
        border-color:#67e8f9;
    }
    .metric-purple {
        background:linear-gradient(135deg,#f5f3ff,#fdf4ff);
        border-color:#c4b5fd;
    }
    .metric-red {
        background:linear-gradient(135deg,#fff1f2,#fff7f7);
        border-color:#fda4af;
    }
    .metric-orange {
        background:linear-gradient(135deg,#fff7ed,#fffbeb);
        border-color:#fdba74;
    }
    .metric-label {
        color:#475569 !important;
        font-size:11px;
        font-weight:850;
        text-transform:uppercase;
        letter-spacing:.8px;
    }
    .metric-value {
        color:#172033 !important;
        font-size:34px;
        line-height:1.1;
        font-weight:900;
        margin-top:9px;
    }
    .metric-note {
        color:#64748b !important;
        font-size:11px;
        margin-top:4px;
    }

    .risk-panel {
        padding:19px 22px;
        border-radius:18px;
        background:linear-gradient(135deg,#f5f3ff 0%,#eef2ff 48%,#ecfeff 100%);
        border:1px solid #a78bfa;
        box-shadow:0 10px 26px rgba(79,70,229,.13);
        margin:10px 0 17px;
        position:relative; overflow:hidden;
    }
    .risk-panel:after { content:""; position:absolute; right:-35px; top:-45px; width:130px; height:130px; border-radius:50%; background:radial-gradient(circle,#c4b5fd88,transparent 70%); }
    .risk-number { font-size:30px;font-weight:900;color:#5b21b6; }
    .mini-label {
        color:#6d28d9;
        font-size:11px;
        font-weight:850;
        text-transform:uppercase;
        letter-spacing:.8px;
    }

    /* =========================================================
       FINAL SCAN RESULT CARDS
       Light, colorful and high-contrast - no heavy black blocks.
       ========================================================= */
    .finding-card {
        padding:22px 24px;
        border-radius:18px;
        margin:0 0 16px;
        background:#ffffff;
        box-shadow:0 8px 24px rgba(15,23,42,.08);
        border:1px solid #e2e8f0;
        color:#1e293b !important;
    }

    .finding-card h3 {
        color:#172033 !important;
        font-size:19px;
        font-weight:900;
        margin:0 0 10px;
    }

    .finding-card div {
        color:#334155 !important;
        line-height:1.65;
        font-size:13px;
    }

    .finding-card b {
        color:#172033 !important;
        font-weight:850;
    }

    .finding-card code {
        color:#075985 !important;
        background:#e0f2fe !important;
        border:1px solid #bae6fd;
        padding:4px 8px;
        border-radius:6px;
        font-weight:700;
    }

    /* Severity-specific backgrounds */
    .finding-card.high {
        border:1px solid #fecaca;
        border-left:7px solid #ef4444;
        background:linear-gradient(135deg,#fff5f5 0%,#ffffff 55%);
    }

    .finding-card.medium {
        border:1px solid #fed7aa;
        border-left:7px solid #f59e0b;
        background:linear-gradient(135deg,#fffaf0 0%,#ffffff 55%);
    }

    .finding-card.low {
        border:1px solid #bbf7d0;
        border-left:7px solid #22c55e;
        background:linear-gradient(135deg,#f2fff7 0%,#ffffff 55%);
    }

    .severity-pill {
        display:inline-flex;
        align-items:center;
        padding:6px 13px;
        border-radius:999px;
        font-size:11px;
        font-weight:900;
        letter-spacing:.7px;
    }

    .pill-high {
        color:#b91c1c !important;
        background:#fee2e2;
        border:1px solid #fca5a5;
    }

    .pill-medium {
        color:#b45309 !important;
        background:#fef3c7;
        border:1px solid #fbbf24;
    }

    .pill-low {
        color:#15803d !important;
        background:#dcfce7;
        border:1px solid #86efac;
    }

    /* Result section filter */
    .result-filter-label {
        color:#172033 !important;
        font-weight:800;
    }

    /* Reproduction / PoC area */
    [data-testid="stExpander"] {
        border:1px solid #dbe4ef !important;
        border-radius:12px !important;
        background:#f8fafc !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color:#172033 !important;
        font-weight:750 !important;
    }

    /* Code blocks stay readable instead of becoming muddy black */
    [data-testid="stCodeBlock"] {
        border:1px solid #cbd5e1 !important;
        border-radius:10px !important;
    }

    .stTextInput input,
    .stSelectbox [data-baseweb="select"],
    .stFileUploader section {
        background:#ffffff !important;
        color:#172033 !important;
        border:1px solid #cbd5e1 !important;
        border-radius:12px !important;
    }
    .stTextInput input::placeholder {
        color:#64748b !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        color:#172033 !important;
    }
    .stFileUploader section {
        padding:14px !important;
        color:#334155 !important;
    }
    .stFileUploader section * {
        color:#334155 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background:#f8fafc !important;
        border:2px dashed #94a3b8 !important;
        border-radius:12px !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color:#334155 !important;
    }
    .stButton > button,.stDownloadButton > button {
        min-height:46px;border-radius:12px;font-weight:850;color:white;
        border:1px solid rgba(255,255,255,.15);
        background:linear-gradient(135deg,#2563eb,#7c3aed,#db2777);
        box-shadow:0 9px 23px rgba(79,70,229,.24);
        transition:.18s ease;
    }
    .stButton > button:hover,.stDownloadButton > button:hover {
        transform:translateY(-2px);
        box-shadow:0 13px 30px rgba(99,102,241,.35);
        border-color:#93c5fd;
    }
    
    /* Theme-safe expander: never fall back to unreadable dark text/background */
    [data-testid="stExpander"] {
        border:1px solid #cbd5e1 !important;
        border-radius:12px !important;
        background:#ffffff !important;
        color:#172033 !important;
    }
    [data-testid="stAlert"] { border-radius:12px; }
    [data-testid="stAlert"] p {
        font-weight:650;
    }
    [data-testid="stDataFrame"] {
        border:1px solid #cbd5e1;
        border-radius:15px;
        overflow:hidden;
        background:#ffffff;
    }
    [data-testid="stDataFrame"] * {
        color:#172033 !important;
    }
    [data-testid="stProgressBar"] > div > div { border-radius:999px; }
    hr {
        border-color: #e5eaf2 !important;
    }
    .target-box {
        padding:14px 16px;
        border-radius:12px;
        border:1px solid #22b8d5;
        background:linear-gradient(135deg,#ecfeff,#eff6ff,#f5f3ff);
        color:#155e75;
        font-family:monospace;
        font-weight:650;
        overflow-x:auto;
        box-shadow:0 6px 18px rgba(6,182,212,.08);
    }
    /* =========================================================
       THEME-SAFE VISIBILITY LAYER
       Keeps every important label readable even when Streamlit
       browser/app theme is switched to Dark.
       ========================================================= */

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background:#ffffff !important;
        color:#172033 !important;
    }

    /* Sidebar: dark navy remains, but ALL text stays bright */
    [data-testid="stSidebar"] {
        background:linear-gradient(180deg,#0b1733 0%,#102552 52%,#142d5c 100%) !important;
        color:#ffffff !important;
        border-right:2px solid #31548c !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {
        color:#f8fbff !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {
        color:#c9d8ef !important;
    }

    /* =========================================================
       SIDEBAR INPUTS — LIGHT, CLEAR AND THEME-SAFE
       The input box itself, its BaseWeb wrapper, placeholder and
       password-eye area all stay light/readable in Light + Dark.
       ========================================================= */
    [data-testid="stSidebar"] .stTextInput [data-baseweb="input"],
    [data-testid="stSidebar"] .stTextInput [data-baseweb="base-input"],
    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="base-input"] {
        background:#f8fbff !important;
        border:2px solid #6ea8ff !important;
        border-radius:12px !important;
        box-shadow:0 2px 8px rgba(37,99,235,.10) !important;
    }

    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] [data-baseweb="input"] input,
    [data-testid="stSidebar"] [data-baseweb="base-input"] input {
        background:#f8fbff !important;
        color:#111827 !important;
        -webkit-text-fill-color:#111827 !important;
        caret-color:#2563eb !important;
        font-weight:600 !important;
    }

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder,
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color:#64748b !important;
        opacity:1 !important;
        -webkit-text-fill-color:#64748b !important;
    }

    /* Password eye / input action area */
    [data-testid="stSidebar"] [data-baseweb="input"] > div,
    [data-testid="stSidebar"] [data-baseweb="base-input"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] button {
        background:#f8fbff !important;
        color:#334155 !important;
        border-color:#cbd5e1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] svg,
    [data-testid="stSidebar"] [data-baseweb="base-input"] svg {
        color:#334155 !important;
        fill:#334155 !important;
        stroke:#334155 !important;
    }

    /* =========================================================
       OPENAPI FILE UPLOADER — REMOVE BLACK BUTTON
       ========================================================= */
    [data-testid="stFileUploaderDropzone"] {
        background:#f8fbff !important;
        border:2px dashed #7dd3fc !important;
        border-radius:14px !important;
        color:#172033 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background:linear-gradient(135deg,#e0f2fe,#dbeafe) !important;
        color:#075985 !important;
        -webkit-text-fill-color:#075985 !important;
        border:1px solid #60a5fa !important;
        border-radius:10px !important;
        font-weight:800 !important;
        box-shadow:0 4px 12px rgba(37,99,235,.12) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background:linear-gradient(135deg,#bae6fd,#bfdbfe) !important;
        color:#0c4a6e !important;
        -webkit-text-fill-color:#0c4a6e !important;
        border-color:#3b82f6 !important;
    }

    [data-testid="stFileUploaderDropzone"] button *,
    [data-testid="stFileUploaderDropzone"] svg {
        color:#075985 !important;
        fill:#075985 !important;
        stroke:#075985 !important;
    }

    [data-testid="stFileUploaderDropzone"] section,
    [data-testid="stFileUploaderDropzone"] section * {
        color:#334155 !important;
        -webkit-text-fill-color:#334155 !important;
    }

    /* Sidebar checkbox/radio labels */
    [data-testid="stSidebar"] [role="checkbox"],
    [data-testid="stSidebar"] [role="radio"],
    [data-testid="stSidebar"] [data-baseweb="checkbox"] label,
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        color:#f8fbff !important;
    }

    /* Main-page native Streamlit controls stay readable in BOTH themes */
    .stTextInput input,
    .stTextArea textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    .stSelectbox [data-baseweb="select"],
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] section {
        background:#ffffff !important;
        color:#172033 !important;
        -webkit-text-fill-color:#172033 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    [data-baseweb="input"] input::placeholder,
    [data-baseweb="textarea"] textarea::placeholder {
        color:#64748b !important;
        opacity:1 !important;
        -webkit-text-fill-color:#64748b !important;
    }

    /* Selectbox text and dropdown menu */
    .stSelectbox [data-baseweb="select"] *,
    [data-baseweb="select"] input,
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"] {
        color:#172033 !important;
    }

    [data-baseweb="popover"],
    [role="listbox"] {
        background:#ffffff !important;
    }

    /* Native labels/captions */
    .stMarkdown, .stCaption, label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] * {
        color:#172033 !important;
    }

    /* Keep designed dark hero text intentionally bright */
    .hero, .hero * {
        color:inherit;
    }
    .hero .subtitle { color:#dbeafe !important; }
    .hero .info-box { color:#e0f7ff !important; }

    /* Alerts: readable in both Light and Dark Streamlit themes */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div {
        font-weight:650 !important;
    }

    /* Code blocks: high contrast regardless of selected theme */
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code {
        color:#e2e8f0 !important;
    }

    /* Dataframe text remains dark on its white surface */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] * {
        color:#172033 !important;
    }

    /* Progress bar is visible in dark/light mode */
    [data-testid="stProgressBar"] > div {
        background:#e2e8f0 !important;
    }
    [data-testid="stProgressBar"] > div > div {
        background:linear-gradient(90deg,#06b6d4,#6366f1,#ec4899) !important;
    }

    /* Dark-mode fallback selectors used by Streamlit/browser theme */
    @media (prefers-color-scheme: dark) {
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background:#ffffff !important;
            color:#172033 !important;
        }
        .stMarkdown, .stCaption, label,
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] * {
            color:#172033 !important;
        }
        [data-testid="stSidebar"] {
            background:linear-gradient(180deg,#0b1733 0%,#102552 52%,#142d5c 100%) !important;
        }
        [data-testid="stSidebar"] input {
            background:#ffffff !important;
            color:#111827 !important;
            -webkit-text-fill-color:#111827 !important;
        }
    }

    /* =========================================================
       FINAL OVERRIDE — FORCE READABILITY AFTER STREAMLIT THEME
       ========================================================= */
    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="base-input"] {
        background:#f8fbff !important;
        border:2px solid #6ea8ff !important;
        color:#111827 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] input,
    [data-testid="stSidebar"] [data-baseweb="base-input"] input {
        background:#f8fbff !important;
        color:#111827 !important;
        -webkit-text-fill-color:#111827 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] input::placeholder,
    [data-testid="stSidebar"] [data-baseweb="base-input"] input::placeholder {
        color:#64748b !important;
        -webkit-text-fill-color:#64748b !important;
        opacity:1 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"] button,
    [data-testid="stSidebar"] [data-baseweb="base-input"] button {
        background:#f8fbff !important;
        color:#334155 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background:#e0f2fe !important;
        color:#075985 !important;
        -webkit-text-fill-color:#075985 !important;
        border:1px solid #60a5fa !important;
    }

    .footer { text-align:center;padding:26px 10px 8px;color:#68819e;font-size:12px; }
    @media (max-width:800px) {
        .step-row { grid-template-columns:1fr 1fr; }
        .hero { padding:23px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)




if "scan_report" not in st.session_state:
    st.session_state.scan_report = None

if "uploaded_endpoint_count" not in st.session_state:
    st.session_state.uploaded_endpoint_count = 0

if "uploaded_endpoints" not in st.session_state:
    st.session_state.uploaded_endpoints = []

if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://127.0.0.1:8000"




st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">● SECURITY SCANNER · ACTIVE</div>
        <div class="main-title">🛡️ SentinelAPI</div>
        <div class="subtitle">
            Zero-Trust API Vulnerability Scanner · OpenAPI-driven security analysis
        </div>
        <div class="info-box">
            🔐 Use this scanner only with APIs you own, control, or are explicitly authorized to test.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <div class="step-row">
        <div class="step s1">
            <span class="step-num">1</span><span class="step-title">Configure</span>
            <div class="step-text">Set API target & authentication</div>
        </div>
        <div class="step s2">
            <span class="step-num">2</span><span class="step-title">Upload</span>
            <div class="step-text">Load OpenAPI / Swagger JSON</div>
        </div>
        <div class="step s3">
            <span class="step-num">3</span><span class="step-title">Scan</span>
            <div class="step-text">Run security vulnerability checks</div>
        </div>
        <div class="step s4">
            <span class="step-num">4</span><span class="step-title">Report</span>
            <div class="step-text">Review findings & export report</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



def normalize_base_url(url):
    if not url:
        return ""

    return url.rstrip("/")


def get_openapi_server(spec):
    """
    Extract server URL from OpenAPI specification.
    """

    servers = spec.get("servers", [])

    if servers and isinstance(servers, list):

        server = servers[0]

        if isinstance(server, dict):

            url = server.get("url")

            if url:
                return normalize_base_url(url)

    return ""


def extract_endpoints(spec):
    """
    Extract API endpoints and HTTP methods
    from OpenAPI/Swagger specification.
    """

    endpoints = []

    paths = spec.get("paths", {})

    if not isinstance(paths, dict):
        return endpoints

    allowed_methods = {
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "head",
        "options"
    }

    for path, path_data in paths.items():

        if not isinstance(path_data, dict):
            continue

        for method, operation in path_data.items():

            method_lower = method.lower()

            if method_lower not in allowed_methods:
                continue

            if not isinstance(operation, dict):
                operation = {}

            endpoint = {
                "path": path,
                "method": method_lower.upper(),
                "summary": operation.get(
                    "summary",
                    operation.get(
                        "description",
                        ""
                    )
                ),
                "operation_id": operation.get(
                    "operationId",
                    ""
                ),
                "security": operation.get(
                    "security",
                    spec.get("security", [])
                )
            }

            endpoints.append(endpoint)

    return endpoints


def replace_path_parameters(path, value="1"):
    """
    Replace OpenAPI path parameters.

    Example:
    /users/{user_id}
    becomes
    /users/1
    """

    return re.sub(
        r"\{[^}]+\}",
        str(value),
        path
    )


def is_parameterized(path):
    return "{" in path and "}" in path


def endpoint_requires_auth(endpoint):
    """
    Check whether endpoint declares security
    requirements in OpenAPI.
    """

    security = endpoint.get("security")

    if security is None:
        return False

    if security == []:
        return False

    return True


def safe_json(response_text):
    try:
        return json.loads(response_text)
    except Exception:
        return None


def find_sensitive_fields(data, parent=""):
    """
    Recursively search response JSON for
    sensitive fields.
    """

    sensitive_names = [
        "password",
        "password_hash",
        "api_key",
        "token",
        "secret",
        "credit_card",
        "ssn",
        "authorization",
        "access_token",
        "refresh_token"
    ]

    found = []

    if isinstance(data, dict):

        for key, value in data.items():

            key_lower = str(key).lower()

            for sensitive in sensitive_names:

                if sensitive in key_lower:

                    field_name = (
                        f"{parent}.{key}"
                        if parent
                        else str(key)
                    )

                    found.append(field_name)

                    break

            new_parent = (
                f"{parent}.{key}"
                if parent
                else str(key)
            )

            found.extend(
                find_sensitive_fields(
                    value,
                    new_parent
                )
            )

    elif isinstance(data, list):

        for index, item in enumerate(data):

            new_parent = (
                f"{parent}[{index}]"
                if parent
                else f"[{index}]"
            )

            found.extend(
                find_sensitive_fields(
                    item,
                    new_parent
                )
            )

    return list(dict.fromkeys(found))


def create_finding(
    title,
    vulnerability_type,
    severity,
    endpoint,
    description,
    evidence,
    recommendation
):

    finding = Finding(
        title=title,
        vulnerability_type=vulnerability_type,
        severity=severity,
        endpoint=endpoint,
        description=description,
        evidence=evidence,
        recommendation=recommendation
    )

    add_finding(finding)

    return finding


def scan_auth_endpoint(
    endpoint,
    method
):

    result = send_request(
        method=method,
        path=endpoint,
        token=None
    )

    if result["status_code"] == 0:
        return

    if result["status_code"] == 200:

        create_finding(
            title="Missing Authentication",
            vulnerability_type="Authentication Misconfiguration",
            severity="HIGH",
            endpoint=endpoint,
            description=(
                "The endpoint returned a successful response "
                "without an authentication token."
            ),
            evidence=(
                f"{method} {endpoint} returned "
                f"HTTP {result['status_code']} "
                "without authentication."
            ),
            recommendation=(
                "Require valid authentication before "
                "allowing access to protected resources."
            )
        )


def scan_exposure_endpoint(
    endpoint,
    method,
    token
):

    result = send_request(
        method=method,
        path=endpoint,
        token=token
    )

    if result["status_code"] == 0:
        return

    if result["status_code"] < 200:
        return

    if result["status_code"] >= 300:
        return

    data = safe_json(result["response"])

    if data is None:
        return

    fields = find_sensitive_fields(data)

    if not fields:
        return

    create_finding(
        title="Sensitive Data Exposure",
        vulnerability_type="Excessive Data Exposure",
        severity="HIGH",
        endpoint=endpoint,
        description=(
            "The API response contains fields that may expose "
            "sensitive information."
        ),
        evidence=(
            "Sensitive fields detected: "
            + ", ".join(fields)
        ),
        recommendation=(
            "Return only the minimum data required by the client "
            "and remove sensitive fields from API responses."
        )
    )


def scan_bola_endpoint(
    path,
    method,
    token
):

    if method != "GET":
        return

    if not is_parameterized(path):
        return

    endpoint_one = replace_path_parameters(
        path,
        "1"
    )

    endpoint_two = replace_path_parameters(
        path,
        "2"
    )

    result_one = send_request(
        method="GET",
        path=endpoint_one,
        token=token
    )

    result_two = send_request(
        method="GET",
        path=endpoint_two,
        token=token
    )

    if result_one["status_code"] == 0:
        return

    if result_two["status_code"] == 0:
        return

    if (
        result_one["status_code"] == 200
        and
        result_two["status_code"] == 200
    ):

        create_finding(
            title="Possible Broken Object Level Authorization",
            vulnerability_type="BOLA / IDOR",
            severity="HIGH",
            endpoint=path,
            description=(
                "The same authenticated session was able to "
                "access multiple object identifiers."
            ),
            evidence=(
                f"Authenticated request to {endpoint_one} "
                f"returned HTTP {result_one['status_code']}; "
                f"request to {endpoint_two} returned HTTP "
                f"{result_two['status_code']} using the same token."
            ),
            recommendation=(
                "Verify that the authenticated user owns or has "
                "permission to access the requested object."
            )
        )


def scan_rate_limit_endpoint(
    endpoint,
    method,
    total_requests=10
):

    if method != "POST":
        return

    endpoint_lower = endpoint.lower()

    keywords = [
        "login",
        "signin",
        "auth",
        "token"
    ]

    if not any(
        keyword in endpoint_lower
        for keyword in keywords
    ):
        return

    successful = 0
    rate_limited = 0

    for _ in range(total_requests):

        result = send_request(
            method=method,
            path=endpoint,
            token=None
        )

        status = result["status_code"]

        if status == 429:

            rate_limited += 1

        elif status != 0:

            successful += 1

        time.sleep(0.15)

    if (
        successful == total_requests
        and
        rate_limited == 0
    ):

        create_finding(
            title="Missing Rate Limiting",
            vulnerability_type="Rate Limit Misconfiguration",
            severity="MEDIUM",
            endpoint=endpoint,
            description=(
                "Repeated requests were accepted without "
                "receiving HTTP 429 rate-limit responses."
            ),
            evidence=(
                f"{total_requests} consecutive requests were sent "
                "without a 429 response."
            ),
            recommendation=(
                "Implement rate limiting, especially for "
                "authentication and sensitive endpoints."
            )
        )


def run_dynamic_scan(
    base_url,
    endpoints,
    bearer_token
):

    clear_findings()

    base_url = normalize_base_url(
        base_url
    )

    set_base_url(base_url)

    scan_log = []

    for endpoint_info in endpoints:

        path = endpoint_info["path"]
        method = endpoint_info["method"]

        actual_path = replace_path_parameters(
            path,
            "1"
        )

        scan_log.append(
            f"{method} {actual_path}"
        )

       

        if endpoint_requires_auth(
            endpoint_info
        ):

            scan_auth_endpoint(
                actual_path,
                method
            )

   

        if method == "GET":

            scan_exposure_endpoint(
                actual_path,
                method,
                bearer_token
            )

    

        if (
            method == "GET"
            and
            bearer_token
            and
            is_parameterized(path)
        ):

            scan_bola_endpoint(
                path,
                method,
                bearer_token
            )

      

        if method == "POST":

            scan_rate_limit_endpoint(
                actual_path,
                method
            )

    findings = get_findings()

    high = sum(
        1
        for finding in findings
        if finding.severity == "HIGH"
    )

    medium = sum(
        1
        for finding in findings
        if finding.severity == "MEDIUM"
    )

    low = sum(
        1
        for finding in findings
        if finding.severity == "LOW"
    )

    risk_score = (
        high * 10
        +
        medium * 5
        +
        low * 2
    )

    if risk_score > 100:
        risk_score = 100

    report = {
        "scanner": "SentinelAPI",
        "target": base_url,
        "total_endpoints": len(endpoints),
        "total_vulnerabilities": len(findings),
        "high": high,
        "medium": medium,
        "low": low,
        "risk_score": risk_score,
        "findings": [
            finding.model_dump()
            for finding in findings
        ]
    }

    return report, scan_log


def finding_to_poc(finding):

    endpoint = finding.get(
        "endpoint",
        "/"
    )

    vulnerability = finding.get(
        "vulnerability_type",
        ""
    )

    if "BOLA" in vulnerability or "IDOR" in vulnerability:

        return (
            "GET "
            + endpoint.replace(
                "{user_id}",
                "2"
            )
            + " HTTP/1.1\n"
            "Authorization: Bearer <TOKEN>"
        )

    return (
        f"{finding.get('endpoint', '/')}"
    )




st.sidebar.markdown("## ⚙️ Scanner Configuration")
st.sidebar.caption("Configure your target and scan parameters.")

st.sidebar.markdown("### 🎯 API Target")

manual_base_url = st.sidebar.text_input(
    "API Base URL",
    value=st.session_state.api_base_url,
    help=(
        "Example: http://127.0.0.1:8000"
    )
)

bearer_token = st.sidebar.text_input(
    "Bearer Token",
    value="token-user-1",
    type="password",
    help=(
        "Optional token for authenticated security testing."
    )
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🔎 Vulnerability Classes")

st.sidebar.checkbox(
    "BOLA / IDOR",
    value=True
)

st.sidebar.checkbox(
    "Sensitive Data Exposure",
    value=True
)

st.sidebar.checkbox(
    "Authentication Misconfiguration",
    value=True
)

st.sidebar.checkbox(
    "Rate Limit",
    value=True
)




st.markdown('<div class="section-title">📂 Step 2 · API Specification</div><div class="section-bar"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">Upload an OpenAPI / Swagger JSON file to discover endpoints automatically.</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="process-card upload-card">
        <div class="process-icon">📄</div>
        <h3>Import your API specification</h3>
        <p>Upload an OpenAPI / Swagger JSON file. SentinelAPI discovers routes,
        methods and authentication requirements automatically.</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload OpenAPI JSON file",
    type=["json"],
    help="Upload your OpenAPI or Swagger JSON specification."
)


if uploaded_file is not None:

    try:

        openapi_spec = json.load(
            uploaded_file
        )

        st.success(
            "✅ OpenAPI specification loaded successfully."
        )

    

        detected_server = get_openapi_server(
            openapi_spec
        )

        if detected_server:

            st.session_state.api_base_url = (
                detected_server
            )

            st.info(
                f"🌐 Server detected from OpenAPI: "
                f"`{detected_server}`"
            )

   

        endpoints = extract_endpoints(
            openapi_spec
        )

        st.session_state.uploaded_endpoints = (
            endpoints
        )

        st.session_state.uploaded_endpoint_count = (
            len(endpoints)
        )

        st.success(
            f"🔍 {len(endpoints)} API endpoints detected."
        )

       

        endpoint_rows = []

        for endpoint in endpoints:

            endpoint_rows.append(
                {
                    "Method": endpoint["method"],
                    "Endpoint": endpoint["path"],
                    "Operation ID": endpoint[
                        "operation_id"
                    ],
                    "Authentication": (
                        "Required"
                        if endpoint_requires_auth(
                            endpoint
                        )
                        else "Not declared"
                    )
                }
            )

        if endpoint_rows:

            st.markdown(
                f'<div class="mini-label">🔗 Discovered Endpoints · {len(endpoint_rows)}</div>',
                unsafe_allow_html=True
            )
            st.dataframe(
                endpoint_rows,
                use_container_width=True,
                hide_index=True
            )

    except Exception as error:

        st.error(
            f"❌ Could not parse OpenAPI file: {error}"
        )




st.markdown("---")

st.markdown('<div class="section-title">🚀 Step 3 · Security Scan</div><div class="section-bar"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">Run the configured checks against the discovered API endpoints.</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="process-card scan-card">
        <div class="process-icon">⚡</div>
        <h3>Run the security engine</h3>
        <p>Execute the configured API security checks and generate a structured
        vulnerability report.</p>
    </div>
    """,
    unsafe_allow_html=True
)

scan_button = st.button(
    "🔍 Scan Uploaded API",
    type="primary",
    use_container_width=True
)


if scan_button:

    if uploaded_file is None:

        st.error(
            "❌ Please upload an OpenAPI JSON file first."
        )

    elif not st.session_state.uploaded_endpoints:

        st.error(
            "❌ No API endpoints were found in the uploaded specification."
        )

    else:

        final_base_url = (
            manual_base_url
            or
            st.session_state.api_base_url
        )

        if not final_base_url:

            st.error(
                "❌ API Base URL is required."
            )

        else:

            st.info(
                f"🎯 Scan Target: `{final_base_url}`"
            )

            progress = st.progress(0)

            status_text = st.empty()

            status_text.write(
                "🔄 Starting SentinelAPI scan..."
            )

            progress.progress(10)

            try:

                report, scan_log = run_dynamic_scan(
                    final_base_url,
                    st.session_state.uploaded_endpoints,
                    bearer_token
                )

                progress.progress(100)

                status_text.success(
                    "✅ Scan completed successfully."
                )

                st.session_state.scan_report = (
                    report
                )

            except Exception as error:

                progress.empty()

                st.error(
                    f"❌ Scan failed: {error}"
                )




report = st.session_state.scan_report


if report is not None:

    findings = report.get(
        "findings",
        []
    )

    total_endpoints = report.get(
        "total_endpoints",
        0
    )

    high_count = report.get(
        "high",
        0
    )

    medium_count = report.get(
        "medium",
        0
    )

    low_count = report.get(
        "low",
        0
    )

    risk_score = report.get(
        "risk_score",
        0
    )




    st.markdown("---")

    st.markdown('<div class="section-title">🛡️ Step 4 · Executive Security Summary</div><div class="section-bar"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">High-level security posture from the latest completed scan.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f'<div class="metric-card metric-blue"><div class="metric-label">🔍 API Endpoints</div>'
            f'<div class="metric-value">{total_endpoints}</div>'
            f'<div class="metric-note">Discovered from specification</div></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="metric-card metric-purple"><div class="metric-label">🚨 Vulnerabilities</div>'
            f'<div class="metric-value">{len(findings)}</div>'
            f'<div class="metric-note">Total findings detected</div></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-card metric-red"><div class="metric-label">🔴 High Severity</div>'
            f'<div class="metric-value">{high_count}</div>'
            f'<div class="metric-note">Requires attention</div></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f'<div class="metric-card metric-orange"><div class="metric-label">🟠 Medium Severity</div>'
            f'<div class="metric-value">{medium_count}</div>'
            f'<div class="metric-note">Review recommended</div></div>',
            unsafe_allow_html=True
        )


  

    st.markdown('<div class="section-title">📊 Risk Score</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="risk-panel"><span class="mini-label">CURRENT SECURITY RISK</span>'
        f'<div class="risk-number">{risk_score}/100</div></div>',
        unsafe_allow_html=True
    )

    st.progress(
        min(
            risk_score / 100,
            1.0
        )
    )

    if risk_score == 0:

        st.success(
            "🟢 No detected security findings."
        )

    elif risk_score < 30:

        st.warning(
            f"🟡 Risk Score: {risk_score}/100"
        )

    elif risk_score < 70:

        st.warning(
            f"🟠 Risk Score: {risk_score}/100"
        )

    else:

        st.error(
            f"🔴 Risk Score: {risk_score}/100"
        )


  

    st.markdown('<div class="section-title">🎯 Scan Target</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="target-box">{report.get("target", "")}</div>',
        unsafe_allow_html=True
    )


    

    st.markdown('<div class="section-title">📈 Severity Distribution</div>', unsafe_allow_html=True)

    chart_data = {
        "Severity": [
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        "Count": [
            high_count,
            medium_count,
            low_count
        ]
    }

    st.bar_chart(
        chart_data,
        x="Severity",
        y="Count"
    )


    

    st.markdown("---")

    st.markdown('<div class="section-title">🚨 Security Findings</div><div class="section-bar"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="process-card findings-card">
            <div class="process-icon">🔬</div>
            <h3>Investigate detected vulnerabilities</h3>
            <p>Filter findings by severity, inspect evidence and open the reproduction
            section when a proof-of-concept is available.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="section-caption">Inspect, filter and reproduce each detected issue.</div>', unsafe_allow_html=True)

    if not findings:

        st.success(
            "✅ No vulnerabilities were detected."
        )

    else:

        severity_filter = st.selectbox(
            "Filter by Severity",
            [
                "ALL",
                "HIGH",
                "MEDIUM",
                "LOW"
            ]
        )

        filtered_findings = []

        for finding in findings:

            if (
                severity_filter == "ALL"
                or
                finding.get(
                    "severity"
                ) == severity_filter
            ):

                filtered_findings.append(
                    finding
                )


        for index, finding in enumerate(
            filtered_findings,
            start=1
        ):

            severity = finding.get(
                "severity",
                "LOW"
            )

            severity_class = (
                severity.lower()
            )

            with st.container():

                st.markdown(
                    f"""
                    <div class="finding-card {severity_class}">

                    <h3>
                    {index}. {finding.get("title", "Security Finding")}
                    </h3>

                    <span class="severity-pill pill-{severity_class}">
                        {severity}
                    </span>

                    <br><br>

                    <b>Type:</b>
                    {finding.get("vulnerability_type", "")}

                    <br><br>

                    <b>Endpoint:</b>
                    <code>{finding.get("endpoint", "")}</code>

                    <br><br>

                    <b>Description:</b>
                    {finding.get("description", "")}

                    <br><br>

                    <b>Evidence:</b>
                    {finding.get("evidence", "")}

                    <br><br>

                    <b>Recommendation:</b>
                    {finding.get("recommendation", "")}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            for index, finding in enumerate(
                filtered_findings,
                start=1
            ):

                severity = finding.get(
                    "severity",
                    "LOW"
                )

                severity_class = severity.lower()

                vulnerability_type = finding.get(
                    "vulnerability_type",
                    ""
                )

                title = finding.get(
                    "title",
                    "Security Finding"
                )

                endpoint = finding.get(
                    "endpoint",
                    ""
                )

            description = finding.get(
                "description",
                ""
            )

            evidence = finding.get(
                "evidence",
                ""
            )

            recommendation = finding.get(
                "recommendation",
                ""
            )

          

            if "BOLA" in vulnerability_type or "IDOR" in vulnerability_type:

                simple_explanation = (
                    "SentinelAPI tested the same API resource with "
                    "different object IDs using the same authentication. "
                    "Both requests were successful. This may indicate "
                    "that the API is not properly checking whether the "
                    "current user is allowed to access that object."
                )

                user_meaning = (
                    "In simple words: one logged-in user may be able "
                    "to change an ID such as /users/1 to /users/2 and "
                    "possibly see another user's information."
                )

                verification = (
                    "This is NOT automatically a confirmed vulnerability. "
                    "A HTTP 200 response only means the request succeeded. "
                    "You should verify whether the authenticated user "
                    "actually has permission to access the second object."
                )

            elif "Sensitive Data" in vulnerability_type:

                simple_explanation = (
                    "SentinelAPI found fields in the API response that "
                    "may contain sensitive information."
                )

                user_meaning = (
                    "In simple words: the API may be returning more "
                    "private or sensitive information than the application "
                    "actually needs."
                )

                verification = (
                    "Check whether the detected fields really contain "
                    "sensitive information and whether the current user "
                    "is allowed to receive them."
                )

            elif "Authentication" in vulnerability_type:

                simple_explanation = (
                    "SentinelAPI accessed this endpoint without sending "
                    "an authentication token and received a successful response."
                )

                user_meaning = (
                    "In simple words: a person may be able to access "
                    "this API resource without logging in."
                )

                verification = (
                    "Check whether this endpoint is intentionally public. "
                    "If it contains protected information, authentication "
                    "should be required."
                )

            elif "Rate Limit" in vulnerability_type:

                simple_explanation = (
                    "SentinelAPI sent multiple requests to the endpoint "
                    "and did not receive a rate-limit response."
                )

                user_meaning = (
                    "In simple words: the API may allow too many requests "
                    "in a short period of time."
                )

                verification = (
                    "Check whether rate limiting is required for this "
                    "endpoint, especially if it handles login, authentication "
                    "or other sensitive operations."
                )

            else:

                simple_explanation = (
                    description
                    if description
                    else
                    "SentinelAPI detected a security condition that "
                    "should be reviewed."
                )

                user_meaning = (
                    "In simple words: this finding needs to be reviewed "
                    "to understand whether it creates a real security risk."
                )

                verification = (
                    "Review the evidence and verify the behavior manually "
                    "before treating this finding as a confirmed vulnerability."
                )

            

            with st.container():

                st.markdown(
                    f"""
                    <div class="finding-card {severity_class}">

                    <h3>
                    {index}. {title}
                    </h3>

                    <span class="severity-pill pill-{severity_class}">
                        {severity}
                    </span>

                    <br><br>

                    <div style="
                        padding:15px;
                        border-radius:12px;
                        background:#f8fafc;
                        border:1px solid #dbe4ef;
                        margin-bottom:16px;
                    ">

                    <b>🧠 What is happening?</b>
                    <br>
                    {simple_explanation}

                    <br><br>

                    <b>💡 In simple words</b>
                    <br>
                    {user_meaning}

                    <br><br>

                    <b>📌 What does this result mean?</b>
                    <br>
                    {verification}

                    </div>

                    <b>Type:</b>
                    {vulnerability_type}

                    <br><br>

                    <b>Endpoint:</b>
                    <code>{endpoint}</code>

                    <br><br>

                    <b>Description:</b>
                    {description}

                    <br><br>

                    <b>Evidence:</b>
                    {evidence}

                    <br><br>

                    <b>Recommendation:</b>
                    {recommendation}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

              

                with st.expander(
                    "🧪 Reproduction / PoC"
                ):

                    st.markdown(
                        """
                        **How to reproduce this test**

                        The section below shows the technical request
                        used by SentinelAPI. It is provided for developers
                        and security testers who want to verify the finding.
                        """
                    )

                    st.code(
                        finding_to_poc(
                            finding
                        ),
                        language="http"
                    )

                    st.info(
                        "ℹ️ The PoC is technical evidence. "
                        "A finding should be manually verified before "
                        "being treated as a confirmed vulnerability."
                    )


    

    st.markdown("---")

    st.markdown('<div class="section-title">📥 Export Report</div><div class="section-bar"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="process-card export-card">
            <div class="process-icon">📦</div>
            <h3>Save your security report</h3>
            <p>Download the complete scan result in JSON format for documentation,
            review or further processing.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="section-caption">Download the complete scan report as JSON.</div>', unsafe_allow_html=True)

    report_json = json.dumps(
        report,
        indent=4
    )

    st.download_button(
        label="⬇️ Download JSON Report",
        data=report_json,
        file_name="sentinelapi_scan_report.json",
        mime="application/json",
        use_container_width=True
    )




st.markdown("---")

st.markdown(
    '<div class="footer">SentinelAPI · Zero-Trust API Vulnerability Scanner · Hackathon MVP</div>',
    unsafe_allow_html=True
)