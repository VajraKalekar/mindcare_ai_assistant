import streamlit as st
from orchestrator import run_all_agents
from tracker import save_session, get_user_sessions, get_session_count
from charts import show_mood_chart

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="centered"
)

# ─── Global CSS injection ─────────────────────────────────────────────────────
# This is where all the visual magic happens.
# Streamlit allows injecting raw HTML/CSS via st.markdown with unsafe_allow_html=True
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base app styling ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Hide default Streamlit elements that look cheap */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Animated starfield background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* ── Hero section ── */
.hero-container {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(127, 119, 221, 0.15);
    border: 1px solid rgba(127, 119, 221, 0.4);
    color: #AFA9EC;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    animation: fadeInDown 0.6s ease;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #AFA9EC 50%, #7F77DD 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem;
    line-height: 1.2;
    animation: fadeInUp 0.7s ease;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #8888aa;
    margin: 0 0 2rem;
    line-height: 1.7;
    animation: fadeInUp 0.8s ease;
}

/* ── Glowing orb decorations ── */
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    pointer-events: none;
    animation: pulse 4s ease-in-out infinite;
}
.orb-1 {
    width: 300px; height: 300px;
    background: #7F77DD;
    top: -100px; left: -100px;
}
.orb-2 {
    width: 200px; height: 200px;
    background: #1D9E75;
    top: 50px; right: -80px;
    animation-delay: 2s;
}

/* ── Trust pills ── */
.trust-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 2rem;
    animation: fadeInUp 0.9s ease;
}
.trust-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #aaaacc;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 20px;
}

