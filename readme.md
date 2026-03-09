# AI Readiness Chatbot — Setup & Run Guide
## AI Strategy Workshops for School Heads · India 2026

---

## Prerequisites
- Python 3.9 or higher
- VS Code with Python extension
- An Anthropic API key (get one at https://console.anthropic.com)

---

## Setup Steps

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

**Option A — Environment variable (recommended):**
```bash
# Windows (Command Prompt):
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows (PowerShell):
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Mac/Linux:
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Option B — Create a .env file in the project folder:**
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Then add `python-dotenv` to requirements.txt and add these lines to the top of app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at http://localhost:8501

---

## What the App Does

**Phase 1 — Assessment (10 questions):**
- Personal AI tool experience
- School AI planning stage
- Stakeholder readiness (board, teachers, parents)
- Biggest concern about AI
- DPDP Act 2023 awareness
- Teacher readiness
- AI policy status
- Personal leadership support needs (multi-select)
- Parent engagement level
- Open-ended challenge question

**Phase 2 — Claude Analysis:**
- Maps answers to the CCSCR framework
  (Curriculum · Capacity · Safety · Community · ROI & Strategy)
- Generates personalised gap analysis with traffic-light ratings
- Provides 3-4 specific priority action areas
- Maps gaps to specific workshop sessions
- Suggests 90-day quick wins
- Streams the response live for a polished feel

**Fallback mode (no API key):**
- A rule-based analysis engine kicks in automatically
- Covers all 5 CCSCR dimensions based on scored responses
- Fully functional without Claude API

---

## Customisation

- **Questions:** Edit the `QUESTIONS` list in app.py
- **Analysis prompt:** Edit `ANALYSIS_SYSTEM_PROMPT` to adjust tone, framework, or workshop details
- **Styling:** All CSS is in the `st.markdown("""<style>...""")` block at the top
- **Cities / pricing:** Update the workshop CTA section near the bottom of app.py

---

## File Structure
```
ai_readiness_chatbot/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## Deployment Options
- **Streamlit Cloud:** Push to GitHub → connect at share.streamlit.io → add API key in Secrets
- **Local network:** Run with `streamlit run app.py --server.address 0.0.0.0` to share on LAN
