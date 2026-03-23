import json
import os
from datetime import datetime

# ─── File path ────────────────────────────────────────────────────────────────
# All session data is stored in this single JSON file
# It sits in the project root folder
SESSION_FILE = "session_data.json"


def load_all_sessions() -> dict:
    """
    Reads the JSON file and returns all sessions for all users.
    If the file doesn't exist yet, returns an empty dictionary.
    """
    if not os.path.exists(SESSION_FILE):
        return {}

    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, start fresh
        return {}


def save_session(nickname: str, user_data: dict) -> None:
    """
    Saves one session entry under the given nickname.
    If the nickname already exists, the new entry is appended.
    If it's a new nickname, a fresh list is created for them.

    Only saves the three numeric scores we need for the chart
    plus the timestamp — we never save the user's personal
    text descriptions for privacy.
    """
    # Load whatever is already saved
    all_sessions = load_all_sessions()

    # Build the entry for this session — numbers only, no personal text
    new_entry = {
        "date": datetime.now().strftime("%d %b %Y"),
        "time": datetime.now().strftime("%H:%M"),
        "emotional_state": user_data["emotional_state"],
        "stress_level": user_data["stress_level"],
        "sleep_hours": user_data["sleep_hours"]
    }

    # Add under the nickname key
    nickname_clean = nickname.strip().lower()  # normalize: "Arjun" == "arjun"

    if nickname_clean not in all_sessions:
        all_sessions[nickname_clean] = []  # first time this nickname is used

    all_sessions[nickname_clean].append(new_entry)

    # Write back to file
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(all_sessions, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save session data: {e}")


def get_user_sessions(nickname: str) -> list:
    """
    Returns the list of all past sessions for a given nickname.
    Returns an empty list if the nickname has no history yet.
    """
    all_sessions = load_all_sessions()
    nickname_clean = nickname.strip().lower()
    return all_sessions.get(nickname_clean, [])


def get_session_count(nickname: str) -> int:
    """
    Returns how many sessions this nickname has completed.
    Useful for showing 'Session 3 of your journey' type messages.
    """
    return len(get_user_sessions(nickname))