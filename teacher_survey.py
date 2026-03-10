"""
Teacher AI Literacy Survey
AI Strategy Workshops Initiative — India 2026

Run with:  streamlit run teacher_survey.py
Requires:  pip install streamlit
"""

import streamlit as st
import csv
import os
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Teacher AI Literacy Survey",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #0f1f3d 0%, #162847 50%, #1a3a5c 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 760px; }

/* Header */
.survey-header {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 28px;
    text-align: center;
}
.survey-header h1 {
    font-family: 'Playfair Display', serif !important;
    color: #ffffff;
    font-size: 1.65rem;
    font-weight: 700;
    margin: 10px 0 8px;
    line-height: 1.3;
}
.survey-header p {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    margin: 0;
    line-height: 1.6;
}
.gold-tag {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.4);
    color: #e0bc6e;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 10px;
}

/* Progress */
.progress-wrap {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.progress-text { color: rgba(255,255,255,0.5); font-size: 0.78rem; white-space: nowrap; }

/* Section cards */
.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 3px solid #0e9d8a;
    border-radius: 14px;
    padding: 22px 24px 18px;
    margin-bottom: 20px;
}
.section-title {
    font-family: 'Playfair Display', serif;
    color: #e0bc6e;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.q-label {
    color: rgba(255,255,255,0.82);
    font-size: 0.88rem;
    font-weight: 500;
    margin-bottom: 8px;
    line-height: 1.5;
}

/* Radio & select overrides */
div[data-testid="stRadio"] > label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.82rem !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    padding: 9px 14px !important;
    color: rgba(255,255,255,0.82) !important;
    font-size: 0.85rem !important;
    margin-bottom: 5px !important;
    transition: all 0.2s !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: #0e9d8a !important;
    background: rgba(14,157,138,0.1) !important;
}

div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}
div[data-testid="stMultiSelect"] span {
    color: white !important;
    font-size: 0.85rem !important;
}

.stTextInput > div > div > input,
.stTextArea textarea {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 0.88rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.3) !important; }

.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Slider */
.stSlider label { color: rgba(255,255,255,0.75) !important; font-size: 0.82rem !important; }
.stSlider > div > div > div { color: white !important; }

/* Submit button */
.stButton > button {
    background: linear-gradient(135deg, #0e9d8a, #13b89f) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 14px 40px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    margin-top: 10px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0b8a79, #0e9d8a) !important;
    box-shadow: 0 4px 20px rgba(14,157,138,0.4) !important;
    transform: translateY(-1px) !important;
}

/* Thank you */
.thankyou-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 18px;
    padding: 48px 36px;
    text-align: center;
    margin-top: 20px;
}
.thankyou-card h2 {
    font-family: 'Playfair Display', serif;
    color: #ffffff;
    font-size: 1.8rem;
    margin: 16px 0 12px;
}
.thankyou-card p {
    color: rgba(255,255,255,0.65);
    font-size: 0.92rem;
    line-height: 1.7;
    max-width: 480px;
    margin: 0 auto 10px;
}
.teal-highlight { color: #13b89f; font-weight: 600; }
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: 24px 0;
}

/* Validation warning */
div.stAlert > div {
    background: rgba(201,168,76,0.12) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    border-radius: 10px !important;
    color: #e0bc6e !important;
    font-size: 0.85rem !important;
}

/* Section label helper */
.field-label {
    color: rgba(255,255,255,0.6);
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CSV_FILE = "teacher_survey_responses.csv"

COMFORT_OPTIONS = [
    "Never used any AI tool",
    "Tried once or twice out of curiosity",
    "Use occasionally for personal tasks",
    "Use regularly — fairly comfortable",
    "Use confidently across multiple tools",
]

FREQUENCY_OPTIONS = [
    "Never",
    "Rarely (once a month or less)",
    "Sometimes (a few times a month)",
    "Often (weekly)",
    "Very often (almost daily)",
]

AGREEMENT_OPTIONS = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree",
]

CONCERN_OPTIONS = [
    "AI will replace teachers",
    "Students cheating / academic dishonesty",
    "Student over-reliance on AI",
    "Data privacy and safety of students",
    "My own lack of AI skills",
    "AI producing biased or incorrect content",
    "Screen time and mental health impact",
    "Losing human connection in teaching",
    "No clear school policy on AI use",
    "I have no major concerns",
]

PD_OPTIONS = [
    "Hands-on training with AI tools (ChatGPT, Gemini etc.)",
    "How to design AI-proof assessments",
    "Managing AI-empowered students in class",
    "Creating AI-assisted lesson plans",
    "Understanding DPDP Act & data safety",
    "AI for differentiated / personalised learning",
    "AI ethics and responsible use in schools",
    "How to talk to parents about AI",
]

