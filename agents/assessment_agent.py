from utils.groq_client import call_llm

SYSTEM_PROMPT = """You are a compassionate clinical psychologist specializing in mental health assessment.

Your job is to carefully read the user's situation and provide:
1. A warm, empathetic summary of their current emotional state
2. Key patterns or concerns you notice (be specific)
3. Their strengths and protective factors
4. An overall severity level: Mild | Moderate | Significant

Rules:
- Use plain, kind language — no jargon
- Be specific to THEIR situation, not generic
- Keep your response under 300 words
- Never diagnose. You are providing a wellness assessment, not a clinical diagnosis.
- Always end with one sentence of encouragement"""

def run_assessment(user_data: dict) -> str:
    """
    user_data is a dictionary with all the form inputs from the user.
    We convert it into a readable message for the AI.
    """
    user_message = f"""
Please assess the following person's mental wellbeing:

Emotional state (1-10, where 10 is best): {user_data['emotional_state']}/10
They describe their feelings as: {user_data['feelings_description']}

Sleep: {user_data['sleep_hours']} hours per night. Quality: {user_data['sleep_quality']}
Stress level (1-10): {user_data['stress_level']}/10
Main stressors: {user_data['main_stressors']}

Support system: {user_data['support_system']}
Recent life changes: {user_data['life_changes']}
Current symptoms they notice: {user_data['symptoms']}
"""
    return call_llm(SYSTEM_PROMPT, user_message)