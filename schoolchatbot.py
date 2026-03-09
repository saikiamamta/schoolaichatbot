"""
AI Readiness Chatbot for School Leaders
AI Strategy Workshops Initiative — India 2026

Run with:  streamlit run app.py
Requires:  pip install streamlit anthropic
Set env:   ANTHROPIC_API_KEY=your_key_here
"""

import streamlit as st
import os
import json
import time
from dotenv import load_dotenv
load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Readiness Assessment | School Leaders",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0f1f3d 0%, #162847 60%, #1a3a5c 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 780px; }

/* ── Header card ── */
.header-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 18px;
    padding: 28px 32px 22px;
    margin-bottom: 20px;
}
.header-card h1 {
    font-family: 'Playfair Display', serif !important;
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    line-height: 1.25;
}
.header-card p {
    color: rgba(255,255,255,0.55);
    font-size: 0.875rem;
    margin: 0;
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
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}

/* ── Progress ── */
.progress-wrap {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.progress-text { color: rgba(255,255,255,0.5); font-size: 0.78rem; white-space: nowrap; }

/* ── Chat bubbles ── */
.chat-container { display: flex; flex-direction: column; gap: 14px; margin-bottom: 24px; }

.bubble-bot-wrap { display: flex; gap: 10px; align-items: flex-start; }
.bubble-user-wrap { display: flex; gap: 10px; align-items: flex-start; justify-content: flex-end; }

.bot-avatar {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, #0e9d8a, #13b89f);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0; margin-top: 2px;
    box-shadow: 0 3px 10px rgba(14,157,138,0.35);
}
.user-avatar {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, #c9a84c, #e0bc6e);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0; margin-top: 2px;
}

.bubble-bot {
    background: rgba(255,255,255,0.97);
    color: #1a1a2e;
    border-radius: 16px;
    border-top-left-radius: 4px;
    padding: 14px 18px;
    font-size: 0.92rem;
    line-height: 1.65;
    max-width: 82%;
    box-shadow: 0 3px 14px rgba(0,0,0,0.15);
}
.bubble-bot strong { color: #0e9d8a; }
.bubble-bot ul { margin: 8px 0 4px 18px; }
.bubble-bot li { margin-bottom: 4px; }

.bubble-user {
    background: linear-gradient(135deg, #0f1f3d, #1a3a5c);
    border: 1px solid rgba(201,168,76,0.2);
    color: rgba(255,255,255,0.92);
    border-radius: 16px;
    border-top-right-radius: 4px;
    padding: 12px 16px;
    font-size: 0.88rem;
    line-height: 1.55;
    max-width: 75%;
}

/* ── Analysis / advice card ── */
.advice-card {
    background: rgba(255,255,255,0.97);
    border-radius: 18px;
    padding: 28px 32px;
    margin-top: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    color: #1a1a2e;
    font-size: 0.91rem;
    line-height: 1.7;
}
.advice-card h2 {
    font-family: 'Playfair Display', serif;
    color: #0f1f3d;
    font-size: 1.35rem;
    margin-bottom: 6px;
}
.advice-card h3 {
    color: #0e9d8a;
    font-size: 1rem;
    font-weight: 600;
    margin: 18px 0 6px;
}
.advice-card .score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0e9d8a, #13b89f);
    color: white;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
}
.advice-card .workshop-cta {
    background: linear-gradient(135deg, #0f1f3d, #1a3a5c);
    border: 1px solid rgba(201,168,76,0.35);
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 20px;
    color: rgba(255,255,255,0.9);
    font-size: 0.88rem;
}
.advice-card .workshop-cta strong { color: #e0bc6e; }

/* ── Streamlit widget overrides ── */
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    color: rgba(255,255,255,0.88) !important;
    font-size: 0.88rem !important;
    margin-bottom: 6px !important;
    transition: all 0.2s !important;
    display: block !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #0e9d8a !important;
    background: rgba(14,157,138,0.12) !important;
}

div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}

.stTextInput > div > div > input, .stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.35) !important; }

