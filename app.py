import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# HYNET WATER HYACINTH HARVESTING DASHBOARD
# ==========================================

st.set_page_config(
    page_title="HYNET Robot Dashboard",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #f4f8f5;
    }

    h1 {
        color: #146c43;
    }

    h2, h3 {
        color: #198754;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #cce3d3;
        padding: 15px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# SAMPLE HARVESTING DATA
# ==========================================

data = {
    "Session": [
        "Session 1",
        "Session 2",
        "Session 3",
        "Session 4",
        "Session 5",
        "Session 6"
    ],
    "Date": [
        "2026-10-20",
        "2026-10-21",
        "2026-10-22",
        "2026-10-23",
        "2026-10-24",
        "2026-10-25"
    ],
    "Duration (min)": [30, 45, 35, 50, 40, 55],
    "Battery Start (%)": [100, 95, 90, 85, 80, 75],
    "Battery End (%)": [85, 78, 73, 65, 66, 58],
    "Hyacinth Collected (kg)": [12, 18, 15, 24, 20, 28],
    "Area Covered (m²)": [100, 150, 120, 190, 160, 220]
}

df = pd.DataFrame(data)


# ==========================================
# PERFORMANCE CALCULATIONS
# ==========================================

df["Battery Used (%)"] = (
    df["Battery Start (%)"] - df["Battery End (%)"]
)

df["Harvesting Rate (kg/hr)"] = (
    df["Hyacinth Collected (kg)"]
    / df["Duration (min)"] * 60
).round(2)

df["Area Rate (m²/hr)"] = (
    df["Area Covered (m²)"]
    / df["Duration (min)"] * 60
).round(2)


# ==========================================
# SIDEBAR CONTROLS
# ==========================================

st.sidebar.title("🌿 HYNET CONTROLS")

st.sidebar.write("Water Hyacinth Harvesting Robot")

st.sidebar.markdown("---")

device_status = st.sidebar.selectbox(
    "Robot Status",
    ["Active", "Idle", "Offline"]
)

battery_level = st.sidebar.slider(
    "Current Battery Level (%)",
    min_value=0,
    max_value=100,
    value=58
)

selected_session = st.sidebar.selectbox(
    "Select Harvesting Session",
    df["Session"].tolist()
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Demonstration mode: the dashboard uses sample data. "
    "The physical robot is not connected."
)


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🌿 HYNET Water Hyacinth Harvesting Robot")

st.subheader("Smart Monitoring and Performance Analytics")

st.write(
    "A centralized monitoring system for tracking robot status, "
    "battery consumption, harvesting activity, and session performance."
)

st.caption(
    "Dashboard time: "
    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

st.markdown("---")


# ==========================================
# DEVICE STATUS MONITORING
# ==========================================

st.header("🤖 Device Monitoring")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Robot Status",
    device_status
)

col2.metric(
    "Battery Level",
    f"{battery_level}%"
)

col3.metric(
    "Total Harvested",
    f"{df['Hyacinth Collected (kg)'].sum()} kg"
)

col4.metric(
    "Total Sessions",
    len(df)
)

if device_status == "Active":
    st.success("Robot is active and ready for harvesting.")

elif device_status == "Idle":
    st.warning("Robot is idle. Harvesting is currently paused.")

else:
    st.error("Robot is offline. Check its power and connection.")

if battery_level <= 20:
    st.error("LOW BATTERY! Recharge the robot.")

elif battery_level <= 40:
    st.warning("Battery is getting low. Plan recharging.")

else:
    st.success("Battery level is satisfactory.")

st.progress(battery_level / 100)

st.markdown("---")


# ==========================================
# OVERALL PERFORMANCE SUMMARY
# ==========================================

st.header("📊 Overall Harvesting Performance")

total_harvested = df["Hyacinth Collected (kg)"].sum()

total_duration = df["Duration (min)"].sum()

total_area = df["Area Covered (m²)"].sum()

average_rate = total_harvested / total_duration * 60

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Hyacinth Collected",
    f"{total_harvested} kg"
)

col2.metric(
    "Operating Time",
    f"{total_duration} minutes"
)

col3.metric(
    "Area Covered",
    f"{total_area} m²"
)

