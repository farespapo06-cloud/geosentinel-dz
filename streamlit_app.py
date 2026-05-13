import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# --- 1. نظام التحقق من الهوية (Authentication) ---
def check_password():
    """يرجع True إذا كانت كلمة المرور صحيحة."""
    def password_entered():
        if st.session_state["password"] == "DZ_ADMIN_2026": # يمكنك تغيير كلمة المرور هنا
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # حذف كلمة المرور من الحالة للأمان
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # عرض واجهة تسجيل الدخول
        st.title("🔐 GeoSentinel-DZ | الدخول الآمن")
        st.text_input("أدخل كلمة المرور للوصول إلى أنظمة الرصد", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("⚠️ كلمة المرور خاطئة. الوصول مرفوض.")
        return False
    else:
        return st.session_state["password_correct"]

# تفعيل التحقق
if check_password():
    # --- 2. تشغيل التطبيق بعد نجاح تسجيل الدخول ---
    
    st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Secured")

    if 'threats' not in st.session_state:
        st.session_state.threats = []

    # --- القائمة الجانبية ---
    with st.sidebar:
        st.success("✅ تم التحقق من الهوية: مسؤول الرصد")
        st.header("🚨 أنظمة الرصد المتقدمة")
        radar_scan = st.toggle("🛰️ رادار مسح الحدود", value=True)
        thermal_detect = st.toggle("🌡️ كشف ليلي حراري (Night Vision)")
        track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
        
        st.markdown("---")
        
        if st.button("🔍 إجراء مسح استخباراتي شامل"):
            st.session_state.threats = [
                {"loc": [21.32, 0.95], "type": "تحرك بري مشبوه", "icon": "truck", "temp": "42°C"},
                {"loc": [37.20, 7.50], "type": "هدف بحري مجهول", "icon": "ship", "temp": "31°C"},
                {"loc": [25.10, 9.10], "type": "نشاط غير قانوني", "icon": "bullseye", "temp": "38°C"}
            ]
            st.warning("تم رصد أهداف جديدة")

        show_flights = st.toggle("✈️ رادار الطيران (FlightRadar24)", value=True)
        
        if st.button("🚪 تسجيل الخروج"):
            del st.session_state["password_correct"]
            st.rerun()

    # --- منطق الرؤية الليلية (CSS) ---
    if thermal_detect:
        st.markdown("""
        <style>
            .night-vision { filter: sepia(100%) hue-rotate(80deg) saturate(300%) brightness(0.8) contrast(1.2); }
        </style>
        """, unsafe_allow_html=True)

    # --- بناء الخريطة ---
    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")

    # إضافة أداة القياس
    m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='kilometers', active_color='#FFFF00'))

    # رسم الحدود
    algeria_border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(algeria_border, color="#00FF00" if thermal_detect else "yellow", weight=4, dash_array='8').add_to(m)

    # ملاحقة المسارات (👣)
    if track_hidden:
        path1 = [[19.2, 3.5], [20.0, 2.8], [21.2, 1.5], [21.8, 0.9]]
        folium.PolyLine(path1, color="#00FFFF" if thermal_detect else "purple", weight=3, dash_array='5').add_to(m)

    # إظهار التهديدات
    for threat in st.session_state.threats:
        popup_text = f"{threat['type']} | الحرارة: {threat.get('temp', 'N/A')}" if thermal_detect else threat['type']
        folium.Marker(location=threat["loc"], icon=folium.Icon(color='red', icon=threat['icon'], prefix='fa'), popup=popup_text).add_to(m)

    # عرض الواجهة
    st.title("🛡️ GeoSentinel-DZ")
    with st.container():
        if thermal_detect: st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=550)
        if thermal_detect: st.markdown('</div>', unsafe_allow_html=True)

    if show_flights:
        st.markdown("---")
        st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5", height=500)
