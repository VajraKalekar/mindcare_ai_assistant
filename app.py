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
# ─── Particles canvas + scroll animations (injected once at top) ──────────────
st.markdown("""
<canvas id="particles-canvas" style="
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    opacity: 0.5;
"></canvas>

<script>
(function() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = Array.from({length: 60}, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.8 + 0.4,
        dx: (Math.random() - 0.5) * 0.35,
        dy: (Math.random() - 0.5) * 0.35,
        alpha: Math.random() * 0.5 + 0.15,
        color: Math.random() > 0.5 ? '127,119,221' : '29,158,117'
    }));

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${p.color},${p.alpha})`;
            ctx.fill();
            p.x += p.dx; p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width)  p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        });

        // Draw faint connection lines between close particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(127,119,221,${0.08 * (1 - dist/100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(draw);
    }
    draw();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
})();
</script>

<script>
// Scroll-triggered fade-in observer
(function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    function attachObserver() {
        document.querySelectorAll('.scroll-reveal').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(28px)';
            el.style.transition = 'opacity 0.65s ease, transform 0.65s ease';
            observer.observe(el);
        });
    }

    // Run after Streamlit renders
    setTimeout(attachObserver, 800);
    setInterval(attachObserver, 2000);
})();
</script>
""", unsafe_allow_html=True)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── Background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 20%, #1a1535 0%, #0f0f1a 40%, #0a1628 100%);
    min-height: 100vh;
}