col4.metric(
    "Average Harvesting Rate",
    f"{average_rate:.2f} kg/hr"
)

st.markdown("---")


# ==========================================
# BATTERY CONSUMPTION ANALYSIS
# ==========================================

st.header("🔋 Battery Consumption Analysis")

fig_battery = px.bar(
    df,
    x="Session",
    y="Battery Used (%)",
    text="Battery Used (%)",
    color="Battery Used (%)",
    color_continuous_scale="Greens",
    title="Battery Consumption per Session",
    hover_data=[
        "Battery Start (%)",
        "Battery End (%)",
        "Duration (min)"
    ]
)

fig_battery.update_layout(
    xaxis_title="Operating Session",
    yaxis_title="Battery Consumed (%)",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig_battery,
    use_container_width=True
)


# ==========================================
# HARVESTING ACTIVITY
# ==========================================

st.header("🌱 Water Hyacinth Harvesting Activity")

fig_harvest = px.bar(
    df,
    x="Session",
    y="Hyacinth Collected (kg)",
    text="Hyacinth Collected (kg)",
    color="Hyacinth Collected (kg)",
    color_continuous_scale="Teal",
    title="Water Hyacinth Collected per Session"
)

fig_harvest.update_layout(
    xaxis_title="Operating Session",
    yaxis_title="Hyacinth Collected (kg)",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig_harvest,
    use_container_width=True
)


# ==========================================
# SESSION-WISE HARVESTING EFFICIENCY
# ==========================================

st.header("📈 Session-wise Harvesting Efficiency")

fig_rate = px.line(
    df,
    x="Session",
    y="Harvesting Rate (kg/hr)",
    markers=True,
    text="Harvesting Rate (kg/hr)",
    title="Harvesting Rate Across Sessions"
)

fig_rate.update_layout(
    xaxis_title="Operating Session",
    yaxis_title="Harvesting Rate (kg/hr)",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig_rate,
    use_container_width=True
)


# ==========================================
# AREA COVERAGE ANALYSIS
# ==========================================

st.header("🗺️ Area Coverage Analysis")

fig_area = px.bar(
    df,
    x="Session",
    y="Area Covered (m²)",
    text="Area Covered (m²)",
    color="Area Covered (m²)",
    color_continuous_scale="Greens",
    title="Area Covered During Each Session"
)

fig_area.update_layout(
    xaxis_title="Operating Session",
    yaxis_title="Area Covered (m²)",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig_area,
    use_container_width=True
)


# ==========================================
# INDIVIDUAL SESSION DETAILS
# ==========================================

st.header("🔎 Individual Session Details")

session_data = df[
    df["Session"] == selected_session
].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Hyacinth Collected",
    f"{session_data['Hyacinth Collected (kg)']} kg"
)

col2.metric(
    "Session Duration",
    f"{session_data['Duration (min)']} minutes"
)

col3.metric(
    "Battery Consumed",
    f"{session_data['Battery Used (%)']}%"
)

st.write(f"**Session:** {session_data['Session']}")

st.write(f"**Date:** {session_data['Date']}")

st.write(
    f"**Area Covered:** {session_data['Area Covered (m²)']} m²"
)

st.write(
    f"**Harvesting Rate:** "
    f"{session_data['Harvesting Rate (kg/hr)']} kg/hr"
)

st.write(
    f"**Area Coverage Rate:** "
    f"{session_data['Area Rate (m²/hr)']} m²/hr"
)

st.write(
    f"**Battery Remaining at Session End:** "
    f"{session_data['Battery End (%)']}%"
)

st.markdown("---")


# ==========================================
# COMPLETE SESSION HISTORY
# ==========================================

st.header("📋 Complete Session History")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# DOWNLOAD CSV REPORT
# ==========================================

st.header("📥 Download Performance Report")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Session Report (CSV)",
    data=csv_data,
    file_name="hynet_harvesting_report.csv",
    mime="text/csv"
)


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">
        <h3>🌿 HYNET Smart Aquatic Weed Management</h3>
        <p>Monitoring and analytics for efficient water hyacinth harvesting.</p>
        <p>Built with Python, Streamlit, Pandas and Plotly.</p>
        <p>Prototype dashboard using sample operational data.</p>
    </div>
    """,
    unsafe_allow_html=True
)