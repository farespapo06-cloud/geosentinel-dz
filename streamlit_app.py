import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# إدارة حالة التهديدات
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود", value=True)
    track_hidden = st.toggle("👣 ملاحقة المسارات", value=True)
    
    st.markdown("---")
    
    # زر المسح الشامل (تم إصلاح النصوص هنا)
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك بري", "icon": "truck"},
            {"loc": [37.20, 7.50], "type": "هدف بحري", "icon": "ship"},
            {"loc": [25.10, 9.10], "type": "نشاط مشبوه", "icon": "bullseye"}
        ]
        st.warning("تم رصد أهداف جديدة")

    show_flights = st.toggle("✈️ رادار الطيران", value=True)

# --- الخريطة ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")

# رسم الحدود (البرية والبحرية)
algeria_border = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], 
    [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]
]

folium.PolyLine(algeria_border, color="yellow", weight=4, dash_array='5').add_to(m)

# إضافة التهديدات المكتشفة
for threat in st.session_state.threats:
    folium.Marker(
        location=threat["loc"],
        icon=folium.Icon(color='red', icon=threat['icon'], prefix='fa'),
        popup=threat["type"]
    ).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=500)

# --- رادار الطيران ---
if show_flights:
    st.markdown("---")
    url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(url, height=500)