# ── CSV helper ─────────────────────────────────────────────────────────────────
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

# ── THANK YOU PAGE ─────────────────────────────────────────────────────────────
if st.session_state.submitted:
    st.markdown("""
    <div class="survey-header">
        <div class="gold-tag">AI Strategy Workshops · India 2026</div>
        <h1>📋 Teacher AI Literacy Survey</h1>
    </div>
    <div class="thankyou-card">
        <div style="font-size:3.5rem;">🙏</div>
        <h2>Thank You!</h2>
        <p>Your responses have been recorded successfully.</p>
        <p>Your honest inputs will help your school leadership design a <span class="teal-highlight">meaningful AI strategy</span> that supports you — not one that is imposed on you.</p>
        <hr class="divider">
        <p style="font-size:0.82rem;color:rgba(255,255,255,0.4);">
            AI Strategy Workshops for School Heads · India 2026<br>
            Responses are confidential and used for school planning purposes only.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Submit Another Response"):
        st.session_state.submitted = False
        st.rerun()
    st.stop()

# ── SURVEY HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="survey-header">
    <div class="gold-tag">AI Strategy Workshops · India 2026</div>
    <h1>📋 Teacher AI Literacy Survey</h1>
    <p>This short survey helps your school understand where teachers stand on AI — so leadership can build the right support systems for you.<br>
    <strong style="color:rgba(255,255,255,0.75);">All responses are anonymous and confidential.</strong></p>
</div>
""", unsafe_allow_html=True)

# Progress indicator (static — all on one page)
st.markdown("""
<div class="progress-wrap">
    <span class="progress-text">7 sections &nbsp;·&nbsp; Approx. 5 minutes</span>
    <div style="flex:1;height:4px;background:rgba(255,255,255,0.1);border-radius:4px;">
        <div style="height:100%;width:100%;background:linear-gradient(90deg,#0e9d8a,#c9a84c);border-radius:4px;"></div>
    </div>
    <span class="progress-text">Please answer all questions</span>
</div>
""", unsafe_allow_html=True)

# ── SECTION 0: ABOUT YOU ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">👤 About You</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="field-label">Your Name (optional)</div>', unsafe_allow_html=True)
    teacher_name = st.text_input("", placeholder="e.g. Meena Sharma", key="name",
                                  label_visibility="collapsed")
with col2:
    st.markdown('<div class="field-label">School Name</div>', unsafe_allow_html=True)
    school_name = st.text_input("", placeholder="e.g. Sunrise International", key="school",
                                 label_visibility="collapsed")

col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="field-label">Subject / Department</div>', unsafe_allow_html=True)
    subject = st.text_input("", placeholder="e.g. Mathematics", key="subject",
                             label_visibility="collapsed")
with col4:
    st.markdown('<div class="field-label">Years of Teaching Experience</div>', unsafe_allow_html=True)
    experience = st.selectbox("", [
        "Less than 2 years", "2–5 years", "6–10 years",
        "11–20 years", "More than 20 years"
    ], key="experience", label_visibility="collapsed")

st.markdown('<div class="field-label" style="margin-top:12px;">Classes You Teach</div>',
            unsafe_allow_html=True)
classes = st.multiselect("", [
    "Primary (Grades 1–5)", "Middle School (Grades 6–8)",
    "Secondary (Grades 9–10)", "Senior Secondary (Grades 11–12)"
], key="classes", label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 1: PERSONAL AI COMFORT ────────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">🤖 Section 1 — Personal AI Tool Usage & Comfort</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">1. How would you describe your personal comfort with AI tools?</div>',
            unsafe_allow_html=True)
q1_comfort = st.radio("", COMFORT_OPTIONS, key="q1", index=None,
                       label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">2. Which AI tools have you personally used? (Select all that apply)</div>',
            unsafe_allow_html=True)
q2_tools = st.multiselect("", [
    "ChatGPT", "Google Gemini", "Microsoft Copilot",
    "Canva AI", "Grammarly", "Perplexity AI",
    "BYJU's / EdTech platforms", "WhatsApp AI features",
    "None — I haven't used any AI tools"
], key="q2", label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">3. How do you feel about AI entering the education space?</div>',
            unsafe_allow_html=True)
q3_feeling = st.radio("", [
    "Very positive — I welcome it",
    "Cautiously optimistic — I see potential but have concerns",
    "Neutral — I haven't formed a strong view yet",
    "Concerned — I worry about the impact on teaching",
    "Strongly against — I think it does more harm than good",
], key="q3", index=None, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 2: LESSON PLANNING & CONTENT ──────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">📚 Section 2 — AI in Lesson Planning & Content Creation</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">4. How often do you currently use AI tools to help plan lessons or create teaching content?</div>',
            unsafe_allow_html=True)