div[data-testid="stSelectSlider"] { color: white !important; }
.stSlider > div { color: white; }
.stSlider label { color: rgba(255,255,255,0.75) !important; font-size: 0.83rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #0e9d8a, #13b89f) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 28px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0b8a79, #0e9d8a) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(14,157,138,0.4) !important;
}

.section-label {
    color: rgba(255,255,255,0.6);
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}

div.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────

TOTAL_QUESTIONS = 10

# The system prompt that grounds Claude in the project context
ANALYSIS_SYSTEM_PROMPT = """
You are an expert AI education strategist working on the "AI Strategy Workshops for School Heads" initiative in India (2026).

You have deep knowledge of:

1. THE CCSCR FRAMEWORK — The workshop is built on 6 dimensions that every school principal must address:
   C — Curriculum & Pedagogy: How AI transforms teaching-learning, content creation, adaptive assessments, and classroom dynamics
   C — Capacity Building: Training teachers, managing AI-empowered classrooms, professional development pathways
   S — Safety & Compliance: DPDP Act 2023 compliance (penalties up to ₹200 crore), cyber safety, emotional safety, data governance, parental consent protocols
   C — Community Engagement: Educating parents on AI risks/benefits, parent communication frameworks, building stakeholder trust
   R — ROI & Strategy: Measuring impact, AI integration matrix, decision frameworks, cost-benefit analysis, efficiency gains

2. KEY CONTEXT:
   - India's NEP 2020 mandates AI from Grade 6; CBSE AI curriculum active in 4,538+ schools
   - Union Budget 2025-26 allocated ₹500 crore for AI Centre of Excellence in Education
   - 62% of Indian educators already use generative AI (Teamlease 2024-25)
   - <20% of Indian school leaders use data for curriculum decisions (Global School Leaders research)
   - DPDP Act 2023 & Rules 2025: strict children's data protection; 72-hour breach reporting
   - Research (Kim, Univ of Idaho, 2025): leaders are more optimistic than teachers about AI, but often overestimate teacher readiness

3. THE WORKSHOP OFFERING:
   - One full day, 5-star hotel venue, 80-100 principals per city, 10 cities across India
   - Unique differentiator: round tables of 6-7 principals each with a dedicated student engineer for hands-on AI tool practice
   - Tools covered (free/freemium): ChatGPT, Google Gemini, Microsoft Copilot, Canva AI, Grammarly, Perplexity AI
   - 7 sessions: AI Foundations → Strategic Framework → Hands-on Tools → Policy/Compliance → ROI Measurement → Parent Engagement → Action Planning
   - Fee: ₹5,000 per principal
   - Post-workshop: Sustainable model, ongoing community, virtual follow-up sessions

4. SCORING RUBRIC for principal readiness (used internally):
   - Personal AI Readiness Score: 1-5 scale across 5 leadership dimensions
   - Institutional Readiness: Based on planning stage, stakeholder openness, barriers
   - Urgency Flags: DPDP non-awareness, no AI policy, teacher resistance, parent concerns
   - CCSCR Gap Map: Which of the 5 dimensions are most underdeveloped

Your role: Analyse the principal's 10 assessment responses, identify their specific gaps against the CCSCR framework, and provide warm, expert, consulting-style advice. Then explain precisely how the workshop addresses those gaps. Be specific, not generic. Reference their actual answers.

TONE: Warm but authoritative. Like a trusted advisor who has worked with hundreds of school leaders. Not salesy. Encouraging but honest about gaps.

OUTPUT FORMAT — respond in valid markdown only, using this exact structure:

## 🎯 Your AI Leadership Readiness Profile

[2-3 sentences personalised summary based on their answers]

**Overall Readiness Level:** [Emerging / Developing / Advancing / Leading] — [1 sentence explaining why]

---

## 📊 Your CCSCR Gap Analysis

For each relevant dimension, rate as 🔴 Needs Attention / 🟡 In Progress / 🟢 Strong, with 2-3 lines of specific, personalised insight drawn from their answers.

**C — Curriculum & Pedagogy:** [rating + insight]
**C — Capacity Building:** [rating + insight]  
**S — Safety & Compliance:** [rating + insight]
**C — Community (Parent) Engagement:** [rating + insight]
**R — ROI & Strategy:** [rating + insight]

---

## 🛠️ Your Priority Action Areas

List 3-4 specific, actionable next steps tailored to this principal's situation. Each should be concrete (not "learn more about AI") with a clear why.

---

## 🏫 How the Workshop Directly Addresses Your Gaps

Map their specific gaps to specific workshop sessions. Be precise — e.g. "Given your concern about DPDP compliance, Session 4 (Policy & Compliance) will walk you through a 5-point tool evaluation checklist and give you ready-to-use policy templates."

Mention the student engineer round-table format and how it benefits someone at their readiness level.

---

## ✅ Your 90-Day Quick Wins

3 specific things they can do immediately (before or after the workshop) based on their current stage.
"""


