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
    st.title("🛰️ نظام الرصد GeoSentinel-DZ")
    st.header("الحدود الجزائرية (البرية، الجوية، البحرية)")
    
    st.divider()
    
    # وحدة المقارنة الزمنية (تحليل التغيرات الأرضية)
    st.subheader("⏳ تحليل الأقمار الصناعية (مقارنة)")
    timeline = st.select_slider("عرض التغيرات الميدانية منذ عام:", options=["2020", "2021", "2022", "2023", "2024", "2025", "2026"])
    
    st.divider()
    
    # قفلات أنظمة التجسس والرصد الحديثة
    st.subheader("🚨 أنظمة الرصد النشطة")
    sat_tracking = st.toggle("🛰️ ربط الأقمار الصناعية (Earth Engine)", value=True)
    thermal_scan = st.toggle("🌡️ رصد حراري ليلي (مركبات/معدات عسكرية)", value=True)
    terror_monitor = st.toggle("👤 تتبع تحركات الإرهاب والتهريب", value=True)
    hidden_paths = st.toggle("👣 كشف المسارات البشرية والأرضية", value=True)
    
    st.divider()
    
    # زر تحديث الرصد الاستخباري (الخوارزمية الشاملة)
    if st.button("📡 إجراء مسح شامل للحدود", use_container_width=True):
        # محاكاة لنتائج رصد الأقمار الصناعية والروابط العالمية
        scenarios = {
            "استحداث مطار عسكري حدودي": {"color": "darkred", "cat": "بناء هيكلي", "url": "https://www.reuters.com/world/africa/"},
            "تحرك معدات عسكرية ثقيلة (دبابات)": {"color": "red", "cat": "تحرك عسكري", "url": "https://twitter.com/search?q=Military+Movements+Algeria"},
            "تغير مسارات المهربين (رصد أرضي)": {"color": "orange", "cat": "تهريب", "url": "https://www.aljazeera.net/news/maghreb/"},
            "بناء ثكنات / خنادق حدودية جديدة": {"color": "brown", "cat": "تحصينات", "url": "https://www.france24.com/ar/"},
            "رصد مسيرة/مركبة (كشف حراري)": {"color": "cyan", "cat": "تسلل", "url": "https://www.bbc.com/arabic"}
        }
        event, details = random.choice(list(scenarios.items()))
        
        entry = {
            "ID": f"INT-DZ-{random.randint(1000, 9999)}",
            "الحدث": event,
            "التصنيف": details['cat'],
            "LAT": round(random.uniform(20.0, 36.5), 4),
            "LON": round(random.uniform(-1.5, 9.5), 4),
            "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": details['color'],
            "link": details['url']
        }
        st.session_state.intelligence_data.append(entry)
        st.rerun()

# 3. واجهة العرض الرئيسية (الخرائط والرادارات)
st.warning(f"⚠️ نظام التجسس الجغرافي نشط | مقارنة البيانات الاستخباراتية من {timeline} إلى 2026")

# تقسيم الشاشة (الميدان والحدود | الملاحة الجوية والبحرية)
col_intel, col_radars = st.columns([2, 1])

with col_intel:
    st.subheader("🗺️ خريطة الرصد الاستخباراتي والحدودي")
    # استخدام طبقة الأقمار الصناعية (Satellite) لمحاكاة الرؤية الاستخباراتية
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Satellite Intel Core"
    )

    # رسم الحدود الجزائرية (الخط السيادي)
    borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(borders, color="white", weight=3, dash_array='8, 8').add_to(m)

    # إسقاط التهديدات والمعدات المكتشفة
    for d in st.session_state.intelligence_data:
        popup_info = f"""
        <div style='width: 210px; text-align: right; font-family: Arial;'>
            <h5 style='color:{d['color']}; margin-bottom:5px;'>{d['الحدث']}</h5>
            <p style='font-size: 12px;'><b>الفئة:</b> {d['التصنيف']}</p>
            <p style='font-size: 11px;'><b>الإحداثيات:</b> {d['LAT']}, {d['LON']}</p>
            <hr>
            <a href='{d['link']}' target='_blank'>
                <button style='background:{d['color']}; color:white; border:none; padding:6px; border-radius:4px; width:100%; cursor:pointer;'>
                    فتح المصدر العالمي 🔗
                </button>
            </a>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]],
            radius=14, color=d["color"], weight=3,
            fill=True, fill_color=d["color"], fill_opacity=0.5,
            popup=folium.Popup(popup_info, max_width=300)
        ).add_to(m)

    st_folium(m, width="100%", height=650, key="main_border_intel")

with col_radars:
    # رصد الطيران الجوي (FlightRadar24)
    st.subheader("✈️ الرصد الجوي الحي")
    st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5", height=320)
    
    st.divider()
    
    # رصد الملاحة البحرية (Marine Traffic)
    st.subheader("🚢 الرصد البحري الحي")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:36.0/centerx:4.0/maptype:4", height=320)

# 4. سجل تحليل التهديدات والمقارنة التاريخية
if st.session_state.intelligence_data:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الشامل (تحركات المهربين، الإرهاب، والمعدات العسكرية)")
    df = pd.DataFrame(st.session_state.intelligence_data)
    st.dataframe(df[['ID', 'الحدث', 'التصنيف', 'التوقيت', 'LAT', 'LON']], use_container_width=True)
