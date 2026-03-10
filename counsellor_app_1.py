"""
AI Study Counsellor — Hybrid Voice + Text
School AI Guidance Programme · India 2026

SETUP (Mac · Python 3.11 · VS Code · venv):
  1.  source .venv/bin/activate
  2.  pip install streamlit openai python-dotenv fpdf2
  3.  .env file:  OPENAI_API_KEY=sk-your-key-here
  4.  streamlit run counsellor_app.py
  5.  git add . && git commit -m "hybrid voice+text" && git push

VOICE: OpenAI Whisper (STT) + TTS model tts-1, voice=nova (warm female)
TEXT:  Standard chat
BOTH:  gpt-4o-mini for counsellor AI brain
"""

from dotenv import load_dotenv
import os
load_dotenv()                          # reads .env into os.environ
api_key = os.getenv("OPENAI_API_KEY")  # used everywhere below

import streamlit as st
import csv
import json
import re
import base64
import tempfile
from datetime import datetime

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Study Counsellor",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
CSV_FILE = "counsellor_log.csv"

SEMINARS = {
    "S1": {"title": "Seminar 1: Screen Time & Holistic Growth",
           "desc":  "Understanding the harms of excessive screen time and building healthy digital habits.",
           "color": "#e8450a", "icon": "📱"},
    "S2": {"title": "Seminar 2: AI as the Right Study Companion",
           "desc":  "How to use AI to build real understanding — not just copy answers.",
           "color": "#d97706", "icon": "🤝"},
    "S3": {"title": "Seminar 3: Ethics, Safety & Verification",
           "desc":  "Ethical AI use, data privacy, spotting misinformation, and verifying outputs.",
           "color": "#0d9488", "icon": "🛡️"},
    "S4": {"title": "Seminar 4: Using AI Well Across Subjects",
           "desc":  "Subject-specific strategies for Maths, Science, English, History and more.",
           "color": "#4338ca", "icon": "📚"},
}

# ── System prompts ────────────────────────────────────────────────────────────
# Voice prompt: shorter replies — this will be spoken aloud
SYSTEM_PROMPT_VOICE = """You are a warm, friendly AI study counsellor speaking WITH a student (aged 13–18) at an Indian school.

CRITICAL — you are speaking aloud via text-to-speech:
- Keep EVERY reply to 1–2 short sentences only. No lists, no bullet points.
- Sound natural and conversational, like a real person talking.
- No asterisks, no markdown, no emojis in text — they sound bad when spoken.

Assess these FOUR areas naturally across 8–12 back-and-forth exchanges:
1. SCREEN TIME: Hours/day on AI tools for studies? Total screen time?
   Concern if: 3+ hrs/day on AI, or 6+ hrs total screen time.
2. LEARNING QUALITY: Do they copy AI answers or use AI to understand concepts?
   Concern if: copying answers, AI doing homework for them.
3. SAFETY & ETHICS: Do they verify AI output? Know about privacy and plagiarism?
   Concern if: never verified AI, shares personal info, unaware of ethics.
4. SUBJECTS: Which subjects? Dependent or healthy use?
   Concern if: AI for every subject with no independent effort.

Start by warmly greeting them and asking their name and class.
After covering all 4 areas, give a short warm spoken closing (1–2 sentences), then output the JSON block.

FINAL ASSESSMENT — your spoken closing first, then immediately this JSON:
```json
{
  "student_name": "...",
  "student_class": "...",
  "screen_time_hours": <number or null>,
  "total_screen_hours": <number or null>,
  "screen_time_high": <true/false>,
  "passive_use": <true/false>,
  "safety_gap": <true/false>,
  "subject_use": <true/false>,
  "subjects_mentioned": ["..."],
  "key_observations": ["obs 1", "obs 2", "obs 3"],
  "counsellor_note": "Warm 2-sentence personalised note to student",
  "referrals": ["S1","S2","S3","S4"]
}
```
Only include seminar codes truly needed: S1=screen_time_high, S2=passive_use, S3=safety_gap, S4=subject_use."""