# ── Session state init ─────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "phase": "intro",          # intro → questions → analysing → advice
        "q_index": 0,
        "answers": {},
        "chat_history": [],        # list of {role, content}
        "analysis_result": "",
        "name": "",
        "school": "",
        "city": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Question definitions ───────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "q1_personal_experience",
        "text": "How would you describe your **personal experience** with AI tools so far?",
        "type": "radio",
        "options": [
            "I've never used any AI tool",
            "I've tried a few tools casually (e.g. ChatGPT, Google Gemini)",
            "I use AI tools occasionally for personal tasks like drafting emails or research",
            "I use AI tools regularly and feel fairly comfortable with them",
            "I actively use AI tools for school leadership tasks and have explored several platforms",
        ],
        "key": "personal_experience",
    },
    {
        "id": "q2_school_ai_stage",
        "text": "Where is your **school currently** on its AI integration journey?",
        "type": "radio",
        "options": [
            "AI is on our radar but there's no concrete plan yet",
            "We're in early planning — discussing possibilities with the team",
            "We've piloted one or two AI tools (e.g. for attendance, content creation)",
            "We have a partial AI strategy and have rolled out a few initiatives",
            "We have a formal AI policy and multiple AI initiatives running across the school",
        ],
        "key": "school_ai_stage",
    },
    {
        "id": "q3_stakeholder_readiness",
        "text": "How open are the **key stakeholders** in your school to AI adoption?",
        "type": "radio",
        "options": [
            "Board is supportive but teachers and parents are largely unaware or resistant",
            "Teachers show interest but board hasn't prioritised AI and parents are concerned",
            "Mix — some stakeholders enthusiastic, others worried about safety or job replacement",
            "Most stakeholders are generally positive but need structured guidance",
            "Broad alignment — board, teachers, parents and students are all engaged",
        ],
        "key": "stakeholder_readiness",
    },
    {
        "id": "q4_biggest_concern",
        "text": "What is your **single biggest concern** about AI in your school right now?",
        "type": "radio",
        "options": [
            "Student data privacy and DPDP Act compliance",
            "Teachers not being ready — resistance, lack of skills, or fear of AI",
            "Students over-relying on AI and losing critical thinking / academic integrity",
            "Not knowing how to measure impact or justify the cost (ROI)",
            "Unsupervised AI use at home — mental health, cyber safety, exposure to harmful content",
        ],
        "key": "biggest_concern",
    },
    {
        "id": "q5_dpdp_awareness",
        "text": "Are you aware of the **DPDP Act 2023** (Digital Personal Data Protection) and what it means for AI tools your school uses?",
        "type": "radio",
        "options": [
            "Not aware of this at all",
            "I've heard of it but haven't looked into its implications for our school",
            "Somewhat aware — I know it exists but our compliance status is unclear",
            "Aware and we've started reviewing our tools and data practices",
            "Fully aware — we have policies and consent mechanisms in place",
        ],
        "key": "dpdp_awareness",
    },
    {
        "id": "q6_teacher_readiness",
        "text": "How would you rate your **teachers' current readiness** to use AI in their classrooms?",
        "type": "radio",
        "options": [
            "Most teachers are unaware or strongly resistant",
            "A few early adopters, but the majority haven't engaged with AI yet",
            "About half the staff are exploring AI tools on their own initiative",
            "Most teachers are open and have had some basic training",
            "Teachers are well-supported with training, tools, and clear guidelines",
        ],
        "key": "teacher_readiness",
    },
    {
        "id": "q7_ai_policy",
        "text": "Does your school have any **AI policy or guidelines** — for staff, students, or parents?",
        "type": "radio",
        "options": [
            "No policy at all — it's a free-for-all right now",
            "Some informal norms but nothing written down",
            "Basic acceptable-use guidelines for students only",
            "A draft policy is in progress but not yet finalised",
            "A formal AI policy exists covering staff, students, and data governance",
        ],
        "key": "ai_policy",
    },
    {
        "id": "q8_personal_leadership_areas",
        "text": "Which areas do you feel you **personally need the most support** in as an AI leader? (Choose up to 3)",
        "type": "multiselect",
        "options": [
            "Understanding AI deeply enough to make strategic decisions",
            "Creating an AI strategy and priority roadmap for my school",
            "Selecting the right tools — evaluating cost, safety, and fit",
            "Building and measuring ROI on AI investments",
            "Managing DPDP compliance and data governance",
            "Training and bringing teachers on board",
            "Using AI to improve my own personal efficiency (meetings, reports, emails)",
            "Communicating and educating parents about AI",
            "Handling AI-empowered student behaviour in classrooms",
        ],
        "key": "personal_leadership_needs",
    },
    {
        "id": "q9_parent_engagement",
        "text": "How is your school currently **engaging parents** on the topic of AI?",
        "type": "radio",
        "options": [
            "Parents haven't been spoken to about AI at all",
            "We've mentioned AI informally but there's no structured communication",
            "We've had one or two meetings or circulars about AI",
            "We have a parent communication plan and address AI concerns proactively",
            "Parents are actively involved — we run AI literacy sessions for them",
        ],
        "key": "parent_engagement",
    },
    {
        "id": "q10_open_challenge",
        "text": "In your own words — what is the **one thing** you wish you had clarity on about AI in your school, that you haven't been able to figure out yet?",
        "type": "textarea",
        "placeholder": "E.g. 'How do I know which AI tools are actually safe for students?' or 'How do I get my board to take AI seriously?'",
        "key": "open_challenge",
    },
]


