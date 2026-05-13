import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# إدارة الحالة لتخزين التهديدات
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    radar_scan = st.toggle("🛰️ رادار مسح الحدود", value=True)
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.markdown("---")
    
    # زر المسح الشامل (Logic لإظهار التهديدات)
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك بري مشبوه", "icon": "truck"},
            {"loc": [37.20, 7.50], "type": "هدف بحري مجهول", "icon": "ship"},
            {"loc": [25.10, 9.10], "type": "نشاط غير قانوني", "icon": "bullseye"}
        ]
        st.warning("تم رصد أهداف جديدة على الحدود")

    show_flights = st.toggle("✈️ رادار الطيران (FlightRadar24)", value=True)

# --- الخريطة الرئيسية ---
st.subheader("خريطة الرصد العملياتي والحدود الوطنية")
m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")

# 1. رسم كامل الحدود (البرية والبحرية)
algeria_border = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], 
    [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]
]
folium.PolyLine(algeria_border, color="yellow", weight=5, dash_array='8').add_to(m)

# 2. تفعيل المسارات المخفية (👣) - مسارات تكتيكية محدثة
if track_hidden:
    # مسار تسلل في أقصى الجنوب
    path1 = [[19.2, 3.5], [20.0, 2.8], [21.2, 1.5], [21.8, 0.9]]
    folium.PolyLine(path1, color="purple", weight=3, dash_array='5', tooltip="مسار مرصود 1").add_to(m)
    
    # مسار في المنطقة الشرقية
    path2 = [[24.5, 9.7], [25.5, 9.2], [26.8, 8.8]]
    folium.PolyLine(path2, color="purple", weight=3, dash_array='5', tooltip="مسار مرصود 2").add_to(m)

# 3. إظهار التهديدات عند تفعيل المسح
for threat in st.session_state.threats:
    folium.Marker(
        location=threat["loc"],
        icon=folium.Icon(color='red', icon=threat['icon'], prefix='fa'),
        popup=threat["type"]
    ).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=500)

# --- قسم FlightRadar24 ---
if show_flights:
    st.markdown("---")
    st.subheader("✈️ رادار الطيران المباشر")
    url = "https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5"
    st.components.v1.iframe(url, height=500)
