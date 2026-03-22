from agents.assessment_agent import run_assessment
from agents.action_agent import run_action_plan
from agents.followup_agent import run_followup_plan


def run_all_agents(user_data: dict) -> dict:
    """
    Runs all 3 agents with the same user data.
    Returns a dictionary with all 3 results.
    """
    print("Running Assessment Agent...")
    assessment = run_assessment(user_data)

    print("Running Action Agent...")
    action_plan = run_action_plan(user_data)

    print("Running Follow-up Agent...")
    followup = run_followup_plan(user_data)

    return {
        "assessment": assessment,
        "action_plan": action_plan,
        "followup": followup
    }