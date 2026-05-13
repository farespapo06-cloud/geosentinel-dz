import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from datetime import datetime

# --- 1. إعدادات المنصة الاحترافية ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Operational", page_icon="🛡️")

# --- 2. نظام الدخول الآمن (Geosentinel-auth) ---
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
    # الاحتفاظ بكافة البيانات السابقة (التحديث المستمر)
    if 'threats' not in st.session_state: 
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك مهربين (برج باجي مختار)", "id": "TRK-09", "link": "https://earth.google.com/web/@21.32,0.95,342a,d,35y"},
            {"loc": [25.10, 9.10], "type": "نشاط مشبوه (حدود شرقية)", "id": "ACT-22", "link": "https://earth.google.com/web/@25.10,9.10,500a,d,35y"}
        ]
    
    # محاكاة بيانات طائرات FlightAware (أهداف حية)
    live_flights = [
        {"loc": [24.50, 2.50], "callsign": "AH6192", "alt": "32000ft", "link": "https://www.flightaware.com/live/flight/AH6192"},
        {"loc": [36.70, 3.20], "callsign": "DZA104", "alt": "15000ft", "link": "https://www.flightaware.com/live/flight/DZA104"}
    ]

    # --- القائمة الجانبية ---
    with st.sidebar:
        st.header("🎮 مركز العمليات الحية")
        layer_select = st.selectbox("طبقة القشرة الأرضية", ["Google Satellite", "Esri Terrain", "Night Vision"])
        tracks_on = st.toggle("👣 تتبع مسارات المهربين", value=True)
        flights_on = st.toggle("✈️ ربط رادار FlightAware", value=True)
        
        st.markdown("---")
        if st.button("🔍 تحديث البيانات الاستخباراتية"):
            st.toast("يتم جلب بيانات الساتليت وFlightAware...")

    # --- بناء الخريطة المتكاملة ---
    st.title("🛡️ GeoSentinel-DZ | الرصد المباشر")
    
    # ربط القشرة الأرضية (Google Earth/Satellite)
    if layer_select == "Google Satellite":
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
        attr = 'Google'
    else:
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        attr = 'Esri'

    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles=tiles, attr=attr)

    # 1. رسم المسارات (👣) المرتبطة بروابط تحليل
    if tracks_on:
        path_coords = [[19.2, 3.5], [20.1, 2.7], [21.3, 1.4]]
        folium.PolyLine(path_coords, color="cyan", weight=3, dash_array='5').add_to(m)
        # نقطة تفاعلية على المسار
        folium.Marker(
            [20.1, 2.7], 
            icon=folium.DivIcon(html='<div style="color:white; font-size:10pt;">👣 مسار نشط</div>'),
            popup=folium.Popup('<a href="https://earth.google.com/web/" target="_blank">رؤية تضاريس المسار (Google Earth)</a>', max_width=200)
        ).add_to(m)

    # 2. ربط الطائرات (FlightAware Style)
    if flights_on:
        for f in live_flights:
            folium.Marker(
                f['loc'],
                icon=folium.Icon(color='blue', icon='plane', prefix='fa'),
                popup=folium.Popup(f"<b>الرحلة: {f['callsign']}</b><br>الارتفاع: {f['alt']}<br><a href='{f['link']}' target='_blank'>تتبع مباشر على FlightAware</a>", max_width=250)
            ).add_to(m)

    # 3. تهديدات الإرهاب والتهريب (الرصد الاستخباراتي)
    for t in st.session_state.threats:
        folium.Marker(
            t['loc'],
            icon=folium.Icon(color='red', icon='warning', prefix='fa'),
            popup=folium.Popup(f"<b>{t['type']}</b><br>المعرف: {t['id']}<br><a href='{t['link']}' target='_blank'>فتح في Google Earth</a>", max_width=250)
        ).add_to(m)

    # عرض الخريطة
    st_folium(m, width="100%", height=650)

    st.info("💡 اضغط على أي هدف (طائرة، تهديد، مسار) للانتقال المباشر إلى منصات التحليل العالمية.")