# Text prompt: richer replies — read on screen
SYSTEM_PROMPT_TEXT = """You are a warm, friendly, non-judgmental AI study counsellor at an Indian school talking to a student (aged 13–18) one-on-one.

Have a natural, flowing conversation — NOT a rigid questionnaire. Be curious and encouraging.

Assess FOUR areas naturally across 8–12 exchanges:
AREA 1 — SCREEN TIME: Hours/day on AI tools for studies? Total screen time?
  Concern: 3+ hrs/day on AI, or 6+ hrs total.
AREA 2 — LEARNING QUALITY: Copy AI answers, or use AI to genuinely understand?
  Concern: copying answers, AI doing homework.
AREA 3 — SAFETY & ETHICS: Verify AI output? Know about privacy and plagiarism?
  Concern: never verified AI, shares personal info, unaware of ethics.
AREA 4 — SUBJECTS: Which subjects? Dependent or healthy use?
  Concern: AI for all subjects with no independent effort.

Start by greeting them and asking their name and class.
After 8–12 exchanges covering all 4 areas, close warmly and add the JSON assessment.

FINAL ASSESSMENT:
```json
{
  "student_name": "...",
  "student_class": "...",
  "screen_time_hours": <number or null>,
  "total_screen_hours": <number or null>,
  "screen_time_high": <true/false>,
  "passive_use": <true/false>,
  "safety_gap": <true/false>,
  "subject_use": <true/false>,
  "subjects_mentioned": ["..."],
  "key_observations": ["obs 1", "obs 2", "obs 3"],
  "counsellor_note": "Warm personalised 2–3 sentence note",
  "referrals": ["S1","S2","S3","S4"]
}
```
Only include seminar codes truly needed: S1=screen_time_high, S2=passive_use, S3=safety_gap, S4=subject_use.
TONE: Never lecture. 2–4 sentences per reply. Use student's name once you know it."""

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family:'DM Sans',sans-serif !important; }
.stApp { background:#f7f4ef; color:#1a1a1a; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:1.5rem 1.5rem 4rem; max-width:720px; margin:0 auto; }

/* Header */
.app-header { text-align:center; padding:1.5rem 0 1.2rem;
  border-bottom:2px solid #e8e2d9; margin-bottom:1.8rem; }
.app-title { font-family:'DM Serif Display',serif !important;
  font-size:1.6rem; color:#1a1a1a; margin:0 0 4px; line-height:1.2; }
.app-subtitle { font-size:0.85rem; color:#999; }

/* Welcome card */
.welcome-card { background:white; border-radius:20px; padding:2rem 2.2rem;
  box-shadow:0 2px 20px rgba(0,0,0,.06); margin-bottom:1.4rem;
  border:1px solid #ede8e0; }
.welcome-title { font-family:'DM Serif Display',serif;
  font-size:1.4rem; color:#1a1a1a; margin-bottom:10px; }
.welcome-body { font-size:.93rem; color:#555; line-height:1.7; margin-bottom:16px; }
.privacy-pill { display:inline-flex; align-items:center; gap:5px;
  background:#f0fdf4; border:1px solid #86efac; border-radius:20px;
  padding:4px 12px; font-size:.78rem; color:#166534;
  font-weight:600; margin-right:6px; margin-bottom:5px; }

/* Mode picker cards */
.mode-pick-wrap { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin:16px 0; }
.mode-pick-card { background:white; border:2px solid #e8e2d9; border-radius:18px;
  padding:26px 18px; text-align:center; }
.mode-pick-card.active { border-color:#1a1a1a; background:#1a1a1a; }
.mode-pick-icon { font-size:2.6rem; margin-bottom:10px; }
.mode-pick-label { font-size:1rem; font-weight:700; color:#1a1a1a; }
.mode-pick-card.active .mode-pick-label { color:white; }
.mode-pick-desc { font-size:.8rem; color:#888; margin-top:5px; line-height:1.4; }
.mode-pick-card.active .mode-pick-desc { color:#aaa; }

/* Info box */
.info-box { border-radius:12px; padding:13px 17px; font-size:.87rem;
  line-height:1.6; margin-bottom:14px; }
.info-box-voice { background:#f0fdf9; border:1px solid #99f6e4; color:#0d9488; }
.info-box-text  { background:#f7f4ef; border:1px solid #e8e2d9; color:#888; }

/* Mic button */
.mic-wrap { text-align:center; padding:20px 0 10px; }
.mic-btn-idle { width:90px; height:90px; border-radius:50%;
  background:#1a1a1a; border:none; cursor:pointer; font-size:2.2rem;
  color:white; box-shadow:0 4px 24px rgba(0,0,0,.18);
  transition:all .2s; display:inline-flex; align-items:center; justify-content:center; }
.mic-btn-rec  { background:#e8450a;
  box-shadow:0 0 0 8px rgba(232,69,10,.2), 0 4px 24px rgba(232,69,10,.35); }
.mic-status { font-size:.82rem; font-weight:700; color:#888;
  text-transform:uppercase; letter-spacing:1px; margin-top:10px; }

/* Chat bubbles */
.chat-wrap { display:flex; flex-direction:column; gap:14px; margin-bottom:18px; }
.msg-ai { display:flex; gap:10px; align-items:flex-start; }
.msg-ai-av { width:34px; height:34px; background:#1a1a1a; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:.95rem; flex-shrink:0; margin-top:2px; }
.msg-ai-bub { background:white; border:1px solid #ede8e0;
  border-radius:4px 18px 18px 18px; padding:13px 17px;
  font-size:.95rem; line-height:1.65;
  box-shadow:0 1px 8px rgba(0,0,0,.05); max-width:85%; }
.msg-stu { display:flex; justify-content:flex-end; }
.msg-stu-bub { background:#1a1a1a; color:white;
  border-radius:18px 4px 18px 18px; padding:13px 17px;
  font-size:.95rem; line-height:1.65; max-width:82%; }
.msg-voice-tag { font-size:.71rem; color:#0d9488; font-weight:700;
  text-align:right; margin-top:3px; }

/* Progress dots */
.prog-dots { display:flex; gap:6px; justify-content:center; margin-bottom:12px; }
.dot { width:8px; height:8px; border-radius:50%; background:#ddd; }
.dot-done { background:#0d9488; }
.dot-active { background:#1a1a1a; }

/* Transcript preview */
.transcript-preview { background:#f0fdf9; border:1px solid #99f6e4;
  border-radius:12px; padding:12px 17px; font-size:.95rem;
  color:#1a1a1a; margin-bottom:12px; line-height:1.6; }
.transcript-label { font-size:.72rem; font-weight:700; color:#0d9488;
  text-transform:uppercase; letter-spacing:.8px; margin-bottom:4px; }

/* Inputs */
.stTextInput>div>div>input { background:white !important;
  border:2px solid #e8e2d9 !important; border-radius:14px !important;
  padding:13px 17px !important; font-size:.95rem !important;
  font-family:'DM Sans',sans-serif !important; color:#1a1a1a !important; }
.stTextInput>div>div>input:focus { border-color:#1a1a1a !important; box-shadow:none !important; }
.stTextInput label { display:none !important; }

/* Buttons */
.stButton>button { background:#1a1a1a !important; color:white !important;
  border:none !important; border-radius:12px !important;
  font-family:'DM Sans',sans-serif !important; font-weight:700 !important;
  font-size:.95rem !important; padding:13px 28px !important;
  width:100% !important; transition:background .2s !important; }
.stButton>button:hover { background:#333 !important; }
.btn-secondary>button { background:white !important; color:#1a1a1a !important;
  border:2px solid #e8e2d9 !important; }
.btn-secondary>button:hover { border-color:#1a1a1a !important; }

/* Referral card */
.ref-card { background:white; border-radius:20px; padding:2rem;
  box-shadow:0 4px 30px rgba(0,0,0,.08); border:1px solid #ede8e0; margin-top:18px; }
.ref-header { font-family:'DM Serif Display',serif; font-size:1.35rem;
  color:#1a1a1a; margin-bottom:4px; }
.ref-name { font-size:.87rem; color:#888; margin-bottom:16px; }
.sem-badge { border-radius:14px; padding:14px 16px; margin-bottom:9px;
  display:flex; align-items:flex-start; gap:12px; }
.sem-icon { font-size:1.4rem; flex-shrink:0; margin-top:2px; }
.sem-title { font-weight:700; font-size:.94rem; margin-bottom:3px; }
.sem-desc { font-size:.82rem; color:#555; line-height:1.5; }
.obs-box { background:#f7f4ef; border-radius:12px; padding:13px 16px; margin:13px 0; }
.obs-label { font-size:.71rem; font-weight:700; text-transform:uppercase;
  letter-spacing:1px; color:#888; margin-bottom:7px; }
.obs-item { font-size:.86rem; color:#444; padding:4px 0;
  border-bottom:1px solid #ede8e0; line-height:1.5; }
.obs-item:last-child { border-bottom:none; }
.cnote { background:#fff9f0; border-left:3px solid #d97706;
  border-radius:0 12px 12px 0; padding:12px 16px;
  font-size:.89rem; color:#444; line-height:1.6;
  font-style:italic; margin-top:13px; }
.hr { border:none; border-top:1px solid #ede8e0; margin:16px 0; }

/* Selectbox */
.stSelectbox>div>div { background:white !important; border:2px solid #e8e2d9 !important;
  border-radius:12px !important; font-family:'DM Sans',sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "phase": "welcome",      # welcome | chat | result
        "mode": None,            # "voice" | "text"
        "messages": [],          # [{role, content, via_voice?}]
        "assessment": None,
        "student_class": "",
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "tts_b64": None,         # base64 mp3 waiting to autoplay
        "rec_key": 0,            # incremented to reset audio_input widget
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════════════════════
# OPENAI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def openai_client():
    if not api_key:
        return None
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def call_ai(messages: list) -> str:
    client = openai_client()
    if not client:
        return fallback_response(messages)
    try:
        prompt = SYSTEM_PROMPT_VOICE if st.session_state.mode == "voice" else SYSTEM_PROMPT_TEXT
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=500,
            temperature=0.75,
            messages=[{"role": "system", "content": prompt}] + messages,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Small technical issue — please try again. ({str(e)[:60]})"


def whisper_transcribe(audio_bytes: bytes) -> str:
    """Whisper STT: audio bytes → transcript string."""
    client = openai_client()
    if not client:
        return ""
    suffix = ".webm"
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en",
            )
        os.unlink(tmp_path)
        return result.text.strip()
    except Exception as e:
        st.error(f"Transcription error: {str(e)[:100]}")
        return ""


def tts_speak(text: str) -> bytes | None:
    """OpenAI TTS → mp3 bytes. Voice: nova (warm female)."""
    client = openai_client()
    if not client:
        return None
    clean = re.sub(r"```json[\s\S]*?```", "", text).strip()
    clean = re.sub(r"[*_`#]", "", clean)
    if not clean:
        return None
    try:
        resp = client.audio.speech.create(
            model="tts-1",
            voice="nova",        # warm & friendly female voice
            input=clean[:4000],
        )
        return resp.content
    except Exception as e:
        st.warning(f"Voice error: {str(e)[:80]}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK (demo mode — no API key)
# ══════════════════════════════════════════════════════════════════════════════
_FALLBACKS = [
    "Hi there! I'm your AI study counsellor. I'd love to chat about how you use AI for studying. What's your name and which class are you in?",
    "Great to meet you! Do you use AI tools like ChatGPT or Gemini for your studies? Roughly how many hours a day?",
    "Interesting! When you use AI to study, do you usually ask it to give you the answer directly, or ask it to explain step by step?",
    "That's helpful. Do you ever fact-check what AI tells you? Have you ever caught it giving wrong information?",
    "Good to know! Which subjects do you use AI for the most — Maths, Science, English, History?",
    "Almost done — do you know about not sharing personal info with AI, or what counts as plagiarism when using AI for schoolwork?",
    "Thanks so much for sharing all this! I have a great picture now. Let me prepare your personalised guidance.",
]

def fallback_response(messages):
    count = sum(1 for m in messages if m["role"] == "user")
    if count < len(_FALLBACKS):
        return _FALLBACKS[count]
    return _mock_assessment(messages)


def _mock_assessment(messages):
    text = " ".join(m["content"] for m in messages if m["role"] == "user").lower()
    hrs = int(m.group(1)) if (m := re.search(r"(\d+)\s*hour", text)) else 2
    passive   = any(w in text for w in ["answer", "solve", "do it", "write it"])
    no_verify = not any(w in text for w in ["check", "verify", "wrong", "fact"])
    subjects  = [s.title() for s in
                 ["maths","math","science","english","history","physics","chemistry","biology"]
                 if s in text]
    nm = re.search(r"(?:i(?:'m| am)|name(?:'s| is)|call me)\s+([A-Z][a-z]+)",
                   " ".join(m["content"] for m in messages if m["role"] == "user"))
    name = nm.group(1) if nm else "Student"
    refs = []
    if hrs >= 3:    refs.append("S1")
    if passive:     refs.append("S2")
    if no_verify:   refs.append("S3")
    if subjects:    refs.append("S4")
    if not refs:    refs = ["S2", "S3"]
    a = {
        "student_name": name,
        "student_class": st.session_state.student_class or "Not specified",
        "screen_time_hours": hrs, "total_screen_hours": hrs + 2,
        "screen_time_high": hrs >= 3, "passive_use": passive,
        "safety_gap": no_verify, "subject_use": bool(subjects),
        "subjects_mentioned": subjects or ["General"],
        "key_observations": [
            f"Uses AI ~{hrs} hr/day for studies",
            "Uses AI for direct answers" if passive else "Uses AI to build understanding",
            "Needs verification habits guidance" if no_verify else "Aware of AI limitations",
        ],
        "counsellor_note": f"Thanks for being so open, {name}! I've picked sessions that'll help you get the most from AI while keeping your learning strong.",
        "referrals": refs,
    }
    return (f"Thanks so much for chatting with me today, {name}! "
            "Here's your personalised guidance.\n\n"
            "```json\n" + json.dumps(a, indent=2) + "\n```")

# ══════════════════════════════════════════════════════════════════════════════
# SHARED HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def extract_assessment(text):
    m = re.search(r"```json\s*([\s\S]+?)\s*```", text)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    m2 = re.search(r'\{[\s\S]*"referrals"[\s\S]*\}', text)
    if m2:
        try: return json.loads(m2.group(0))
        except: pass
    return None


def clean_text(text):
    return re.sub(r"```json[\s\S]*?```", "", text).strip()


def autoplay_tts(b64: str):
    """Inject an autoplay <audio> tag into the page."""
    st.markdown(
        f'<audio autoplay style="width:100%;border-radius:10px;margin:6px 0 14px;">'
        f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
        unsafe_allow_html=True,
    )


def log_csv(assessment):
    row = {
        "session_id":       st.session_state.session_id,
        "timestamp":        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode":             st.session_state.mode or "text",
        "student_name":     assessment.get("student_name", ""),
        "student_class":    assessment.get("student_class", ""),
        "screen_time_hours":assessment.get("screen_time_hours", ""),
        "total_screen_hours":assessment.get("total_screen_hours", ""),
        "screen_time_high": assessment.get("screen_time_high", ""),
        "passive_use":      assessment.get("passive_use", ""),
        "safety_gap":       assessment.get("safety_gap", ""),
        "subject_use":      assessment.get("subject_use", ""),
        "subjects_mentioned":", ".join(assessment.get("subjects_mentioned", [])),
        "referrals":        ", ".join(assessment.get("referrals", [])),
        "key_observations": " | ".join(assessment.get("key_observations", [])),
        "counsellor_note":  assessment.get("counsellor_note", ""),
    }
    exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if not exists: w.writeheader()
        w.writerow(row)


def generate_pdf(assessment):
    if not PDF_AVAILABLE:
        return None
    try:
        pdf = FPDF(); pdf.add_page(); pdf.set_margins(20, 20, 20)
        pdf.set_fill_color(26,26,26); pdf.rect(0,0,210,28,'F')
        pdf.set_font("Helvetica","B",15); pdf.set_text_color(255,255,255)
        pdf.set_xy(20,9); pdf.cell(0,10,"AI Study Counsellor — Referral Card")
        pdf.set_font("Helvetica","",8); pdf.set_text_color(170,170,170)
        pdf.set_xy(20,20)
        tag = "(Voice Session)" if assessment.get("mode")=="voice" else "(Text Session)"
        pdf.cell(0,5,f"Generated: {datetime.now().strftime('%d %B %Y')}  ·  {tag}  ·  School AI Guidance Programme")
        pdf.set_xy(20,35); pdf.set_font("Helvetica","B",13); pdf.set_text_color(26,26,26)
        pdf.cell(0,7,f"{assessment.get('student_name','Student')}  ·  {assessment.get('student_class','')}",ln=True)
        subj = ", ".join(assessment.get("subjects_mentioned",[]))
        if subj:
            pdf.set_font("Helvetica","",9); pdf.set_text_color(120,120,120)
            pdf.cell(0,5,f"Subjects: {subj}",ln=True)
        pdf.ln(4)
        pdf.set_draw_color(220,215,205); pdf.line(20,pdf.get_y(),190,pdf.get_y()); pdf.ln(5)
        pdf.set_font("Helvetica","B",8); pdf.set_text_color(150,150,150); pdf.cell(0,5,"OBSERVATIONS",ln=True); pdf.ln(1)
        pdf.set_font("Helvetica","",9); pdf.set_text_color(60,60,60)
        for obs in assessment.get("key_observations",[]):
            pdf.set_x(20); pdf.cell(4,5,chr(149)); pdf.multi_cell(160,5,obs)
        pdf.ln(2)
        note = assessment.get("counsellor_note","")
        if note:
            pdf.set_fill_color(255,250,240); pdf.set_font("Helvetica","I",9); pdf.set_text_color(80,60,20)
            pdf.set_x(20); pdf.multi_cell(170,6,note,fill=True)
        pdf.ln(4); pdf.line(20,pdf.get_y(),190,pdf.get_y()); pdf.ln(5)
        pdf.set_font("Helvetica","B",8); pdf.set_text_color(150,150,150); pdf.cell(0,5,"RECOMMENDED SESSIONS",ln=True); pdf.ln(2)
        cmap = {"S1":(232,69,10),"S2":(217,119,6),"S3":(13,148,136),"S4":(67,56,202)}
        for code in assessment.get("referrals",[]):
            sem = SEMINARS.get(code,{}); c = cmap.get(code,(26,26,26))
            pdf.set_fill_color(*c); pdf.set_text_color(255,255,255)
            pdf.set_font("Helvetica","B",9); pdf.set_x(20)
            pdf.cell(170,7,f"  {sem.get('icon','')}  {sem.get('title','')}",fill=True,ln=True)
            pdf.set_fill_color(245,242,237); pdf.set_text_color(80,80,80)
            pdf.set_font("Helvetica","",8); pdf.set_x(20)
            pdf.multi_cell(170,5,f"  {sem.get('desc','')}",fill=True); pdf.ln(2)
        pdf.set_y(-18); pdf.set_font("Helvetica","",7); pdf.set_text_color(180,180,180)
        pdf.cell(0,5,"AI Strategy Workshops for School Heads · India 2026 · Confidential",align="C")
        return bytes(pdf.output())
    except Exception:
        return None

# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def render_header():
    badge = ""
    if st.session_state.mode == "voice":
        badge = '<span style="background:#0d9488;color:white;font-size:.7rem;font-weight:800;padding:3px 9px;border-radius:8px;margin-left:8px;vertical-align:middle;">🎙️ VOICE</span>'
    elif st.session_state.mode == "text":
        badge = '<span style="background:#4338ca;color:white;font-size:.7rem;font-weight:800;padding:3px 9px;border-radius:8px;margin-left:8px;vertical-align:middle;">💬 TEXT</span>'
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">🎓 AI Study Counsellor{badge}</div>
        <div class="app-subtitle">School AI Guidance Programme · India 2026</div>
    </div>""", unsafe_allow_html=True)


def render_progress():
    n_user = sum(1 for m in st.session_state.messages if m["role"] == "user")
    total = 5
    done = min(n_user // 2, total)
    dots = "".join(
        f'<div class="dot dot-done"></div>' if i < done
        else f'<div class="dot dot-active"></div>' if i == done
        else f'<div class="dot"></div>'
        for i in range(total)
    )
    st.markdown(f'<div class="prog-dots">{dots}</div>', unsafe_allow_html=True)


def render_messages():
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            txt = clean_text(msg["content"])
            if txt:
                st.markdown(f"""
                <div class="msg-ai">
                  <div class="msg-ai-av">🤖</div>
                  <div class="msg-ai-bub">{txt}</div>
                </div>""", unsafe_allow_html=True)
        else:
            vtag = '<div class="msg-voice-tag">🎙️ via voice</div>' if msg.get("via_voice") else ""
            st.markdown(f"""
            <div class="msg-stu">
              <div>
                <div class="msg-stu-bub">{msg["content"]}</div>
                {vtag}
              </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_referral_card(a):
    name    = a.get("student_name", "Student")
    cls     = a.get("student_class", "")
    subj    = ", ".join(a.get("subjects_mentioned", []))
    obs     = a.get("key_observations", [])
    note    = a.get("counsellor_note", "")
    refs    = a.get("referrals", [])

    st.markdown(f"""
    <div class="ref-card">
      <div class="ref-header">Your Personalised Guidance Plan</div>
      <div class="ref-name">{name} · {cls}{("  ·  Subjects: " + subj) if subj else ""}</div>
    """, unsafe_allow_html=True)

    if obs:
        items = "".join(f'<div class="obs-item">• &nbsp;{o}</div>' for o in obs)
        st.markdown(f'<div class="obs-box"><div class="obs-label">What we noticed</div>{items}</div>', unsafe_allow_html=True)

    if note:
        st.markdown(f'<div class="cnote">💬 &nbsp;{note}</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin:16px 0 10px;"><div style="font-size:.71rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#888;margin-bottom:10px;">Recommended Sessions</div>', unsafe_allow_html=True)
    for code in refs:
        sem = SEMINARS.get(code)
        if sem:
            st.markdown(f"""
            <div class="sem-badge" style="background:{sem['color']}18;border:1.5px solid {sem['color']}40;">
              <div class="sem-icon">{sem['icon']}</div>
              <div>
                <div class="sem-title" style="color:{sem['color']};">{sem['title']}</div>
                <div class="sem-desc">{sem['desc']}</div>
              </div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN FLOW
# ══════════════════════════════════════════════════════════════════════════════
render_header()

# ─── WELCOME ──────────────────────────────────────────────────────────────────
if st.session_state.phase == "welcome":

    st.markdown("""
    <div class="welcome-card">
      <div class="welcome-title">Hi there! 👋</div>
      <div class="welcome-body">
        I'm your school's AI study counsellor. I'll have a quick friendly chat about how you
        use AI tools for studying — no right or wrong answers, nothing you say gets you in trouble.
        It's just to help point you to the right sessions.
      </div>
      <span class="privacy-pill">🔒 Private & Confidential</span>
      <span class="privacy-pill">⏱️ 5–8 minutes</span>
      <span class="privacy-pill">✅ No judgment</span>
    </div>
    """, unsafe_allow_html=True)

    # ── MODE PICKER ───────────────────────────────────────────────────────────
    st.markdown('<div style="font-size:.85rem;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">How would you like to chat?</div>', unsafe_allow_html=True)

    col_v, col_t = st.columns(2)
    with col_v:
        if st.button("🎙️  Voice Mode\n\nSpeak your answers aloud", key="pick_voice", use_container_width=True):
            st.session_state.mode = "voice"
            st.rerun()
        if st.session_state.mode == "voice":
            st.markdown('<div style="text-align:center;font-size:.8rem;color:#0d9488;font-weight:700;margin-top:4px;">✓ Selected</div>', unsafe_allow_html=True)

    with col_t:
        if st.button("💬  Text Mode\n\nType your answers", key="pick_text", use_container_width=True):
            st.session_state.mode = "text"
            st.rerun()
        if st.session_state.mode == "text":
            st.markdown('<div style="text-align:center;font-size:.8rem;color:#4338ca;font-weight:700;margin-top:4px;">✓ Selected</div>', unsafe_allow_html=True)

    # Info box
    if st.session_state.mode == "voice":
        st.markdown("""
        <div class="info-box info-box-voice">
          🎙️ <strong>Voice mode:</strong> The counsellor speaks to you via audio.
          You record your reply by clicking the mic button.
          Uses Whisper (speech-to-text) + Nova TTS voice (warm female).
          Make sure your speakers and microphone are enabled.
        </div>""", unsafe_allow_html=True)
    elif st.session_state.mode == "text":
        st.markdown("""
        <div class="info-box info-box-text">
          💬 <strong>Text mode:</strong> Read the counsellor's messages and type your replies below.
        </div>""", unsafe_allow_html=True)

    # Class selector
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    cls_opts = [""] + [f"Class {i}" for i in range(6, 13)] + ["Other"]
    st.session_state.student_class = st.selectbox(
        "Your class (optional — helps personalise your session)",
        cls_opts, key="cls_sel")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.session_state.mode:
        if st.button("Start My Session →", key="start_btn"):
            with st.spinner("Starting..."):
                first = call_ai([])
            st.session_state.messages.append({"role": "assistant", "content": first})
            if st.session_state.mode == "voice":
                audio = tts_speak(clean_text(first))
                if audio:
                    st.session_state.tts_b64 = base64.b64encode(audio).decode()
            st.session_state.phase = "chat"
            st.rerun()
    else:
        st.markdown('<div style="text-align:center;color:#bbb;font-size:.88rem;padding:8px 0;">↑ Choose Voice or Text above to begin</div>', unsafe_allow_html=True)


# ─── CHAT ─────────────────────────────────────────────────────────────────────
elif st.session_state.phase == "chat":

    render_progress()
    render_messages()

    # Autoplay any pending TTS
    if st.session_state.tts_b64:
        autoplay_tts(st.session_state.tts_b64)
        st.session_state.tts_b64 = None

    # Check if last AI message has the final assessment JSON
    if st.session_state.messages:
        last = st.session_state.messages[-1]
        if last["role"] == "assistant":
            assessment = extract_assessment(last["content"])
            if assessment:
                st.session_state.assessment = assessment
                st.session_state.phase = "result"
                log_csv(assessment)
                st.rerun()

    # ── VOICE INPUT ───────────────────────────────────────────────────────────
    if st.session_state.mode == "voice":

        st.markdown("""
        <div style="background:white;border-radius:20px;padding:22px 20px 18px;
                    box-shadow:0 2px 16px rgba(0,0,0,.06);border:1px solid #ede8e0;
                    text-align:center;margin-bottom:14px;">
          <div style="font-size:.78rem;font-weight:700;color:#888;
                      text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">
            🎙️ Your turn — click the button below and speak
          </div>
        """, unsafe_allow_html=True)

        # st.audio_input — available in Streamlit ≥ 1.33
        # Falls back to file_uploader for older versions
        audio_data = None
        try:
            audio_data = st.audio_input(
                "Click to record · click again to stop",
                key=f"audio_{st.session_state.rec_key}",
            )
        except AttributeError:
            st.markdown('<div style="font-size:.82rem;color:#888;margin-bottom:6px;">Record a voice note then upload it:</div>', unsafe_allow_html=True)
            audio_data = st.file_uploader(
                "Voice recording",
                type=["webm", "mp3", "wav", "m4a", "ogg"],
                key=f"audio_upload_{st.session_state.rec_key}",
                label_visibility="collapsed",
            )

        st.markdown("</div>", unsafe_allow_html=True)

        if audio_data is not None:
            raw = audio_data.read() if hasattr(audio_data, "read") else bytes(audio_data)
            if raw:
                with st.spinner("🎧 Transcribing..."):
                    transcript = whisper_transcribe(raw)

                if transcript:
                    st.markdown(f"""
                    <div class="transcript-preview">
                      <div class="transcript-label">You said:</div>
                      {transcript}
                    </div>""", unsafe_allow_html=True)

                    st.session_state.messages.append(
                        {"role": "user", "content": transcript, "via_voice": True})

                    with st.spinner("💭 Thinking..."):
                        reply = call_ai(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                    with st.spinner("🔊 Generating voice response..."):
                        audio_out = tts_speak(clean_text(reply))
                    if audio_out:
                        st.session_state.tts_b64 = base64.b64encode(audio_out).decode()

                    # Reset the recorder widget key so it clears
                    st.session_state.rec_key += 1
                    st.rerun()
                else:
                    st.warning("Couldn't catch that — please try again.")
                    st.session_state.rec_key += 1
                    st.rerun()

        # Text fallback in voice mode
        st.markdown('<div style="text-align:center;font-size:.8rem;color:#ccc;margin:8px 0 2px;">or type if mic isn\'t working</div>', unsafe_allow_html=True)
        with st.form("voice_fallback_form", clear_on_submit=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                fb = st.text_input("fb", placeholder="Type here instead…", label_visibility="collapsed")
            with c2:
                fb_go = st.form_submit_button("Send")
        if fb_go and fb.strip():
            st.session_state.messages.append({"role": "user", "content": fb.strip()})
            with st.spinner("💭 Thinking..."):
                reply = call_ai(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.spinner("🔊 Generating voice..."):
                audio_out = tts_speak(clean_text(reply))
            if audio_out:
                st.session_state.tts_b64 = base64.b64encode(audio_out).decode()
            st.rerun()

    # ── TEXT INPUT ────────────────────────────────────────────────────────────
    else:
        with st.form("text_form", clear_on_submit=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                txt = st.text_input("msg", placeholder="Type your reply here…", label_visibility="collapsed")
            with c2:
                go = st.form_submit_button("Send")
        if go and txt.strip():
            st.session_state.messages.append({"role": "user", "content": txt.strip()})
            with st.spinner(""):
                reply = call_ai(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()


# ─── RESULT ───────────────────────────────────────────────────────────────────
elif st.session_state.phase == "result":
    assessment = st.session_state.assessment

    # Autoplay any pending TTS
    if st.session_state.tts_b64:
        autoplay_tts(st.session_state.tts_b64)
        st.session_state.tts_b64 = None

    # Final AI message (text — sans JSON)
    if st.session_state.messages:
        last = st.session_state.messages[-1]
        txt = clean_text(last["content"])
        if txt:
            st.markdown(f"""
            <div class="msg-ai" style="margin-bottom:14px;">
              <div class="msg-ai-av">🤖</div>
              <div class="msg-ai-bub">{txt}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    render_referral_card(assessment)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if os.path.isfile(CSV_FILE):
            with open(CSV_FILE, "rb") as f:
                st.download_button(
                    "⬇️  Session Logs (CSV)", f,
                    file_name=f"counsellor_log_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv", use_container_width=True)
    with col2:
        if PDF_AVAILABLE:
            pdf = generate_pdf(assessment)
            if pdf:
                n = assessment.get("student_name","student").replace(" ","_")
                st.download_button(
                    "🖨️  Referral Card (PDF)", pdf,
                    file_name=f"referral_{n}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf", use_container_width=True)
        else:
            st.info("Install fpdf2 for PDF: `pip install fpdf2`")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("Start New Student Session", key="new_sess", use_container_width=True):
        for k in ["phase","messages","assessment","student_class",
                  "session_id","mode","tts_b64","rec_key","pending_voice_text"]:
            st.session_state.pop(k, None)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Counsellor Dashboard")
    st.markdown("---")
    if api_key:
        st.success("✅ OpenAI connected")
        st.caption("Model: gpt-4o-mini · Voice: nova")
    else:
        st.warning("⚠️ No API key — demo mode")
        st.caption("Add OPENAI_API_KEY to .env")
    st.markdown("---")
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        st.markdown(f"**{len(rows)} student(s) assessed**")
        st.markdown("---")
        for row in reversed(rows[-10:]):
            icon = "🎙️" if row.get("mode") == "voice" else "💬"
            st.markdown(f"""
            <div style="background:#f7f4ef;border-radius:10px;padding:9px 12px;
                        margin-bottom:7px;font-size:.8rem;">
              <strong>{row.get('student_name','?')}</strong> {icon} · {row.get('student_class','')}<br>
              <span style="color:#888;">{row.get('timestamp','')}</span><br>
              <span style="color:#0d9488;font-weight:700;">{row.get('referrals','')}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.caption("No sessions yet.")