q4_frequency = st.radio("", FREQUENCY_OPTIONS, key="q4", index=None,
                          label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">5. Which of the following have you used AI for in your teaching? (Select all that apply)</div>',
            unsafe_allow_html=True)
q5_uses = st.multiselect("", [
    "Writing lesson plans",
    "Creating worksheets or practice questions",
    "Explaining difficult concepts in simpler language",
    "Translating content into regional languages",
    "Making presentations or visual aids",
    "Generating quiz questions",
    "Searching for teaching resources",
    "I have not used AI for any teaching tasks",
], key="q5", label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">6. "AI tools save me meaningful time in lesson preparation."</div>',
            unsafe_allow_html=True)
q6_time = st.radio("", AGREEMENT_OPTIONS, key="q6", index=None,
                    label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 3: ASSESSMENT & FEEDBACK ──────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">📝 Section 3 — AI in Student Assessment & Feedback</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">7. Have you used AI to help with student assessment or providing feedback?</div>',
            unsafe_allow_html=True)
q7_assessment = st.radio("", [
    "No — I haven't tried this",
    "I've experimented with it once or twice",
    "Yes — I use AI occasionally for assessment tasks",
    "Yes — I regularly use AI to support assessment and feedback",
], key="q7", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">8. How confident are you in identifying when a student has used AI to complete their work?</div>',
            unsafe_allow_html=True)
q8_detect = st.radio("", [
    "Not at all confident — I can't tell",
    "Slightly confident — I sometimes suspect but can't be sure",
    "Moderately confident — I can usually tell",
    "Very confident — I have clear methods to identify AI use",
], key="q8", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">9. "AI-assisted assessment helps me give better, more personalised feedback to students."</div>',
            unsafe_allow_html=True)
q9_feedback = st.radio("", AGREEMENT_OPTIONS, key="q9", index=None,
                        label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 4: CLASSROOM MANAGEMENT ──────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">🏫 Section 4 — Managing AI-Empowered Students in the Classroom</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">10. How often do you notice students using AI tools during class or for homework?</div>',
            unsafe_allow_html=True)
q10_students = st.radio("", FREQUENCY_OPTIONS, key="q10", index=None,
                         label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">11. What is your biggest classroom challenge related to students and AI? (Choose one)</div>',
            unsafe_allow_html=True)
q11_challenge = st.radio("", [
    "Students submitting AI-generated work as their own",
    "Students being distracted by AI tools on devices",
    "Students knowing more about AI than I do",
    "Unequal access — some students use AI, others don't",
    "Students not developing critical thinking skills",
    "I haven't faced significant AI-related classroom challenges yet",
], key="q11", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">12. "I feel equipped to manage a classroom where students actively use AI tools."</div>',
            unsafe_allow_html=True)
q12_equipped = st.radio("", AGREEMENT_OPTIONS, key="q12", index=None,
                         label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 5: POLICY & DPDP ──────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">🔒 Section 5 — School AI Policy & DPDP Act Awareness</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">13. Does your school have a clear AI policy or guidelines for teachers and students?</div>',
            unsafe_allow_html=True)
q13_policy = st.radio("", [
    "Yes — and I am aware of it",
    "Yes — but I haven't read it properly",
    "I think one exists but I'm not sure",
    "No policy exists as far as I know",
    "I don't know",
], key="q13", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">14. Are you aware of the DPDP Act 2023 (Digital Personal Data Protection) and what it means for student data in schools?</div>',
            unsafe_allow_html=True)
q14_dpdp = st.radio("", [
    "Not aware of this at all",
    "I've heard of it but don't know the details",
    "Somewhat aware — I know it affects how we handle student data",
    "Fully aware — I understand our school's obligations",
], key="q14", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">15. "I know which AI tools are safe and appropriate to use with students."</div>',
            unsafe_allow_html=True)
q15_safe_tools = st.radio("", AGREEMENT_OPTIONS, key="q15", index=None,
                           label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 6: PROFESSIONAL DEVELOPMENT ──────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">🎓 Section 6 — Professional Development Needs in AI</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">16. Have you attended any AI training or professional development session so far?</div>',
            unsafe_allow_html=True)
q16_training = st.radio("", [
    "No — none at all",
    "Only a very brief introductory session",
    "One or two structured workshops",
    "Regular ongoing training",
], key="q16", index=None, label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">17. What kind of AI training would help you most? (Select up to 3)</div>',
            unsafe_allow_html=True)
q17_pd_needs = st.multiselect("", PD_OPTIONS, max_selections=3,
                               key="q17", label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">18. What is your preferred format for AI training?</div>',
            unsafe_allow_html=True)
