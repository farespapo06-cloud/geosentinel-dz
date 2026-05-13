import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
# from opensky_api import OpenSkyApi  # تأكد من تثبيت المكتبة: pip install opensky-api
# from opensky_api import OpenSkyApi
# --- 1. بروتوكول GeoSentinel-Auth (نفس إعداداتك) ---
def check_security():
    if "auth_ok" not in st.session_state:
        st.sidebar.warning("🔐 نظام مؤمن: ادخل مفتاح العبور")
        key = st.sidebar.text_input("Security Key:", type="password")
        if key == "DZ_ELITE_2026":
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.stop()

check_security()

# --- التوقيت الحي بالثانية ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.title(f"🛡️ GeoSentinel-DZ | Live: {now}")

# --- القائمة الجانبية (كما في الصورة 1000046454.jpg) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    time_mode = st.radio("نطاق البحث:", 
                        ("الوضع الحالي (بث حي 2026)", "الأرشيف (2020)", "التحليل العشري (10 سنوات)"), index=0)
    st.divider()
    st.subheader("🚨 رادار التهديدات")
    osint = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)", value=True)
    live_traffic = st.toggle("✈️🚢 ربط OpenSky والملاحة البحرية", value=True)
    thermal = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")

    if st.button("تحديث الرصد الحي"):
        st.rerun()

# --- إعداد الخريطة ---
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5) # تم التوسيع لتشمل كامل الجزائر

if thermal:
    folium.TileLayer('CartoDB dark_matter').add_to(m)
else:
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                     attr='Google', name='Satellite Live').add_to(m)

# رسم الحدود الوطنية باللون الأحمر (نفس إعداداتك)
algeria_full_border = [[37.0,-2.0],[38.0,2.0],[38.5,5.0],[37.5,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_full_border, color="red", weight=4).add_to(m)

# --- 2. جلب البيانات الحقيقية من OpenSky API ---
if live_traffic:
    try:
        api = OpenSkyApi()
        # تحديد مربع البحث فوق الجزائر (خطوط العرض والطول)
        states = api.get_states(bbox=(19.0, 37.5, -8.5, 12.0))
        
        if states:
            for s in states.states:
                # إنشاء نافذة معلومات لكل طائرة (مع رابط FlightAware للصور)
                html_plane = f"""
                <div style='direction: rtl; text-align: right; font-family: Arial; width:200px;'>
                    <h4 style='color:blue;'>✈️ رصد حي (OpenSky)</h4>
                    <p><b>رقم النداء:</b> {s.callsign if s.callsign else 'N/A'}</p>
                    <p><b>الارتفاع:</b> {int(s.baro_altitude) if s.baro_altitude else 0} م</p>
                    <p><b>السرعة:</b> {int(s.velocity * 3.6) if s.velocity else 0} كم/س</p>
                    <hr>
                    <a href='https://www.flightaware.com/live/flight/{s.callsign.strip() if s.callsign else ""}' target='_blank' 
                       style='background:blue; color:white; padding:5px; text-decoration:none; border-radius:3px; display:block; text-align:center;'>
                       👁️ رؤية الطائرة الحقيقية
                    </a>
                </div>
                """
                folium.Marker(
                    location=[s.latitude, s.longitude],
                    popup=folium.Popup(html_plane, max_width=250),
                    icon=folium.Icon(color='blue', icon='plane', prefix='fa')
                ).add_to(m)
        else:
            st.info("لا توجد طائرات حالياً في المجال الجوي المحدد.")
    except Exception as e:
        st.error(f"خطأ في الاتصال بـ OpenSky: {e}")

# --- 3. الملاحة البحرية (الربط المباشر كما طلبتم) ---
ships = [
    {"loc": [36.75, 5.08], "id": "605066120", "name": "TASSILI II", "type": "Passenger Ship"},
    {"loc": [36.88, 6.91], "id": "241445000", "name": "MARAN GAS", "type": "LNG Carrier"}
]
for s in ships:
    link = f"https://www.marinetraffic.com/en/ais/details/ships/mmsi:{s['id']}"
    html_ship = f"""
    <div style='direction: rtl; text-align: right; width:200px;'>
        <h4 style='color:darkblue;'>🚢 رصد بحري</h4>
        <p><b>الاسم:</b> {s['name']}</p>
        <hr>
        <a href='{link}' target='_blank' style='background:darkblue; color:white; padding:5px; text-decoration:none; border-radius:3px; display:block; text-align:center;'>
            👁️ صور السفينة الحقيقية
        </a>
    </div>
    """
    folium.Marker(s["loc"], popup=folium.Popup(html_ship, max_width=250),
                  icon=folium.Icon(color='darkblue', icon='ship', prefix='fa')).add_to(m)

# --- 4. إنذار OSINT (نفس الصورة 1000046453.jpg) ---
if osint:
    html_red = """<div style='direction: rtl; text-align: right;'><b>🔴 إنذار OSINT</b><br>تحرك حدودي مشبوه<br><a href='#' target='_blank'>👁️ رؤية المصدر</a></div>"""
    folium.Marker([22.5, 3.0], popup=folium.Popup(html_red), icon=folium.Icon(color='red', icon='warning')).add_to(m)

st_folium(m, width="100%", height=650)
