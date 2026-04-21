import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Ticket Dashboard", layout="wide")
st.markdown("""
<style>

/* Sidebar (Login background) */
section[data-testid="stSidebar"] {
    background-color: #1f4e79 !important;
}

/* Sidebar labels (Username / Password) */
section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Input boxes (Username & Password) */
section[data-testid="stSidebar"] input {
    background-color: white !important;
    color: black !important;
    border-radius: 6px;
    border: 1px solid #ccc;
}

/* Search + Filters */
div[data-baseweb="input"] > div {
    background-color: #e6f0fa !important;
    border: 1px solid #1f4e79 !important;
    border-radius: 6px;
}

div[data-baseweb="select"] > div {
    background-color: #e6f0fa !important;
    border: 1px solid #1f4e79 !important;
    border-radius: 6px;
}

/* Table header → BLUE */
thead tr th {
    background-color: #1f4e79 !important;
    color: white !important;
    font-weight: bold;
    text-align: left;
}

/* Labels (filters etc.) */
label {
    color: #1f4e79 !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)# ---------------------------
# Simple User Access
# ---------------------------
st.sidebar.title("🔑 Login")
user = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Example credentials (replace with secure method in prod)
credentials = {
    "admin": "admin123",
    "engineer": "eng123",
    "viewer": "view123"
}

if user not in credentials or credentials[user] != password:
    st.warning("🚫 Invalid credentials")
    st.stop()

# ---------------------------
# Header
# ---------------------------
col1, col2 = st.columns([1, 6])
#with col1:
    #st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/Bosch-logo.png", width=120)
with col2:
    st.title("🎫 Shopfloor Ticket Dashboard")

# ---------------------------
# Sample Data (replace with AI-generated tickets)
# ---------------------------
data = [
    {"ticket_id": "T001", "reason": "Machine failure", "priority": "High", "status": "Open", "time": "2026-04-03 10:00"},
    {"ticket_id": "T002", "reason": "Temperature warning", "priority": "Medium", "status": "Reopen", "time": "2026-04-03 10:05"},
    {"ticket_id": "T003", "reason": "Minor vibration", "priority": "Low", "status": "Closed", "time": "2026-04-03 10:10"},
    {"ticket_id": "T004", "reason": "System failure", "priority": "High", "status": "Open", "time": "2026-04-03 10:15"},
]

df = pd.DataFrame(data)

# ---------------------------
# Search + Filters
# ---------------------------
search = st.text_input("🔍 Search Ticket (ID / Reason)")
if search:
    df = df[
        df["ticket_id"].str.contains(search, case=False) |
        df["reason"].str.contains(search, case=False)
    ]

col1, col2 = st.columns(2)
with col1:
    priority_filter = st.selectbox("Filter Priority", ["All", "High", "Medium", "Low"])
with col2:
    status_filter = st.selectbox("Filter Status", ["All", "Open", "Closed", "Reopen"])

if priority_filter != "All":
    df = df[df["priority"] == priority_filter]
if status_filter != "All":
    df = df[df["status"] == status_filter]

# ---------------------------
# Sorting
# ---------------------------
sort_option = st.selectbox("Sort By", ["Time (Latest)", "Priority", "Status"])
if sort_option == "Time (Latest)":
    df = df.sort_values(by="time", ascending=False)
elif sort_option == "Priority":
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    df["priority_rank"] = df["priority"].map(priority_order)
    df = df.sort_values(by="priority_rank")
elif sort_option == "Status":
    df = df.sort_values(by="status")

df = df[["ticket_id", "reason", "priority", "status", "time"]]
df.columns = ["Ticket ID", "Reason", "Priority", "Status", "Time"]

# ---------------------------
# Styling Functions
# ---------------------------
def highlight_priority(val):
    if val == "High":
        return "background-color: red; color: white"
    elif val == "Medium":
        return "background-color: orange"
    elif val == "Low":
        return "background-color: yellow"
    return ""

def highlight_status(val):
    if val == "Open":
        return "background-color: lightgreen"
    elif val == "Reopen":
        return "background-color: lightblue"
    elif val == "Closed":
        return "background-color: lightgray"
    return ""

styled_df = df.style.map(highlight_priority, subset=["Priority"]) \
                    .map(highlight_status, subset=["Status"])

# ---------------------------
# Professional Table Styling
# ---------------------------
def style_table(df):
    return df.style.set_table_styles([

        # Table
        {
            "selector": "table",
            "props": [
                ("border-collapse", "collapse"),
                ("width", "100%"),
                ("background-color", "#ffffff"),
                ("border", "1px solid #e0e0e0"),
                ("border-radius", "8px"),
                ("overflow", "hidden")
            ]
        },

        # Header
        {
            "selector": "th",
            "props": [
                ("background-color", "#f7f9fc"),
                ("color", "#333"),
                ("font-weight", "600"),
                ("text-align", "left"),
                ("padding", "12px"),
                ("border-bottom", "2px solid #e0e0e0")
            ]
        },

        # Cells
        {
            "selector": "td",
            "props": [
                ("padding", "10px"),
                ("border-bottom", "1px solid #f0f0f0"),
                ("color", "#444")
            ]
        },

        # Hover
        {
            "selector": "tr:hover",
            "props": [
                ("background-color", "#f5f7fa")
            ]
        }
    ])

# Apply both styles (your logic + UI)
styled_df = style_table(df) \
    .map(highlight_priority, subset=["Priority"]) \
    .map(highlight_status, subset=["Status"])

# ---------------------------
# Display inside Card
# ---------------------------
st.markdown("""
<div style='
    border:1px solid #e0e0e0;
    border-radius:10px;
    padding:15px;
    background-color:#ffffff;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
'>
""", unsafe_allow_html=True)

st.subheader("📋 Ticket Details")

st.dataframe(styled_df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------
# Charts Side by Side (Fixed + Beautified)
# ---------------------------
st.subheader("📊 Ticket Analytics")

col1, col2 = st.columns(2)

priority_counts = df["Priority"].value_counts()
total = priority_counts.sum()

# Define correct colors (High, Medium, Low)
color_map = {
    "High": "red",
    "Medium": "orange",
    "Low": "yellow"
}

bar_colors = [color_map.get(p, "gray") for p in priority_counts.index]




# ---------------------------
# Bar Chart (Improved)
# ---------------------------
with col1:
    #st.markdown("### 📊 Tickets by Priority")


    fig1, ax1 = plt.subplots(figsize=(5, 4))

    bars = ax1.bar(
        priority_counts.index,
        priority_counts.values,
        color=bar_colors
    )

    # Add percentage labels on top
    for i, v in enumerate(priority_counts.values):
        percent = (v / total) * 100
        ax1.text(i, v + 0.1, f"{percent:.1f}%", ha='center', fontsize=10)

    ax1.set_ylabel("Number of Tickets")
    ax1.set_xlabel("Priority")

    # Clean look
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig1, use_container_width=True)

def convert_to_excel(df):
    return df.to_excel(index=False)

# Create Excel file in memory
import io
output = io.BytesIO()

with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Tickets')

excel_data = output.getvalue()

# Download button
st.download_button(
    label="📥 Download Tickets as Excel",
    data=excel_data,
    file_name="ticket_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


