import streamlit as st
from llm_engine import analyze_job, generate_response
import json

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="FreelanceGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
    /* ---------- Global ---------- */
    .stApp {
        background: linear-gradient(180deg, #e8f4fc 0%, #f4faff 100%);
    }

    /* ---------- Hero Header ---------- */
    .hero {
        background: linear-gradient(135deg, #5eb8f0 0%, #3d8fd1 100%);
        padding: 2.5rem 2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(93, 184, 240, 0.25);
    }
    .hero h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #e8f4fc;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 12px;
        color: white;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #5eb8f0 0%, #3d8fd1 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 3px 10px rgba(93, 184, 240, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(93, 184, 240, 0.45);
        background: linear-gradient(135deg, #3d8fd1 0%, #2e7ab8 100%);
        color: white !important;
    }
    .stButton > button:focus {
        color: white !important;
    }

    /* ---------- Risk Badge Cards ---------- */
    .risk-card {
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 1rem 0;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }
    .risk-high {
        background: linear-gradient(135deg, #ffe0e0 0%, #ffc9c9 100%);
        color: #c92a2a;
        border-left: 6px solid #fa5252;
    }
    .risk-medium {
        background: linear-gradient(135deg, #fff4d9 0%, #ffe9b3 100%);
        color: #e67700;
        border-left: 6px solid #f59f00;
    }
    .risk-low {
        background: linear-gradient(135deg, #d9f7e0 0%, #b8f0c5 100%);
        color: #2b8a3e;
        border-left: 6px solid #37b24d;
    }

    /* ---------- Flag Cards ---------- */
    .flag-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        border-left: 5px solid #5eb8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .flag-card.high { border-left-color: #fa5252; }
    .flag-card.medium { border-left-color: #f59f00; }
    .flag-card.low { border-left-color: #fab005; }

    .flag-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #1c4966;
        margin-bottom: 0.3rem;
    }
    .flag-evidence {
        background: #eef7fd;
        padding: 0.5rem 0.8rem;
        border-radius: 8px;
        font-style: italic;
        color: #495057;
        font-size: 0.92rem;
        margin-top: 0.4rem;
    }

    /* ---------- Metric Cards ---------- */
    [data-testid="stMetricValue"] {
        color: #2e7ab8 !important;
        font-weight: 800;
    }
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(93, 184, 240, 0.15);
        border-top: 4px solid #5eb8f0;
    }

    /* ---------- Text Area ---------- */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #d0e8f7 !important;
        background: white !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #5eb8f0 !important;
        box-shadow: 0 0 0 3px rgba(94, 184, 240, 0.2) !important;
    }

    /* ---------- Selectbox ---------- */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #d0e8f7 !important;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(93, 184, 240, 0.12);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        color: #495057;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5eb8f0 0%, #3d8fd1 100%) !important;
        color: white !important;
    }

    /* ---------- Info / Success Boxes ---------- */
    .stAlert {
        border-radius: 12px;
    }

    /* ---------- Section Headers ---------- */
    h3 {
        color: #1c4966 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Hero Header ----------------
st.markdown("""
<div class="hero">
    <h1>🛡️ FreelanceGuard</h1>
    <p>AI Safety Copilot for Freelancers — Spot risks before you commit.</p>
    <span class="hero-badge">⚡ Powered by Groq LLaMA · PakAngels Cohort 11</span>
</div>
""", unsafe_allow_html=True)

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["🔍 Analyze a Job", "📊 Evaluation Results"])

# ================= TAB 1: ANALYZE =================
with tab1:
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    # -------- Quick Example Buttons --------
    st.markdown("#### 🎯 Try a sample job post")
    col1, col2, col3 = st.columns(3)

    if col1.button("🔴 Suspicious Job", width='stretch'):
        st.session_state["input_text"] = (
            "We need someone to build an AI chatbot within 24 hours. Budget $30. "
            "Before hiring, please complete this full sample project. Contact me on Telegram."
        )
        st.rerun()

    if col2.button("🟠 Ambiguous Job", width='stretch'):
        st.session_state["input_text"] = (
            "Looking for a data entry expert. Simple work, details after hiring. "
            "Pay discussed later. Send your WhatsApp number."
        )
        st.rerun()

    if col3.button("🟢 Legit Job", width='stretch'):
        st.session_state["input_text"] = (
            "Looking for Python developer to build REST API. Budget $300. "
            "Requirements attached. Payment via platform milestones."
        )
        st.rerun()

    st.markdown("#### 📝 Or paste your own job post")
    user_input = st.text_area(
        "Paste the job post or client message:",
        height=180,
        key="input_text",
        placeholder="Paste any freelance job post or client message here...",
        label_visibility="collapsed"
    )

    col_btn1, col_btn2 = st.columns([1, 4])
    analyze_clicked = col_btn1.button("🔍 Analyze Now", type="primary", width='stretch')

    if analyze_clicked and user_input.strip():
        with st.spinner("🧠 Analyzing the job post for risk signals..."):
            try:
                result = analyze_job(user_input)
                st.session_state["result"] = result
                st.session_state["input"] = user_input
            except Exception as e:
                st.error(f"Error: {e}")

    # -------- Results Section --------
    if "result" in st.session_state:
        result = st.session_state["result"]
        level = result.get("risk_level", "UNKNOWN")
        icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}.get(level, "⚪")
        css_class = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(level, "")

        st.markdown("<br>", unsafe_allow_html=True)

        # Big risk badge
        st.markdown(f"""
        <div class="risk-card {css_class}">
            {icon} Risk Level: {level}
        </div>
        """, unsafe_allow_html=True)

        # Risk Score Bar
        score_map = {"LOW": 25, "MEDIUM": 60, "HIGH": 90}
        score = score_map.get(level, 0)
        st.progress(score / 100, text=f"Risk Score: {score}/100")

        # Red Flags
        st.markdown("### 🚩 Detected Red Flags")
        indicators = result.get("risk_indicators", [])
        if not indicators:
            st.success("✅ No red flags detected in this opportunity.")
        else:
            for flag in indicators:
                sev = flag.get("severity", "medium").lower()
                nice_name = flag.get("type", "unknown").replace("_", " ").title()
                st.markdown(f"""
                <div class="flag-card {sev}">
                    <div class="flag-title">⚠️ {nice_name} <span style="font-weight:400; opacity:0.7;">({sev})</span></div>
                    <div class="flag-evidence">"{flag.get("evidence", "")}"</div>
                </div>
                """, unsafe_allow_html=True)

        # Explanation
        st.markdown("### 📖 What This Means")
        st.write(result.get("explanation", "No explanation provided."))

        # Recommended Action
        st.markdown("### ✅ Recommended Action")
        st.info(result.get("recommended_action", "No action provided."))

        # Response Generator
        st.markdown("### ✉️ Generate a Safe Response")
        action = st.selectbox(
            "Choose how you want to respond:",
            ["Ask for clarification", "Respond safely", "Decline opportunity"]
        )

        if st.button("💬 Generate Response"):
            with st.spinner("✍️ Drafting a professional response..."):
                try:
                    msg = generate_response(st.session_state["input"], result, action)
                    st.session_state["response_msg"] = msg
                except Exception as e:
                    st.error(f"Error: {e}")

        if "response_msg" in st.session_state:
            st.text_area("Your message:", st.session_state["response_msg"], height=180)

            # -------- Download Report as PDF --------
            try:
                from fpdf import FPDF

                def sanitize(text: str) -> str:
                    if not isinstance(text, str):
                        text = str(text)
                    replacements = {
                        "\u2018": "'", "\u2019": "'",
                        "\u201C": '"', "\u201D": '"',
                        "\u2013": "-", "\u2014": "-",
                        "\u2026": "...", "\u00A0": " ",
                        "\u2022": "-",
                        "\\(": "", "\\)": "",
                        "\\[": "", "\\]": "",
                        "\\$": "$",
                        "\\%": "%",
                        "\\&": "&",
                        "\\_": "_",
                    }
                    for k, v in replacements.items():
                        text = text.replace(k, v)
                    return text.encode("latin-1", errors="ignore").decode("latin-1")

                if st.button("📄 Download Full Report (PDF)"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", size=16)
                    pdf.cell(0, 10, sanitize("FreelanceGuard - Risk Analysis Report"), ln=True)
                    pdf.ln(4)

                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 8, sanitize(f"Risk Level: {level}"), ln=True)
                    pdf.cell(0, 8, sanitize(f"Risk Score: {score}/100"), ln=True)
                    pdf.ln(4)

                    pdf.set_font("Arial", "B", size=13)
                    pdf.cell(0, 8, "Red Flags:", ln=True)
                    pdf.set_font("Arial", size=11)
                    if not indicators:
                        pdf.multi_cell(0, 6, "None detected.")
                    else:
                        for flag in indicators:
                            nice = flag.get("type", "").replace("_", " ").title()
                            line = f'- {nice} ({flag.get("severity", "")}): "{flag.get("evidence", "")}"'
                            pdf.multi_cell(0, 6, sanitize(line))
                    pdf.ln(4)

                    pdf.set_font("Arial", "B", size=13)
                    pdf.cell(0, 8, "Explanation:", ln=True)
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 6, sanitize(result.get("explanation", "")))
                    pdf.ln(4)

                    pdf.set_font("Arial", "B", size=13)
                    pdf.cell(0, 8, "Recommended Action:", ln=True)
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 6, sanitize(result.get("recommended_action", "")))
                    pdf.ln(4)

                    pdf.set_font("Arial", "B", size=13)
                    pdf.cell(0, 8, "Suggested Response:", ln=True)
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 6, sanitize(st.session_state["response_msg"]))

                    pdf.output("freelanceguard_report.pdf")
                    with open("freelanceguard_report.pdf", "rb") as f:
                        st.download_button(
                            "⬇️ Download PDF",
                            f,
                            file_name="freelanceguard_report.pdf",
                            mime="application/pdf",
                            width='stretch'
                        )
            except ImportError:
                st.warning("PDF generation unavailable. Install fpdf: py -m pip install fpdf")

        # Reset Button
        st.markdown("---")
        if st.button("🔄 Analyze Another Job", width='stretch'):
            st.session_state["input_text"] = ""
            for key in ["result", "input", "response_msg"]:
                st.session_state.pop(key, None)
            st.rerun()

