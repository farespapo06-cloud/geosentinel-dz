import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الاحترافية (GeoSentinel-DZ)
st.set_page_config(page_title="GeoSentinel-DZ | Strategic Command", layout="wide")

# 2. تهيئة مخازن البيانات (التراكم اليدوي للأهداف)
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. لوحة التحكم الاستراتيجي (القائمة الجانبية)
with st.sidebar:
    st.title("⚙️ لوحة التحكم الاستراتيجي")
    
    st.subheader("📅 التحليل الزمني")
    period = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT (التواصل الاجتماعي)", value=True)
    air_active = st.toggle("✈️ رصد الملاحة الجوية والبحرية", value=True)
    thermal_active = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")
    
    st.divider()
    
    # أزرار التحكم اليدوية (صور 1000046550.jpg)
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        # محاكاة رصد هدف جديد في منطقة استراتيجية (مثل برج باجي مختار)
        new_target = {
            "id": len(st.session_state.all_detections) + 1,
            "lat": random.uniform(21.5, 23.0), 
            "lon": random.uniform(0.5, 2.0),
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": "Border Activity Detected" if not thermal_active else "Thermal Signature"
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

    if st.button("🗑️ تنظيف سجل الرادار"):
        st.session_state.all_detections = []
        st.rerun()

# 4. واجهة العرض الرئيسية
if air_active:
    st.warning("⚠️ خادم OpenSky لا يستجيب حالياً. جاري العرض بدون بيانات الرادار الحي.")

st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

# 5. بناء الخريطة (Satellite View)
# مركز الخريطة على الجزائر
m = folium.Map(
    location=[28.0, 3.0], 
    zoom_start=5, 
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
    attr="Esri Satellite"
)

# إضافة خط الحدود السيادية (الطبقة الحدودية البيضاء)
algeria_borders = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]
]
folium.PolyLine(algeria_borders, color="white", weight=2, opacity=0.7, dash_array='5, 5').add_to(m)

# تثبيت الأهداف المرصودة على الخريطة (صور 1000046551.jpg)
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["lat"], d["lon"]],
        radius=12,
        color="red",
        fill=True,
        fill_color="yellow",
        popup=f"Target ID: {d['id']}\nTime: {d['time']}\nType: {d['type']}"
    ).add_to(m)

# عرض الخريطة ومنع الوميض الأبيض (Flicker Fix)
st_folium(m, width="100%", height=550, key="strategic_map_v3", returned_objects=[])

# 6. سجل الأهداف الرقمي (الجدول السفلي)
if st.session_state.all_detections:
    st.markdown("### 📋 سجل الأهداف المرصودة (تراكمي)")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['id', 'time', 'lat', 'lon', 'type']], use_container_width=True)
