from utils.groq_client import call_llm

SYSTEM_PROMPT = """You are a long-term mental wellness strategist and therapist.

Your job is to help the person build sustainable wellbeing over the coming weeks and months. Provide:
1. A 4-week basic wellness plan (week by week, each week has ONE focus)
2. Three habits to build gradually (start tiny — make them realistic)
3. Warning signs to watch for (when to seek professional help)
4. One long-term goal they can work toward

Rules:
- Realistic for a busy person (student/working adult)
- Free strategies only
- Warm, hopeful, and non-overwhelming tone
- Keep under 400 words
- Be specific to THEIR situation"""

def run_followup_plan(user_data: dict) -> str:
    user_message = f"""
Design a long-term wellness strategy for this person:

Current emotional state: {user_data['feelings_description']}
Stress level: {user_data['stress_level']}/10
Life changes they're dealing with: {user_data['life_changes']}
Current symptoms: {user_data['symptoms']}
Support system: {user_data['support_system']}
Sleep: {user_data['sleep_hours']} hours, {user_data['sleep_quality']} quality
Main stressors: {user_data['main_stressors']}
"""
    return call_llm(SYSTEM_PROMPT, user_message)