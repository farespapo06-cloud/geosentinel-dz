import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. الإعدادات وتصميم الواجهة
st.set_page_config(page_title="GeoSentinel-DZ | Ultimate Command", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. روابط الاستخبارات والأقمار الصناعية
with st.sidebar:
    st.title("⚙️ غرفة العمليات")
    
    st.subheader("🌐 روابط الأقمار والاستخبارات")
    cols = st.columns(2)
    with cols[0]:
        st.markdown("[🌍 Google Earth](https://earth.google.com/web/)")
        st.markdown("[📡 Sentinel Hub](https://apps.sentinel-hub.com/)")
    with cols[1]:
        st.markdown("[✈️ FlightRadar](https://www.flightradar24.com/)")
        st.markdown("[🚢 MarineTraffic](https://www.marinetraffic.com/)")

    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    radar_mode = st.toggle("🛰️ تفعيل الرادار الشامل", value=True)
    
    # ميزة توليد أهداف متنوعة (بري، بحري، جوي) مع صور
    if st.button("🔍 إجراء مسح ميداني شامل", use_container_width=True):
        categories = {
            "عربة مشبوهة": {"icon": "🚚", "color": "red", "img": "https://img.freepik.com/free-photo/military-truck-desert_181624-1234.jpg"},
            "دورية حدودية": {"icon": "🛡️", "color": "blue", "img": "https://img.freepik.com/free-photo/soldier-guarding-border_181624-5678.jpg"},
            "طائرة مجهولة": {"icon": "✈️", "color": "orange", "img": "https://img.freepik.com/free-photo/fighter-jet-sky_181624-91011.jpg"},
            "باخرة رصد": {"icon": "🚢", "color": "darkblue", "img": "https://img.freepik.com/free-photo/cargo-ship-sea_181624-1121.jpg"}
        }
        name, data = random.choice(list(categories.items()))
        
        # توزيع جغرافي (بري في الجنوب، بحري في الشمال)
        is_sea = name == "باخرة رصد"
        lat = random.uniform(37.0, 38.5) if is_sea else random.uniform(21.0, 26.0)
        lon = random.uniform(2.0, 6.0) if is_sea else random.uniform(0.0, 5.0)

        target = {
            "ID": f"DZ-{random.randint(1000, 9999)}",
            "النوع": f"{data['icon']} {name}",
            "LAT": round(lat, 4), "LON": round(lon, 4),
            "الوقت": datetime.now().strftime("%H:%M:%S"),
            "اللون": data['color'],
            "الصورة": data['img']
        }
        st.session_state.all_detections.append(target)
        st.rerun()

# 3. عرض الحالة والخرائط
st.success("✅ النظام متصل - الرصد المحلي نشط ومستجيب.")
st.subheader("🗺️ خريطة الرصد العملياتي الموحد (2026)")

m = folium.Map(
    location=[28.0, 3.0], zoom_start=5,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri Satellite"
)

# رسم الحدود السيادية (كما في 1000046560.jpg)
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

# عرض الأهداف مع الصور في الـ Popup
for d in st.session_state.all_detections:
    html = f"""
    <div style="width:150px">
        <img src="{d['الصورة']}" width="100%" style="border-radius:5px"><br>
        <b>النوع:</b> {d['النوع']}<br>
        <b>المعرف:</b> {d['ID']}<br>
        <b>الوقت:</b> {d['الوقت']}
    </div>
    """
    folium.Marker(
        location=[d["LAT"], d["LON"]],
        icon=folium.Icon(color=d["اللون"], icon='info-sign'),
        popup=folium.Popup(html, max_width=200)
    ).add_to(m)

st_folium(m, width="100%", height=550, key="v_final_ultra")

# 4. السجل وتصدير التقرير
if st.session_state.all_detections:
    st.divider()
    st.subheader("📋 التقرير الاستخباري المفصل")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df.drop(columns=['اللون', 'الصورة']), use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل التقرير (CSV)", csv, "GeoSentinel_Report.csv", use_container_width=True)
