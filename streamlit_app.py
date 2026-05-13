import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات المنصة السيادية
st.set_page_config(page_title="GeoSentinel-DZ | Ultimate Hub", layout="wide")

if 'field_detections' not in st.session_state:
    st.session_state.field_detections = []

# 2. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ مركز العمليات الموحد")
    
    # القفلة الزمنية (تغيرات المنطقة)
    st.subheader("⏳ تحليل التغيرات (منذ 2024)")
    time_node = st.select_slider("الإطار الزمني المختار:", options=["2024", "2025", "2026"])
    
    st.divider()
    
    # قفلات أنظمة الرصد
    st.subheader("🚨 أنظمة الرصد النشطة")
    radar_active = st.toggle("🛰️ تفعيل المسح الراداري", value=True)
    marine_active = st.toggle("🚢 رصد النشاط البحري", value=True)
    
    # زر رصد التغيرات الميدانية (حفر، مطار، خندق، ثكنة)
    if st.button("🛰️ مسح التغيرات الميدانية", use_container_width=True):
        terrains = {
            "مطار عسكري مستحدث": {"color": "red", "img": "https://img.freepik.com/free-photo/aerial-view-airport_181624-2345.jpg"},
            "خندق دفاعي / سواتر": {"color": "orange", "img": "https://img.freepik.com/free-photo/trench-warfare-desert_181624-789.jpg"},
            "ثكنة / قاعدة عمليات": {"color": "darkred", "img": "https://img.freepik.com/free-photo/military-base-aerial_181624-1122.jpg"},
            "حفر / أشغال هندسية": {"color": "yellow", "img": "https://img.freepik.com/free-photo/excavation-site-desert_181624-556.jpg"}
        }
        name, info = random.choice(list(terrains.items()))
        target = {
            "ID": f"TR-{random.randint(100, 999)}",
            "التغيير": name,
            "LAT": round(random.uniform(22.0, 32.0), 4),
            "LON": round(random.uniform(1.0, 6.0), 4),
            "الوقت": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "color": info['color'],
            "image": info['img']
        }
        st.session_state.field_detections.append(target)
        st.rerun()

    st.divider()
    if st.button("🗑️ مسح سجلات الرصد"):
        st.session_state.field_detections = []
        st.rerun()

# 3. واجهة العرض الرئيسية (Main Interface)
st.success(f"✅ رصد التغيرات نشط | رادار الطيران (Flight) متصل | رادار السفن (Marine) متصل")

# تقسيم الشاشة: خريطة الميدان (يسار) | الرادارات الحية (يمين)
col_main, col_live = st.columns([2, 1])

with col_main:
    st.subheader("🗺️ خريطة الرصد وتغيرات الأرض")
    # الخريطة بنمط الدوائر الرادارية كما في 1000046563.jpg
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite"
    )

    # الحدود السيادية
    algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

    # عرض التغيرات كدوائر رادارية (رؤية التهديد بالصور عند الضغط)
    for d in st.session_state.field_detections:
        popup_html = f"""
        <div style="width: 180px; text-align: center; font-family: Arial;">
            <b style="color:{d['color']}; font-size: 14px;">{d['التغيير']}</b><br>
            <img src="{d['image']}" width="100%" style="border-radius: 8px; margin: 5px 0;">
            <p style="font-size: 11px; margin:0;"><b>ID:</b> {d['ID']} | {d['الوقت']}</p>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]],
            radius=15, color=d["color"], weight=3,
            fill=True, fill_color=d["color"], fill_opacity=0.4,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width="100%", height=600, key="radar_vFinal_Sovereign")

with col_live:
    # رادار الطيران الحي (FlightRadar)
    st.subheader("✈️ رادار الطيران")
    flight_url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5"
    st.components.v1.iframe(flight_url, height=300)
    
    st.divider()
    
    # رادار السفن الحي (Marine Traffic)
    st.subheader("🚢 رادار الملاحة البحرية")
    marine_url = "https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:37.0/centerx:4.0/maptype:4/shownames:false/mmsi:0/shipid:0/fleet:/fleet_id:/vessel:0/container:true/show_menu:false"
    st.components.v1.iframe(marine_url, height=300)

# 4. جدول البيانات التفصيلي
if st.session_state.field_detections:
    st.markdown("---")
    st.subheader("📋 سجل تحليل التغيرات الميدانية")
    df = pd.DataFrame(st.session_state.field_detections)
    st.dataframe(df[['ID', 'التغيير', 'LAT', 'LON', 'الوقت']], use_container_width=True)
