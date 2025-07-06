# Conversational AI Calendar Agent

This project is a conversational AI agent that helps users book appointments on Google Calendar via natural language chat.

## Tech Stack
- Backend: FastAPI (Python)
- Agent Framework: Custom Python (NLU logic)
- Frontend: Streamlit
- Calendar: Google Calendar API

## Output
![running](https://github.com/user-attachments/assets/c6fa549e-afc3-4039-9877-e2713ecc9c1a)

## Features
- Natural language chat for booking and checking calendar slots
- Understands:
  - Time-of-day words ("afternoon", "morning", "evening")
  - Relative weekdays ("this Friday")
  - "Next week" expressions
  - Time ranges ("3-5 PM", "between 3 and 5 PM")
  - Explicit dates and times ("2024-06-20", "3 PM")
- Checks Google Calendar for availability
- Books confirmed time slots
- Interactive chat UI with slot selection

## Setup
1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Google Calendar API credentials (see below).
4. Run the backend and frontend servers.

## Google Calendar API Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a project and enable the Google Calendar API
- Create OAuth 2.0 credentials and download the `credentials.json` file
- Place `credentials.json` in the project root

## Running

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Start the FastAPI backend:**
   ```bash
   uvicorn main:app --reload
   ```
   - The first time you run this, a browser window will open for Google authentication. Complete the process with your test user Google account.
   - Keep this terminal window open while using the app.

3. **In a new terminal, activate the virtual environment again:**
   ```bash
   source venv/bin/activate
   ```

4. **Start the Streamlit frontend:**
   ```bash
   streamlit run app.py
   ```
   - Open the provided local URL in your browser 

5. **Start chatting!**
   - Try example queries like:
     - "Hey, I want to schedule a call for tomorrow afternoon."
     - "Do you have any free time this Friday?"
     - "Book a meeting between 3-5 PM next week."

## Troubleshooting
- **OAuth Error:** Make sure your Google account is added as a test user in the Google Cloud Console.
- **Port in Use:** If you get an "address already in use" error, kill the process using that port or use a different port.
- **Connection Error:** Ensure the backend is running before starting the frontend.

## Example Conversations Your Agent Can Handle
- "Hey, I want to schedule a call for tomorrow afternoon."
- "Do you have any free time this Friday?"
- "Book a meeting between 3-5 PM next week."
- "Book a meeting at 10 AM on 2024-06-20."
- "What slots are available in the evening next Monday?"
