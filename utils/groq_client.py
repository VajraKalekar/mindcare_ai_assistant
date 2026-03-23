import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_client():
    # Try Streamlit secrets first (used on Streamlit Cloud)
    # Fall back to .env file (used locally)
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Add it to .streamlit/secrets.toml for cloud "
            "or .env for local."
        )
    return Groq(api_key=api_key)


def call_llm(system_prompt: str, user_message: str) -> str:
    client = get_client()

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content

        except Exception as e:
            if "429" in str(e) and attempt < 2:
                import time
                time.sleep(10)
                continue
            raise e