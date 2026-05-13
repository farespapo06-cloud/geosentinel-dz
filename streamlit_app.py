import streamlit as st
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

st.set_page_config(page_title="GeoSentinel-DZ | Intelligence", layout="wide")

# 1. تهيئة مخزن البيانات الدائم للجلسة (لمنع الحذف التلقائي)
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# منطقة التهديد (Bordj Badji Mokhtar كمثال)
THREAT_ZONE = {"lat_min": 21.0, "lat_max": 25.0, "lon_min": 0.0, "lon_max": 5.0}

@st.cache_resource
def get_base_map():
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    return folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr="Esri Satellite")

# 2. القائمة الجانبية (أدوات الرصد المتقدمة - كما في صورة 1000046454_3.jpg)
with st.sidebar:
    st.title("🛡️ أدوات الرصد المتقدمة")
    st.info(f"إجمالي الأهداف المرصودة: {len(st.session_state.all_detections)}")
    
    if st.button("🛰️ إجراء مسح شامل الآن"):
        # إضافة أهداف جديدة فوق القديمة
        for _ in range(3):
            lat = random.uniform(20.0, 35.0)
            lon = random.uniform(-2.0, 10.0)
            is_threat = THREAT_ZONE["lat_min"] <= lat <= THREAT_ZONE["lat_max"] and THREAT_ZONE["lon_min"] <= lon <= THREAT_ZONE["lon_max"]
            
            new_entry = {
                "id": len(st.session_state.all_detections) + 1,
                "lat": lat, "lon": lon,
                "time": datetime.now().strftime("%H:%M:%S"),
                "type": "⚠️ تهديد حدودي" if is_threat else "✅ نشاط عادي",
                "color": "red" if is_threat else "blue"
            }
            st.session_state.all_detections.append(new_entry)
        st.rerun()

    if st.button("🗑️ مسح سجل البيانات بالكامل"):
        st.session_state.all_detections = []
        st.rerun()

# 3. عرض الخريطة التراكمية
m = get_base_map()
for d in st.session_state.all_detections:
    folium.Marker(
        location=[d["lat"], d["lon"]],
        popup=f"ID: {d['id']} | {d['type']}",
        icon=folium.Icon(color=d["color"], icon="bolt" if d["color"]=="red" else "info-sign")
    ).add_to(m)

# رسم منطقة التهديد بشكل دائم (صورة 1000046453_3.jpg)
folium.Rectangle(bounds=[[21.0, 0.0], [25.0, 5.0]], color="yellow", fill=True, opacity=0.1).add_to(m)

st_folium(m, width="100%", height=500, key="pro_radar_map")

# 4. سجل الأهداف المكتشفة (تنسيق الصور 1000046536.jpg)
st.subheader("📋 سجل العمليات التاريخي")
if st.session_state.all_detections:
    # عرض الأحدث أولاً
    for det in reversed(st.session_state.all_detections):
        with st.expander(f"الهدف #{det['id']} - {det['time']} - {det['type']}"):
            col1, col2 = st.columns(2)
            col1.metric("خط العرض", f"{det['lat']:.4f}")
            col2.metric("خط الطول", f"{det['lon']:.4f}")
