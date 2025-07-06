import re
from datetime import datetime, timedelta
import calendar

# Helper to get next weekday (0=Monday, 6=Sunday)
def get_next_weekday(target_weekday):
    today = datetime.now()
    days_ahead = target_weekday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

# Helper to get next week (Monday)
def get_next_week():
    today = datetime.now()
    days_ahead = 7 - today.weekday()
    next_monday = today + timedelta(days=days_ahead)
    return next_monday.strftime("%Y-%m-%d")

# Map time-of-day words to time ranges
time_of_day_map = {
    "morning": (9, 12),
    "afternoon": (12, 17),
    "evening": (17, 20),
}

# Simple intent and slot extraction (improved)
def extract_intent_and_slots(message: str):
    intent = None
    date = None
    time = None
    summary = None
    time_range = None

    msg = message.lower()

    # Intent detection
    if any(word in msg for word in ["book", "schedule", "meeting", "call"]):
        intent = "book_appointment"
    elif any(word in msg for word in ["free", "available", "slots"]):
        intent = "check_availability"

    # Date extraction
    date_match = re.search(r"(tomorrow|today|\d{4}-\d{2}-\d{2})", msg)
    if date_match:
        if date_match.group(1) == "tomorrow":
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_match.group(1) == "today":
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            date = date_match.group(1)
    # Relative weekday (e.g., this Friday)
    weekday_match = re.search(r"this (monday|tuesday|wednesday|thursday|friday|saturday|sunday)", msg)
    if weekday_match:
        weekday_str = weekday_match.group(1)
        weekday_num = list(calendar.day_name).index(weekday_str.capitalize())
        date = get_next_weekday(weekday_num)
    # Next week
    if "next week" in msg:
        date = get_next_week()

    # Time-of-day (e.g., afternoon)
    for tod in time_of_day_map:
        if tod in msg:
            time_range = time_of_day_map[tod]
            time = f"{time_range[0]}:00 - {time_range[1]}:00"
            break

    # Time range (e.g., 3-5 PM, 3 to 5 PM, between 3 and 5 PM)
    range_match = re.search(r"(between )?(\d{1,2})(:(\d{2}))? ?(am|pm)? ?(to|-) ?(\d{1,2})(:(\d{2}))? ?(am|pm)?", msg)
    if range_match:
        start_hour = int(range_match.group(2))
        end_hour = int(range_match.group(7))
        start_period = range_match.group(5)
        end_period = range_match.group(10)
        # Convert to 24h
        if start_period == "pm" and start_hour < 12:
            start_hour += 12
        if end_period == "pm" and end_hour < 12:
            end_hour += 12
        time = f"{start_hour}:00 - {end_hour}:00"

    # Single time (e.g., 3 PM)
    if not time:
        time_match = re.search(r"(\d{1,2})(:(\d{2}))? ?(am|pm)", msg)
        if time_match:
            hour = int(time_match.group(1))
            period = time_match.group(4)
            if period == "pm" and hour < 12:
                hour += 12
            time = f"{hour}:00"

    # Summary extraction (fallback to message)
    summary = message

    return {
        "intent": intent,
        "date": date,
        "time": time,
        "summary": summary
    }

# Build the agent
def get_agent():
    agent = Agent(
        initial_state=BookingState(),
        steps=[extract_step],
    )
    return agent 