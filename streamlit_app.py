import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import requests
import pandas as pd
from datetime import datetime

# --- 1. إعدادات المنصة السيادية ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Full Suite", page_icon="🛡️")

# --- 2. جلب بيانات الطائرات الحقيقية (المجال الجوي الجزائري) ---
def get_live_flights():
    # حدود المجال الجوي الجزائري للجلب المباشر
    url = "https://opensky-network.org/api/states/all?lamin=19.0&lomin=-8.0&lamax=37.0&lomax=12.0"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        flights = []
        if data['states']:
            for s in data['states']:
                flights.append({
                    "callsign": s[1].strip() if s[1] else "Unknown",
                    "lat": s[6],
                    "lon": s[5],
                    "alt": s[7],
                    "velocity": s[9],
                    "origin": s[2]
                })
        return flights
    except:
        return []

# --- 3. نظام الدخول العملياتي ---
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
    # تهيئة مخزن البيانات لعدم فقدانها
    if 'threats' not in st.session_state: st.session_state.threats = []
    if 'log_data' not in st.session_state: st.session_state.log_data = []

    # --- القائمة الجانبية (كل الأدوات التي تكلمنا عليها) ---
    with st.sidebar:
        st.header("🎮 مركز العمليات")
        thermal_on = st.toggle("🌡️ الرؤية الليلية الحرارية")
        tracks_on = st.toggle("👣 تتبع مسارات القشرة الأرضية", value=True)
        flights_on = st.toggle("✈️ رادار الطيران المباشر (OpenSky)", value=True)
        
        st.markdown("---")
        if st.button("🔍 مسح استخباراتي شامل", use_container_width=True):
            # إضافة تهديدات افتراضية مع روابط Google Earth
            new_threats = [
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [21.32, 0.95], "type": "تحرك مشبوه - برج باجي مختار", "link": "https://earth.google.com/web/@21.32,0.95,300a,d,35y"},
                {"time": datetime.now().strftime("%H:%M:%S"), "loc": [25.10, 9.10], "type": "نشاط حدودي شرقي", "link": "https://earth.google.com/web/@25.10,9.10,300a,d,35y"}
            ]
            st.session_state.threats = new_threats
            for t in new_threats: st.session_state.log_data.insert(0, t)
            st.success("تم تحديث خارطة التهديدات")

        if st.button("🗑️ مسح السجل التاريخي"):
            st.session_state.log_data = []
            st.session_state.threats = []
            st.rerun()

    # --- بناء الخريطة المتكاملة (Satellite + Data) ---
    st.title("🛡️ واجهة الرصد الاستراتيجي | GeoSentinel-DZ")
    
    # استخدام Google Hybrid لرؤية القشرة الأرضية بوضوح تام
    m = folium.Map(location=[28.0, 2.0], zoom_start=5, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                   attr='Google Hybrid')
    
    m.add_child(plugins.MeasureControl(position='topleft'))

    # 1. الحدود الوطنية الثابتة (لا تُحذف)
    border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(border, color="yellow", weight=5, dash_array='8', tooltip="الحدود الجزائرية").add_to(m)

    # 2. مسارات المهربين والإرهاب (👣) مع روابط Google Earth
    if tracks_on:
        path_coords = [[19.2, 3.5], [20.1, 2.7], [21.3, 1.4]]
        folium.PolyLine(path_coords, color="#00FFFF", weight=3, dash_array='5').add_to(m)
        folium.Marker(
            [20.1, 2.7], 
            icon=folium.Icon(color='black', icon='bolt', prefix='fa'),
            popup=folium.Popup('<a href="https://earth.google.com/web/@20.1,2.7,500a,d,35y" target="_blank">تحليل تضاريس المسار (Google Earth)</a>', max_width=250)
        ).add_to(m)

    # 3. دمج الطائرات الحية (Real Flight Tracking)
    if flights_on:
        live_data = get_live_flights()
        for f in live_data:
            if f['lat'] and f['lon']:
                fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
                folium.Marker(
                    [f['lat'], f['lon']],
                    icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(20, 20)),
                    popup=folium.Popup(f"<b>الرحلة: {f['callsign']}</b><br>المنشأ: {f['origin']}<br><a href='{fa_link}' target='_blank'>تتبع مباشر على FlightAware</a>", max_width=250)
                ).add_to(m)

    # 4. التهديدات النشطة (التي تم رصدها بالمسح)
    for t in st.session_state.threats:
        folium.Marker(
            t['loc'],
            icon=folium.Icon(color='red', icon='warning', prefix='fa'),
            popup=folium.Popup(f"<b>{t['type']}</b><br><a href='{t['link']}' target='_blank'>رؤية صور الأقمار الصناعية</a>", max_width=250)
        ).add_to(m)

    # تطبيق الرؤية الليلية
    if thermal_on:
        st.markdown("<style>.night-vision { filter: sepia(100%) hue-rotate(80deg) saturate(250%) brightness(0.7); }</style>", unsafe_allow_html=True)

    # عرض الخريطة
    with st.container():
        if thermal_on: st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=650)
        if thermal_on: st.markdown('</div>', unsafe_allow_html=True)

    # سجل النشاطات العملياتي
    if st.session_state.log_data:
        st.markdown("---")
        st.subheader("📋 سجل الرصد الاستخباراتي")
        st.table(pd.DataFrame(st.session_state.log_data).head(10))