# ── Helpers ────────────────────────────────────────────────────────────────────
def add_bot_message(content: str):
    st.session_state.chat_history.append({"role": "bot", "content": content})

def add_user_message(content: str):
    st.session_state.chat_history.append({"role": "user", "content": content})

def render_chat_history():
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            st.markdown(f"""
            <div class="bubble-bot-wrap">
                <div class="bot-avatar">🤖</div>
                <div class="bubble-bot">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-user-wrap">
                <div class="bubble-user">{msg["content"]}</div>
                <div class="user-avatar">👤</div>
            </div>""", unsafe_allow_html=True)

def score_responses() -> dict:
    """Compute a simple readiness score across CCSCR dimensions."""
    a = st.session_state.answers

    # Map answers to 0-4 index scores
    def idx(key):
        opts = next((q["options"] for q in QUESTIONS if q["key"] == key), [])
        val = a.get(key, "")
        if isinstance(val, str) and val in opts:
            return opts.index(val)
        return 1

    scores = {
        "personal": idx("personal_experience"),
        "school_stage": idx("school_ai_stage"),
        "stakeholders": idx("stakeholder_readiness"),
        "dpdp": idx("dpdp_awareness"),
        "teachers": idx("teacher_readiness"),
        "policy": idx("ai_policy"),
        "parents": idx("parent_engagement"),
    }

    # Overall 0-100
    total = sum(scores.values())
    max_possible = 4 * len(scores)
    pct = round((total / max_possible) * 100)

    if pct <= 25:
        level = "Emerging"
    elif pct <= 50:
        level = "Developing"
    elif pct <= 75:
        level = "Advancing"
    else:
        level = "Leading"

    return {"scores": scores, "pct": pct, "level": level}

