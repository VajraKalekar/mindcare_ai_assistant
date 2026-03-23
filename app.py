import streamlit as st
from orchestrator import run_all_agents

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mental Wellbeing Support",
    page_icon="🧠",
    layout="centered"
)

# ─── Header ──────────────────────────────────────────────────────────────────
st.title("🧠 Mental Wellbeing Support Agent")
st.markdown("""
Welcome. This tool uses a team of AI agents to give you personalized mental wellness support.
**Your responses are not stored anywhere.** Take your time filling this in honestly.
""")
st.divider()

# ─── Input Form ──────────────────────────────────────────────────────────────
st.header("Tell us how you're doing")

with st.form("wellbeing_form"):
    st.subheader("1. Your emotional state")
    emotional_state = st.slider(
        "On a scale of 1-10, how are you feeling overall? (1 = very low, 10 = great)",
        min_value=1, max_value=10, value=5
    )
    feelings_description = st.text_area(
        "Describe how you've been feeling lately (be as detailed as you like):",
        placeholder="e.g. I've been feeling anxious and overwhelmed, struggling to focus on my studies..."
    )

    st.subheader("2. Sleep")
    sleep_hours = st.slider("How many hours of sleep do you get on average?", 2, 12, 6)
    sleep_quality = st.selectbox(
        "How would you rate your sleep quality?",
        ["Very poor", "Poor", "Fair", "Good", "Excellent"]
    )

    st.subheader("3. Stress")
    stress_level = st.slider("Stress level (1 = no stress, 10 = extremely stressed)", 1, 10, 5)
    main_stressors = st.text_area(
        "What are your main sources of stress?",
        placeholder="e.g. exams, family pressure, financial worries, relationship issues..."
    )

    st.subheader("4. Your support system")
    support_system = st.text_area(
        "Who or what do you have for support? (friends, family, counselor, hobbies, etc.)",
        placeholder="e.g. I have a few close friends but feel hesitant to burden them..."
    )

    st.subheader("5. Recent life changes")
    life_changes = st.text_area(
        "Any significant changes in your life recently?",
        placeholder="e.g. moved to a new city, started college, lost a job, breakup..."
    )

    st.subheader("6. Symptoms")
    symptoms = st.multiselect(
        "Which of these are you currently experiencing? (select all that apply)",
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

    # Safety notice
    st.warning("""
    ⚠️ **Important:** This tool is for general wellness support only, not a substitute for
    professional mental health care. If you are in crisis or having thoughts of self-harm,
    please contact a crisis helpline immediately:
    **iCall (India): 9152987821** | **Vandrevala Foundation: 1860-2662-345**
    """)

    submitted = st.form_submit_button(
        "🔍 Get My Personalized Support Plan",
        use_container_width=True
    )

# ─── Processing and Output ────────────────────────────────────────────────────
if submitted:

    # ── Validation ────────────────────────────────────────────────────────────
    if not feelings_description.strip():
        st.error("Please describe how you're feeling before submitting.")
        st.stop()

    # ── Pack form data ────────────────────────────────────────────────────────
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

    # ── Call orchestrator (crisis check + agents) ─────────────────────────────
    with st.spinner("Your AI support team is analysing your situation... (this takes 10-20 seconds)"):
        try:
            results = run_all_agents(user_data)
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.info("Check that your GROQ_API_KEY in the .env file is correct.")
            st.stop()

    # ─────────────────────────────────────────────────────────────────────────
    # CRISIS PATH — shown ONLY when crisis keywords were detected
    # No AI output is shown. Only human helpline numbers.
    # ─────────────────────────────────────────────────────────────────────────
    if results.get("crisis_detected"):

        st.error("🚨 We're concerned about your safety right now")

        st.markdown(f"""
        <div style="
            background-color: #fff0f0;
            border: 1.5px solid #E24B4A;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin: 1rem 0;
            font-size: 15px;
            line-height: 1.7;
            color: #333;
        ">
            {results['message']}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📞 Free Helplines — Available Right Now")

        for name, number in results["resources"].items():
            st.markdown(f"""
            <div style="
                background: white;
                border: 0.5px solid #E24B4A;
                border-left: 4px solid #E24B4A;
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <span style="font-weight:600; font-size:14px; color:#333;">{name}</span>
                <span style="font-size:18px; font-weight:700;
                      color:#A32D2D; letter-spacing:0.03em;">{number}</span>
            </div>
            """, unsafe_allow_html=True)

        st.info(
            "💙 You don't have to go through this alone. "
            "These helplines are free, confidential, and available 24/7. "
            "Talking to someone is a sign of strength, not weakness."
        )

        # Hard stop — normal AI results must never appear during a crisis
        st.stop()

    # ─────────────────────────────────────────────────────────────────────────
    # NORMAL PATH — only reaches here when no crisis detected
    # ─────────────────────────────────────────────────────────────────────────
    st.success("✅ Your personalized support plan is ready!")
    st.divider()

    st.header("Your Mental Wellbeing Report")

    with st.expander("🧠 Assessment: Understanding Your Current State", expanded=True):
        st.markdown(results["assessment"])

    with st.expander("🎯 Immediate Action Plan: What To Do Right Now", expanded=True):
        st.markdown(results["action_plan"])

    with st.expander("🔄 Long-term Strategy: Building Lasting Wellbeing", expanded=True):
        st.markdown(results["followup"])

    st.divider()
    st.caption(
        "Remember: This AI-generated plan is a starting point. "
        "Please seek professional help if you need more support."
    )