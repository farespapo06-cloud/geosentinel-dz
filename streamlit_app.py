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
    st.title("🛰️ GeoSentinel-DZ")
    st.header("الأمن القومي: بر / جو / بحر")
    
    st.divider()
    
    # تحليل التغيرات منذ 2020 (مقارنة الأقمار الصناعية)
    st.subheader("⏳ تحليل التغيرات (منذ 2020)")
    timeline = st.select_slider("عرض الحالة الأرضية لعام:", options=["2020", "2021", "2022", "2023", "2024", "2025", "2026"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد الإقليمي")
    sat_tracking = st.toggle("🛰️ ربط الأقمار الصناعية (وارث)", value=True)
    thermal_scan = st.toggle("🌡️ كشف حراري (معدات ثقيلة/دبابات)", value=True)
    terror_monitor = st.toggle("👤 ملاحقة الإرهاب (الساحل والمغرب العربي)", value=True)
    border_encroachment = st.toggle("🚧 رصد الخنادق والمطارات الحدودية", value=True)
    
    st.divider()
    
    if st.button("📡 إجراء مسح استخباراتي شامل", use_container_width=True):
        # قاعدة بيانات التهديدات محصورة جغرافياً في الجزائر والدول المجاورة فقط
        regional_threats = {
            "استحداث مطار عسكري (حدود ليبيا/النيجر)": {"color": "darkred", "cat": "بناء عسكري", "url": "https://www.reuters.com/world/africa/"},
            "تحرك رتل عسكري (شمال مالي)": {"color": "red", "cat": "نشاط مسلح", "url": "https://www.aljazeera.net/news/maghreb/"},
            "تسلل عبر خنادق مستحدثة (الحدود الغربية)": {"color": "orange", "cat": "تهريب/تسلل", "url": "https://www.france24.com/ar/tag/%D8%A7%D9%84%D9%85%D8%BA%D8%B1%D8%A8-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A/"},
            "نشاط مشبوه في الصحراء الغربية": {"color": "purple", "cat": "رصد جيوسياسي", "url": "https://www.aps.dz/ar/algerie"},
            "قاعدة إمداد جديدة (حدود موريتانيا)": {"color": "brown", "cat": "تحصينات", "url": "https://www.bbc.com/arabic/topics/cpz0ze2n1vmt"}
        }
        event, details = random.choice(list(regional_threats.items()))
        
        # حصر الإحداثيات داخل الجزائر وجوارها المباشر فقط
        entry = {
            "ID": f"DZ-INT-{random.randint(1000, 9999)}",
            "الحدث": event,
            "التصنيف": details['cat'],
            "LAT": round(random.uniform(19.0, 36.0), 4), # من حدود مالي للوسط
            "LON": round(random.uniform(-8.0, 11.0), 4), # من موريتانيا لليبيا
            "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": details['color'],
            "link": details['url']
        }
        st.session_state.intelligence_data.append(entry)
        st.rerun()

# 3. واجهة العرض الرئيسية
st.info(f"✅ نظام التجسس الجغرافي محصور في نطاق: الجزائر، تونس، ليبيا، مالي، النيجر، موريتانيا، الصحراء الغربية")

col_intel, col_flight = st.columns([1.8, 1.2])

with col_intel:
    st.subheader("🗺️ خريطة الرصد الاستخباراتي (بر/بحر)")
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Sovereign Satellite"
    )

    # رسم حدود الدول المعنية للتوضيح الاستخباراتي
    algeria_zone = [[37.0, 8.5], [19.0, 5.0], [21.0, -8.0], [36.0, -2.0], [37.0, 8.5]]
    folium.PolyLine(algeria_zone, color="cyan", weight=2, opacity=0.5).add_to(m)

    for d in st.session_state.intelligence_data:
        popup_html = f"""
        <div style='width: 200px; text-align: right; font-family: Arial;'>
            <h5 style='color:{d['color']};'>{d['الحدث']}</h5>
            <p style='font-size:12px;'><b>المكان:</b> {d['LAT']}, {d['LON']}</p>
            <hr>
            <a href='{d['link']}' target='_blank'>
                <button style='background:{d['color']}; color:white; border:none; padding:8px; border-radius:5px; width:100%; cursor:pointer;'>المصدر الإقليمي 🔗</button>
            </a>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]], radius=15, color=d["color"], weight=3, fill=True,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width="100%", height=650, key="regional_intel_map")

with col_flight:
    # دمج FlightAware مع تركيز الإحداثيات على الجزائر (مركز 28, 3)
    st.subheader("✈️ الرصد الجوي (FlightAware)")
    # الرابط الآن يفتح مباشرة على خريطة حية للمنطقة المعنية
    st.components.v1.iframe("https://www.flightaware.com/live/map?lat=28.0&lon=3.0&zoom=5", height=320)
    
    st.divider()
    
    # الرصد البحري (Marine Traffic) للسواحل الجزائرية
    st.subheader("🚢 الرصد البحري (المتوسط)")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:6/centery:37.0/centerx:4.0/maptype:4", height=320)

# 4. سجل التهديدات
if st.session_state.intelligence_data:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الإقليمي (الجزائر ودول الجوار)")
    df = pd.DataFrame(st.session_state.intelligence_data)
    st.dataframe(df[['ID', 'الحدث', 'التصنيف', 'التوقيت', 'LAT', 'LON']], use_container_width=True)
