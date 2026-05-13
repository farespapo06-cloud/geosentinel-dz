import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import random

# 1. إعدادات النظام السيادي الموحد
st.set_page_config(page_title="الحدود الجزائرية (البرية، الجوية، البحرية)", layout="wide")

if 'intelligence_data' not in st.session_state:
    st.session_state.intelligence_data = []

# 2. مركز التحكم الاستخباراتي (القائمة الجانبية)
with st.sidebar:
    st.title("🛰️ GeoSentinel-DZ v2026")
    st.header("الحدود الجزائرية (بر / جو / بحر)")
    
    st.divider()
    
    # تحليل التغيرات منذ 2020
    st.subheader("⏳ تحليل الأقمار الصناعية")
    timeline = st.select_slider("مقارنة التغيرات الميدانية منذ:", options=["2020", "2021", "2022", "2023", "2024", "2025", "2026"])
    
    st.divider()
    
    # أنظمة التجسس والرصد
    st.subheader("🚨 أنظمة الرصد النشطة")
    sat_tracking = st.toggle("🛰️ ربط الأقمار الصناعية (وارث/Earth Engine)", value=True)
    thermal_scan = st.toggle("🌡️ رصد حراري (معدات ثقيلة/مسيرات)", value=True)
    terror_monitor = st.toggle("👤 ملاحقة الإرهاب والتهريب", value=True)
    hidden_paths = st.toggle("👣 رصد التغيرات الأرضية والمسارات", value=True)
    
    st.divider()
    
    if st.button("📡 إجراء مسح استخباراتي شامل", use_container_width=True):
        scenarios = {
            "استحداث قاعدة جوية حدودية": {"color": "darkred", "cat": "بناء عسكري", "url": "https://www.reuters.com/world/africa/"},
            "تحرك رتل عسكري (دبابات ومعدات)": {"color": "red", "cat": "تحرك عسكري", "url": "https://twitter.com/search?q=Algeria+Border+Security"},
            "تسلل عبر مسارات مخفية": {"color": "purple", "cat": "إرهاب/تهريب", "url": "https://www.aljazeera.net/"},
            "بناء خنادق وتحصينات جديدة": {"color": "brown", "cat": "تحصينات", "url": "https://www.france24.com/ar/"}
        }
        event, details = random.choice(list(scenarios.items()))
        
        entry = {
            "ID": f"INTEL-DZ-{random.randint(1000, 9999)}",
            "الحدث": event,
            "التصنيف": details['cat'],
            "LAT": round(random.uniform(22.0, 36.0), 4),
            "LON": round(random.uniform(-1.0, 9.0), 4),
            "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": details['color'],
            "link": details['url']
        }
        st.session_state.intelligence_data.append(entry)
        st.rerun()

# 3. واجهة العرض الرئيسية
st.warning(f"⚠️ نظام الاستخبارات الجغرافية نشط | مقارنة البيانات من {timeline} | منصة FlightAware مدمجة")

col_intel, col_radars = st.columns([1.8, 1.2])

with col_intel:
    st.subheader("🗺️ خريطة الرصد الاستخباراتي والحدودي")
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Satellite Intel Core"
    )

    # رسم الحدود الجزائرية (الخط السيادي)
    borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(borders, color="white", weight=3, dash_array='8, 8').add_to(m)

    for d in st.session_state.intelligence_data:
        popup_info = f"""
        <div style='width: 200px; text-align: right;'>
            <h5 style='color:{d['color']};'>{d['الحدث']}</h5>
            <p><b>الفئة:</b> {d['التصنيف']}</p>
            <a href='{d['link']}' target='_blank'>
                <button style='background:{d['color']}; color:white; border:none; padding:6px; width:100%; border-radius:4px;'>المصدر الاستخباري 🔗</button>
            </a>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]],
            radius=15, color=d["color"], weight=3, fill=True,
            popup=folium.Popup(popup_info, max_width=250)
        ).add_to(m)

    st_folium(m, width="100%", height=650, key="border_intel_map")

with col_radars:
    # دمج FlightAware للرصد الجوي
    st.subheader("✈️ الرصد الجوي (FlightAware)")
    # استخدام خريطة FlightAware المباشرة للمنطقة
    st.components.v1.iframe("https://ar.flightaware.com/live/map", height=320)
    
    st.divider()
    
    # الرصد البحري (Marine Traffic)
    st.subheader("🚢 الرصد البحري الحي")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:36.0/centerx:4.0/maptype:4", height=320)

# 4. سجل تحليل التهديدات
if st.session_state.intelligence_data:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الشامل (تحركات المهربين، الإرهاب، والمعدات)")
    df = pd.DataFrame(st.session_state.intelligence_data)
    st.dataframe(df[['ID', 'الحدث', 'التصنيف', 'التوقيت', 'LAT', 'LON']], use_container_width=True)
