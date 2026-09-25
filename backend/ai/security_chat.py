import json
import streamlit as st
from google import genai


# ============================================================
# SentinelAPI - AI Security Copilot
# ============================================================

MODEL_NAME = "gemini-3.1-flash-lite"


def get_gemini_client():
    """
    Create and return Gemini API client using
    the API key stored in Streamlit secrets.
    """

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured in "
            ".streamlit/secrets.toml"
        )

    return genai.Client(api_key=api_key)


def build_security_context(
    target="",
    endpoints=None,
    findings=None,
    risk_score=0,
    summary=None,
):
    """
    Create a compact security context for the AI.
    """

    endpoints = endpoints or []
    findings = findings or []
    summary = summary or {}

    context = {
        "target": target,
        "scan_summary": {
            "total_findings": len(findings),
            "high": summary.get("HIGH", 0),
            "medium": summary.get("MEDIUM", 0),
            "low": summary.get("LOW", 0),
            "risk_score": risk_score,
        },
        "endpoints": endpoints,
        "findings": findings,
    }

    return json.dumps(
        context,
        indent=2,
        default=str
    )


def ask_security_copilot(
    question,
    security_context,
    chat_history=None,
):
    """
    Send a security question to Gemini using
    SentinelAPI scan information as context.
    """

    client = get_gemini_client()

    chat_history = chat_history or []

    history_text = ""

    for message in chat_history[-10:]:
        role = message.get("role", "user")
        content = message.get("content", "")

        history_text += (
            f"{role.upper()}: {content}\n"
        )

    system_instruction = """
You are SentinelAPI Security Copilot.

You are an API security assistant for a Zero-Trust API
Vulnerability Scanner.

Your job is to explain API security findings clearly and
help the developer understand and fix security problems.

IMPORTANT RULES:

1. Use the provided SentinelAPI scan context as your primary
   source of truth.

2. NEVER invent a vulnerability that is not supported by the
   provided scan data.

3. Clearly distinguish between:
   - Confirmed finding
   - Possible/Potential finding
   - Manual verification required

4. If the scanner reports a possible BOLA/IDOR, do not claim
   that it is definitely vulnerable unless the evidence proves it.

5. Explain:
   - What the vulnerability means
   - Why it matters
   - Affected endpoint
   - Evidence
   - Security impact
   - How to fix it
   - How to verify the fix

6. If the user asks "what problems are there?", summarize the
   actual findings from the scan.

7. If the user asks "which API is best?", explain that SentinelAPI
   can compare APIs using measurable security characteristics,
   but do not invent information about APIs that are not present
   in the supplied context.

8. If information is missing, explicitly say:
   "This information is not available in the current scan context."

9. Never expose API keys, passwords, bearer tokens, or other secrets.

10. Keep answers practical and developer-friendly.

11. When suggesting fixes, provide concise code examples when
    useful. Mention the framework when known.

12. Do not replace the scanner's evidence with assumptions.

13. The user may ask questions in Hindi, Hinglish, or English.
    Answer in the same language style as the user.

CURRENT SENTINELAPI SCAN CONTEXT:
"""


    prompt = f"""
{system_instruction}

{security_context}

PREVIOUS CHAT:
{history_text}

USER QUESTION:
{question}

Give a clear and useful security-focused answer.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text