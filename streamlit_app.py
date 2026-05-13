import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. الإعدادات الأساسية
st.set_page_config(page_title="GeoSentinel-DZ | Regional Command", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ مركز العمليات السيادي")
    
    st.subheader("⏳ أرشيف التغيرات (منذ 2024)")
    time_node = st.select_slider("السنة المستهدفة:", options=["2024", "2025", "2026"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد المتقدمة")
    radar_active = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_active = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)", value=True)
    stealth_active = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.divider()
    
    if st.button("🔍 إجراء مسح استخباراتي شامل", use_container_width=True):
        # تصنيفات مرتبطة بالمنطقة مع روابط إخبارية موثوقة (رويترز أفريقيا، فرانس 24، هسبريس، إلخ)
        threat_catalog = {
            "مطار عسكري حدودي مستحدث": {"color": "darkred", "img": "https://img.freepik.com/free-photo/military-airbase_181624-1.jpg", "link": "https://www.reuters.com/world/africa/"},
            "خندق دفاعي / سواتر ترابية": {"color": "orange", "img": "https://img.freepik.com/free-photo/trench_181624-2.jpg", "link": "https://twitter.com/search?q=Border+Security+Africa"},
            "مسار تسلل مخفي (خارج الرادار)": {"color": "purple", "img": "https://img.freepik.com/free-photo/secret-path_181624-3.jpg", "link": "https://www.aljazeera.net/news/maghreb/"},
            "تحرك صامت (مركبات كهربائية)": {"color": "cyan", "img": "https://img.freepik.com/free-photo/thermal-car_181624-4.jpg", "link": "https://www.france24.com/ar/tag/%D8%A7%D9%84%D8%AC%D8%B2%D8%A7%D8%A6%D8%B1/"},
            "ثكنة تجمع / قاعدة إسناد": {"color": "red", "img": "https://img.freepik.com/free-photo/military-camp_181624-5.jpg", "link": "https://www.bbc.com/arabic/topics/ckdxnw89dqet"}
        }
        
        name, info = random.choice(list(threat_catalog.items()))
        
        # تركيز الإحداثيات حصرياً على الجزائر وحدودها (تجنب سوريا أو إيران)
        target = {
            "ID": f"DZ-OP-{random.randint(1000, 9999)}",
            "النوع": name,
            "LAT": round(random.uniform(21.0, 35.0), 4),
            "LON": round(random.uniform(-1.0, 8.0), 4),
            "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": info['color'],
            "image": info['img'],
            "news_link": info['link']
        }
        st.session_state.all_detections.append(target)
        st.rerun()

# 3. واجهة العرض الرئيسية
st.success(f"✅ جميع الأنظمة مرتبطة بالإحداثيات الإقليمية للجزائر وحدودها | الإطار: {time_node}")

main_col, radar_col = st.columns([2, 1])

with main_col:
    st.subheader("🗺️ خريطة الرصد وتغيرات الميدان")
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite"
    )

    # الحدود السيادية (الخط المقطع)
    algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

    for d in st.session_state.all_detections:
        popup_html = f"""
        <div style="width: 200px; text-align: center; font-family: Arial;">
            <b style="color:{d['color']}; font-size: 14px;">{d['النوع']}</b><br>
            <img src="{d['image']}" width="100%" style="border-radius: 8px; margin: 5px 0;"><br>
            <a href="{d['news_link']}" target="_blank">
                <button style="background-color:{d['color']}; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer; width:100%;">
                    المصدر الاستخباري 🔗
                </button>
            </a><br>
            <small style="color:grey;">ID: {d['ID']} | {d['الوقت']}</small>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]],
            radius=12, color=d["color"], weight=3,
            fill=True, fill_color=d["color"], fill_opacity=0.4,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width="100%", height=600, key="operational_map_dz")

with radar_col:
    # دمج تتبع الطائرات (FlightRadar24) بشكل ثابت
    st.subheader("✈️ تتبع الطيران الحي")
    st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5", height=320)
    
    st.divider()
    
    # دمج تتبع السفن (Marine Traffic) بشكل ثابت
    st.subheader("🚢 الملاحة البحرية")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:37.0/centerx:4.0/maptype:4/show_menu:false", height=320)

# 4. السجل العملياتي
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الموحد (الجزائر والحدود)")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['ID', 'النوع', 'LAT', 'LON', 'الوقت']], use_container_width=True)