def build_analysis_prompt() -> str:
    """Build the user prompt for Claude analysis."""
    a = st.session_state.answers
    name = st.session_state.name
    school = st.session_state.school
    city = st.session_state.city

    lines = [
        f"PRINCIPAL: {name}",
        f"SCHOOL: {school}",
        f"CITY: {city}",
        "",
        "ASSESSMENT RESPONSES:",
    ]
    for q in QUESTIONS:
        val = a.get(q["key"], "Not answered")
        if isinstance(val, list):
            val = ", ".join(val) if val else "None selected"
        lines.append(f"\n{q['text'].replace('**','').replace('*','')}")
        lines.append(f"→ {val}")

    score_data = score_responses()
    lines.append(f"\n[INTERNAL SCORE: {score_data['pct']}% — {score_data['level']} level]")

    return "\n".join(lines)


def call_claude_streaming(prompt: str):
    """Stream analysis from OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        yield generate_fallback_analysis()
        return

    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1800,
            stream=True,
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        yield f"\n\n*[Note: Could not connect. Error: {str(e)[:80]}]*\n\n"
        yield generate_fallback_analysis()


def generate_fallback_analysis() -> str:
    """Fallback if no API key — rule-based analysis."""
    a = st.session_state.answers
    scores = score_responses()
    level = scores["level"]
    pct = scores["pct"]

    dpdp_low = scores["scores"].get("dpdp", 4) <= 1
    policy_low = scores["scores"].get("policy", 4) <= 1
    teacher_low = scores["scores"].get("teachers", 4) <= 1
    parent_low = scores["scores"].get("parents", 4) <= 1

    concern = a.get("biggest_concern", "")
    needs = a.get("personal_leadership_needs", [])
    open_q = a.get("open_challenge", "")

    text = f"""
## 🎯 Your AI Leadership Readiness Profile

Based on your responses, you are at the **{level}** stage of your AI leadership journey — scoring {pct}% on our composite readiness index. This is honest, actionable, and a great starting point. Many of India's best school leaders are exactly where you are right now.

**Overall Readiness Level: {level}** — Your school has the intent and some early momentum, but structured strategy, policy, and capacity building are the next critical steps.

---

## 📊 Your CCSCR Gap Analysis

**C — Curriculum & Pedagogy:** {"🔴 Needs Attention" if scores['scores']['school_stage'] <= 1 else "🟡 In Progress" if scores['scores']['school_stage'] <= 3 else "🟢 Strong"} — {"Your school hasn't yet begun piloting AI in teaching-learning processes. This is the most impactful area to unlock first." if scores['scores']['school_stage'] <= 1 else "You've started exploring AI in pedagogy but need a structured framework to scale classroom-level adoption safely and effectively."}

**C — Capacity Building:** {"🔴 Needs Attention" if teacher_low else "🟡 In Progress" if scores['scores']['teachers'] <= 2 else "🟢 Strong"} — {"Most teachers are unaware or resistant — the biggest barrier to any AI initiative is an unprepared teaching staff. This requires a change management approach, not just training." if teacher_low else "Teachers are beginning to engage, but without clear institutional guidelines and scaffolded professional development, progress will remain patchy."}

**S — Safety & Compliance:** {"🔴 Needs Attention — URGENT" if dpdp_low else "🟡 In Progress"} — {"You are currently unaware of DPDP Act 2023 implications for your school. This is an urgent risk: penalties can reach ₹200 crore and schools using AI tools that process student data without compliant consent mechanisms are already exposed." if dpdp_low else "You're aware of DPDP but compliance is still work-in-progress. You need a tool evaluation checklist, data governance policy, and parent consent templates — all of which the workshop provides."}

**C — Community (Parent) Engagement:** {"🔴 Needs Attention" if parent_low else "🟡 In Progress" if scores['scores']['parents'] <= 2 else "🟢 Strong"} — {"Parents in your school haven't been brought into the AI conversation. With 32+ million children in India using unsupervised AI at home, schools that don't lead this conversation will face growing anxiety, distrust, and potential backlash." if parent_low else "You've started communicating with parents but need structured frameworks — parent education programs, AI-at-home guidance, and transparent policy communication."}

**R — ROI & Strategy:** {"🔴 Needs Attention" if not a.get("ai_policy") or policy_low else "🟡 In Progress" if scores['scores']['policy'] <= 2 else "🟢 Strong"} — {"Without a formal AI policy or strategy framework, your school is making reactive, piecemeal decisions. Research shows <20% of Indian school leaders currently use data for strategic decisions — this workshop specifically addresses that gap." if policy_low else "You have early strategic thinking in place. The next step is building a measurable AI integration roadmap with clear ROI metrics and a governance framework."}

