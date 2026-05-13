import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# --- القائمة الجانبية (Sidebar) بناءً على صورة 1000046572.jpg ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية")
    
    st.markdown("---")
    st.button("🔍 إجراء مسح استخباراتي شامل")
    
    # تفعيل ربط الطيران
    show_flights = st.button("✈️ ربط الطيران (FlightRadar24)")

# --- رسم الخريطة مع الحدود الكاملة ---
center = [28.0339, 1.6596]
m = folium.Map(location=center, zoom_start=5, tiles="Esri World Imagery")

# 1. إضافة حدود الجزائر كاملة (استخدام رابط GeoJSON موثوق)
border_url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries/DZA.geojson"
folium.GeoJson(
    border_url,
    name="الحدود الجزائرية",
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'yellow', # لون الحدود ليكون واضحاً على خلفية القمر الصناعي
        'weight': 3,
        'dashArray': '5, 5'
    }
).add_to(m)

# 2. إضافة نطاق مسح الرادار كما في صورة 1000046570.jpg
if radar_scan:
    # مثال لنطاق مسح في منطقة حدودية
    folium.Circle(
        location=[21.3286, 0.9544], # منطقة برج باجي مختار
        radius=150000,
        color="cyan",
        fill=True,
        fill_opacity=0.3,
        popup="نطاق مسح الرادار النشط"
    ).add_to(m)

# عرض الخريطة
st.subheader("خريطة الرصد العملياتي والحدود الوطنية")
st_folium(m, width="100%", height=500)

# --- قسم FlightRadar24 (إظهار الطائرات) ---
if show_flights:
    st.markdown("---")
    st.subheader("🛰️ مراقبة حركة الطيران (بث مباشر)")
    # دمج خريطة FlightRadar24 الحية للمجال الجوي الجزائري
    # الإحداثيات مضبوطة لتغطي الجزائر
    flight_embed_url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(flight_embed_url, height=600, scrolling=True)
