from agents.assessment_agent import run_assessment
from agents.action_agent import run_action_plan
from agents.followup_agent import run_followup_plan

# ─── Crisis Keywords ──────────────────────────────────────────────────────────
# These are grouped by category so you can explain each group to your panel
CRISIS_KEYWORDS = [
    # Suicidal ideation
    "want to die", "want to end my life", "end it all", "end my life",
    "kill myself", "killing myself", "suicide", "suicidal",
    "don't want to be here", "don't want to live", "no reason to live",
    "better off dead", "better off without me",

    # Self harm
    "self harm", "self-harm", "hurt myself", "cutting myself",
    "hurting myself", "harm myself",

    # Hopelessness (strong indicators)
    "can't go on", "cannot go on", "can't take it anymore",
    "cannot take it anymore", "no point in living", "life is pointless",
    "nothing to live for", "i give up on life",

    # Crisis phrases
    "in crisis", "mental breakdown", "losing my mind",
    "i give up", "completely hopeless", "feel like disappearing"
]

# ─── Crisis Resources (India-focused) ─────────────────────────────────────────
CRISIS_RESOURCES = {
    "iCall (TISS)": "9152987821",
    "Vandrevala Foundation": "1860-2662-345",
    "AASRA": "9820466627",
    "iCall WhatsApp": "9152987821",
    "Snehi": "044-24640050"
}

def check_for_crisis(user_data: dict) -> bool:
    """
    Scans all user-entered text fields for crisis keywords.
    Returns True if any crisis keyword is found, False if safe.

    We check every text field — not just the main description —
    because someone might mention crisis signals anywhere in the form.
    """
    # Collect all text the user typed into one single lowercase string
    text_to_scan = " ".join([
        str(user_data.get("feelings_description", "")),
        str(user_data.get("main_stressors", "")),
        str(user_data.get("life_changes", "")),
        str(user_data.get("support_system", "")),
    ]).lower()

    # Check if any crisis keyword exists in that combined text
    for keyword in CRISIS_KEYWORDS:
        if keyword in text_to_scan:
            return True  # crisis detected — stop here

    return False  # all clear — proceed normally


def get_crisis_response() -> dict:
    """
    Returns a structured crisis response dictionary.
    This is returned instead of the normal agent output
    when a crisis is detected.
    """
    resources_text = "\n".join([
        f"• {name}: {number}"
        for name, number in CRISIS_RESOURCES.items()
    ])

    return {
        "crisis_detected": True,
        "message": (
            "We noticed some of what you shared may indicate you're going through "
            "an extremely difficult time. Your safety is the most important thing.\n\n"
            "Please reach out to one of these free, confidential helplines right now. "
            "Real people are available to talk and help you through this."
        ),
        "resources": CRISIS_RESOURCES,
        "resources_text": resources_text,
        # These are empty so app.py doesn't break if it tries to access them
        "assessment": None,
        "action_plan": None,
        "followup": None
    }


def run_all_agents(user_data: dict) -> dict:
    """
    Main orchestrator function called by app.py.

    Step 1: Check for crisis signals FIRST — before any API call
    Step 2: If crisis → return crisis response immediately
    Step 3: If safe → run all 3 agents and return combined results
    """

    # ── STEP 1: Crisis check (always runs first, costs nothing) ──
    if check_for_crisis(user_data):
        print("⚠️  Crisis keywords detected — skipping agents, returning resources")
        return get_crisis_response()

    # ── STEP 2: Normal flow — run all 3 agents ──
    print("✅ No crisis detected — running agents normally")

    print("Running Assessment Agent...")
    assessment = run_assessment(user_data)

    print("Running Action Agent...")
    action_plan = run_action_plan(user_data)

    print("Running Follow-up Agent...")
    followup = run_followup_plan(user_data)

    return {
        "crisis_detected": False,
        "assessment": assessment,
        "action_plan": action_plan,
        "followup": followup
    }