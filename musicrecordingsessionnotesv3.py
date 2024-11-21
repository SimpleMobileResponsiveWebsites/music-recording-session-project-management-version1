import streamlit as st
import pandas as pd
from datetime import datetime

# Session Details (combine Artist, Genre, etc. into a single dictionary)
SESSION_DETAILS = {
    "Artist": "",
    "Genre": "",
    "Session Date": datetime.now(),
    "Studio": "",
    "Engineer": ""
}

# Instruments & Tools
INSTRUMENTS_TOOLS = [
    "Guitar", "Piano", "Drums", "Bass", "Vocals",
    "Mixing Console", "Microphones", "Synthesizer", "DAW (Digital Audio Workstation)"
]

# Page Configuration
st.set_page_config(page_title="Music Recording Session Management", layout="wide")

# Main Page
st.title("Music Recording Session Management")

# Add a new session
st.header("Add a New Session")
with st.form("session_form"):
    session_name = st.text_input("Session Name", "")
    musicians = st.text_input("Musicians (comma-separated)", "")
    equipment = st.multiselect("Equipment/Instruments Used", INSTRUMENTS_TOOLS, [])
    session_status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
    session_date = st.date_input("Session Date", datetime.now())
    bpm = st.number_input("BPM (Beats Per Minute)", min_value=1, step=1)  # Added BPM input
    key = st.text_input("Key (e.g., C Major, A Minor)", "")  # Added Key input
    session_notes = st.text_area("Notes", "")

    submitted = st.form_submit_button("Add Session")

if submitted and session_name:
    new_session = {
        "Session Name": session_name,
        "Musicians": musicians,
        "Equipment": ", ".join(equipment),
        "Status": session_status,
        "Date": session_date,
        "BPM": bpm,  # Added BPM to the new session
        "Key": key,  # Added Key to the new session
        "Notes": session_notes,
    }
    # **Fixed Line (Initialize sessions if not in session_state):**
    st.session_state.sessions = pd.DataFrame(columns=[
        "Session Name", "Musicians", "Equipment", "Status", "Date", "BPM", "Key", "Notes"
    ]) if "sessions" not in st.session_state else st.session_state.sessions
    st.session_state.sessions = pd.concat([st.session_state.sessions, pd.DataFrame([new_session])], ignore_index=True)
    st.success("Session added successfully!")

# Removed the unused sidebar section

# Display Sessions
st.header("Session Overview")

# Filter sessions based on the selected filter (assuming filter functionality remains)
# ... (code for filtering remains the same)

# Notes Section
st.header("Session Notes")
session_notes = st.text_area("Document session ideas, lyrics, or settings here.", "")
if st.button("Save Notes"):
    with open("session_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}]\n{session_notes}\n")
    st.success("Notes saved successfully!")
