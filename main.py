from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import extract_intent_and_slots
from calendar_utils import get_calendar_service, is_time_slot_free, create_event
from datetime import datetime, timedelta

app = FastAPI()

# Allow CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Conversational AI Calendar Agent Backend"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        state = extract_intent_and_slots(user_message)
        service = get_calendar_service()

        if state["intent"] == "check_availability" and state["date"]:
            # Check for free slots on the given date (simple: check every hour 9-17)
            date = state["date"]
            available_slots = []
            for hour in range(9, 18):
                start_time = f"{date}T{hour:02d}:00:00Z"
                end_time = f"{date}T{hour+1:02d}:00:00Z"
                if is_time_slot_free(service, start_time, end_time):
                    available_slots.append(f"{hour}:00 - {hour+1}:00")
            if available_slots:
                response = f"Available slots on {date}: " + ", ".join(available_slots)
            else:
                response = f"No free slots found on {date}."
        elif state["intent"] == "book_appointment" and state["date"] and state["time"]:
            # Book the slot (assume 1 hour duration)
            date = state["date"]
            time_str = state["time"].replace("am", "").replace("pm", "")
            hour = int(time_str.split(":")[0])
            if "pm" in state["time"].lower() and hour < 12:
                hour += 12
            start_time = f"{date}T{hour:02d}:00:00Z"
            end_time = f"{date}T{hour+1:02d}:00:00Z"
            if is_time_slot_free(service, start_time, end_time):
                event = create_event(service, state["summary"], start_time, end_time)
                response = f"Booked: {event.get('summary')} at {state['time']} on {date}."
            else:
                response = f"Sorry, {state['time']} on {date} is not available."
        else:
            response = "Please specify what you want to do and provide a date/time."
        return {"response": response}
    except Exception as e:
        import traceback
        print("Exception in /chat endpoint:", e)
        traceback.print_exc()
        return {"response": f"(Backend error: {str(e)})"} 