---

## 🛠️ Your Priority Action Areas

1. **Establish DPDP compliance immediately** — Audit every AI tool currently used in your school against a 5-point privacy checklist (data storage, consent, deletion rights, breach protocols, cross-border transfers). This is non-negotiable.

2. **Develop a school AI policy (even a draft)** — Before scaling any AI initiative, you need an acceptable-use policy for students, staff guidelines, and a data governance statement. The workshop provides customisable templates.

3. **Create a teacher readiness roadmap** — Run a quick survey of your staff's AI confidence, identify your 3-5 "AI champions," and design a phased capacity-building plan. Early adopters become your internal trainers.

4. **Start one measurable AI pilot** — Pick a single, low-risk use case (e.g. using Gemini for drafting parent communications or Canva AI for newsletters) and measure time saved over 30 days. This builds your evidence base for scaling.

---

## 🏫 How the Workshop Directly Addresses Your Gaps

{"Given your **DPDP unawareness**, Session 4 (Policy, Privacy & Compliance) is particularly critical for you — you'll leave with a 5-point tool evaluation checklist and ready-to-customize policy templates." if dpdp_low else ""}

{"Since **teacher resistance** is a live challenge, you'll benefit greatly from Session 2's AI Integration Matrix — a practical framework to sequence AI adoption in a way that brings teachers along, not over them." if teacher_low else ""}

{"With **parent engagement** still nascent, Session 6 (Parent & Community Strategy) gives you a structured program template, communication frameworks, and scripts to handle the most common parent concerns." if parent_low else ""}

The **student engineer round-table format** is especially valuable at your readiness level — you'll get hands-on practice with ChatGPT, Gemini, Copilot, and Canva AI in a low-pressure environment, guided by a student tech mentor, so you leave the day genuinely comfortable using these tools.

Session 7 (Action Planning) will help you build your **personal 90-day AI roadmap** — not a generic one, but one grounded in your school's specific context, stakeholder dynamics, and resource constraints.

---

## ✅ Your 90-Day Quick Wins

1. **Week 1-2:** Download and read the DPDP Act 2023 one-pager for schools. Review the top 3 AI tools your school currently uses against basic privacy criteria.

2. **Month 1:** Call a staff meeting to gauge teacher AI awareness and identify 3 willing "AI champions" who will pilot new tools alongside you.

3. **Month 2-3:** Hold one parent town hall on AI — share what AI your school is using, what safeguards are in place, and what parents can do at home. Use the communication framework from the workshop.

---

*Your open question — "{open_q[:120] if open_q else 'How to get started'}" — will be directly addressed in the workshop through the Strategic Decision Framework and peer discussions with principals facing the same challenge.*
"""
    return text


# ── Page rendering ─────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <div class="gold-tag">AI Strategy Workshops · India 2026</div>
    <h1>🏫 AI Readiness Assessment for School Leaders</h1>
    <p>A 5-minute diagnostic followed by personalised consulting advice — tailored to your school's context</p>
</div>
""", unsafe_allow_html=True)

# Progress
if st.session_state.phase == "questions":
    q_num = st.session_state.q_index + 1
    pct = int((q_num / TOTAL_QUESTIONS) * 100)
    st.markdown(f"""
    <div class="progress-wrap">
        <span class="progress-text">Question {q_num} of {TOTAL_QUESTIONS}</span>
        <div style="flex:1;height:4px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden;">
            <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#0e9d8a,#c9a84c);border-radius:4px;transition:width 0.4s;"></div>
        </div>
        <span class="progress-text">{pct}%</span>
    </div>
    """, unsafe_allow_html=True)
elif st.session_state.phase in ("analysing", "advice"):
    st.markdown("""
    <div class="progress-wrap">
        <span class="progress-text">Assessment complete ✓</span>
        <div style="flex:1;height:4px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden;">
            <div style="height:100%;width:100%;background:linear-gradient(90deg,#0e9d8a,#c9a84c);border-radius:4px;"></div>
        </div>
        <span class="progress-text">Analysis ready</span>
    </div>
    """, unsafe_allow_html=True)

