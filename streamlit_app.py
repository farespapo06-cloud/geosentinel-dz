import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# دالة توليد الأهداف الجوية
def fetch_sat_data():
    targets = []
    for i in range(5):
        targets.append({
            "المعرف": f"SAT-{random.randint(100, 999)}",
            "Lat": round(random.uniform(23.0, 32.0), 4),
            "Lon": round(random.uniform(2.0, 7.0), 4),
            "الحالة": "إشارة فضائية مستقرة"
        })
    return targets

# القائمة الجانبية
with st.sidebar:
    st.header("🛰️ الرصد الفضائي")
    # زر يدوي لمنع الوميض التلقائي المزعج
    if st.button("🔄 تحديث المسح الآن"):
        st.rerun()
    st.divider()
    sat_active = st.toggle("رؤية القمر الصناعي (SATELLITE)", value=True)

st.title("🛡️ GeoSentinel-DZ | Live Feed")

# الربط بالأقمار الصناعية
if sat_active:
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Esri Satellite"
else:
    tiles = "CartoDB dark_matter"
    attr = "CartoDB"

# بناء الخريطة
m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr=attr)

# رسم الحدود الحمراء (كما في تصميمك الأصلي)
folium.PolyLine([[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]], 
                color="red", weight=3).add_to(m)

# الأهداف
data = fetch_sat_data()
for t in data:
    folium.CircleMarker([t["Lat"], t["Lon"]], radius=10, color="cyan", fill=True).add_to(m)
    folium.Marker([t["Lat"], t["Lon"]], icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(m)

# عرض الخريطة بمفتاح ثابت لمنع البياض
st_folium(m, width="100%", height=550, key="final_stable_map")

# الجدول
st.divider()
st.table(pd.DataFrame(data))
