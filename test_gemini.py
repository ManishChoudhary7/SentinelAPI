import streamlit as st
from google import genai

# ==============================
# SentinelAPI - Gemini API Test
# ==============================

st.set_page_config(
    page_title="SentinelAPI - Gemini Test",
    page_icon="🛡️"
)

st.title("🛡️ SentinelAPI")
st.subheader("Gemini AI Connection Test")

try:
    # Get API key from Streamlit secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]

    # Create Gemini client
    client = genai.Client(api_key=API_KEY)

    # Send test request
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Say hello to SentinelAPI in one short sentence."
    )

    # Display response
    st.success("✅ Gemini API Connected Successfully!")
    st.write("### 🤖 Gemini Response")
    st.write(response.text)

except Exception as e:
    st.error("❌ Gemini API Connection Failed")
    st.code(str(e))