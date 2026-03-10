"""
AI Safety Workshop — Interactive Facilitator App
"Navigating AI: What We Know, What We Fear, What We Must Do"
For Senior Students & Parents

Run with:  streamlit run workshop_app.py
Requires:  pip install streamlit plotly

FACILITATOR CONTROLS:
  - Use the sidebar buttons to move between slides
  - On each poll slide: enter vote counts then click REVEAL
  - All votes auto-save to workshop_votes.csv
"""

import streamlit as st
import plotly.graph_objects as go
import csv
import os
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Safety Workshop",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

/* Dark projector-ready background */
.stApp {
    background-color: #111111;
    color: #f0f0f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 100%; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1a1a1a !important;
    border-right: 1px solid #333 !important;
}
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* Sidebar nav buttons */
div[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: #2a2a2a !important;
    border: 1px solid #444 !important;
    border-radius: 8px !important;
    color: #ccc !important;
    font-size: 0.82rem !important;
    padding: 8px 12px !important;
    text-align: left !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    margin-bottom: 3px !important;
    transition: all 0.15s !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: #e8450a !important;
    border-color: #e8450a !important;
    color: white !important;
}

/* Active slide button */
.active-slide button {
    background: #e8450a !important;
    border-color: #e8450a !important;
    color: white !important;
}

/* Main content area buttons */
.main-btn > button,
.stButton > button {
    background: #e8450a !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: 12px 32px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #c23d08 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #444 !important;
    color: #888 !important;
    transform: none !important;
    cursor: not-allowed !important;
}