# ================= TAB 2: EVALUATION =================
with tab2:
    st.markdown("### 📊 Evaluation on Representative Scenarios")
    st.markdown(
        "FreelanceGuard was evaluated on **40 test cases** — 25 real-world freelance job posts "
        "from Upwork and 15 targeted edge cases (multilingual, adversarial, ultra-short). "
        "All cases are grounded in platform safety guidance (Upwork, FTC)."
    )

    st.caption(
        "📋 **Methodology:** Each case was manually labeled with an expected risk level "
        "(HIGH/MEDIUM/LOW) and expected red-flag categories. The system output was compared "
        "against these labels using exact-match for risk level and subset-match for red flags."
    )

    st.markdown("---")

    # -------- Primary Metrics --------
    col_a, col_b = st.columns(2)
    col_a.metric("✅ Red Flag Detection", "36/40", "90.0%")
    col_b.metric("🎯 Risk Level Classification", "30/40", "75.0%")


    st.markdown("---")
    st.markdown("### 🧪 Test Case Breakdown")
    st.markdown(
        """
        - **25 real-world cases** — sourced from live Upwork job postings (Feb 2024)
        - **15 targeted synthetic cases** — multilingual (Urdu), emoji-heavy, ultra-short, adversarial scams
        - **Distribution:** 17 LOW · 11 MEDIUM · 12 HIGH
        - **Coverage:** 13 risk categories, including off-platform, unpaid work, upfront payment, sensitive info, urgency, vagueness, toxic culture, pay mismatch, and more
        """
    )

    st.markdown("---")
    st.markdown("### 📊 Coverage by Risk Category")

    coverage_data = {
        "Risk Category": [
            "Off-Platform Communication/Payment",
            "Unpaid / Free Work Request",
            "Upfront Payment Request",
            "Sensitive Information Request",
            "Suspicious External Links",
            "Unrealistic Promises",
            "Excessive Urgency / Pressure",
            "Vague or Suspicious Requirements",
            "Discriminatory Requirements",
            "Experience Preference Bias",
            "Toxic Work Culture",
            "Unrealistic Availability",
            "Pay Mismatch for Scope",
        ],
        "Test Cases": [
            "10, 26, 33, 34, 35, 36, 38",
            "31, 34",
            "26, 28, 35",
            "27, 29, 32",
            "29",
            "26, 32, 36",
            "1, 10, 13, 18, 26, 28, 34, 36",
            "2, 8, 15, 16, 17, 19, 21, 37, 39",
            "2",
            "11",
            "13",
            "13",
            "17, 21",
        ],
        "Accuracy": [
            "7/7 (100%)",
            "2/2 (100%)",
            "3/3 (100%)",
            "3/3 (100%)",
            "1/1 (100%)",
            "3/3 (100%)",
            "8/8 (100%)",
            "5/9 (55.6%)",
            "1/1 (100%)",
            "1/1 (100%)",
            "1/1 (100%)",
            "1/1 (100%)",
            "2/2 (100%)",
        ],
    }
    st.dataframe(coverage_data, width='stretch', hide_index=True)

    st.caption(
        "💡 **Note:** 'Vague Requirements' shows 55.6% accuracy because vagueness is inherently subjective. "
        "We deliberately avoided over-tuning so the tool doesn't flag every post as MEDIUM."
    )

    st.markdown("---")
    st.markdown("### 📁 Sample Test Cases")

    sample_data = {
        "ID": [10, 26, 31, 34, 3, 30, 40, 22],
        "Job Post (excerpt)": [
            "Simple data entry. Payment outside Upwork. WhatsApp me. Urgent hiring.",
            "URGENT! $5000/week. No experience. Send WhatsApp + $50 fee.",
            "Complete this 10-hour unpaid test project. If selected, we will hire you.",
            "Build chatbot in 24 hours. $30. Free sample first. Contact on Telegram.",
            "Data Engineer role. Python, Spark, Airflow, AWS. Diverse workplace.",
            "Python dev for REST API. $300. Payment via platform milestones.",
            "Senior React developer. 6-month project. $60-80/hr. Platform escrow.",
            "Blackbaud Implementation Developer. $25-70/hr. UK client.",
        ],
        "Expected": ["HIGH", "HIGH", "HIGH", "HIGH", "LOW", "LOW", "LOW", "LOW"],
        "Detected": ["HIGH", "HIGH", "HIGH", "HIGH", "LOW", "MEDIUM", "LOW", "LOW"],
        "Match": ["✅", "✅", "✅", "✅", "✅", "🟠", "✅", "✅"],
    }
    st.dataframe(sample_data, width='stretch', hide_index=True)

    st.markdown("---")
    st.markdown("### 📥 Full Evaluation Data")
    st.caption(
        "The complete 40-case evaluation results are available in the GitHub repository "
        "as `evaluation_results.csv`. Every case, expected label, detected label, and match status is documented."
    )

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem; color: #5a7a94; font-size: 0.9rem;">
    ⚠️ <strong>FreelanceGuard</strong> provides AI-assisted risk assessment. It does not definitively confirm fraud. 
    Always verify clients and use platform protections.<br>
    Built for PakAngels GenAI & Agentic AI Mid-Term Hackathon · Cohort 11
</div>
""", unsafe_allow_html=True)