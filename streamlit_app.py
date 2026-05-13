import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="GeoSentinel-DZ | Ultimate", layout="wide")

# إحداثيات التهديد الافتراضية
THREAT_ZONE = {"lat_min": 25.0, "lat_max": 28.0, "lon_min": 3.0, "lon_max": 6.0}

# استخدام Caching متقدم جداً لمنع البياض (صورة 1000046534.jpg)
@st.cache_resource
def load_fixed_map():
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr="Esri Satellite", control_scale=True)
    # إضافة طبقة الحدود بشكل دائم
    folium.Rectangle(bounds=[[19.0, -8.0], [37.0, 12.0]], color="red", fill=False, weight=2).add_to(m)
    return m

if 'radar_history' not in st.session_state:
    st.session_state.radar_history = []

with st.sidebar:
    st.header("🛰️ رادار GeoSentinel")
    if st.button("🛰️ تشغيل المسح الشامل"):
        new_targets = []
        for _ in range(7):
            lat, lon = random.uniform(22.0, 34.0), random.uniform(1.0, 9.0)
            is_threat = THREAT_ZONE["lat_min"] <= lat <= THREAT_ZONE["lat_max"] and THREAT_ZONE["lon_min"] <= lon <= THREAT_ZONE["lon_max"]
            new_targets.append({"lat": lat, "lon": lon, "threat": is_threat})
        st.session_state.radar_history = new_targets
        st.rerun()

# عرض الخريطة مع استخدام مفتاح (Key) ديناميكي مرتبط بالبيانات لمنع التجمد
m = load_fixed_map()

# إضافة الأهداف كطبقة متغيرة فوق الخريطة الثابتة
target_layer = folium.FeatureGroup(name="Targets")
for t in st.session_state.radar_history:
    color = "red" if t["threat"] else "blue"
    icon_type = "warning" if t["threat"] else "info-sign"
    folium.Marker(location=[t["lat"], t["lon"]], 
                  icon=folium.Icon(color=color, icon=icon_type)).add_to(target_layer)

target_layer.add_to(m)

# هذا السطر هو السر في ثبات الخريطة على الجوال
st_folium(m, width="100%", height=550, key="stable_map_v3", returned_objects=[])

# تقرير الرصد (تحسين التنسيق بناءً على صورة 1000046532.jpg)
if st.session_state.radar_history:
    st.markdown("### 📋 سجل الأهداف المكتشفة")
    col1, col2 = st.columns(2)
    for i, t in enumerate(st.session_state.radar_history):
        with (col1 if i % 2 == 0 else col2):
            if t["threat"]:
                st.error(f"🚨 تهديد: {t['lat']:.3f}, {t['lon']:.3f}")
            else:
                st.success(f"✅ آمن: {t['lat']:.3f}, {t['lon']:.3f}")