/* ── Noise texture overlay for depth ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    opacity: 0.4;
    pointer-events: none;
    z-index: 0;
}

/* ── Hero ── */
.hero-container {
    text-align: center;
    padding: 3.5rem 2rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(127,119,221,0.12);
    border: 1px solid rgba(127,119,221,0.35);
    color: #AFA9EC;
    font-size: 11px;
    font-weight: 600;
    padding: 6px 18px;
    border-radius: 20px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
    animation: fadeInDown 0.7s ease both;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #c8c4f8 40%, #7F77DD 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem;
    line-height: 1.15;
    animation: fadeInUp 0.8s ease both;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-size: 1rem;
    color: #6666aa;
    margin: 0 0 2rem;
    line-height: 1.8;
    animation: fadeInUp 0.9s ease both;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
}
.orb-1 {
    width: 320px; height: 320px;
    background: radial-gradient(circle, #534AB7, transparent);
    top: -80px; left: -80px;
    opacity: 0.2;
    animation: orbFloat 8s ease-in-out infinite;
}
.orb-2 {
    width: 240px; height: 240px;
    background: radial-gradient(circle, #1D9E75, transparent);
    top: 60px; right: -60px;
    opacity: 0.15;
    animation: orbFloat 10s ease-in-out infinite reverse;
}
.orb-3 {
    width: 180px; height: 180px;
    background: radial-gradient(circle, #D85A30, transparent);
    bottom: -40px; left: 40%;
    opacity: 0.1;
    animation: orbFloat 12s ease-in-out infinite;
}

/* ── Trust pills ── */
.trust-row {
    display: flex; gap: 10px;
    justify-content: center; flex-wrap: wrap;
    margin-bottom: 2.5rem;
    animation: fadeInUp 1s ease both;
}
.trust-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #888899;
    font-size: 12px; font-weight: 500;
    padding: 6px 14px; border-radius: 20px;
    transition: border-color 0.2s, color 0.2s;
}
.trust-pill:hover {
    border-color: rgba(127,119,221,0.4);
    color: #AFA9EC;
}

/* ── Stat cards ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 2rem;
    animation: fadeInUp 1.1s ease both;
}
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(127,119,221,0.15);
    border-radius: 16px; padding: 1.3rem;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
    cursor: default;
}
.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(127,119,221,0.45);
    background: rgba(127,119,221,0.07);
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #7F77DD, #5DCAA5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.stat-label { font-size: 12px; color: #555577; }

/* ── Section header ── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin: 1.8rem 0 1rem;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(127,119,221,0.12);
}
.section-icon {
    width: 38px; height: 38px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.icon-purple { background: rgba(127,119,221,0.15); }
.icon-teal   { background: rgba(29,158,117,0.15); }
.icon-coral  { background: rgba(216,90,48,0.15); }
.section-title { font-size: 15px; font-weight: 600; color: #d0d0f0; margin: 0; }
.section-sub   { font-size: 12px; color: #555577; margin: 2px 0 0; }

/* ── Emotion meter (mood display) ── */
.emotion-bar {
    display: flex; align-items: center;
    gap: 14px; margin: 0.5rem 0 1.2rem;
    padding: 12px 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(127,119,221,0.15);
    border-radius: 12px;
}
.emotion-face {
    font-size: 2rem;
    transition: all 0.3s ease;
    filter: drop-shadow(0 0 8px rgba(127,119,221,0.4));
}
.emotion-label {
    font-size: 13px; color: #8888bb; flex: 1;
}
.emotion-score {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem; font-weight: 700;
    color: #AFA9EC;
}
<div class="welcome-card">
/* ── Welcome card ── */
.welcome-card {
    background: rgba(127,119,221,0.07);
    border: 1px solid rgba(127,119,221,0.2);
    border-radius: 16px; padding: 1.1rem 1.4rem;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 14px;
    animation: fadeInUp 0.5s ease both;
    transition: border-color 0.3s;
}
.welcome-card:hover { border-color: rgba(127,119,221,0.4); }
.welcome-avatar {
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #3C3489, #7F77DD);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 20px; font-weight: 700; color: white;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(127,119,221,0.3);
}
.welcome-text { font-size: 14px; color: #b0b0d0; line-height: 1.6; }
.welcome-text strong { color: #AFA9EC; }

/* ── Result cards ── */
.result-card {
    border-radius: 18px; padding: 1.5rem 1.7rem;
    margin-bottom: 14px; position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.result-card:hover {
    transform: translateY(-3px);
}
.result-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
}
.result-card::after {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.05;
}
.card-assessment {
    background: linear-gradient(135deg, rgba(29,158,117,0.09), rgba(29,158,117,0.04));
    border: 1px solid rgba(29,158,117,0.22);
}
.card-assessment::before { background: linear-gradient(180deg, #1D9E75, #5DCAA5); }
.card-assessment::after  { background: #1D9E75; }
.card-assessment:hover   { box-shadow: 0 8px 32px rgba(29,158,117,0.12); }

.card-action {
    background: linear-gradient(135deg, rgba(127,119,221,0.09), rgba(127,119,221,0.04));
    border: 1px solid rgba(127,119,221,0.22);
}
.card-action::before { background: linear-gradient(180deg, #534AB7, #7F77DD); }
.card-action::after  { background: #7F77DD; }
.card-action:hover   { box-shadow: 0 8px 32px rgba(127,119,221,0.12); }

.card-followup {
    background: linear-gradient(135deg, rgba(216,90,48,0.09), rgba(216,90,48,0.04));
    border: 1px solid rgba(216,90,48,0.22);
}
.card-followup::before { background: linear-gradient(180deg, #D85A30, #F0997B); }
.card-followup::after  { background: #D85A30; }
.card-followup:hover   { box-shadow: 0 8px 32px rgba(216,90,48,0.12); }

.card-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 600;
    padding: 4px 12px; border-radius: 20px;
    margin-bottom: 12px; letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-teal   { background: rgba(29,158,117,0.18);  color: #5DCAA5;  border: 1px solid rgba(29,158,117,0.3); }
.badge-purple { background: rgba(127,119,221,0.18); color: #AFA9EC;  border: 1px solid rgba(127,119,221,0.3); }
.badge-coral  { background: rgba(216,90,48,0.18);   color: #F0997B;  border: 1px solid rgba(216,90,48,0.3); }
.card-content { font-size: 14px; color: #b0b0cc; line-height: 1.85; }
<div class="welcome-card scroll-reveal">

/* ── Crisis card ── */
.crisis-card {
    background: rgba(226,75,74,0.09);
    border: 1px solid rgba(226,75,74,0.35);
    border-radius: 16px; padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    animation: pulseRed 2.5s ease-in-out infinite;
}
.helpline-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(226,75,74,0.25);
    border-left: 4px solid #E24B4A;
    border-radius: 11px; padding: 13px 16px;
    margin-bottom: 10px;
    display: flex; justify-content: space-between; align-items: center;
    transition: background 0.2s, transform 0.2s;
}
.helpline-card:hover {
    background: rgba(226,75,74,0.07);
    transform: translateX(4px);
}
.helpline-name   { font-weight: 600; font-size: 14px; color: #e0e0f0; }
.helpline-number { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; color: #F09595; letter-spacing: 0.05em; }

/* ── Submit button ── */
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #3C3489 0%, #7F77DD 100%) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important; font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(127,119,221,0.35) !important;
    position: relative !important;
}
div.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(127,119,221,0.5) !important;
}
div.stFormSubmitButton > button:active {
    transform: translateY(0px) scale(0.99) !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(127,119,221,0.2) !important;
    border-radius: 11px !important;
    color: #d0d0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(127,119,221,0.55) !important;
    box-shadow: 0 0 0 3px rgba(127,119,221,0.1) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #534AB7, #7F77DD) !important;
}

/* ── Multiselect tags ── */
span[data-baseweb="tag"] {
    background: rgba(127,119,221,0.2) !important;
    border: 1px solid rgba(127,119,221,0.4) !important;
    border-radius: 8px !important;
    color: #AFA9EC !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(127,119,221,0.15) !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(127,119,221,0.3) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(127,119,221,0.3);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(127,119,221,0.5); }

hr { border-color: rgba(127,119,221,0.12) !important; }

/* ── Animations ── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes orbFloat {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(15px,-20px) scale(1.05); }
    66%      { transform: translate(-10px,10px) scale(0.97); }
}
@keyframes pulseRed {
    0%,100% { box-shadow: 0 0 0 0 rgba(226,75,74,0); }
    50%      { box-shadow: 0 0 24px 4px rgba(226,75,74,0.12); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes glow {
    0%,100% { opacity: 0.6; }
    50%      { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)


# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container scroll-reveal">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="hero-badge">✦ &nbsp; AI-Powered Mental Wellness</div>
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
<div class="stats-row scroll-reveal">
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">🤖 Specialised AI agents</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">~20s</div>
        <div class="stat-label">⚡ To your full report</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">🆓 Free, no sign-up needed</div>
    </div>
</div>
""", unsafe_allow_html=True)

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

    # ── Emotion avatar — responds to slider value ──────────────────────────
    emotion_map = {
        1: ("😞", "Very low — feeling really down"),
        2: ("😟", "Low — struggling quite a bit"),
        3: ("😔", "Below average — things feel heavy"),
        4: ("😐", "Somewhat low — not quite yourself"),
        5: ("😶", "Neutral — getting through the day"),
        6: ("🙂", "Okay — managing reasonably well"),
        7: ("😊", "Fairly good — some positive moments"),
        8: ("😄", "Good — feeling balanced and calm"),
        9: ("😁", "Great — energetic and positive"),
        10: ("🤩", "Excellent — feeling really well!"),
    }
    face, label = emotion_map[emotional_state]
    st.markdown(f"""
        <div class="emotion-bar">
            <div class="emotion-face">{face}</div>
            <div class="emotion-label">{label}</div>
            <div class="emotion-score">{emotional_state}/10</div>
        </div>
        """, unsafe_allow_html=True)
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
    # ── Stress avatar ──────────────────────────────────────────────────────
    stress_map = {
        1: ("😌", "Very calm — feeling at ease"),
        2: ("🧘", "Calm — mostly relaxed"),
        3: ("😎", "Low stress — mostly in control"),
        4: ("🙂", "Mild stress — manageable"),
        5: ("😐", "Moderate — noticeable tension"),
        6: ("😤", "Elevated — stress is building"),
        7: ("😰", "High — feeling the pressure"),
        8: ("😣", "Very high — quite overwhelmed"),
        9: ("😩", "Severe — barely holding on"),
        10: ("🤯", "Extreme — completely overwhelmed"),
    }
    s_face, s_label = stress_map[stress_level]
    st.markdown(f"""
       <div class="emotion-bar" style="border-color:rgba(216,90,48,0.2);">
           <div class="emotion-face">{s_face}</div>
           <div class="emotion-label">{s_label}</div>
           <div class="emotion-score" style="color:#F0997B;">{stress_level}/10</div>
       </div>
       """, unsafe_allow_html=True)

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
        <div class="scroll-reveal" style="text-align:center; padding:1.5rem 0 1rem;">
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
    <div class="result-card card-followup scroll-reveal">
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
        <div class="section-header scroll-reveal">
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
