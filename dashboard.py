import streamlit as st
import time
import pandas as pd
import random
import requests

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="VISH-KANYA Command Center",
    layout="wide",
    page_icon="🛡️"
)

# ---------------------------
# CUSTOM CYBER CSS
# ---------------------------
st.markdown("""
    <style>
    .main { background-color: #0e1117; }

    .stTextArea textarea {
        background-color: #1a1c24;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        font-family: 'Courier New', monospace;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #00ffcc;
        color: black;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
    }

    .ticker-container {
        background-color: #1a1c24;
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# REPORT GENERATOR
# ---------------------------
def generate_report_content(analysis_text):
    return f"""
VISH-KANYA FORENSIC REPORT
ID: VK-901
TIMESTAMP: {time.ctime()}

RESULT:
{analysis_text}
"""


# ---------------------------
# SIDEBAR STATUS
# ---------------------------
with st.sidebar:
    st.title("🛡️ System Vitals")

    try:
        requests.get("http://127.0.0.1:9000/", timeout=2)
        st.success("🟢 ENGINE READY")
    except:
        st.error("🔴 BACKEND OFFLINE")

    st.metric("Threats Scanned", "1,402", "+18%")
    st.divider()


# ---------------------------
# THREAT TICKER
# ---------------------------
scams = ["KYC Fraud", "Lottery Scam", "UPI Phishing", "Customs Impersonation"]
cities = ["Delhi", "Mumbai", "Jamtara", "Hyderabad", "Bangalore"]

ticker_data = " | ".join([
    f"🚨 {random.choice(scams)} in {random.choice(cities)}"
    for _ in range(5)
])

st.markdown(f"""
    <div class="ticker-container">
        <marquee scrollamount="6"
        style="color:#ff4b4b; font-weight:bold;">
            {ticker_data} | AES-256 ACTIVE
        </marquee>
    </div>
""", unsafe_allow_html=True)


# ---------------------------
# MAIN DASHBOARD
# ---------------------------
st.title("🛡️ VISH-KANYA: AI Forensic Command Center")
st.markdown("---")

col_main, col_stats = st.columns([2, 1])

# ---------------------------
# LEFT SIDE
# ---------------------------
with col_main:

    st.subheader("📡 Live Transcript Analysis")

    transcript_input = st.text_area(
        "Paste call transcript:",
        height=200
    )

    if st.button("🚀 EXECUTE FORENSIC SCAN"):

        if transcript_input.strip() == "":
            st.warning("⚠️ Please enter transcript first")

        else:
            with st.spinner("Running Gemini Scan..."):

                backend_url = "http://127.0.0.1:9000/analyze-dashboard"

                payload = {
                    "transcript": transcript_input
                }

                headers = {
                    "x-api-key": "VISH_KANYA_2026"
                }

                response = requests.post(
                    backend_url,
                    json=payload,
                    headers=headers,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    analysis_text = result["analysis"]

                    st.success("✅ Scan Complete")
                    st.info(analysis_text)

                    report_data = generate_report_content(analysis_text)

                    st.download_button(
                        "📄 Download FIR TXT Report",
                        report_data,
                        file_name="VK_Report.txt"
                    )

                else:
                    st.error("Backend Error")
                    st.code(response.text)


# ---------------------------
# RIGHT SIDE
# ---------------------------
with col_stats:
    st.subheader("📍 Threat Map")

    map_df = pd.DataFrame({
        "lat": [28.61, 19.07, 24.31, 12.97],
        "lon": [77.20, 72.87, 86.65, 77.59]
    })

    st.map(map_df)

st.caption("VISH-KANYA Cyber Forensic Unit")
