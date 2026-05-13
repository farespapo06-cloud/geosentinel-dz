import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Tactical Analysis")

# إدارة حالة التهديدات
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود", value=True)
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (Night Vision)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    # ميزة قياس المسافات
    st.info("📏 ميزة 'تحديد المسافة' مفعلة الآن على الخريطة")
    
    st.markdown("---")
    
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك بري مشبوه", "icon": "truck", "temp": "42°C"},
            {"loc": [37.20, 7.50], "type": "هدف بحري مجهول", "icon": "ship", "temp": "31°C"},
            {"loc": [25.10, 9.10], "type": "نشاط غير قانوني", "icon": "bullseye", "temp": "38°C"}
        ]
        st.warning("تم رصد أهداف جديدة")

    show_flights = st.toggle("✈️ رادار الطيران (FlightRadar24)", value=True)

# --- منطق الرؤية الليلية (CSS) ---
night_vision_css = """
<style>
    .night-vision {
        filter: sepia(100%) hue-rotate(80deg) saturate(300%) brightness(0.8) contrast(1.2);
    }
</style>
"""
if thermal_detect:
    st.markdown(night_vision_css, unsafe_allow_html=True)

# --- بناء الخريطة ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")

# 1. إضافة أداة تحديد المسافة (MeasureControl)
measure_control = plugins.MeasureControl(
    position='topleft',
    primary_length_unit='kilometers',
    secondary_length_unit='miles',
    primary_area_unit='sqmeters',
    active_color='#FFFF00',
    completed_color='#FF0000'
)
m.add_child(measure_control)

# 2. رسم الحدود الوطنية
algeria_border = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], 
    [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]
]
border_color = "#00FF00" if thermal_detect else "yellow"
folium.PolyLine(algeria_border, color=border_color, weight=4, dash_array='8').add_to(m)

# 3. ملاحقة المسارات (👣)
if track_hidden:
    path_color = "#00FFFF" if thermal_detect else "purple"
    path1 = [[19.2, 3.5], [20.0, 2.8], [21.2, 1.5], [21.8, 0.9]]
    folium.PolyLine(path1, color=path_color, weight=3, dash_array='5').add_to(m)

# 4. إظهار التهديدات
for threat in st.session_state.threats:
    popup_text = f"{threat['type']}"
    if thermal_detect:
        popup_text += f" | الحرارة: {threat['temp']}"
    
    icon_color = 'orange' if thermal_detect else 'red'
    folium.Marker(
        location=threat["loc"],
        icon=folium.Icon(color=icon_color, icon=threat['icon'], prefix='fa'),
        popup=popup_text
    ).add_to(m)

# عرض الخريطة
st.subheader("GeoSentinel-DZ | نظام تحليل المسافات والرصد")

with st.container():
    if thermal_detect:
        st.markdown('<div class="night-vision">', unsafe_allow_html=True)
    st_folium(m, width="100%", height=550)
    if thermal_detect:
        st.markdown('</div>', unsafe_allow_html=True)

# --- رادار الطيران ---
if show_flights:
    st.markdown("---")
    url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(url, height=500)
