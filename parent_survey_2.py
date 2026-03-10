"""
Parent AI Concerns Survey — Redesigned
AI Strategy Workshops Initiative — India 2026

Run with:  streamlit run parent_survey.py
Requires:  pip install streamlit
"""

import streamlit as st
import csv
import os
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Parent Survey — AI & My Child",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

.stApp {
    background-color: #fdf6ef;
    background-image:
        radial-gradient(circle at 15% 20%, rgba(255, 140, 80, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 85% 75%, rgba(255, 100, 90, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(255, 200, 120, 0.04) 0%, transparent 60%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 700px;
}

/* ── Header ── */
.page-header {
    background: linear-gradient(135deg, #e8470a 0%, #f97316 55%, #fb923c 100%);
    border-radius: 24px;
    padding: 36px 36px 32px;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px rgba(233, 71, 10, 0.25);
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -20px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.header-tag {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.95);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.25);
}
.page-header h1 {
    font-family: 'Lora', serif !important;
    color: #ffffff !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin: 0 0 10px !important;
    line-height: 1.3 !important;
    text-shadow: 0 1px 4px rgba(0,0,0,0.15);
}
.page-header p {
    color: rgba(255,255,255,0.88) !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
    margin: 0 !important;
    max-width: 520px;
}
.header-emoji {
    font-size: 2.4rem;
    margin-bottom: 12px;
    display: block;
}

/* ── Info strip ── */
.info-strip {
    display: flex;
    gap: 10px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}
.info-chip {
    background: #ffffff;
    border: 1.5px solid #e8d5c4;
    border-radius: 30px;
    padding: 7px 16px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #7c4a2d;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ── About card ── */
.about-card {
    background: #ffffff;
    border: 1.5px solid #f0e0d0;
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}
.about-card .card-title {
    font-family: 'Lora', serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8470a;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Question cards ── */
.q-card {
    background: #ffffff;
    border: 1.5px solid #f0e0d0;
    border-radius: 18px;
    padding: 26px 28px 22px;
    margin-bottom: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s;
}
.q-card:hover {
    box-shadow: 0 4px 24px rgba(233,71,10,0.1);
    border-color: #f4b89a;
}
.q-step {
    display: inline-block;
    background: linear-gradient(135deg, #e8470a, #f97316);
    color: white;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}
.q-text {
    font-family: 'Lora', serif;
    color: #1e1209;
    font-size: 1.02rem;
    font-weight: 600;
    line-height: 1.55;
    margin-bottom: 6px;
}
.q-hint {
    color: #a07050;
    font-size: 0.8rem;
    font-weight: 500;
    margin-bottom: 16px;
    font-style: italic;
}

/* ── Radio buttons — complete override ── */
div[data-testid="stRadio"] > label { display: none !important; }

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: #fdf6ef !important;
    border: 2px solid #e8d5c4 !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    color: #3d1f0a !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    line-height: 1.45 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background: #fff3e8 !important;
    border-color: #f97316 !important;
    color: #c23d08 !important;
}

/* Selected state */
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #fff3e8, #ffe8d5) !important;
    border-color: #e8470a !important;
    color: #c23d08 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(233,71,10,0.15) !important;
}

/* Hide actual radio circle */
div[data-testid="stRadio"] div[role="radiogroup"] label input[type="radio"] {
    display: none !important;
}

/* ── Multiselect ── */
div[data-testid="stMultiSelect"] > label { display: none !important; }
div[data-testid="stMultiSelect"] > div {
    background: #fdf6ef !important;
    border: 2px solid #e8d5c4 !important;
    border-radius: 12px !important;
}
div[data-testid="stMultiSelect"] > div:focus-within {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: linear-gradient(135deg, #e8470a, #f97316) !important;
    border-radius: 8px !important;
}
div[data-testid="stMultiSelect"] input {
    color: #3d1f0a !important;
    font-size: 0.9rem !important;
}

/* ── Text inputs ── */
.stTextInput > label, .stTextArea > label,
.stSelectbox > label { display: none !important; }

.stTextInput > div > div > input {
    background: #fdf6ef !important;
    border: 2px solid #e8d5c4 !important;
    border-radius: 12px !important;
    color: #3d1f0a !important;
    font-size: 0.9rem !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input::placeholder { color: #c0956a !important; }

.stTextArea textarea {
    background: #fdf6ef !important;
    border: 2px solid #e8d5c4 !important;
    border-radius: 12px !important;
    color: #3d1f0a !important;
    font-size: 0.9rem !important;
    font-family: 'Nunito', sans-serif !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
    background: #ffffff !important;
}
.stTextArea textarea::placeholder { color: #c0956a !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #fdf6ef !important;
    border: 2px solid #e8d5c4 !important;
    border-radius: 12px !important;
    color: #3d1f0a !important;
    font-size: 0.9rem !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #f97316 !important;
}

/* ── Field labels ── */
.field-label {
    color: #7c4a2d;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 7px;
}

/* ── Submit button ── */
.stButton > button {
    background: linear-gradient(135deg, #e8470a 0%, #f97316 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    padding: 15px 40px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 20px rgba(233,71,10,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #c23d08 0%, #e8470a 100%) !important;
    box-shadow: 0 6px 28px rgba(233,71,10,0.45) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Warning / validation ── */
div.stAlert > div {
    background: #fff3e8 !important;
    border: 1.5px solid #f4b89a !important;
    border-radius: 12px !important;
    color: #c23d08 !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
}

/* ── Thank you page ── */
.thankyou-wrap {
    background: #ffffff;
    border: 1.5px solid #f0e0d0;
    border-radius: 24px;
    padding: 56px 40px;
    text-align: center;
    box-shadow: 0 4px 32px rgba(0,0,0,0.07);
    margin-top: 10px;
}
.thankyou-wrap .big-emoji { font-size: 4rem; margin-bottom: 18px; }
.thankyou-wrap h2 {
    font-family: 'Lora', serif !important;
    color: #1e1209 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin: 0 0 14px !important;
}
.thankyou-wrap .sub {
    color: #7c4a2d;
    font-size: 0.95rem;
    line-height: 1.7;
    max-width: 440px;
    margin: 0 auto 22px;
}
.thankyou-wrap .highlight {
    display: inline-block;
    background: linear-gradient(135deg, #fff3e8, #ffe8d5);
    border: 1.5px solid #f4b89a;
    border-radius: 12px;
    padding: 14px 22px;
    color: #c23d08;
    font-size: 0.88rem;
    font-weight: 700;
    max-width: 440px;
    margin: 0 auto;
}
.thankyou-wrap .footer-small {
    color: #c0956a;
    font-size: 0.75rem;
    margin-top: 28px;
    line-height: 1.6;
}

/* ── Footer ── */
.page-footer {
    text-align: center;
    color: #c0956a;
    font-size: 0.76rem;
    margin-top: 28px;
    line-height: 1.7;
}

/* ── Divider ── */
.soft-divider {
    border: none;
    border-top: 1.5px solid #f0e0d0;
    margin: 6px 0 20px;
}
</style>
""", unsafe_allow_html=True)

# ── CSV helper ─────────────────────────────────────────────────────────────────
CSV_FILE = "parent_survey_responses.csv"

def save_to_csv(data: dict):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# ── Session state ──────────────────────────────────────────────────────────────
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ══════════════════════════════════════════════════════════════════════════════
# THANK YOU PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.submitted:
    st.markdown("""
    <div class="thankyou-wrap">
        <div class="big-emoji">🙏</div>
        <h2>Thank You!</h2>
        <p class="sub">
            Your voice matters. Your honest feedback will be read by school leadership
            and will directly shape how they support parents and students with AI.
        </p>
        <div class="highlight">
            📋 &nbsp;Your response has been recorded successfully.
        </div>
        <p class="footer-small">
            AI Strategy Workshops for School Heads · India 2026<br>
            All responses are confidential and used solely for school planning purposes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Submit Another Response"):
        st.session_state.submitted = False
        st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SURVEY PAGE
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-tag">Parent Survey &nbsp;·&nbsp; Confidential &nbsp;·&nbsp; 2 Minutes</div>
    <span class="header-emoji">👨‍👩‍👧‍👦</span>
    <h1>AI & My Child — Your Views Matter</h1>
    <p>
        AI tools are entering our children's lives rapidly — at school and at home.
        This quick 5-question survey helps your school understand
        <strong>what parents think and need</strong>, so we can act on it together.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Info chips ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-strip">
    <div class="info-chip">⏱️ &nbsp;2 minutes</div>
    <div class="info-chip">🔒 &nbsp;Anonymous &amp; confidential</div>
    <div class="info-chip">📋 &nbsp;5 questions only</div>
</div>
""", unsafe_allow_html=True)

# ── About You ──────────────────────────────────────────────────────────────────
st.markdown('<div class="about-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🏫 &nbsp;About Your Child & School</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="field-label">School Name</div>', unsafe_allow_html=True)
    school = st.text_input("school", placeholder="e.g. Sunrise International School")

with col2:
    st.markdown('<div class="field-label">Child\'s Current Grade</div>', unsafe_allow_html=True)
    grade = st.selectbox("grade", [
        "Grade 1 – 3",
        "Grade 4 – 5",
        "Grade 6 – 8",
        "Grade 9 – 10",
        "Grade 11 – 12",
    ])

st.markdown("</div>", unsafe_allow_html=True)

# ── Q1 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-step">Question 1 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">How aware are you of the AI tools your child is already using — at school or at home?</div>', unsafe_allow_html=True)

q1 = st.radio("q1", [
    "🔴  Not aware at all — I don't know what they're using",
    "🟠  Slightly aware — I've noticed something but don't know much",
    "🟡  Somewhat aware — I know of a few tools they use",
    "🟢  Very aware — I know exactly what they use and how",
], index=None, key="q1_r")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q2 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-step">Question 2 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">What worries you most about AI and your child?</div>', unsafe_allow_html=True)
st.markdown('<div class="q-hint">Select all that apply — pick as many as feel true for you</div>', unsafe_allow_html=True)

q2 = st.multiselect("q2", [
    "My child becoming too dependent on AI instead of thinking for themselves",
    "Exposure to harmful, inappropriate or false AI-generated content",
    "Loss of critical thinking, creativity and problem-solving skills",
    "Student data privacy — who can access my child's information",
    "My child using AI to cheat on schoolwork or exams",
    "Negative effects on mental health, attention span or social skills",
    "Some students having AI advantages that others don't",
    "Teachers not being trained to handle AI in classrooms",
    "I don't have significant concerns about AI right now",
], key="q2_m")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q3 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-step">Question 3 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">How well does your school currently communicate with you about AI in your child\'s education?</div>', unsafe_allow_html=True)

q3 = st.radio("q3", [
    "😶  Nothing at all — I've heard no communication from school about AI",
    "🤔  Very little — only vague or occasional mentions",
    "🙂  Somewhat — I've received some information but would like more",
    "😊  Well — I feel informed and comfortable with how the school handles it",
], index=None, key="q3_r")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q4 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-step">Question 4 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">What would help you most as a parent in guiding your child\'s use of AI at home?</div>', unsafe_allow_html=True)

q4 = st.radio("q4", [
    "📖  A simple, clear guide on safe vs. risky AI tools for children",
    "🎓  A parent session or workshop — what AI is and what to watch for",
    "📋  Clear school guidelines on AI so I can reinforce the same rules at home",
    "💬  Tips on how to have healthy conversations with my child about AI",
    "⚠️  Information on warning signs of harmful or excessive AI use",
], index=None, key="q4_r")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q5 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-step">Question 5 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">In your own words — what is the one thing you wish your school would do about AI and your child?</div>', unsafe_allow_html=True)
st.markdown('<div class="q-hint">Your honest answer will be read directly by school leadership. There are no right or wrong answers.</div>', unsafe_allow_html=True)

q5 = st.text_area("q5",
    placeholder="e.g. 'I wish the school would tell us which apps are safe to allow at home' or 'I want to understand how AI affects my child's learning...'",
    height=110, key="q5_t")
st.markdown("</div>", unsafe_allow_html=True)

# ── Submit ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Submit My Response  ✅"):
    errors = []
    if not school.strip():
        errors.append("Please enter your school name.")
    if not q1:
        errors.append("Please answer Question 1 — AI awareness.")
    if not q3:
        errors.append("Please answer Question 3 — school communication.")
    if not q4:
        errors.append("Please answer Question 4 — support needed.")

    if errors:
        for e in errors:
            st.warning(e)
    else:
        record = {
            "timestamp":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "school":              school.strip(),
            "child_grade":         grade,
            "q1_ai_awareness":     q1,
            "q2_concerns":         " | ".join(q2) if q2 else "None selected",
            "q3_school_comms":     q3,
            "q4_support_needed":   q4,
            "q5_open_message":     q5.strip() if q5 else "Not provided",
        }
        save_to_csv(record)
        st.session_state.submitted = True
        st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    🏫 &nbsp;AI Strategy Workshops for School Heads &nbsp;·&nbsp; India 2026<br>
    All responses are anonymous and used solely for school planning purposes.
</div>
""", unsafe_allow_html=True)
