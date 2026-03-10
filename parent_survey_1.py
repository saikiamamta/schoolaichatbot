"""
Parent AI Concerns Survey — 5 Questions
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
    page_title="Parent Survey — AI in Our School",
    page_icon="👨‍👩‍👧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #1a0a2e 0%, #2d1654 50%, #1a0a2e 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 680px; }

/* Header */
.survey-header {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,180,120,0.3);
    border-radius: 20px;
    padding: 32px 32px 26px;
    margin-bottom: 28px;
    text-align: center;
}
.survey-header .emoji { font-size: 2.8rem; margin-bottom: 10px; }
.survey-header h1 {
    font-family: 'Playfair Display', serif !important;
    color: #ffffff;
    font-size: 1.7rem;
    font-weight: 700;
    margin: 0 0 10px;
    line-height: 1.3;
}
.survey-header p {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    line-height: 1.65;
    margin: 0;
}
.orange-tag {
    display: inline-block;
    background: rgba(255,160,80,0.15);
    border: 1px solid rgba(255,160,80,0.35);
    color: #ffb366;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 12px;
}

/* Question cards */
.q-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-left: 3px solid #b36bff;
    border-radius: 16px;
    padding: 24px 26px 20px;
    margin-bottom: 18px;
}
.q-number {
    color: #b36bff;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.q-text {
    color: rgba(255,255,255,0.88);
    font-size: 0.97rem;
    font-weight: 500;
    line-height: 1.55;
    margin-bottom: 16px;
}
.q-sub {
    color: rgba(255,255,255,0.45);
    font-size: 0.8rem;
    margin-top: -10px;
    margin-bottom: 14px;
    font-style: italic;
}

/* Radio overrides */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 10px !important;
    padding: 11px 16px !important;
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.88rem !important;
    margin-bottom: 6px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: #b36bff !important;
    background: rgba(179,107,255,0.1) !important;
}

/* Multiselect */
div[data-testid="stMultiSelect"] > label { display: none !important; }
div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}
div[data-testid="stMultiSelect"] span { color: white !important; font-size: 0.85rem !important; }

/* Text input */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 0.9rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.28) !important; }
.stTextInput > label, .stTextArea > label { display: none !important; }

/* Selectbox */
.stSelectbox > label { display: none !important; }
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Submit button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #b36bff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 14px 40px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #a855f7) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.45) !important;
    transform: translateY(-1px) !important;
}

/* Thank you */
.thankyou-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,180,120,0.25);
    border-radius: 20px;
    padding: 52px 36px;
    text-align: center;
    margin-top: 10px;
}
.thankyou-card h2 {
    font-family: 'Playfair Display', serif;
    color: #ffffff;
    font-size: 1.9rem;
    margin: 16px 0 14px;
}
.thankyou-card p {
    color: rgba(255,255,255,0.6);
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 460px;
    margin: 0 auto 10px;
}

/* Warning */
div.stAlert > div {
    background: rgba(255,160,80,0.1) !important;
    border: 1px solid rgba(255,160,80,0.3) !important;
    border-radius: 10px !important;
    color: #ffb366 !important;
    font-size: 0.85rem !important;
}

.footer-note {
    text-align: center;
    color: rgba(255,255,255,0.25);
    font-size: 0.75rem;
    margin-top: 24px;
    line-height: 1.6;
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

# ── THANK YOU ──────────────────────────────────────────────────────────────────
if st.session_state.submitted:
    st.markdown("""
    <div class="thankyou-card">
        <div style="font-size:3.5rem;">🙏</div>
        <h2>Thank You!</h2>
        <p>Your feedback has been recorded and will be shared with the school leadership team.</p>
        <p style="color:rgba(255,255,255,0.38);font-size:0.8rem;margin-top:20px;">
            AI Strategy Workshops for School Heads · India 2026<br>
            Your responses are confidential and used solely for school planning.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Submit Another Response"):
        st.session_state.submitted = False
        st.rerun()
    st.stop()

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="survey-header">
    <div class="orange-tag">For Parents · 2 Minutes · Confidential</div>
    <div class="emoji">👨‍👩‍👧</div>
    <h1>AI in Our School — Your Voice Matters</h1>
    <p>AI is entering our children's classrooms rapidly. This quick 5-question survey helps your school understand <strong style="color:rgba(255,255,255,0.8);">what parents think, feel and need</strong> — so we can act on it.</p>
