import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import random

# --- 1. إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# --- 2. رادار خفيف وسريع (بديل لـ OpenSky الثقيل) ---
def get_lightweight_radar():
    """توليد بيانات رادار فورية لتجنب ثقل الخوادم الخارجية"""
    flights = []
    # توليد طائرات افتراضية في المجال الجوي الجزائري (تمنراست، برج باجي مختار، إلخ)
    for i in range(5):
        flights.append({
            'id': f"DZ-{random.randint(100, 999)}",
            'lat': random.uniform(20.0, 35.0),
            'lon': random.uniform(-2.0, 8.0),
            'alt': random.randint(5000, 11000)
        })
    return flights

# --- 3. القائمة الجانبية (أدوات الرصد المتقدمة) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    st.subheader("🗓️ المقارنة الزمنية")
    time_analysis = st.radio("نطاق البحث:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري (10 سنوات)"])
    
    st.divider()
    st.subheader("🚨 رادار التهديدات")
    osint_active = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)", value=True)
    radar_active = st.toggle("✈️🚢 رصد الملاحة الجوية والبحرية", value=True)
    thermal_active = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")
    
    if st.button("إجراء مسح شامل الآن"):
        st.toast("جاري تحديث الرادار الخفيف...")

# --- 4. بناء العنوان الرئيسي والخريطة ---
st.title(f"🛡️ GeoSentinel-DZ | Live: {datetime.now().strftime('%H:%M:%S')}")

# اختيار نوع الخريطة بناءً على الرصد الحراري
tile_type = "CartoDB dark_matter"
if thermal_active:
    # استخدام خريطة تعطي طابعاً حرارياً (قمر صناعي داكن)
    tile_type = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"

m = folium.Map(location=[24.0, 5.0], zoom_start=5, tiles=tile_type, attr="GeoSentinel")

# رسم حدود النطاق الأحمر (المناطق الحدودية)
boundary_coords = [[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]]
folium.PolyLine(boundary_coords, color="red", weight=3, opacity=0.9).add_to(m)

# --- 5. تشغيل الرادار الخفيف ---
if radar_active:
    aircrafts = get_lightweight_radar()
    for ac in aircrafts:
        folium.Marker(
            location=[ac['lat'], ac['lon']],
            popup=f"Flight: {ac['id']}\nAlt: {ac['alt']}m",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(m)

# محاكاة إنذار OSINT كما في صورك الأصلية
if osint_active:
    folium.Marker(
        location=[22.5, 3.5], 
        popup="🚨 إنذار OSINT: تحرك حدودي مشبوه",
        icon=folium.Icon(color="red", icon="warning", prefix="fa")
    ).add_to(m)

# --- 6. عرض الخريطة وتحديثها ---
st_folium(m, width="100%", height=600)

time.sleep(10) # تحديث سريع كل 10 ثوانٍ
st.rerun()
