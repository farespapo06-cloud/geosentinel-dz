import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# --- إدارة الحالة (Session State) للتهديدات ---
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.markdown("---")
    
    # وظيفة المسح الشامل لإظهار التهديدات
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        # توليد نقاط تهديد عشوائية على الحدود عند النقر
        st.session_state.threats = [
            {"loc": [21.3, 0.9], "type": "تحرك مشبوه"},
            {"loc": [25.0, 9.0], "type": "اختراق حدودي"},
            {"loc": [37.5, 4.0], "type": "هدف بحري مجهول"}
        ]
        st.success("تم تحديد أهداف محتملة")

    show_flights = st.toggle("✈️ تفعيل رادار الطيران (FlightRadar24)", value=True)

# --- إعداد الخريطة والحدود ---
center = [28.0339, 1.6596]
m = folium.Map(location=center, zoom_start=5, tiles="Esri World Imagery")

# رسم كامل الحدود (البرية والبحرية)
full_border = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], 
    [36.0, -2.1], [37.5, 1.0], [38.0, 4.0], [37.2, 8.6] # إغلاق الحدود البحرية
]

folium.PolyLine(
    full_border,
    color="yellow",
    weight=4,
    dash_array='5',
    tooltip="الحدود الوطنية الكاملة"
).add_to(m)

# إظهار التهديدات الناتجة عن المسح الشامل
for threat in st.session_state.threats:
    folium.Marker(
        location=threat["loc"],
        icon=folium.Icon(color='red', icon='bolt', prefix='fa'),
        popup=f"تنبيه: {threat['type']}"
    ).add_to(m)

# عرض الخريطة
st.subheader("خريطة الرصد العملياتي الشامل")
st_folium(m, width="100%", height=550)

# --- قسم FlightRadar24 ---
if show_flights:
    st.markdown("---")
    flight_url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(flight_url, height=500)
