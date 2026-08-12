from agents import function_tool, RunContextWrapper
from db import log_action, get_actions
from models import CaseContext


@function_tool
def request_ambulance(ctx: RunContextWrapper[CaseContext], location: str, injury_description: str) -> str:
    """
    Request an ambulance for a victim who needs medical attention.

    Args:
        location: Where the ambulance should be sent
        injury_description: What injuries the victim has reported
    """
    log_action(ctx.context.case_id, "request_ambulance", f"Location: {location}, Injuries: {injury_description}")
    return "Ambulance has been dispatched. ETA 10 minutes."

@function_tool
def freeze_account(ctx: RunContextWrapper[CaseContext], account_type: str, platform: str) -> str:
    """
    Send an emergency freeze request for a compromised account.

    Args:
        account_type: Type of account (bank, email, social media, crypto)
        platform: Name of the platform or bank
    """
    log_action(ctx.context.case_id, "freeze_account", f"Account: {account_type}, Platform: {platform}")
    return f"Emergency freeze request sent to {platform}. They will act within 30 minutes."

@function_tool
def alert_nearby_units(ctx: RunContextWrapper[CaseContext], location: str, item_stolen: str) -> str:
    """
    Alert patrol units near the crime scene to look for the stolen item or suspect.

    Args:
        location: Where the theft happened
        item_stolen: What was stolen
    """
    log_action(ctx.context.case_id, "alert_nearby_units", f"Location: {location}, Stolen: {item_stolen}")
    return f"Nearby units have been alerted to watch for {item_stolen} around {location}."