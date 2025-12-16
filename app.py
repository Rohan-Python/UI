import streamlit as st
import pandas as pd
import folium
from geopy.distance import geodesic
from streamlit_folium import st_folium
import os

st.set_page_config(layout="wide")
st.title("📍 Sales Executive & Project Tracking Dashboard")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.xlsx")

@st.cache_data
def load_data():
    sales = pd.read_excel(DATA_FILE, sheet_name="sales_executives")
    projects = pd.read_excel(DATA_FILE, sheet_name="projects")
    return sales, projects

sales_df, project_df = load_data()


# ---------------------------------------------------
# Distance Calculation
# ---------------------------------------------------
def calculate_nearest_projects(sales, projects):
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

    df = pd.DataFrame(records)
    return df.sort_values("Distance (km)")

distance_df = calculate_nearest_projects(sales_df, project_df)

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("🔍 Filters")
selected_exec = st.sidebar.selectbox(
    "Select Sales Executive",
    ["All"] + list(sales_df.exec_name)
)

if selected_exec != "All":
    distance_df = distance_df[distance_df["Sales Executive"] == selected_exec]

# ---------------------------------------------------
# Map
# ---------------------------------------------------
m = folium.Map(location=[16.0, 78.0], zoom_start=6, tiles="OpenStreetMap")

# Sales Executives Markers
for _, row in sales_df.iterrows():
    folium.Marker(
        [row.latitude, row.longitude],
        popup=f"<b>{row.exec_name}</b><br>{row.city}",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

# Project Sites Markers
for _, row in project_df.iterrows():
    folium.Marker(
        [row.latitude, row.longitude],
        popup=f"""
        <b>{row.project_name}</b><br>
        Contractor: {row.contractor}<br>
        PM: {row.project_manager}<br>
        Contact: {row.contact}
        """,
        icon=folium.Icon(color="red", icon="wrench")
    ).add_to(m)

st.subheader("🗺️ Live Map View")
st_folium(m, width=1200, height=600)

# ---------------------------------------------------
# Nearest Projects Table
# ---------------------------------------------------
st.subheader("📊 Nearest Projects to Sales Executives")

st.dataframe(
    distance_df,
    use_container_width=True
)

# ---------------------------------------------------
# Smart Suggestions
# ---------------------------------------------------
st.subheader("🚀 Visit Suggestions")

suggestions = (
    distance_df
    .groupby("Sales Executive")
    .first()
    .reset_index()
)

st.success("Suggested nearest project for each sales executive:")
st.table(suggestions)

