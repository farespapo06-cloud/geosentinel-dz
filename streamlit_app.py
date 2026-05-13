import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Tactical Platform", page_icon="🛡️")

# --- 2. نظام الدخول المؤقت (Geosentinel-auth) ---
def login_screen():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>🛡️ GeoSentinel-DZ</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>نظام الرصد والتحليل الجيومكاني</h3>", unsafe_allow_html=True)
            
            with st.container(border=True):
                password = st.text_input("رمز الدخول العملياتي", type="password")
                if st.button("تسجيل الدخول", use_container_width=True):
                    if password == "DZ_ADMIN_2026": # كلمة المرور الحالية
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("⚠️ الرمز غير صحيح. الوصول مرفوض.")
            st.info("ملاحظة: هذا النظام محمي ومشفر برمجياً.")
        return False
    return True

# --- 3. تشغيل المنصة في حال نجاح الدخول ---
if login_screen():
    
    # إدارة حالة التهديدات والبيانات
    if 'threats' not in st.session_state:
        st.session_state.threats = []

    # --- القائمة الجانبية (الأوامر) ---
    with st.sidebar:
        st.header("🎮 لوحة التحكم بالرصد")
        radar_on = st.toggle("🛰️ تفعيل رادار الحدود", value=True)
        thermal_on = st.toggle("🌡️ الرؤية الليلية الحرارية")
        tracks_on = st.toggle("👣 ملاحقة المسارات", value=True)
        
        st.markdown("---")
        
        if st.button("🔍 مسح استخباراتي شامل", use_container_width=True):
            st.session_state.threats = [
                {"loc": [21.32, 0.95], "type": "تحرك بري", "icon": "truck", "temp": "41°C"},
                {"loc": [25.10, 9.10], "type": "نشاط حدودي", "icon": "bullseye", "temp": "39°C"}
            ]
            st.toast("تم تحديث قاعدة بيانات التهديدات")

        show_flights = st.toggle("✈️ حركة الطيران المباشرة", value=False)
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- تطبيق فلتر الرؤية الليلية ---
    if thermal_on:
        st.markdown("""
        <style>
            .night-vision-filter { filter: sepia(100%) hue-rotate(80deg) saturate(250%) brightness(0.7) contrast(1.3); }
        </style>
        """, unsafe_allow_html=True)

    # --- بناء الخريطة ---
    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")
    
    # أداة قياس المسافات (المُسماة)
    m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='kilometers'))

    # رسم الحدود (تتغير حسب الوضع)
    b_color = "#00FF00" if thermal_on else "yellow"
    border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(border, color=b_color, weight=4, dash_array='8', tooltip="الحدود الوطنية").add_to(m)

    # المسارات (👣)
    if tracks_on:
        p_color = "#00FFFF" if thermal_on else "purple"
        path = [[19.2, 3.5], [20.0, 2.8], [21.2, 1.5], [21.8, 0.9]]
        folium.PolyLine(path, color=p_color, weight=3, dash_array='5', tooltip="مسار مرصود").add_to(m)

    # وضع الأهداف
    for t in st.session_state.threats:
        pop = f"{t['type']} | {t['temp']}" if thermal_on else t['type']
        folium.Marker(t['loc'], icon=folium.Icon(color='red', icon=t['icon'], prefix='fa'), popup=pop).add_to(m)

    # العرض النهائي
    st.title("🛡️ GeoSentinel-DZ")
    
    if thermal_on:
        st.markdown('<div class="night-vision-filter">', unsafe_allow_html=True)
    st_folium(m, width="100%", height=600)
    if thermal_on:
        st.markdown('</div>', unsafe_allow_html=True)

    if show_flights:
        st.markdown("---")
        st.subheader("✈️ رادار الطيران المباشر")
        st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=2.0&z=5", height=500)
