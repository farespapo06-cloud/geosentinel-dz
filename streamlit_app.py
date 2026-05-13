import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ", page_icon="🛡️")

# --- 2. نظام الدخول (Geosentinel-auth) ---
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
                    else:
                        st.error("⚠️ الرمز غير صحيح")
        return False
    return True

if login_screen():
    # استعادة البيانات السابقة
    if 'threats' not in st.session_state: st.session_state.threats = []
    if 'log_data' not in st.session_state: st.session_state.log_data = []

    # --- القائمة الجانبية ---
    with st.sidebar:
        st.header("🎮 لوحة التحكم")
        thermal_on = st.toggle("🌡️ الرؤية الليلية الحرارية")
        tracks_on = st.toggle("👣 ملاحقة المسارات", value=True)
        
        st.markdown("---")
        # إعادة الزر الأساسي الذي يعمل يدوياً بدقة
        if st.button("🔍 مسح استخباراتي شامل", use_container_width=True):
            new_threats = [
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [21.32, 0.95], "type": "تحرك بري مشبوه", "status": "نشط", "temp": "42°C"},
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [25.10, 9.10], "type": "نشاط حدودي", "status": "مراقب", "temp": "39°C"},
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [37.20, 7.50], "type": "هدف بحري", "status": "نشط", "temp": "31°C"}
            ]
            st.session_state.threats = new_threats
            for t in new_threats:
                st.session_state.log_data.insert(0, t)
            st.success("تم المسح بنجاح")

        if st.button("🗑️ مسح السجل", use_container_width=True):
            st.session_state.log_data = []
            st.session_state.threats = []
            st.rerun()

        show_flights = st.toggle("✈️ رادار الطيران المباشر")
        st.markdown("---")
        if st.button("🚪 خروج"):
            st.session_state.authenticated = False
            st.rerun()

    # --- بناء الخريطة ---
    st.title("🛡️ GeoSentinel-DZ | واجهة الرصد")
    
    # فلتر الرؤية الليلية
    if thermal_on:
        st.markdown("<style>.night-vision { filter: sepia(100%) hue-rotate(80deg) saturate(200%) brightness(0.6) contrast(1.2); }</style>", unsafe_allow_html=True)

    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")
    m.add_child(plugins.MeasureControl(position='topleft'))

    # الحدود الوطنية (التي اختفت في الصورة السابقة أعدتها بدقة)
    border_color = "#00FF00" if thermal_on else "yellow"
    border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(border, color=border_color, weight=5, dash_array='8', tooltip="الحدود الجزائرية").add_to(m)

    # ملاحقة المسارات (👣)
    if tracks_on:
        p_color = "#00FFFF" if thermal_on else "purple"
        # مسار برج باجي مختار والحدود الجنوبية
        path = [[19.2, 3.5], [20.0, 2.8], [21.2, 1.5], [21.8, 0.9]]
        folium.PolyLine(path, color=p_color, weight=3, dash_array='5', tooltip="مسار مرصود").add_to(m)

    # عرض الأهداف
    for t in st.session_state.threats:
        popup_text = f"{t['type']} | {t['temp']}"
        folium.Marker(t['loc'], icon=folium.Icon(color='red', icon='warning', prefix='fa'), popup=popup_text).add_to(m)

    # عرض الخريطة
    with st.container():
        if thermal_on: st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=550)
        if thermal_on: st.markdown('</div>', unsafe_allow_html=True)

    # سجل النشاطات
    if st.session_state.log_data:
        st.markdown("---")
        st.subheader("📋 سجل الرصد العملياتي")
        st.table(pd.DataFrame(st.session_state.log_data).head(10))

    if show_flights:
        st.markdown("---")
        st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5", height=500)
