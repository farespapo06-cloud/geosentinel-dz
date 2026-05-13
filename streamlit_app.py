import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# 2. وظيفة ذكية لتوليد الأهداف (Cache لمنع الوميض)
def get_radar_data():
    targets = []
    for i in range(6):
        targets.append({
            "المعرف": f"SAT-{random.randint(100, 999)}",
            "Lat": round(random.uniform(22.0, 34.0), 4),
            "Lon": round(random.uniform(1.0, 8.0), 4),
            "الحالة": "رصد فضائي نشط"
        })
    return targets

# 3. القائمة الجانبية
with st.sidebar:
    st.header("🛰️ مركز العمليات")
    # التحديث اليدوي هو الضمان الوحيد لعدم الوميض على الجوال
    if st.button("🔄 تحديث المسح الجوي"):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    sat_mode = st.toggle("رؤية القمر الصناعي", value=True)

st.title("🛡️ GeoSentinel-DZ | Satellite Feed")

# 4. بناء الخريطة الفضائية (ثابتة)
@st.cache_resource
def create_static_map(is_sat):
    if is_sat:
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        attr = "Esri Satellite"
    else:
        tiles = "CartoDB dark_matter"
        attr = "CartoDB"
    
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr=attr)
    # رسم الحدود الحمراء مرة واحدة فقط
    folium.PolyLine([[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]], 
                    color="red", weight=4).add_to(m)
    return m

# استدعاء الخريطة المحفوظة
base_map = create_static_map(sat_mode)

# 5. إضافة الأهداف الجوية فوق الخريطة الثابتة
data = get_radar_data()
for t in data:
    folium.CircleMarker([t["Lat"], t["Lon"]], radius=10, color="cyan", fill=True).add_to(base_map)
    folium.Marker([t["Lat"], t["Lon"]], icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(base_map)

# عرض الخريطة بمفتاح ثابت لمنع البياض المتكرر
st_folium(base_map, width="100%", height=550, key="fixed_geo_sentinel")

# 6. الجدول السفلي
st.divider()
st.table(pd.DataFrame(data))
