# Conversational AI Calendar Agent

This project is a conversational AI agent that helps users book appointments on Google Calendar via natural language chat.

## Tech Stack
- Backend: FastAPI (Python)
- Agent Framework: Custom Python (NLU logic)
- Frontend: Streamlit
- Calendar: Google Calendar API

## Output
<img width="1431" alt="Screenshot 2025-07-06 at 3 54 53 PM" src="https://github.com/user-attachments/assets/18a4fcfe-535b-4cc5-a46e-d3e26b394c60" />
<img width="1440" alt="Screenshot 2025-07-06 at 3 54 26 PM" src="https://github.com/user-attachments/assets/7bad4867-4581-4fc6-8ea7-6ad04a3bee40" />


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


## Example Conversations Your Agent Can Handle
- "Hey, I want to schedule a call for tomorrow afternoon."
- "Do you have any free time this Friday?"
- "Book a meeting between 3-5 PM next week."
