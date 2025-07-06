import streamlit as st
import requests

st.title("Conversational AI Calendar Agent")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state["messages"].append(("user", user_input))
    # Send to FastAPI backend
    response = requests.post(
        "https://ai-calendar-agent-1.onrender.com/chat",
        json={"message": user_input}
    )
    if response.status_code == 200:
        try:
            bot_reply = response.json().get("response", "(No response)")
        except ValueError:
            bot_reply = "(Invalid JSON response)"
    else:
        bot_reply = f"(Error: {response.status_code})"
    st.session_state["messages"].append(("bot", bot_reply))

# Display chat history and handle available slots
for sender, msg in st.session_state["messages"]:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        if msg.startswith("Available slots on"):
            st.markdown(f"**Agent:** {msg}")
            # Extract slots and show as buttons
            try:
                slots = msg.split(": ")[1].split(", ")
                for slot in slots:
                    if st.button(f"Book {slot}"):
                        # Find the date from the message
                        date = msg.split(" on ")[1].split(":")[0]
                        book_msg = f"Book a meeting at {slot.split(' - ')[0]} on {date}"
                        st.session_state["messages"].append(("user", book_msg))
                        response = requests.post(
                            "http://localhost:8000/chat",
                            json={"message": book_msg}
                        )
                        bot_reply = response.json().get("response", "(No response)")
                        st.session_state["messages"].append(("bot", bot_reply))
                        st.experimental_rerun()
            except Exception:
                pass
        else:
            st.markdown(f"**Agent:** {msg}") 
