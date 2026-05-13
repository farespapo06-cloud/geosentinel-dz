import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="GeoSentinel-DZ | Secure", layout="wide")

# 1. إعداد منطقة الحظر (إحداثيات التهديد)
# أي هدف داخل هذا المربع يعتبر تهديداً
THREAT_ZONE = {"lat_min": 25.0, "lat_max": 28.0, "lon_min": 3.0, "lon_max": 6.0}

@st.cache_resource
def get_base_map():
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr="Esri Satellite")
    # رسم الحدود الآمنة باللون الأحمر
    folium.Rectangle(bounds=[[19.0, -8.0], [37.0, 12.0]], color="red", fill=False, weight=2).add_to(m)
    return m

# 2. منطق كشف التهديدات
def check_threat(lat, lon):
    if (THREAT_ZONE["lat_min"] <= lat <= THREAT_ZONE["lat_max"] and 
        THREAT_ZONE["lon_min"] <= lon <= THREAT_ZONE["lon_max"]):
        return "⚠️ تهديد عالي", "red"
    return "آمن", "blue"

# 3. تحديث البيانات
if 'targets' not in st.session_state:
    st.session_state.targets = []

with st.sidebar:
    st.header("🛰️ GeoSentinel-DZ")
    if st.button("🔄 مسح راداري جديد"):
        st.session_state.targets = []
        for _ in range(6):
            lat, lon = random.uniform(22.0, 34.0), random.uniform(1.0, 9.0)
            status, color = check_threat(lat, lon)
            st.session_state.targets.append({"lat": lat, "lon": lon, "status": status, "color": color})
        st.rerun()

# 4. عرض الخريطة بدون وميض
m = get_base_map()
for t in st.session_state.targets:
    folium.Marker(
        location=[t["lat"], t["lon"]],
        icon=folium.Icon(color=t["color"], icon="info-sign")
    ).add_to(m)

st_folium(m, width="100%", height=500, key="secure_map")

# 5. تقرير التهديدات (الجزء الأمني)
if st.session_state.targets:
    st.subheader("📋 تقرير الرصد الفوري")
    for t in st.session_state.targets:
        if t["status"] == "⚠️ تهديد عالي":
            st.error(f"تحذير: تم رصد هدف في الإحداثيات {t['lat']:.4f}, {t['lon']:.4f}")
        else:
            st.success(f"المنطقة {t['lat']:.4f}, {t['lon']:.4f} تحت السيطرة")
