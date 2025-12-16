import streamlit as st
import pandas as pd
import folium
from geopy.distance import geodesic
from streamlit_folium import st_folium
import os

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("📍 Sales Executive & Project Tracking Dashboard")

# ---------------------------------------------------
# Load data safely (Streamlit Cloud compatible)
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.xlsx")

@st.cache_data
def load_data():
    sales = pd.read_excel(DATA_FILE, sheet_name="sales_executives")
    projects = pd.read_excel(DATA_FILE, sheet_name="projects")
    return sales, projects

sales_df, project_df = load_data()

# ---------------------------------------------------
# Helper: Nearest project for a sales executive
# ---------------------------------------------------
def get_nearest_project_for_exec(exec_row, projects_df):
    min_distance = float("inf")
    nearest_project = None

    for _, proj in projects_df.iterrows():
        dist = geodesic(
            (exec_row.latitude, exec_row.longitude),
            (proj.latitude, proj.longitude)
        ).km

        if dist < min_distance:
            min_distance = dist
            nearest_project = proj

    return nearest_project, round(min_distance, 2)

# ---------------------------------------------------
# Distance table (for analytics)
# ---------------------------------------------------
def calculate_all_distances(sales, projects):
    records = []
    for _, s in sales.iterrows():
        for _, p in projects.iterrows():
            dist = geodesic(
                (s.latitude, s.longitude),
                (p.latitude, p.longitude)
            ).km

            records.append({
                "Sales Executive": s.exec_name,
                "Sales City": s.city,
                "Project Name": p.project_name,
                "Contractor": p.contractor,
                "Project Manager": p.project_manager,
                "Contact": p.contact,
                "Distance (km)": round(dist, 2)
            })
    return pd.DataFrame(records)

distance_df = calculate_all_distances(sales_df, project_df)

# ---------------------------------------------------
# Sidebar filter
# ---------------------------------------------------
st.sidebar.header("🔍 Filters")
selected_exec = st.sidebar.selectbox(
    "Select Sales Executive",
    ["All"] + list(sales_df.exec_name)
)

# ---------------------------------------------------
# Map (India Only)
# ---------------------------------------------------
st.subheader("🗺️ Map View (India Only)")

INDIA_BOUNDS = [[6.5, 68.0], [37.5, 97.5]]

m = folium.Map(
    location=[22.0, 78.0],   # Center of India
    zoom_start=5,
    tiles="OpenStreetMap",
    min_zoom=4,
    max_bounds=True
)

m.fit_bounds(INDIA_BOUNDS)
m.options['maxBounds'] = INDIA_BOUNDS

# ---------------------------------------------------
# Sales Executives Markers (Hover shows nearest site)
# ---------------------------------------------------
for _, row in sales_df.iterrows():

    if selected_exec != "All" and row.exec_name != selected_exec:
        continue

    nearest_project, distance_km = get_nearest_project_for_exec(row, project_df)

    tooltip_text = f"""
    <b>{row.exec_name}</b><br>
    City: {row.city}<br><br>
    <b>Nearest Project:</b><br>
    {nearest_project.project_name}<br>
    Contractor: {nearest_project.contractor}<br>
    PM: {nearest_project.project_manager}<br>
    Distance: {distance_km} km
    """

    folium.Marker(
        [row.latitude, row.longitude],
        tooltip=tooltip_text,
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

# ---------------------------------------------------
# Project Site Markers
# ---------------------------------------------------
for _, row in project_df.iterrows():
    folium.Marker(
        [row.latitude, row.longitude],
        popup=f"""
        <b>{row.project_name}</b><br>
        Contractor: {row.contractor}<br>
        Project Manager: {row.project_manager}<br>
        Contact: {row.contact}
        """,
        icon=folium.Icon(color="red", icon="wrench")
    ).add_to(m)

st_folium(m, width=1200, height=600)

# ---------------------------------------------------
# Nearest Projects Table
# ---------------------------------------------------
st.subheader("📊 Distance Between Sales Executives & Projects")

if selected_exec != "All":
    distance_df = distance_df[distance_df["Sales Executive"] == selected_exec]

st.dataframe(distance_df.sort_values("Distance (km)"), use_container_width=True)

# ---------------------------------------------------
# Smart Visit Suggestions
# ---------------------------------------------------
st.subheader("🚀 Recommended Visits")

suggestions = (
    distance_df.sort_values("Distance (km)")
    .groupby("Sales Executive")
    .first()
    .reset_index()
)

st.success("Closest project for each sales executive:")
st.table(suggestions)
