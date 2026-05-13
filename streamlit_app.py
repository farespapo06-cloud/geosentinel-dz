import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. الإعدادات وتثبيت الحالة
st.set_page_config(page_title="GeoSentinel-DZ | Integrated Hub", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. القائمة الجانبية (القفلات كما في الصورة 1000046565.jpg)
with st.sidebar:
    st.title("⚙️ القيادة المركزية")
    time_node = st.select_slider("تحليل التغيرات منذ 2024:", options=["2024", "2025", "2026"])
    
    st.divider()
    st.subheader("🚨 أنظمة الرصد المتقدمة")
    radar_active = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_active = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)", value=True)
    stealth_active = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.divider()
    if st.button("🔍 إجراء مسح استخباراتي شامل", use_container_width=True):
        threat_catalog = {
            "مطار عسكري حدودي": {"color": "darkred", "img": "https://img.freepik.com/free-photo/military-airbase_181624-1.jpg", "link": "https://www.reuters.com/world/africa/"},
            "خندق دفاعي مستحدث": {"color": "orange", "img": "https://img.freepik.com/free-photo/trench_181624-2.jpg", "link": "https://twitter.com/search?q=Border+News+Africa"},
            "مسار تسلل (خارج الرادار)": {"color": "purple", "img": "https://img.freepik.com/free-photo/secret-path_181624-3.jpg", "link": "https://www.aljazeera.net/"},
            "مركبة كهربائية (رصد حراري)": {"color": "cyan", "img": "https://img.freepik.com/free-photo/thermal-car_181624-4.jpg", "link": "https://www.france24.com/ar/"}
        }
        name, info = random.choice(list(threat_catalog.items()))
        # تثبيت الإحداثيات على الجزائر والحدود حصراً
        target = {
            "ID": f"DZ-{random.randint(1000, 9999)}",
            "النوع": name,
            "LAT": round(random.uniform(22.0, 34.0), 4),
            "LON": round(random.uniform(2.0, 7.0), 4),
            "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": info['color'], "image": info['img'], "news_link": info['link']
        }
        st.session_state.all_detections.append(target)
        st.rerun()

# 3. واجهة العرض (دمج FlightRadar مع الخريطة الميدانية)
st.success(f"✅ جميع الأنظمة مرتبطة | الرصد الحراري والمسارات نشطة | الموقع: الجزائر والحدود")

# تقسيم الشاشة (الخريطة يسار | رادار الطيران يمين)
col_map, col_flight = st.columns([1.8, 1.2])

with col_map:
    st.subheader("🗺️ خريطة الرصد وتغيرات الأرض")
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri")
    
    # الحدود (الخط المقطع)
    algeria_borders = [[37.0, 8.5], [19.0, 5.0], [21.0, -1.0], [37.0, 8.5]]
    folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

    for d in st.session_state.all_detections:
        popup_html = f"""
        <div style="width: 180px; text-align: center;">
            <b style="color:{d['color']};">{d['النوع']}</b><br>
            <img src="{d['image']}" width="100%" style="border-radius:5px; margin:5px 0;">
            <a href="{d['news_link']}" target="_blank">
                <button style="background-color:{d['color']}; color:white; border:none; padding:5px; width:100%; border-radius:5px; cursor:pointer;">المصدر الاستخباري 🔗</button>
            </a>
        </div>
        """
        folium.CircleMarker(location=[d["LAT"], d["LON"]], radius=12, color=d["color"], fill=True, popup=folium.Popup(popup_html)).add_to(m)

    st_folium(m, width="100%", height=550, key="dz_main_map")

with col_flight:
    st.subheader("✈️ رادار الطيران (Flight Live)")
    # دمج الرادار الحي مباشرة
    st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5", height=550)

# 4. سجل العمليات
if st.session_state.all_detections:
    st.divider()
    st.subheader("📋 السجل العملياتي الموحد")
    st.dataframe(pd.DataFrame(st.session_state.all_detections)[['ID', 'النوع', 'LAT', 'LON', 'الوقت']], use_container_width=True)
