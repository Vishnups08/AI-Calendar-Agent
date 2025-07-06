import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service


def list_events(service, calendar_id="primary", time_min=None, time_max=None, max_results=10):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        service.events().list(
            calendarId=calendar_id,
            timeMin=time_min or now,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
    )
    return events_result.get("items", [])


def is_time_slot_free(service, start_time, end_time, calendar_id="primary"):
    events = list_events(service, calendar_id, time_min=start_time, time_max=end_time)
    return len(events) == 0


def create_event(service, summary, start_time, end_time, calendar_id="primary"):
    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event 