import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd

# --- إعدادات المنصة السيادية ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Live Airspace")

# --- دالة جلب الطائرات الحقيقية من المجال الجوي (Live Data) ---
def get_live_flights():
    # حدود المجال الجوي الجزائري التقريبية للجلب الاستخباراتي
    url = "https://opensky-network.org/api/states/all?lamin=19.0&lomin=-8.0&lamax=37.0&lomax=12.0"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        flights = []
        if data['states']:
            for s in data['states']:
                flights.append({
                    "callsign": s[1].strip(),
                    "lat": s[6],
                    "lon": s[5],
                    "alt": s[7],
                    "velocity": s[9],
                    "origin_country": s[2]
                })
        return flights
    except:
        return [] # في حال فشل الاتصال يعيد قائمة فارغة

# --- واجهة الدخول المستمرة ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # (كود الدخول المختصر للسرعة)
    pwd = st.sidebar.text_input("Security Key", type="password")
    if st.sidebar.button("Login"):
        if pwd == "DZ_ADMIN_2026":
            st.session_state.authenticated = True
            st.rerun()
else:
    # --- لوحة التحكم الجانبية ---
    with st.sidebar:
        st.header("📡 الرصد المباشر")
        track_smugglers = st.toggle("👣 تتبع مسارات القشرة الأرضية", value=True)
        st.markdown("---")
        if st.button("🔄 تحديث الرادار المباشر"):
            st.rerun()

    st.title("🛡️ مركز قيادة GeoSentinel-DZ | المجال الجوي")

    # --- بناء الخريطة الهجينة (Satellite + Google Earth Layers) ---
    # هذه الطبقة تظهر القشرة الأرضية بدقة عالية (تحركات المهربين)
    m = folium.Map(location=[28.0, 2.0], zoom_start=5, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                   attr='Google Hybrid')

    # 1. جلب وعرض الطائرات الحقيقية (Real-time Integration)
    live_data = get_live_flights()
    for f in live_data:
        if f['lat'] and f['lon']:
            # رابط FlightAware المباشر لكل طائرة موجودة حالياً في سماء الجزائر
            fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
            
            folium.Marker(
                [f['lat'], f['lon']],
                icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(25, 25)),
                popup=folium.Popup(f"""
                    <b>النداء: {f['callsign']}</b><br>
                    المنشأ: {f['origin_country']}<br>
                    السرعة: {f['velocity']} m/s<br>
                    <a href="{fa_link}" target="_blank">🔎 تتبع الهدف على FlightAware</a>
                """, max_width=300)
            ).add_to(m)

    # 2. مسارات المهربين (👣) مرتبطة بـ Google Earth
    if track_smugglers:
        # مثال لمسار في أقصى الجنوب (برج باجي مختار - تينزاوتين)
        smuggler_path = [[21.32, 0.95], [19.57, 2.82]]
        folium.PolyLine(smuggler_path, color="red", weight=4, opacity=0.7, dash_array='10').add_to(m)
        
        folium.Marker(
            [20.5, 1.8],
            icon=folium.Icon(color='black', icon='eye', prefix='fa'),
            popup=folium.Popup('<a href="https://earth.google.com/web/@20.5,1.8,300a,d,35y" target="_blank">فتح مسح الساتليت للقشرة الأرضية</a>', max_width=250)
        ).add_to(m)

    # عرض الخريطة العملياتية
    st_folium(m, width="100%", height=700)
    
    st.success(f"تم رصد {len(live_data)} طائرة نشطة حالياً في المجال الجوي الجزائري.")
