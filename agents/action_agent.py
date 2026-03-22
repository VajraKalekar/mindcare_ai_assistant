from utils.groq_client import call_llm

SYSTEM_PROMPT = """You are a practical mental health counselor focused on immediate, actionable support.

Your job is to give the person concrete things they can DO right now. Provide:
1. THREE immediate coping strategies (things to try today — be very specific and practical)
2. TWO free resources (apps, websites, or hotlines relevant to their situation)
3. ONE "first step" — the single smallest action they should take in the next hour

Rules:
- Be specific. Not "exercise more" but "go for a 15-minute walk around your block right now"
- Free resources only — no paid apps or services
- Warm and encouraging tone, never preachy
- Keep under 350 words
- Format clearly with numbered lists"""

def run_action_plan(user_data: dict) -> str:
    user_message = f"""
Create an immediate action plan for this person:

How they're feeling: {user_data['feelings_description']}
Stress level: {user_data['stress_level']}/10
Main stressors: {user_data['main_stressors']}
Symptoms: {user_data['symptoms']}
Support available: {user_data['support_system']}
Sleep situation: {user_data['sleep_hours']} hours, quality: {user_data['sleep_quality']}
"""
    return call_llm(SYSTEM_PROMPT, user_message)