/* ── Stat cards row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 2rem;
    animation: fadeInUp 1s ease;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(127, 119, 221, 0.2);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-3px);
    border-color: rgba(127, 119, 221, 0.5);
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #7F77DD;
    margin-bottom: 4px;
}
.stat-label {
    font-size: 12px;
    color: #666688;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 1.5rem 0 1rem;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(127, 119, 221, 0.15);
}
.section-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.icon-purple { background: rgba(127, 119, 221, 0.15); }
.icon-teal   { background: rgba(29, 158, 117, 0.15); }
.icon-coral  { background: rgba(216, 90, 48, 0.15); }
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #d0d0f0;
    margin: 0;
}
.section-sub {
    font-size: 12px;
    color: #666688;
    margin: 2px 0 0;
}

/* ── Result cards ── */
.result-card {
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s ease;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.card-assessment {
    background: rgba(29, 158, 117, 0.08);
    border: 1px solid rgba(29, 158, 117, 0.25);
}
.card-assessment::before { background: #1D9E75; }
.card-action {
    background: rgba(127, 119, 221, 0.08);
    border: 1px solid rgba(127, 119, 221, 0.25);
}
.card-action::before { background: #7F77DD; }
.card-followup {
    background: rgba(216, 90, 48, 0.08);
    border: 1px solid rgba(216, 90, 48, 0.25);
}
.card-followup::before { background: #D85A30; }
.card-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    letter-spacing: 0.04em;
}
.badge-teal   { background: rgba(29,158,117,0.2);  color: #5DCAA5; }
.badge-purple { background: rgba(127,119,221,0.2); color: #AFA9EC; }
.badge-coral  { background: rgba(216,90,48,0.2);   color: #F0997B; }
.card-content {
    font-size: 14px;
    color: #c0c0e0;
    line-height: 1.75;
}

/* ── Crisis card ── */
.crisis-card {
    background: rgba(226, 75, 74, 0.1);
    border: 1.5px solid rgba(226, 75, 74, 0.4);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    animation: pulse-red 2s ease-in-out infinite;
}
.helpline-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(226, 75, 74, 0.3);
    border-left: 4px solid #E24B4A;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
}
.helpline-card:hover {
    background: rgba(226, 75, 74, 0.08);
}
.helpline-name   { font-weight: 600; font-size: 14px; color: #e0e0f0; }
.helpline-number { font-size: 17px; font-weight: 700; color: #F09595; letter-spacing: 0.04em; }

/* ── Nickname welcome card ── */
.welcome-card {
    background: rgba(127, 119, 221, 0.08);
    border: 1px solid rgba(127, 119, 221, 0.2);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 14px;
    animation: fadeInUp 0.5s ease;
}
.welcome-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #534AB7, #7F77DD);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 700; color: white;
    flex-shrink: 0;
}
.welcome-text { font-size: 14px; color: #c0c0e0; }
.welcome-text strong { color: #AFA9EC; }

/* ── Submit button ── */
div.stButton > button, div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #534AB7 0%, #7F77DD 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    box-shadow: 0 4px 20px rgba(127, 119, 221, 0.3) !important;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
}

/* ── Streamlit form inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(127, 119, 221, 0.25) !important;
    border-radius: 10px !important;
    color: #d0d0f0 !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(127, 119, 221, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(127, 119, 221, 0.1) !important;
}

/* ── Slider accent ── */
div[data-testid="stSlider"] > div > div > div {
    background: #7F77DD !important;
}

/* ── Expander styling ── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(127, 119, 221, 0.2) !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(127, 119, 221, 0.15) !important;
}

/* ── Animations ── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 0.12; transform: scale(1); }
    50%       { opacity: 0.2;  transform: scale(1.05); }
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(226,75,74,0); }
    50%       { box-shadow: 0 0 20px 2px rgba(226,75,74,0.15); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ── Loading spinner override ── */
div[data-testid="stSpinner"] {
    color: #7F77DD !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="hero-badge">✦ AI-Powered Mental Wellness</div>
    <h1 class="hero-title">Your Mind Deserves<br>Better Support</h1>
    <p class="hero-subtitle">
        A team of specialised AI agents analyses your emotional state,<br>
        builds an action plan, and designs your long-term wellness strategy.
    </p>
    <div class="trust-row">
        <span class="trust-pill">🔒 Not stored personally</span>
        <span class="trust-pill">⚡ Results in 20 seconds</span>
        <span class="trust-pill">🆓 Completely free</span>
        <span class="trust-pill">🇮🇳 India helplines included</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stat cards ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">Specialised AI agents</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">~20s</div>
        <div class="stat-label">To your full report</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Free, no sign-up</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Nickname input ───────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon icon-purple">👤</div>
    <div>
        <p class="section-title">Before you begin</p>
        <p class="section-sub">Enter a nickname to track your progress over time</p>
    </div>
</div>
""", unsafe_allow_html=True)

nickname = st.text_input(
    label="Nickname",
    placeholder="e.g. arjun, student01, anon — anything you'll remember",
    max_chars=30,
    label_visibility="collapsed"
)

# ── Returning user welcome + chart ────────────────────────────────────────────
if nickname and nickname.strip():
    past_sessions  = get_user_sessions(nickname)
    session_count  = get_session_count(nickname)

    if session_count > 0:
        initials = nickname.strip()[0].upper()
        st.markdown(f"""
        <div class="welcome-card">
            <div class="welcome-avatar">{initials}</div>
            <div class="welcome-text">
                Welcome back, <strong>{nickname.capitalize()}</strong>! 
                You have completed <strong>{session_count}</strong> session(s). 
                Your progress chart is below.
            </div>
        </div>
        """, unsafe_allow_html=True)
        show_mood_chart(past_sessions, nickname)
    else:
        initials = nickname.strip()[0].upper()
        st.markdown(f"""
        <div class="welcome-card">
            <div class="welcome-avatar">{initials}</div>
            <div class="welcome-text">
                Hello, <strong>{nickname.capitalize()}</strong>! 
                This is your first session — your progress chart will appear 
                here after your second visit.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ─── Input Form ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-icon icon-teal">💬</div>
    <div>
        <p class="section-title">Tell us how you're doing</p>
        <p class="section-sub">Be as honest as you like — everything stays private</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("wellbeing_form"):

    # ── Section 1 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-purple">😊</div>
        <div><p class="section-title">Emotional state</p></div>
    </div>
    """, unsafe_allow_html=True)

    emotional_state = st.slider(
        "Overall feeling (1 = very low, 10 = great)",
        min_value=1, max_value=10, value=5
    )
    feelings_description = st.text_area(
        "Describe how you've been feeling lately:",
        placeholder="e.g. I've been feeling anxious and overwhelmed, struggling to focus on my studies...",
        height=100
    )

    # ── Section 2 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-purple">🌙</div>
        <div><p class="section-title">Sleep</p></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        sleep_hours = st.slider("Average sleep hours", 2, 12, 6)
    with col2:
        sleep_quality = st.selectbox(
            "Sleep quality",
            ["Very poor", "Poor", "Fair", "Good", "Excellent"]
        )

    # ── Section 3 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-coral">⚡</div>
        <div><p class="section-title">Stress</p></div>
    </div>
    """, unsafe_allow_html=True)

    stress_level = st.slider(
        "Stress level (1 = calm, 10 = extremely stressed)",
        1, 10, 5
    )
    main_stressors = st.text_area(
        "Main sources of stress:",
        placeholder="e.g. exams, family pressure, financial worries...",
        height=80
    )

    # ── Section 4 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-teal">🤝</div>
        <div><p class="section-title">Support system</p></div>
    </div>
    """, unsafe_allow_html=True)

    support_system = st.text_area(
        "Who or what supports you?",
        placeholder="e.g. close friends, family, hobbies, a counselor...",
        height=80
    )

    # ── Section 5 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-purple">🔄</div>
        <div><p class="section-title">Recent life changes</p></div>
    </div>
    """, unsafe_allow_html=True)

    life_changes = st.text_area(
        "Any significant changes lately?",
        placeholder="e.g. new city, college, job change, relationship...",
        height=80
    )

    # ── Section 6 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon icon-coral">🩺</div>
        <div><p class="section-title">Current symptoms</p></div>
    </div>
    """, unsafe_allow_html=True)

    symptoms = st.multiselect(
        "Select all that apply:",
        [
            "Difficulty concentrating",
            "Low motivation",
            "Feeling hopeless",
            "Social withdrawal",
            "Irritability or mood swings",
            "Physical fatigue",
            "Appetite changes",
            "Anxiety or constant worry",
            "Sadness most of the day",
            "Trouble sleeping or sleeping too much",
            "Loss of interest in things I used to enjoy",
            "Feeling disconnected from others"
        ]
    )

    st.warning(
        "⚠️ This tool is for general wellness support only — not a substitute for "
        "professional mental health care. If you are in crisis, please contact a helpline immediately: "
        "iCall (India): 9152987821 | Vandrevala Foundation: 1860-2662-345"
    )

    submitted = st.form_submit_button(
        "Analyse My Wellbeing",
        use_container_width=True
    )

# ─── Processing and Output ────────────────────────────────────────────────────
if submitted:

    if not nickname or not nickname.strip():
        st.error("Please enter a nickname above before submitting.")
        st.stop()

    if not feelings_description.strip():
        st.error("Please describe how you're feeling before submitting.")
        st.stop()

    user_data = {
        "emotional_state": emotional_state,
        "feelings_description": feelings_description,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "stress_level": stress_level,
        "main_stressors": main_stressors if main_stressors.strip() else "Not specified",
        "support_system": support_system if support_system.strip() else "Not specified",
        "life_changes": life_changes if life_changes.strip() else "None mentioned",
        "symptoms": ", ".join(symptoms) if symptoms else "None selected"
    }

    save_session(nickname, user_data)

    with st.spinner("Your AI wellness team is analysing your situation..."):
        try:
            results = run_all_agents(user_data)
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.info("Check that your GROQ_API_KEY in the .env file is correct.")
            st.stop()

    # ── Crisis path ───────────────────────────────────────────────────────────
    if results.get("crisis_detected"):

        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 0.5rem;">
            <span style="font-size:3rem;">🚨</span>
            <h2 style="color:#F09595; margin:0.5rem 0;">We're concerned about your safety</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="crisis-card">
            <p style="font-size:15px; color:#e0c0c0; line-height:1.75; margin:0;">
                {results['message']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-icon" style="background:rgba(226,75,74,0.15);">📞</div>
            <div><p class="section-title" style="color:#F09595;">
                Free helplines — real people, available now</p></div>
        </div>
        """, unsafe_allow_html=True)

        for name, number in results["resources"].items():
            st.markdown(f"""
            <div class="helpline-card">
                <span class="helpline-name">{name}</span>
                <span class="helpline-number">{number}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; padding:1.5rem 0; color:#8888aa; font-size:14px;">
            💙 You don't have to go through this alone.<br>
            These helplines are free, confidential, and available 24/7.
        </div>
        """, unsafe_allow_html=True)

        st.stop()

    # ── Normal path ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 1rem; animation: fadeInUp 0.5s ease;">
        <span style="font-size:2.5rem;">✅</span>
        <h2 style="color:#5DCAA5; margin:0.5rem 0;">Your support plan is ready</h2>
        <p style="color:#666688; font-size:14px;">
            Three specialised agents have analysed your situation
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Assessment card
    st.markdown("""
    <div class="result-card card-assessment">
        <span class="card-badge badge-teal">🧠 Assessment Agent</span>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card-content">{results["assessment"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Action card
    st.markdown("""
    <div class="result-card card-action">
        <span class="card-badge badge-purple">🎯 Action Agent</span>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card-content">{results["action_plan"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Follow-up card
    st.markdown("""
    <div class="result-card card-followup">
        <span class="card-badge badge-coral">🔄 Follow-up Agent</span>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card-content">{results["followup"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Updated mood chart
    updated_sessions = get_user_sessions(nickname)
    if len(updated_sessions) >= 2:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon icon-purple">📈</div>
            <div>
                <p class="section-title">Your progress so far</p>
                <p class="section-sub">Tracking your journey across sessions</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        show_mood_chart(updated_sessions, nickname)

    st.divider()
    st.markdown("""
    <p style="text-align:center; color:#444466; font-size:13px; padding-bottom:1rem;">
        This AI-generated plan is a starting point — not a substitute for professional care.
    </p>
    """, unsafe_allow_html=True)