q18_format = st.radio("", [
    "Hands-on workshop (in person)",
    "Short online videos I can watch at my own pace",
    "Peer learning — learning from a colleague in my school",
    "A structured online course with assignments",
    "Embedded in my daily work — learning by doing",
], key="q18", index=None, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SECTION 7: CONCERNS & FEARS ───────────────────────────────────────────────
st.markdown("""
<div class="section-card">
<div class="section-title">💬 Section 7 — Concerns & Fears About AI</div>
""", unsafe_allow_html=True)

st.markdown('<div class="q-label">19. What are your biggest concerns about AI in education? (Select all that apply)</div>',
            unsafe_allow_html=True)
q19_concerns = st.multiselect("", CONCERN_OPTIONS, key="q19",
                               label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">20. "I am worried that AI will significantly change or reduce my role as a teacher."</div>',
            unsafe_allow_html=True)
q20_job = st.radio("", AGREEMENT_OPTIONS, key="q20", index=None,
                    label_visibility="collapsed")

st.markdown('<div class="q-label" style="margin-top:16px;">21. In your own words — what is the ONE thing about AI in your classroom that you most want your school leadership to understand or address?</div>',
            unsafe_allow_html=True)
q21_open = st.text_area("", placeholder="Share whatever is on your mind — your voice matters here…",
                         height=100, key="q21", label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ── SUBMIT ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.button("✅ Submit My Survey Response"):

    # Validation — required fields
    errors = []
    if not school_name:
        errors.append("Please enter your school name.")
    if not q1_comfort:
        errors.append("Section 1: Please answer Q1 (personal comfort with AI).")
    if not q3_feeling:
        errors.append("Section 1: Please answer Q3 (how you feel about AI).")
    if not q4_frequency:
        errors.append("Section 2: Please answer Q4 (how often you use AI for lessons).")
    if not q6_time:
        errors.append("Section 2: Please answer Q6 (AI saves time).")
    if not q7_assessment:
        errors.append("Section 3: Please answer Q7 (AI in assessment).")
    if not q8_detect:
        errors.append("Section 3: Please answer Q8 (detecting AI use).")
    if not q10_students:
        errors.append("Section 4: Please answer Q10 (students using AI).")
    if not q11_challenge:
        errors.append("Section 4: Please answer Q11 (classroom challenge).")
    if not q12_equipped:
        errors.append("Section 4: Please answer Q12 (feeling equipped).")
    if not q13_policy:
        errors.append("Section 5: Please answer Q13 (school AI policy).")
    if not q14_dpdp:
        errors.append("Section 5: Please answer Q14 (DPDP awareness).")
    if not q16_training:
        errors.append("Section 6: Please answer Q16 (prior AI training).")
    if not q20_job:
        errors.append("Section 7: Please answer Q20 (concern about role).")

    if errors:
        for e in errors:
            st.warning(e)
    else:
        # Build response dict
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "teacher_name": teacher_name or "Anonymous",
            "school_name": school_name,
            "subject": subject,
            "experience": experience,
            "classes_taught": " | ".join(classes) if classes else "Not specified",

            # Section 1
            "q1_personal_comfort": q1_comfort,
            "q2_tools_used": " | ".join(q2_tools) if q2_tools else "None",
            "q3_feeling_about_ai": q3_feeling,

            # Section 2
            "q4_lesson_planning_frequency": q4_frequency,
            "q5_ai_uses_in_teaching": " | ".join(q5_uses) if q5_uses else "None",
            "q6_ai_saves_time": q6_time,

            # Section 3
            "q7_ai_in_assessment": q7_assessment,
            "q8_detect_ai_use_confidence": q8_detect,
            "q9_ai_feedback_quality": q9_feedback or "Not answered",

            # Section 4
            "q10_students_using_ai": q10_students,
            "q11_classroom_challenge": q11_challenge,
            "q12_feel_equipped": q12_equipped,

            # Section 5
            "q13_school_policy": q13_policy,
            "q14_dpdp_awareness": q14_dpdp,
            "q15_knows_safe_tools": q15_safe_tools or "Not answered",

            # Section 6
            "q16_prior_training": q16_training,
            "q17_pd_needs": " | ".join(q17_pd_needs) if q17_pd_needs else "Not specified",
            "q18_preferred_format": q18_format or "Not answered",

            # Section 7
            "q19_concerns": " | ".join(q19_concerns) if q19_concerns else "None",
            "q20_worried_about_role": q20_job,
            "q21_open_message": q21_open or "Not provided",
        }

        save_to_csv(response)
        st.session_state.submitted = True
        st.rerun()

st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.75rem;margin-top:20px;">
    AI Strategy Workshops for School Heads · India 2026 · Responses are confidential
</div>
""", unsafe_allow_html=True)