# ── PHASE: INTRO ───────────────────────────────────────────────────────────────
if st.session_state.phase == "intro":
    st.markdown("""
    <div class="bubble-bot-wrap" style="margin-bottom:12px;">
        <div class="bot-avatar">🤖</div>
        <div class="bubble-bot">
            <strong>Welcome!</strong> I'm your AI strategy advisor for school leaders.<br><br>
            This short assessment — just <strong>10 focused questions</strong> — will gauge where you and your school currently stand on AI adoption.<br><br>
            After your answers, I'll give you a <strong>personalised CCSCR gap analysis</strong> and concrete advice on what to do next — and how our upcoming workshop addresses your specific situation.<br><br>
            Let's start with a quick introduction.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="e.g. Priya Sharma", key="intro_name")
        with col2:
            school = st.text_input("School Name", placeholder="e.g. Sunrise International School", key="intro_school")

        col3, col4 = st.columns(2)
        with col3:
            city = st.text_input("City", placeholder="e.g. Pune", key="intro_city")
        with col4:
            board = st.selectbox("School Board", ["CBSE", "ICSE", "IB", "Cambridge", "State Board", "Other"], key="intro_board")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Begin Assessment →"):
        if not name or not school:
            st.warning("Please enter your name and school to continue.")
        else:
            st.session_state.name = name
            st.session_state.school = school
            st.session_state.city = city
            st.session_state.answers["board"] = board
            add_bot_message(f"<strong>Welcome, {name}!</strong> Let's assess your school's AI readiness across 5 dimensions — this will take about 5 minutes.")
            add_user_message(f"I'm {name}, Principal at {school}, {city} ({board})")
            st.session_state.phase = "questions"
            st.rerun()


# ── PHASE: QUESTIONS ───────────────────────────────────────────────────────────
elif st.session_state.phase == "questions":
    render_chat_history()

    q_index = st.session_state.q_index
    if q_index >= len(QUESTIONS):
        st.session_state.phase = "analysing"
        st.rerun()

    q = QUESTIONS[q_index]

    # Show current question as bot bubble
    st.markdown(f"""
    <div class="bubble-bot-wrap" style="margin-top:8px;">
        <div class="bot-avatar">🤖</div>
        <div class="bubble-bot"><strong>Q{q_index+1} of {TOTAL_QUESTIONS}</strong><br><br>{q["text"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Render answer widget
    answer = None
    widget_key = f"widget_{q['id']}"

    if q["type"] == "radio":
        st.markdown('<div class="section-label">Select one answer</div>', unsafe_allow_html=True)
        answer = st.radio(
            label="",
            options=q["options"],
            index=None,
            key=widget_key,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if answer and st.button("Next →", key=f"next_{q_index}"):
            st.session_state.answers[q["key"]] = answer
            add_user_message(answer)
            # Add brief transition bot message for select questions
            transitions = {
                0: "Got it. Now let's look at your school as an institution.",
                1: "Understood. Let's dig into your stakeholders.",
                2: "That's helpful context. Let's talk about specific concerns.",
                3: "Important to understand. Let's look at compliance awareness.",
                4: "Thanks. Teacher readiness is often the make-or-break factor.",
                5: "Noted. Policy is the backbone of any AI strategy.",
                6: "Good to know. Now let me understand where you need support most.",
                7: "Understood. Nearly there — let's look at parent engagement.",
                8: "Almost done. One final open question for you.",
            }
            if q_index < len(QUESTIONS) - 1:
                add_bot_message(transitions.get(q_index, "Thank you. Next question:"))
            st.session_state.q_index += 1
            st.rerun()

    elif q["type"] == "multiselect":
        st.markdown('<div class="section-label">Select up to 3 that apply most</div>', unsafe_allow_html=True)
        answer = st.multiselect(
            label="",
            options=q["options"],
            max_selections=3,
            key=widget_key,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Next →", key=f"next_{q_index}"):
            val = answer if answer else ["Not specified"]
            st.session_state.answers[q["key"]] = val
            add_user_message("Support needed in: " + ", ".join(val))
            add_bot_message("Almost there — one final open question for me to understand you better.")
            st.session_state.q_index += 1
            st.rerun()

    elif q["type"] == "textarea":
        st.markdown('<div class="section-label">Your answer (in your own words)</div>', unsafe_allow_html=True)
        answer = st.text_area(
            label="",
            placeholder=q.get("placeholder", "Type your answer here…"),
            height=110,
            key=widget_key,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns([3, 1])
        with col_b:
            skip = st.button("Skip →", key=f"skip_{q_index}")
        with col_a:
            submit = st.button("Submit & Get My Analysis →", key=f"next_{q_index}")

        if submit or skip:
            val = answer.strip() if (answer and answer.strip()) else "Not provided"
            st.session_state.answers[q["key"]] = val
            add_user_message(val[:200] if len(val) > 200 else val)
            add_bot_message("Thank you — analysing your responses now. This will take a moment…")
            st.session_state.q_index += 1
            st.session_state.phase = "analysing"
            st.rerun()


# ── PHASE: ANALYSING ───────────────────────────────────────────────────────────
elif st.session_state.phase == "analysing":
    render_chat_history()

    st.markdown("""
    <div class="bubble-bot-wrap" style="margin-top:12px;">
        <div class="bot-avatar">🤖</div>
        <div class="bubble-bot">
            <strong>Analysing your responses…</strong><br><br>
            I'm mapping your answers against the <strong>CCSCR framework</strong> (Curriculum · Capacity · Safety · Community · ROI) and preparing your personalised readiness profile.<br><br>
            <em>This usually takes 15–20 seconds.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        prompt = build_analysis_prompt()
        full_response = ""

        # Stream and collect
        placeholder = st.empty()
        for chunk in call_claude_streaming(prompt):
            full_response += chunk
            placeholder.markdown(f"""
            <div class="advice-card">
            {full_response}
            </div>
            """, unsafe_allow_html=True)

        st.session_state.analysis_result = full_response
        st.session_state.phase = "advice"
        time.sleep(0.5)
        st.rerun()


# ── PHASE: ADVICE ──────────────────────────────────────────────────────────────
elif st.session_state.phase == "advice":
    render_chat_history()

    st.markdown("""
    <div class="bubble-bot-wrap" style="margin-top:12px;">
        <div class="bot-avatar">🤖</div>
        <div class="bubble-bot">
            Here is your <strong>personalised AI leadership readiness analysis</strong> — mapped to the CCSCR framework and your school's specific context.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="advice-card">
    {st.session_state.analysis_result}
    </div>
    """, unsafe_allow_html=True)

    # Workshop CTA
    st.markdown("""
    <br>
    <div style="background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.35);border-radius:16px;padding:24px 28px;margin-top:8px;">
        <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#e0bc6e;margin-bottom:10px;">
            🏫 Ready to bridge these gaps?
        </div>
        <div style="color:rgba(255,255,255,0.82);font-size:0.88rem;line-height:1.7;">
            The <strong style="color:white;">AI Strategy Workshop for School Heads</strong> is a full-day, hands-on workshop coming to 10 cities across India in late 2026.<br><br>
            <strong style="color:#13b89f;">₹5,000 per principal</strong> &nbsp;·&nbsp; Five-star venue &nbsp;·&nbsp; Student engineer mentors at every table &nbsp;·&nbsp; Take-home AI policy templates & strategy roadmap<br><br>
            <em style="color:rgba(255,255,255,0.5);font-size:0.82rem;">Cities: Mumbai · Delhi-NCR · Bangalore · Hyderabad · Kolkata · Pune · Ahmedabad · Chennai · Chandigarh · Jaipur</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Start Over / New Assessment"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col2:
        # Download analysis as text
        if st.session_state.analysis_result:
            name = st.session_state.name
            download_text = f"AI Readiness Assessment Report\n{name} — {st.session_state.school}, {st.session_state.city}\n\n"
            download_text += st.session_state.analysis_result.replace("##", "\n\n##").replace("**", "")
            st.download_button(
                label="⬇️ Download My Analysis",
                data=download_text,
                file_name=f"AI_Readiness_{name.replace(' ','_')}.txt",
                mime="text/plain",
            )