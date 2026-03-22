import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads your .env file


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")
    return Groq(api_key=api_key)


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Sends a message to the LLM and returns the response text.
    system_prompt = the agent's personality and instructions
    user_message  = the actual user data
    """
    client = get_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # free model on Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,  # 0 = very consistent, 1 = more creative
        max_tokens=1024  # max length of response
    )

    return response.choices[0].message.content