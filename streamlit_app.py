import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية")
    
    st.markdown("---")
    # زر الطيران
    show_flights = st.toggle("✈️ تفعيل رادار الطيران (FlightRadar24)")

# --- حل مشكلة الحدود (تجنب الخطأ في 1000046573.jpg) ---
center = [28.0339, 1.6596]
m = folium.Map(location=center, zoom_start=5, tiles="Esri World Imagery")

# استخدام إحداثيات تقريبية ثابتة للحدود لتجنب مشاكل التحميل
algeria_border_points = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]
]

folium.PolyLine(
    algeria_border_points,
    color="yellow",
    weight=3,
    dash_array='10',
    tooltip="الحدود الوطنية"
).add_to(m)

# إظهار الرادار إذا كان مفعل
if radar_scan:
    folium.Circle(
        location=[21.32, 0.95],
        radius=180000,
        color="cyan",
        fill=True,
        fill_opacity=0.3,
        popup="نطاق مسح نشط"
    ).add_to(m)

# عرض الخريطة
st.subheader("خريطة الرصد العملياتي")
st_folium(m, width="100%", height=500)

# --- قسم الطيران (الربط المباشر) ---
if show_flights:
    st.markdown("---")
    st.subheader("✈️ مراقبة دخول الطائرات (بث مباشر)")
    # استخدام تضمين مباشر لرادار الطيران فوق الجزائر
    # هذا الرابط يعرض الطائرات التي تطير حالياً فوق المنطقة
    flight_url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(flight_url, height=600)
