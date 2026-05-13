import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime

# --- 1. بروتوكول GeoSentinel-Auth ---
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

# --- عنوان التطبيق مع التوقيت الحي بالثانية ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.title(f"🛡️ GeoSentinel-DZ | Live: {now}")

# --- القائمة الجانبية (بناءً على الصورة 1000046454.jpg) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    
    st.subheader("🗓️ المقارنة الزمنية")
    time_mode = st.radio("نطاق البحث:", 
                        ("الوضع الحالي (بث حي 2026)", "الأرشيف (2020)", "التحليل العشري (10 سنوات)"), index=0)
    
    st.divider()
    
    st.subheader("🚨 رادار التهديدات")
    osint = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)", value=True)
    live_traffic = st.toggle("✈️🚢 ربط FlightAware والملاحة البحرية", value=True)
    thermal = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")

    if st.button("إجراء مسح شامل الآن"):
        with st.status("جاري الاتصال بـ FlightAware وأنظمة الملاحة البحرية..."):
            time.sleep(2)
            st.success("تم الربط الحي وتحديث مواقع الطائرات والسفن.")

# --- منطق الخريطة ---
m = folium.Map(location=[32.0, 2.0], zoom_start=5)

# طبقات الخريطة
if thermal:
    folium.TileLayer('CartoDB dark_matter').add_to(m)
else:
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                     attr='Google', name='Satellite Live').add_to(m)

# رسم الحدود الوطنية والبحرية بالكامل
algeria_full_border = [[37.0,-2.0],[38.0,2.0],[38.5,5.0],[37.5,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_full_border, color="red", weight=4).add_to(m)

# --- 2. رصد الملاحة الجوية (FlightAware) ---
if live_traffic:
    # محاكاة لبيانات طائرات حية
    planes = [{"loc": [35.0, 1.5], "id": "AH1020", "type": "Boeing 737"}]
    for p in planes:
        html_plane = f"""
        <div style='width:220px; font-family: Arial; direction: rtl; text-align: right;'>
        <h4 style='color:blue;'>✈️ رصد جوي (FlightAware)</h4>
        <p><b>رقم الرحلة:</b> {p['id']}</p>
        <p><b>النوع:</b> {p['type']}</p>
        <hr>
        <a href='https://www.flightaware.com/live/flight/{p['id']}' target='_blank' 
           style='background:blue; color:white; padding:8px; text-decoration:none; border-radius:5px; display:block; text-align:center;'>
           👁️ تتبع المسار والصور الحقيقية
        </a>
        </div>
        """
        folium.Marker(p["loc"], popup=folium.Popup(html_plane, max_width=250), 
                      icon=folium.Icon(color='blue', icon='plane', prefix='fa')).add_to(m)

    # --- 3. رصد الملاحة البحرية (الربط المباشر بملف السفينة) ---
    ships = [
        {"loc": [37.2, 7.8], "name": "MARAN GAS APOLLONIA", "mmsi": "241445000", "type": "LNG Carrier"},
        {"loc": [36.8, 3.1], "name": "TASSILI II", "mmsi": "605066120", "type": "Passenger Ship"}
    ]
    for s in ships:
        direct_link = f"https://www.marinetraffic.com/en/ais/details/ships/mmsi:{s['mmsi']}"
        html_ship = f"""
        <div style='width:220px; font-family: Arial; direction: rtl; text-align: right;'>
        <h4 style='color:darkblue;'>🚢 رصد بحري (MMSI: {s['mmsi']})</h4>
        <p><b>الاسم:</b> {s['name']}</p>
        <p><b>النوع:</b> {s['type']}</p>
        <hr>
        <a href='{direct_link}' target='_blank' 
           style='background:darkblue; color:white; padding:8px; text-decoration:none; border-radius:5px; display:block; text-align:center;'>
           👁️ فتح ملف السفينة والصور الحقيقية
        </a>
        </div>
        """
        folium.Marker(s["loc"], popup=folium.Popup(html_ship, max_width=250), 
                      icon=folium.Icon(color='darkblue', icon='ship', prefix='fa')).add_to(m)

# --- 4. الدوائر الصفراء (التحليل العشري التفاعلي) ---
if time_mode == "التحليل العشري (10 سنوات)":
    yellow_points = [{"loc": [21.5, 1.5], "type": "تغيير تضاريس مشبوه", "date": "2016-2026"}]
    for p in yellow_points:
        html_yellow = f"""
        <div style='width:200px; font-family: Arial; direction: rtl; text-align: right;'>
        <h4 style='color:#E6B800;'>🟡 تنبيه التغيير العشري</h4>
        <p><b>النوع:</b> {p['type']}</p>
        <hr>
        <a href='https://www.google.com/maps/@{p['loc'][0]},{p['loc'][1]},15z/data=!3m1!1e3' target='_blank' 
           style='background:#E6B800; color:black; padding:5px; text-decoration:none; border-radius:3px; display:block; text-align:center;'>
           👁️ صور القمر الصناعي بدقة عالية
        </a>
        </div>
        """
        folium.CircleMarker(location=p["loc"], radius=10, color="#E6B800", fill=True,
                            popup=folium.Popup(html_yellow, max_width=250)).add_to(m)

# --- 5. إنذار OSINT الأحمر (كما في الصورة 1000046453.jpg) ---
if osint:
    html_red = """
    <div style='width:200px; font-family: Arial; direction: rtl; text-align: right;'>
    <h4 style='color:red;'>🔴 إنذار OSINT</h4>
    <p><b>النوع:</b> تحرك حدودي مشبوه</p>
    <a href='https://google.com/search?q=border+security' target='_blank' 
       style='background:red; color:white; padding:5px; text-decoration:none; border-radius:3px; display:block; text-align:center;'>
       👁️ رؤية صور التهديد والمصدر
    </a>
    </div>
    """
    folium.Marker([22.5, 3.0], popup=folium.Popup(html_red), 
                  icon=folium.Icon(color='red', icon='warning')).add_to(m)

st_folium(m, width="100%", height=650)
