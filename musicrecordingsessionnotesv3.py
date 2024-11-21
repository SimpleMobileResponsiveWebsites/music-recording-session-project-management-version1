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

# Sidebar
st.sidebar.title("Recording Session Management")

# Session Details section
st.sidebar.subheader("Session Details")
for detail, value in SESSION_DETAILS.items():
    SESSION_DETAILS[detail] = st.sidebar.text_input(detail, value)

# Session Status Filter
session_filter = st.sidebar.selectbox("Session Status Filter", [
    "All", "Planned", "In Progress", "Completed"
])

st.sidebar.write("---")
st.sidebar.header("Quick Actions")
reset_data = st.sidebar.button("Reset Data")

# State Initialization
if "sessions" not in st.session_state or reset_data:
    st.session_state.sessions = pd.DataFrame(columns=[
        "Session Name", "Musicians", "Equipment", "Status", "Date", "Notes"
    ])

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
    session_notes = st.text_area("Notes", "")
    submitted = st.form_submit_button("Add Session")

if submitted and session_name:
    new_session = {
        "Session Name": session_name,
        "Musicians": musicians,
        "Equipment": ", ".join(equipment),
        "Status": session_status,
        "Date": session_date,
        "Notes": session_notes,
    }
    st.session_state.sessions = pd.concat([st.session_state.sessions, pd.DataFrame([new_session])], ignore_index=True)
    st.success("Session added successfully!")

# Display Sessions
st.header("Session Overview")

# Filter sessions based on the selected filter
filtered_sessions = st.session_state.sessions[st.session_state.sessions["Status"].str.contains(session_filter, case=False, na=False)]

if not filtered_sessions.empty:
    st.dataframe(filtered_sessions, use_container_width=True)
else:
    st.write(f"No sessions available for the filter: {session_filter}.")

# Notes Section
st.header("Session Notes")
session_notes = st.text_area("Document session ideas, lyrics, or settings here.", "")
if st.button("Save Notes"):
    with open("session_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}]\n{session_notes}\n")
    st.success("Notes saved successfully!")
