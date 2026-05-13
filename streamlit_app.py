import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد الصفحة وتوسيع العرض
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# إدارة حالة التهديدات والمسارات
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود", value=True)
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.markdown("---")
    
    # زر المسح الشامل (تم إصلاح منطق التهديدات)
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك بري مشبوه", "icon": "truck"},
            {"loc": [37.20, 7.50], "type": "هدف بحري مجهول", "icon": "ship"},
            {"loc": [25.10, 9.10], "type": "نشاط غير قانوني", "icon": "bullseye"}
        ]
        st.warning("تم تحديد أهداف استراتيجية جديدة")

    show_flights = st.toggle("✈️ رادار الطيران (FlightRadar24)", value=True)

# --- الخريطة الرئيسية ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")

# 1. رسم الحدود الوطنية (البرية والبحرية) بخط واضح
algeria_border = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], 
    [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]
]
folium.PolyLine(algeria_border, color="yellow", weight=5, dash_array='10', tooltip="الحدود الوطنية").add_to(m)

# 2. تغيير وتحديث المسارات المخفية (👣) - مسارات تكتيكية جديدة
if track_hidden:
    # مسار جنوبي متعرج (منطقة برج باجي مختار)
    path_south = [[19.5, 3.2], [20.0, 2.8], [20.8, 2.1], [21.3, 1.2], [21.8, 0.8]]
    folium.PolyLine(path_south, color="purple", weight=4, dash_array='5', tooltip="مسار تسلل مرصود").add_to(m)
    
    # مسار شرقي وعر (ناحية الحدود مع تونس/ليبيا)
    path_east = [[24.5, 9.8], [25.8, 9.3], [27.2, 9.0], [28.5, 8.5]]
    folium.PolyLine(path_east, color="purple", weight=4, dash_array='5', tooltip="نشاط مسار خلفي").add_to(m)

# 3. إظهار التهديدات (الأيقونات الحمراء)
for threat in st.session_state.threats:
    folium.Marker(
        location=threat["loc"],
        icon=folium.Icon(color='red', icon=threat['icon'], prefix='fa'),
        popup=threat["type"]
    ).add_to(m)

# عرض الخريطة
st.subheader("خريطة الرصد العملياتي والحدود")
st_folium(m, width="100%", height=500)

# 4. رادار الطيران المباشر
if show_flights:
    st.markdown("---")
    st.subheader("✈️ رادار الطيران المباشر")
    # تضمين نافذة FlightRadar24
    url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(url, height=500, scrolling=True)
