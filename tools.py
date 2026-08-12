from agents import function_tool

@function_tool
def request_ambulance(location: str, injury_description: str) -> str:
    """
    Request an ambulance for a victim who needs medical attention.

    Args:
        location: Where the ambulance should be sent
        injury_description: What injuries the victim has reported
    """
    print(f"🚑 AMBULANCE REQUESTED to {location} for: {injury_description}")
    return "Ambulance has been dispatched. ETA 10 minutes."