import streamlit as st
import pandas as pd
from datetime import datetime

# Session Details
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

# Notes Section (Moved to top)
st.header("Session Notes")
current_notes = st.text_area("Document session ideas, lyrics, or settings here:", "", key="current_notes")

# Add a new session
st.header("Add a New Session")
with st.form("session_form"):
    session_name = st.text_input("Session Name", "")
    track_name = st.text_input("Track Name", "")
    musicians = st.text_input("Musicians (comma-separated)", "")
    equipment = st.multiselect("Equipment/Instruments Used", INSTRUMENTS_TOOLS, [])
    session_status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
    session_date = st.date_input("Session Date", datetime.now())
    bpm = st.number_input("BPM (Beats Per Minute)", min_value=1, step=1)
    key = st.text_input("Key (e.g., C Major, A Minor)", "")
    
    # Add current notes to the form submission
    submitted = st.form_submit_button("Add Session")

if submitted and session_name:
    new_session = {
        "Session Name": session_name,
        "Track Name": track_name,
        "Musicians": musicians,
        "Equipment": ", ".join(equipment),
        "Status": session_status,
        "Date": session_date,
        "BPM": bpm,
        "Key": key,
        "Notes": current_notes,  # Use the notes from the text area
    }
    
    # Initialize sessions if not in session_state
    if "sessions" not in st.session_state:
        st.session_state.sessions = pd.DataFrame(columns=[
            "Session Name", "Track Name", "Musicians", "Equipment", 
            "Status", "Date", "BPM", "Key", "Notes"
        ])
    
    # Add the new session
    st.session_state.sessions = pd.concat([st.session_state.sessions, 
                                         pd.DataFrame([new_session])], 
                                         ignore_index=True)
    
    # Save notes to file with session details
    with open("session_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}] - Session: {session_name} - Track: {track_name}\n")
        f.write(f"{current_notes}\n")
        f.write("-" * 50 + "\n")
    
    st.success("Session and notes added successfully!")
    
    # Clear the notes area after submission
    st.session_state.current_notes = ""

# Display Sessions
st.header("Session Overview")

# Display the DataFrame if there are sessions
if "sessions" in st.session_state and not st.session_state.sessions.empty:
    st.dataframe(st.session_state.sessions)
    
    # Add download button for CSV
    csv = st.session_state.sessions.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Sessions as CSV",
        data=csv,
        file_name="recording_sessions.csv",
        mime="text/csv"
    )
else:
    st.info("No sessions recorded yet. Add a new session above.")
