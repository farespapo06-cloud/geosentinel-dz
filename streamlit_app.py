import streamlit as st
import folium
from streamlit_folium import st_folium

# Page Setup
st.set_page_config(page_title="GeoSentinel-DZ Intelligence", layout="wide")

st.title("🛰️ GeoSentinel-DZ Intelligence")
st.sidebar.title("Control Panel")

# 1. Satellite vs Standard Toggle
map_mode = st.sidebar.selectbox("Vision Mode", ["Satellite", "Standard Map"])

# 2. Intelligence News Feed (Simulated for Now)
st.sidebar.markdown("---")
st.sidebar.subheader("🗞️ Global News Radar")
st.sidebar.warning("Live Alerts: Algeria Borders")
st.sidebar.write("- **Reuters:** Security monitoring increased in the Sahel region.")
st.sidebar.write("- **AP:** Analysis of regional logistics movements.")

# Center the map on Algeria
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5)

# 3. Enable Google Satellite View
if map_mode == "Satellite":
    google_sat = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    folium.TileLayer(
        tiles=google_sat,
        attr='Google Satellite',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)

# 4. Strategic Monitoring Points
points = [
    {"name": "West: Maghnia", "coords": [34.845, -1.728]},
    {"name": "South-West: Tindouf", "coords": [27.671, -8.147]},
    {"name": "South: Bordj Badji Mokhtar", "coords": [21.328, 0.924]},
    {"name": "South-East: In Guezzam", "coords": [19.572, 5.769]},
    {"name": "East: Debdeb", "coords": [30.151, 9.458]}
]

for p in points:
    folium.Marker(
        location=p["coords"], 
        popup=p["name"], 
        icon=folium.Icon(color='red', icon='eye-open')
    ).add_to(m)

# Display Map
st_folium(m, width="100%", height=600)

st.info("Chronological Earth Analysis (2020-2026) is pending Google Earth Engine API integration.")