</div>
""", unsafe_allow_html=True)

# ── ABOUT ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">About You</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">A little about your child and school</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    school = st.text_input("School Name", placeholder="e.g. Sunrise International")
with col2:
    grade = st.selectbox("Child's Grade", [
        "Grade 1–3", "Grade 4–5", "Grade 6–8",
        "Grade 9–10", "Grade 11–12"
    ])
st.markdown("</div>", unsafe_allow_html=True)

# ── Q1 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">Question 1 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">How aware are you of the AI tools your child is currently using — at school or at home?</div>', unsafe_allow_html=True)
q1 = st.radio("q1", [
    "Not aware at all — I don't know what they're using",
    "Slightly aware — I've noticed them using something but don't know much",
    "Somewhat aware — I know of a few tools they use",
    "Very aware — I know what they use and how they use it",
], index=None, key="q1_radio")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q2 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">Question 2 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">What are your biggest concerns about AI and your child? <br><span style="font-size:0.82rem;color:rgba(255,255,255,0.4);font-weight:400;">Select all that apply</span></div>', unsafe_allow_html=True)
q2 = st.multiselect("q2", [
    "My child becoming too dependent on AI for thinking and learning",
    "Exposure to harmful, inappropriate or biased AI content",
    "Loss of critical thinking and problem-solving skills",
    "Data privacy — who has access to my child's information",
    "AI widening the gap between students who use it and those who don't",
    "My child using AI to cheat on schoolwork",
    "Negative impact on mental health or social skills",
    "Teachers not being prepared to handle AI in classrooms",
    "I don't have significant concerns about AI",
], key="q2_multi")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q3 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">Question 3 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">How well does your school currently communicate with you about how AI is being used in your child\'s education?</div>', unsafe_allow_html=True)
q3 = st.radio("q3", [
    "Not at all — I've heard nothing from the school about AI",
    "Very little — only occasional and vague mentions",
    "Somewhat — I've received some communication but want more",
    "Well — the school keeps me informed and I feel comfortable",
], index=None, key="q3_radio")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q4 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">Question 4 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">As a parent, what kind of support would help you most in guiding your child\'s use of AI at home?</div>', unsafe_allow_html=True)
q4 = st.radio("q4", [
    "A simple guide on which AI tools are safe and which to avoid",
    "A parent workshop or session on AI — what it is and how it works",
    "Clear school guidelines on AI use so I can reinforce them at home",
    "Tips on how to talk to my child about responsible AI use",
    "Information on warning signs of harmful or excessive AI use",
], index=None, key="q4_radio")
st.markdown("</div>", unsafe_allow_html=True)

# ── Q5 ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="q-card">', unsafe_allow_html=True)
st.markdown('<div class="q-number">Question 5 of 5</div>', unsafe_allow_html=True)
st.markdown('<div class="q-text">In your own words — what is the one thing you wish your school would do differently when it comes to AI and your child?</div>', unsafe_allow_html=True)
st.markdown('<div class="q-sub">Your honest answer will be read by school leadership. There are no wrong answers.</div>', unsafe_allow_html=True)
q5 = st.text_area("q5", placeholder="Type your thoughts here…", height=100, key="q5_text")
st.markdown("</div>", unsafe_allow_html=True)

# ── SUBMIT ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.button("✅  Submit My Response"):
    errors = []
    if not school:
        errors.append("Please enter your school name.")
    if not q1:
        errors.append("Please answer Question 1.")
    if not q3:
        errors.append("Please answer Question 3.")
    if not q4:
        errors.append("Please answer Question 4.")

    if errors:
        for e in errors:
            st.warning(e)
    else:
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "school": school,
            "child_grade": grade,
            "q1_ai_awareness": q1,
            "q2_concerns": " | ".join(q2) if q2 else "None selected",
            "q3_school_communication": q3,
            "q4_support_needed": q4,
            "q5_open_message": q5.strip() if q5 else "Not provided",
        }
        save_to_csv(response)
        st.session_state.submitted = True
        st.rerun()

st.markdown("""
<div class="footer-note">
    AI Strategy Workshops for School Heads · India 2026<br>
    Responses are anonymous and used solely for school planning purposes
</div>
""", unsafe_allow_html=True)