/* Reveal button — teal */
.reveal-btn > button {
    background: #0d9488 !important;
    font-size: 1.1rem !important;
    padding: 14px 40px !important;
    width: 100% !important;
}
.reveal-btn > button:hover { background: #0a7c72 !important; }

/* Number inputs */
.stNumberInput > div > div > input {
    background: #1e1e1e !important;
    border: 2px solid #444 !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    font-family: 'Nunito', sans-serif !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #e8450a !important;
}
.stNumberInput label {
    color: #aaa !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── Slide cards ── */
.slide-hero {
    background: linear-gradient(135deg, #1a1a1a 0%, #222 100%);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 3rem 3.5rem;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.title-slide {
    background: #111 !important;
    border: 2px solid #e8450a !important;
}

.tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.tag-coral { background: rgba(232,69,10,0.2); color: #e8450a; border: 1px solid #e8450a; }
.tag-teal  { background: rgba(13,148,136,0.2); color: #0d9488; border: 1px solid #0d9488; }
.tag-amber { background: rgba(217,119,6,0.2);  color: #d97706; border: 1px solid #d97706; }
.tag-indigo{ background: rgba(67,56,202,0.2);  color: #818cf8; border: 1px solid #818cf8; }

.slide-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3.8rem;
    color: #ffffff;
    line-height: 1.05;
    letter-spacing: 1px;
    margin: 0 0 16px;
}
.slide-subtitle {
    font-size: 1.15rem;
    color: #aaa;
    line-height: 1.6;
    max-width: 700px;
}

/* ── Question box ── */
.question-box {
    background: #111;
    border-left: 5px solid #e8450a;
    border-radius: 12px;
    padding: 24px 28px;
    margin: 20px 0;
}
.question-text {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.4;
}

/* ── Answer option cards ── */
.option-card {
    background: #1e1e1e;
    border: 1.5px solid #333;
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 10px;
    font-size: 1.0rem;
    color: #ddd;
    font-weight: 600;
    transition: border-color 0.2s;
}
.option-card:hover { border-color: #555; }
.option-letter {
    display: inline-block;
    background: #e8450a;
    color: white;
    font-weight: 800;
    font-size: 0.85rem;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    text-align: center;
    line-height: 26px;
    margin-right: 12px;
    flex-shrink: 0;
}

/* ── Stat callouts ── */
.stat-row {
    display: flex;
    gap: 20px;
    margin: 24px 0;
}
.stat-box {
    flex: 1;
    background: #1e1e1e;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    border-top: 4px solid;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 8px;
}
.stat-desc { font-size: 0.88rem; color: #aaa; line-height: 1.5; }

/* ── Reveal panels ── */
.reveal-grid {
    display: grid;
    grid-template-columns: 1fr 60px 1fr;
    gap: 0;
    margin: 16px 0;
}
.panel {
    background: #1e1e1e;
    border-radius: 14px;
    padding: 20px 24px;
}
.panel-header {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid;
}
.panel-item {
    font-size: 0.95rem;
    color: #ccc;
    padding: 8px 0;
    border-bottom: 1px solid #2a2a2a;
    line-height: 1.45;
}
.panel-item:last-child { border-bottom: none; }
.vs-col {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #444;
}

/* ── Insight bar ── */
.insight-bar {
    background: #111;
    border: 1.5px solid #e8450a;
    border-radius: 12px;
    padding: 16px 22px;
    margin: 16px 0 10px;
    font-size: 0.95rem;
    color: #ddd;
    line-height: 1.6;
}
.insight-label {
    color: #e8450a;
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ── Discussion bar ── */
.discuss-bar {
    background: #0d9488;
    border-radius: 10px;
    padding: 14px 20px;
    font-size: 0.95rem;
    font-weight: 700;
    color: white;
    line-height: 1.5;
}

/* ── Commitment columns ── */
.commit-col {
    background: #1e1e1e;
    border-radius: 14px;
    padding: 20px 22px;
    height: 100%;
}
.commit-header {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid;
}
.commit-item {
    font-size: 0.9rem;
    color: #ccc;
    padding: 9px 0;
    border-bottom: 1px solid #2a2a2a;
    display: flex;
    gap: 10px;
    line-height: 1.4;
}
.commit-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}

/* ── Theme chips ── */
.theme-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 20px;
}
.theme-chip {
    background: #e8450a;
    color: white;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 7px 16px;
    border-radius: 20px;
}

/* ── Progress bar ── */
.progress-container {
    background: #222;
    border-radius: 6px;
    height: 6px;
    margin: 12px 0;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #e8450a, #0d9488);
    border-radius: 6px;
    transition: width 0.4s ease;
}

/* Divider */
.sdivider {
    border: none;
    border-top: 1px solid #2a2a2a;
    margin: 16px 0;
}

/* Close slide */
.close-quote {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: #e8450a;
    line-height: 1.1;
    margin: 12px 0 20px;
}
.resource-chip {
    display: inline-block;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px 18px;
    margin-right: 12px;
    margin-top: 8px;
}
.resource-name { font-size: 0.9rem; font-weight: 800; color: #0d9488; }
.resource-url  { font-size: 0.78rem; color: #666; margin-top: 2px; }

/* Alerts */
div.stAlert > div {
    background: #1e1e1e !important;
    border: 1px solid #e8450a !important;
    border-radius: 10px !important;
    color: #ddd !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

QUESTIONS = [
    {
        "id": "q1",
        "theme": "Dependency & Critical Thinking",
        "color": "#e8450a",
        "tag_class": "tag-coral",
        "question": "If you had to write a 500-word essay on a topic you know well — would you use an AI tool to help you?",
        "options": [
            "No — I prefer to write it entirely myself",
            "Yes — to help get started or overcome writer's block",
            "Yes — I'd use it to draft and then edit it myself",
            "Yes — I would use whatever the AI produces with light editing",
        ],
        "student_pov": [
            "Most students use AI as a natural starting point",
            "Worry about being judged, not about learning loss",
            "'Everyone does it' is the dominant justification",
        ],
        "parent_pov": [
            "Parents want AI banned from homework entirely",
            "Deep concern about reduced writing skills long-term",
            "Fear their child won't cope in exams without AI",
        ],
        "insight": "Students see AI as a tool; parents see it as a crutch. Both are right — the question is who controls how it's used.",
        "discuss": "At what point does AI 'help' become AI 'doing it for you'? Where should the line be?",
    },
    {
        "id": "q2",
        "theme": "Privacy & Data Safety",
        "color": "#d97706",
        "tag_class": "tag-amber",
        "question": "You've been using a helpful AI study app for 3 months. You discover it has been sharing your chat history with advertisers. What do you do?",
        "options": [
            "Delete the app immediately — privacy is non-negotiable",
            "Read the terms first, then decide — it might be fine",
            "Keep using it, it's too useful to give up",
            "Not sure — I don't fully understand what that means for me",
        ],
        "student_pov": [
            "Only 30% would verify through official channels first",
            "Convenience often wins over privacy in practice",
            "Students underestimate the value of their own data",
        ],
        "parent_pov": [
            "Parents are alarmed — would want to delete immediately",
            "Many parents don't know what apps their child uses daily",
            "Trust in school to vet tools is high — possibly too high",
        ],
        "insight": "Under DPDP Act 2023, schools have legal obligations to protect student data. Every AI tool must be evaluated for compliance — this is the principal's responsibility.",
        "discuss": "Do you know what data the apps on your phone are collecting right now? Should schools publish a list of approved AI tools?",
    },
    {
        "id": "q3",
        "theme": "Mental Health & Emotional Safety",
        "color": "#0d9488",
        "tag_class": "tag-teal",
        "question": "A student in your class is feeling lonely and anxious. They prefer talking to an AI chatbot about their feelings rather than a real person. What is your reaction?",
        "options": [
            "Completely fine — if it helps, it helps",
            "Okay for now, but they should also talk to a real person",
            "Concerning — AI cannot replace human emotional support",
            "Depends — if a counsellor is unavailable, AI might bridge the gap",
        ],
        "student_pov": [
            "Students feel less judged by AI — no social risk at all",
            "Many have already used AI chatbots for emotional support",
            "Privacy is the key draw — AI doesn't gossip or tell teachers",
        ],
        "parent_pov": [
            "Parents are alarmed by AI replacing human connection",
            "Concerned AI will give wrong or harmful mental health advice",
            "Want school to actively discourage emotional AI dependency",
        ],
        "insight": "AI emotional companions are already widely used by teenagers. Schools and parents are largely unaware. This conversation needs to happen before a crisis, not after.",
        "discuss": "What are the warning signs that a student's AI use has crossed into emotional dependency? What should a parent or teacher do?",
    },
    {
        "id": "q4",
        "theme": "Misinformation & AI Ethics",
        "color": "#4338ca",
        "tag_class": "tag-indigo",
        "question": "You receive a convincing voice message that sounds exactly like your principal, saying school is cancelled tomorrow. How do you verify it's real?",
        "options": [
            "I'd call the school office directly to confirm",
            "I'd check the school's official app or website first",
            "I'd ask a classmate — if others got it too, it must be real",
            "I'd believe it — it sounded completely real to me",
        ],
        "student_pov": [
            "Only 30% would verify through official channels first",
            "Peer confirmation is the most common instinct for students",
            "Students overestimate their ability to detect AI-generated fakes",
        ],
        "parent_pov": [
            "Parents are deeply unsettled by the deepfake possibility",
            "Majority would call the school office immediately",
            "Many are unaware that deepfake audio is free and easy to create",
        ],
        "insight": "Deepfake audio and video is now accessible to anyone with a smartphone. Schools need explicit protocols for verifying digital communications — and students need media literacy.",
        "discuss": "What would a school 'deepfake policy' look like? How do you teach a child to be sceptical without making them distrust everything?",
    },
    {
        "id": "q5",
        "theme": "Responsibility & AI Policy",
        "color": "#e8450a",
        "tag_class": "tag-coral",
        "question": "Your school introduces a rule: no AI tools can be used for any assignment without written permission from the subject teacher. Is this the right call?",
        "options": [
            "Yes — clear rules are needed and this is fair",
            "Too strict — AI is a useful tool and should be allowed freely",
            "Partially right — rules should depend on the subject and task",
            "Schools should educate about AI use, not just ban or permit it",
        ],
        "student_pov": [
            "Most students prefer guided use over outright banning",
            "Students feel unfairly targeted — teachers use AI too",
            "Want consistency — different rules per teacher is very confusing",
        ],
        "parent_pov": [
            "Parents are split — worry about both over-restriction and harm",
            "Many parents want stricter rules than their own children do",
            "Strong support for schools educating about responsible AI use",
        ],
        "insight": "Research shows blanket bans don't work — students work around them. Structured, policy-guided AI use with clear learning goals is more effective than prohibition.",
        "discuss": "If you were to write your school's AI policy right now — in one sentence — what would it say? Share at your table, then with the room.",
    },
]

COMMITMENTS = {
    "students": [
        "I will check the privacy policy of one AI app I use this week",
        "I will try writing one assignment without any AI help",
        "I will talk to a real person next time I feel anxious — not an AI",
        "I will fact-check one AI output before using it in schoolwork",
        "I will ask my teacher before using AI on any assignment",
    ],
    "parents": [
        "I will ask my child to show me the AI tools they use this week",
        "I will have one calm, non-judgmental conversation about AI at home",
        "I will learn what the DPDP Act means for my child's school data",
        "I will set one clear household agreement about AI and screen time",
        "I will attend the school's next parent session on AI education",
    ],
}

CSV_FILE = "workshop_votes.csv"
TOTAL_SLIDES = 4 + len(QUESTIONS) * 2  # title + how + context + (poll+reveal)*5 + debrief + commitments + close

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "slide": 0,
        "school": "",
        "votes": {q["id"]: {"student": [0,0,0,0], "parent": [0,0,0,0]} for q in QUESTIONS},
        "revealed": {q["id"]: False for q in QUESTIONS},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════════════════════
# CSV SAVE
# ══════════════════════════════════════════════════════════════════════════════
def save_votes_csv():
    rows = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    school = st.session_state.school or "Not set"
    for q in QUESTIONS:
        qid = q["id"]
        sv = st.session_state.votes[qid]["student"]
        pv = st.session_state.votes[qid]["parent"]
        for i, opt in enumerate(q["options"]):
            rows.append({
                "timestamp": ts,
                "school": school,
                "question_id": qid,
                "question_theme": q["theme"],
                "option": opt,
                "option_letter": chr(65+i),
                "student_votes": sv[i],
                "parent_votes": pv[i],
            })
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

# ══════════════════════════════════════════════════════════════════════════════
# CHART BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def make_chart(qid, options, color):
    sv = st.session_state.votes[qid]["student"]
    pv = st.session_state.votes[qid]["parent"]
    labels = [f"{chr(65+i)}. {opt[:45]}{'…' if len(opt)>45 else ''}" for i, opt in enumerate(options)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="🎓 Students",
        x=labels, y=sv,
        marker_color="#0d9488",
        text=sv, textposition="outside",
        textfont=dict(color="white", size=14, family="Nunito"),
    ))
    fig.add_trace(go.Bar(
        name="👨‍👩‍👧 Parents",
        x=labels, y=pv,
        marker_color="#4338ca",
        text=pv, textposition="outside",
        textfont=dict(color="white", size=14, family="Nunito"),
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cccccc", family="Nunito"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ccc", size=13),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(
            tickfont=dict(color="#aaa", size=11),
            gridcolor="#2a2a2a",
            showline=False,
        ),
        yaxis=dict(
            gridcolor="#2a2a2a",
            tickfont=dict(color="#888"),
            zeroline=False,
        ),
        margin=dict(t=40, b=20, l=10, r=10),
        height=280,
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Build slide index map ──────────────────────────────────────────────────────
# 0=title, 1=how, 2=context, 3-7=polls, 8-12=reveals, 13=debrief, 14=commit, 15=close
SLIDE_MAP = {
    0: "title",
    1: "how",
    2: "context",
    **{3+i: f"poll_{i}" for i in range(5)},
    **{8+i: f"reveal_{i}" for i in range(5)},
    13: "debrief",
    14: "commitments",
    15: "close",
}
SLIDE_LABELS = {
    0: "🏠  Title",
    1: "ℹ️  How This Works",
    2: "📊  Context",
    3: "❓  Q1 — Poll",
    4: "❓  Q2 — Poll",
    5: "❓  Q3 — Poll",
    6: "❓  Q4 — Poll",
    7: "❓  Q5 — Poll",
    8: "📊  Q1 — Reveal",
    9: "📊  Q2 — Reveal",
    10: "📊  Q3 — Reveal",
    11: "📊  Q4 — Reveal",
    12: "📊  Q5 — Reveal",
    13: "💬  Debrief",
    14: "✅  Commitments",
    15: "🎯  Close",
}

def render_title():
    st.markdown("""
    <div style="padding: 2rem 0;">
        <div style="font-size:0.75rem;font-weight:800;letter-spacing:3px;
                    color:#e8450a;text-transform:uppercase;margin-bottom:20px;">
            AI Safety & Ethics Workshop · India 2026
        </div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:5.5rem;
                    color:#fff;line-height:0.95;margin-bottom:24px;">
            NAVIGATING AI<br>
            <span style="color:#e8450a;">WHAT WE KNOW.</span><br>
            <span style="color:#e8450a;">WHAT WE FEAR.</span><br>
            WHAT WE MUST DO.
        </div>
        <div style="font-size:1.2rem;color:#888;margin-bottom:32px;">
            An interactive session for senior students and parents
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <span style="background:#1e1e1e;border:1px solid #333;border-radius:8px;
                         padding:8px 18px;font-size:0.85rem;font-weight:700;color:#aaa;">
                🎓  Senior Students
            </span>
            <span style="background:#1e1e1e;border:1px solid #333;border-radius:8px;
                         padding:8px 18px;font-size:0.85rem;font-weight:700;color:#aaa;">
                👨‍👩‍👧  Parents
            </span>
            <span style="background:#1e1e1e;border:1px solid #333;border-radius:8px;
                         padding:8px 18px;font-size:0.85rem;font-weight:700;color:#aaa;">
                ⏱️  ~60 Minutes
            </span>
            <span style="background:#1e1e1e;border:1px solid #333;border-radius:8px;
                         padding:8px 18px;font-size:0.85rem;font-weight:700;color:#aaa;">
                ❓  5 Questions
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_how():
    st.markdown("""
    <div style="margin-bottom:28px;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:#fff;margin-bottom:8px;">
            HOW THIS SESSION WORKS
        </div>
        <div style="color:#888;font-size:1rem;">
            Four simple steps — repeated for each of the 5 questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("❓", "Poll Question", "A real-life AI scenario appears on screen. Read it carefully before voting."),
        ("🙋", "Vote Separately", "Students vote as a group on the left. Parents vote on the right. Raise hands — facilitator counts."),
        ("📊", "Results Revealed", "Facilitator reveals both sets of votes with a live chart. See where views differ."),
        ("💬", "Table Discussion", "3-minute table discussion on the insight prompt. Then we hear from the room."),
    ]
    cols = st.columns(4)
    for i, (icon, title, body) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style="background:#1e1e1e;border-radius:14px;padding:24px 20px;
                        border-top:4px solid #e8450a;text-align:center;height:220px;">
                <div style="font-size:2.5rem;margin-bottom:14px;">{icon}</div>
                <div style="font-weight:800;font-size:1rem;color:#fff;margin-bottom:10px;">
                    {i+1}. {title}
                </div>
                <div style="font-size:0.88rem;color:#999;line-height:1.5;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:28px;background:#111;border-left:4px solid #e8450a;
                border-radius:10px;padding:16px 22px;font-size:1rem;
                color:#ccc;font-weight:600;">
        🎯 &nbsp; <strong style="color:#e8450a;">No right or wrong answers.</strong>
        Honesty is what makes this session powerful.
        Students and parents will often disagree — that's the whole point.
    </div>
    """, unsafe_allow_html=True)


def render_context():
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:#fff;margin-bottom:24px;">
        WHY WE NEED TO TALK ABOUT THIS — NOW
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    stats = [
        (c1, "62%", "of Indian students use AI tools for homework regularly", "#e8450a"),
        (c2, "₹200Cr", "max penalty for schools violating student data privacy under DPDP Act 2023", "#d97706"),
        (c3, "1 in 3", "teens report feeling anxious or overwhelmed by AI content they've seen online", "#0d9488"),
    ]
    for col, num, desc, color in stats:
        with col:
            st.markdown(f"""
            <div style="background:#1e1e1e;border-radius:14px;padding:28px 20px;
                        text-align:center;border-top:4px solid {color};">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:3.5rem;
                             color:{color};line-height:1;margin-bottom:12px;">{num}</div>
                <div style="font-size:0.9rem;color:#aaa;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:28px;">
        <div style="font-size:0.85rem;font-weight:700;color:#888;
                    text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">
            Today we explore four critical themes:
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <span style="background:#e8450a;color:white;font-size:0.88rem;font-weight:700;
                         padding:8px 18px;border-radius:20px;">🔒 Data Privacy & DPDP</span>
            <span style="background:#e8450a;color:white;font-size:0.88rem;font-weight:700;
                         padding:8px 18px;border-radius:20px;">🧠 Critical Thinking Erosion</span>
            <span style="background:#e8450a;color:white;font-size:0.88rem;font-weight:700;
                         padding:8px 18px;border-radius:20px;">😰 Mental Health & Dependency</span>
            <span style="background:#e8450a;color:white;font-size:0.88rem;font-weight:700;
                         padding:8px 18px;border-radius:20px;">⚠️ Misinformation & Deepfakes</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_poll(q_index):
    q = QUESTIONS[q_index]
    qid = q["id"]

    # Header
    st.markdown(f"""
    <div style="margin-bottom:20px;">
        <span class="tag {q['tag_class']}">
            Question {q_index+1} of 5 &nbsp;·&nbsp; {q['theme']}
        </span>
        <div style="font-size:0.8rem;font-weight:700;color:#666;
                    text-transform:uppercase;letter-spacing:1px;margin-top:6px;">
            POLL — VOTE NOW
        </div>
    </div>
    <div class="question-box">
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options display
    for i, opt in enumerate(q["options"]):
        letter = chr(65 + i)
        st.markdown(f"""
        <div class="option-card">
            <span class="option-letter">{letter}</span>
            {opt}
        </div>
        """, unsafe_allow_html=True)

    # Vote entry section
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#111;border:1px solid #2a2a2a;border-radius:14px;
                padding:20px 24px;margin-top:8px;">
        <div style="font-size:0.78rem;font-weight:800;letter-spacing:1.5px;
                    text-transform:uppercase;color:#888;margin-bottom:16px;">
            📋 &nbsp; Facilitator: Enter vote counts as hands go up
        </div>
    """, unsafe_allow_html=True)

    vote_tabs = st.tabs(["🎓  Student Votes", "👨‍👩‍👧  Parent Votes"])

    with vote_tabs[0]:
        cols = st.columns(4)
        for i in range(4):
            with cols[i]:
                val = st.number_input(
                    f"Option {chr(65+i)}",
                    min_value=0, max_value=999,
                    value=st.session_state.votes[qid]["student"][i],
                    key=f"sv_{qid}_{i}",
                    step=1,
                )
                st.session_state.votes[qid]["student"][i] = val

    with vote_tabs[1]:
        cols = st.columns(4)
        for i in range(4):
            with cols[i]:
                val = st.number_input(
                    f"Option {chr(65+i)}",
                    min_value=0, max_value=999,
                    value=st.session_state.votes[qid]["parent"][i],
                    key=f"pv_{qid}_{i}",
                    step=1,
                )
                st.session_state.votes[qid]["parent"][i] = val

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Reveal button
    st.markdown('<div class="reveal-btn">', unsafe_allow_html=True)
    if st.button(
        f"▶  Reveal Results for Question {q_index+1}",
        key=f"reveal_btn_{qid}",
        use_container_width=True,
    ):
        st.session_state.revealed[qid] = True
        save_votes_csv()
        # Jump to reveal slide
        st.session_state.slide = 8 + q_index
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Instruction footer
    st.markdown(f"""
    <div style="margin-top:12px;background:{q['color']};border-radius:8px;
                padding:10px 18px;font-size:0.9rem;font-weight:700;color:white;">
        📋 &nbsp; Students raise hands on LEFT side of room &nbsp;·&nbsp;
        Parents raise hands on RIGHT side &nbsp;·&nbsp; Count and enter above
    </div>
    """, unsafe_allow_html=True)


def render_reveal(q_index):
    q = QUESTIONS[q_index]
    qid = q["id"]

    # Header
    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <span class="tag {q['tag_class']}">
            Q{q_index+1} Results &nbsp;·&nbsp; {q['theme']}
        </span>
        <div style="color:#888;font-size:0.92rem;font-style:italic;margin-top:8px;">
            "{q['question']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chart
    if any(st.session_state.votes[qid]["student"]) or any(st.session_state.votes[qid]["parent"]):
        st.plotly_chart(
            make_chart(qid, q["options"], q["color"]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.info("No votes recorded yet — go back to the poll slide to enter votes.")

    # Student vs Parent panels
    col_s, col_vs, col_p = st.columns([10, 1, 10])
    with col_s:
        items_html = "".join(
            f'<div class="panel-item">{item}</div>' for item in q["student_pov"]
        )
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header" style="color:#0d9488;border-color:#0d9488;">
                🎓 &nbsp; WHAT STUDENTS TYPICALLY SAY
            </div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    with col_vs:
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:center;
                    height:100%;font-family:'Bebas Neue',sans-serif;
                    font-size:1.6rem;color:#333;padding-top:40px;">VS</div>
        """, unsafe_allow_html=True)

    with col_p:
        items_html = "".join(
            f'<div class="panel-item">{item}</div>' for item in q["parent_pov"]
        )
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header" style="color:#818cf8;border-color:#818cf8;">
                👨‍👩‍👧 &nbsp; WHAT PARENTS TYPICALLY SAY
            </div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    # Insight + Discussion
    st.markdown(f"""
    <div class="insight-bar">
        <div class="insight-label">💡 Key Insight</div>
        {q['insight']}
    </div>
    <div class="discuss-bar">
        💬 &nbsp; <strong>DISCUSS (3 min):</strong> &nbsp; {q['discuss']}
    </div>
    """, unsafe_allow_html=True)


def render_debrief():
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;
                color:#fff;margin-bottom:8px;">
        WHOLE-ROOM DEBRIEF
    </div>
    <div style="color:#888;font-size:1rem;margin-bottom:24px;">
        Where were the biggest gaps between what students and parents said?
    </div>
    """, unsafe_allow_html=True)

    gaps = [
        ("Q1 — Dependency", "#e8450a", "Students see AI as normal. Parents see it as a threat to skills."),
        ("Q2 — Privacy", "#d97706", "Both groups have gaps — students in awareness, parents in knowing what their child uses."),
        ("Q3 — Mental Health", "#0d9488", "The largest gap: students have already adopted AI for emotions. Parents are unaware."),
        ("Q4 — Misinformation", "#4338ca", "Students overestimate detection ability. Parents are fearful but equally unprepared."),
        ("Q5 — Policy", "#e8450a", "Both groups want guidance — the gap is WHO should set the rules and HOW strict they should be."),
    ]

    for label, color, gap in gaps:
        c1, c2 = st.columns([2, 8])
        with c1:
            st.markdown(f"""
            <div style="background:{color};border-radius:10px;padding:14px 12px;
                        text-align:center;font-size:0.82rem;font-weight:800;
                        color:white;height:58px;display:flex;align-items:center;
                        justify-content:center;">{label}</div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#1e1e1e;border-radius:10px;padding:14px 20px;
                        font-size:0.97rem;color:#ccc;height:58px;
                        display:flex;align-items:center;">{gap}</div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:20px;background:#111;border:1px solid #333;
                border-radius:12px;padding:18px 22px;color:#888;
                font-size:0.92rem;line-height:1.6;">
        <strong style="color:#e8450a;">Facilitator:</strong>
        Allow 8–10 minutes here. Ask: "Which gap surprised you most?" and
        "What one thing will you do differently at home this week?"
        Capture key themes on a flip chart if available.
    </div>
    """, unsafe_allow_html=True)


def render_commitments():
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;
                color:#fff;margin-bottom:6px;">
        BEFORE YOU LEAVE — YOUR COMMITMENT CARD
    </div>
    <div style="color:#888;font-size:1rem;margin-bottom:24px;font-style:italic;">
        Each person writes ONE commitment on the card provided. Take it home.
    </div>
    """, unsafe_allow_html=True)

    col_s, col_p = st.columns(2)
    with col_s:
        items_html = "".join(f"""
        <div class="commit-item">
            <div class="commit-dot" style="background:#0d9488;"></div>
            <div>{item}</div>
        </div>""" for item in COMMITMENTS["students"])
        st.markdown(f"""
        <div class="commit-col" style="border-top:4px solid #0d9488;">
            <div class="commit-header" style="color:#0d9488;border-color:#0d9488;">
                🎓 &nbsp; FOR STUDENTS
            </div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    with col_p:
        items_html = "".join(f"""
        <div class="commit-item">
            <div class="commit-dot" style="background:#818cf8;"></div>
            <div>{item}</div>
        </div>""" for item in COMMITMENTS["parents"])
        st.markdown(f"""
        <div class="commit-col" style="border-top:4px solid #818cf8;">
            <div class="commit-header" style="color:#818cf8;border-color:#818cf8;">
                👨‍👩‍👧 &nbsp; FOR PARENTS
            </div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:20px;background:#0d9488;border-radius:10px;
                padding:14px 22px;font-size:0.95rem;font-weight:700;color:white;">
        Facilitator: Hand out physical commitment cards.
        Ask for 2–3 volunteers to share theirs with the room before closing.
    </div>
    """, unsafe_allow_html=True)


def render_close():
    st.markdown("""
    <div style="padding:1.5rem 0;">
        <div style="font-size:0.8rem;font-weight:800;letter-spacing:2px;
                    color:#555;text-transform:uppercase;margin-bottom:16px;">
            AI Safety & Ethics Workshop · India 2026
        </div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;
                    color:#fff;margin-bottom:4px;">
            AI is not going away.
        </div>
        <div class="close-quote">
            THE QUESTION IS WHETHER YOU NAVIGATE IT<br>
            — OR IT NAVIGATES YOU.
        </div>
        <div style="font-size:1.05rem;color:#888;font-style:italic;
                    line-height:1.7;margin-bottom:28px;">
            Today's conversation was the first step.<br>
            The next steps are in your hands — and your home.
        </div>
        <div>
            <span class="resource-chip">
                <div class="resource-name">DPDP Act 2023</div>
                <div class="resource-url">meity.gov.in</div>
            </span>
            <span class="resource-chip">
                <div class="resource-name">AI4Bharat</div>
                <div class="resource-url">ai4bharat.org</div>
            </span>
            <span class="resource-chip">
                <div class="resource-name">CBSE AI Curriculum</div>
                <div class="resource-url">cbseacademic.nic.in</div>
            </span>
            <span class="resource-chip">
                <div class="resource-name">AI Strategy Workshops</div>
                <div class="resource-url">India 2026</div>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download CSV button
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button(
                label="⬇️  Download All Vote Data (CSV)",
                data=f,
                file_name=f"workshop_votes_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:6px 0 16px;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                    color:#e8450a;letter-spacing:1px;">AI SAFETY WORKSHOP</div>
        <div style="font-size:0.75rem;color:#555;margin-top:2px;">
            Facilitator Control Panel
        </div>
    </div>
    """, unsafe_allow_html=True)

    # School name input
    school = st.text_input(
        "School Name",
        value=st.session_state.school,
        placeholder="Enter school name…",
        key="school_input",
    )
    st.session_state.school = school

    st.markdown("<hr style='border-color:#2a2a2a;margin:14px 0;'>", unsafe_allow_html=True)

    # Progress bar
    pct = int((st.session_state.slide / (len(SLIDE_MAP) - 1)) * 100)
    st.markdown(f"""
    <div style="font-size:0.72rem;color:#555;margin-bottom:6px;text-transform:uppercase;
                letter-spacing:0.8px;">Progress</div>
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%;"></div>
    </div>
    <div style="font-size:0.72rem;color:#555;margin-bottom:14px;">
        Slide {st.session_state.slide + 1} of {len(SLIDE_MAP)}
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons
    st.markdown("<div style='font-size:0.72rem;color:#555;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;'>SLIDES</div>", unsafe_allow_html=True)

    for slide_num, label in SLIDE_LABELS.items():
        is_active = (st.session_state.slide == slide_num)
        btn_style = "background:#e8450a!important;color:white!important;border-color:#e8450a!important;" if is_active else ""
        if st.button(label, key=f"nav_{slide_num}"):
            st.session_state.slide = slide_num
            st.rerun()

    st.markdown("<hr style='border-color:#2a2a2a;margin:16px 0;'>", unsafe_allow_html=True)

    # Prev / Next
    col_p, col_n = st.columns(2)
    with col_p:
        if st.button("← Prev", disabled=st.session_state.slide == 0, key="prev"):
            st.session_state.slide = max(0, st.session_state.slide - 1)
            st.rerun()
    with col_n:
        if st.button("Next →", disabled=st.session_state.slide == len(SLIDE_MAP)-1, key="next"):
            st.session_state.slide = min(len(SLIDE_MAP)-1, st.session_state.slide + 1)
            st.rerun()

    # Save button
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("💾  Save All Votes to CSV", use_container_width=True, key="save_all"):
        save_votes_csv()
        st.success("Saved to workshop_votes.csv")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════
slide_key = SLIDE_MAP.get(st.session_state.slide, "title")

if slide_key == "title":
    render_title()
elif slide_key == "how":
    render_how()
elif slide_key == "context":
    render_context()
elif slide_key.startswith("poll_"):
    idx = int(slide_key.split("_")[1])
    render_poll(idx)
elif slide_key.startswith("reveal_"):
    idx = int(slide_key.split("_")[1])
    render_reveal(idx)
elif slide_key == "debrief":
    render_debrief()
elif slide_key == "commitments":
    render_commitments()
elif slide_key == "close":
    render_close()
