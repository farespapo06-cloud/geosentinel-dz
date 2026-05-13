import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# --- 2. محرك بيانات الرادار الجوي ---
def get_satellite_radar():
    targets = []
    for i in range(6):
        targets.append({
            "الهدف": f"TGT-{random.randint(100, 999)}",
            "Lat": round(random.uniform(22.0, 32.0), 4),
            "Lon": round(random.uniform(2.0, 7.0), 4),
            "الارتفاع": f"{random.randint(200, 400)} FL",
            "المصدر": "Satellite-Link"
        })
    return targets

# --- 3. لوحة التحكم الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🛰️ نظام الربط الفضائي")
    # إضافة زر التحديث اليدوي لمنع الوميض التلقائي
    refresh = st.button("🔄 تحديث المسح الجوي")
    st.divider()
    radar_on = st.toggle("تفعيل الرادار", value=True)
    sat_view = st.toggle("رؤية القمر الصناعي (SATELLITE)", value=True)
    st.info("نظام مستقر: تم إيقاف التحديث التلقائي لمنع الوميض.")

# --- 4. العرض الرئيسي (Main Interface) ---
st.title(f"🛡️ GeoSentinel-DZ | Live Feed")

# اختيار نوع الخريطة (ربط الأقمار الصناعية)
if sat_view:
    map_type = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Esri Satellite"
else:
    map_type = "CartoDB dark_matter"
    attr = "CartoDB"

m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=map_type, attr=attr)

# رسم الحدود الاستراتيجية (الخطوط الحمراء)
folium.PolyLine([[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]], 
                color="red", weight=3, opacity=0.8).add_to(m)

# جلب البيانات
data = get_satellite_radar()

if radar_on:
    for t in data:
        # إضافة مؤشرات الأهداف على الخريطة
        folium.CircleMarker([t["Lat"], t["Lon"]], radius=12, color="cyan", pulse_color="white", fill=True).add_to(m)
        folium.Marker([t["Lat"], t["Lon"]], 
                      icon=folium.Icon(color="blue", icon="signal", prefix="fa"),
                      popup=f"Target: {t['الهدف']}").add_to(m)

# عرض الخريطة (استخدام مفتاح ثابت لمنع بياض الشاشة)
st_folium(m, width="100%", height=550, key="stable_sat_map")

# --- 5. جدول البيانات (أسفل الخريطة) ---
st.divider()
st.subheader("📋 سجل البيانات الفضائية")
st.table(pd.DataFrame(data))
