import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from datetime import datetime

# --- 1. إعدادات المنصة ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Advanced Radar", page_icon="🛡️")

# --- 2. نظام الدخول الآمن ---
def login_screen():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>🛡️ GeoSentinel-DZ</h1>", unsafe_allow_html=True)
            with st.container(border=True):
                password = st.text_input("رمز الدخول العملياتي", type="password")
                if st.button("دخول النظام", use_container_width=True):
                    if password == "DZ_ADMIN_2026":
                        st.session_state.authenticated = True
                        st.rerun()
        return False
    return True

if login_screen():
    if 'threats' not in st.session_state: st.session_state.threats = []
    if 'log_data' not in st.session_state: st.session_state.log_data = []

    # --- القائمة الجانبية (لوحة التحكم) ---
    with st.sidebar:
        st.header("🎮 مركز التحكم بالرصد")
        thermal_on = st.toggle("🌡️ الكشف الحراري الليلي")
        tracks_on = st.toggle("👣 إظهار مسارات القشرة الأرضية", value=True)
        show_radar = st.toggle("✈️ رادار الطيران المباشر", value=True)
        
        st.markdown("---")
        if st.button("🔍 مسح استخباراتي شامل (صور أقمار)", use_container_width=True):
            new_threats = [
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [21.32, 0.95], "type": "تحرك مشبوه - برج باجي مختار", "temp": "42°C"},
                {"loc": [25.10, 9.10], "type": "نشاط حدودي شرقي", "temp": "39°C"},
                {"loc": [37.20, 7.50], "type": "هدف بحري - الساحل", "temp": "31°C"}
            ]
            st.session_state.threats = new_threats
            st.toast("تم رصد أهداف حرارية فوق القشرة الأرضية")

        if st.button("🗑️ مسح السجل التاريخي"):
            st.session_state.log_data = []
            st.session_state.threats = []
            st.rerun()

    # --- بناء الخريطة عالية الدقة ---
    st.title("🛡️ واجهة الرصد الاستراتيجي | GeoSentinel-DZ")
    
    # اختيار طبقة الخريطة (صور أقمار صناعية عالية الدقة)
    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles=None)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View (القشرة الأرضية)',
        overlay=False,
        control=True
    ).add_to(m)

    # إضافة أداة القياس
    m.add_child(plugins.MeasureControl(position='topleft'))

    # 1. رسم الحدود الوطنية الثابتة (لا تتغير)
    border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(border, color="yellow", weight=5, dash_array='8', tooltip="الحدود الوطنية").add_to(m)

    # 2. ملاحقة المسارات (👣) فوق القشرة الأرضية
    if tracks_on:
        # مسار واقعي يتبع التضاريس في الجنوب
        path_terrain = [[19.2, 3.5], [20.1, 2.7], [21.3, 1.4], [22.0, 0.8]]
        folium.PolyLine(path_terrain, color="#00FFFF", weight=3, dash_array='5', tooltip="مسار بري مرصود").add_to(m)

    # 3. إظهار التهديدات كأيقونات رادار حمراء
    for t in st.session_state.threats:
        popup_info = f"<b>{t['type']}</b><br>الحرارة: {t.get('temp','N/A')}"
        folium.Marker(
            t['loc'], 
            icon=folium.Icon(color='red', icon='crosshairs', prefix='fa'),
            popup=folium.Popup(popup_info, max_width=300)
        ).add_to(m)

    # تطبيق تأثير الرؤية الليلية إذا تم تفعيله
    if thermal_on:
        st.markdown("<style>.night-vision { filter: sepia(100%) hue-rotate(80deg) saturate(250%) brightness(0.7); }</style>", unsafe_allow_html=True)

    # عرض الخريطة
    with st.container():
        if thermal_on: st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=600)
        if thermal_on: st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. دمج رادار الطيران المباشر (FlightRadar24) ---
    if show_radar:
        st.markdown("---")
        st.subheader("✈️ رادار الطيران المباشر (تتبع الأهداف الجوية)")
        # وضع الرادار في نافذة كبيرة لسهولة الرؤية
        radar_url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
        st.components.v1.iframe(radar_url, height=600, scrolling=True)
