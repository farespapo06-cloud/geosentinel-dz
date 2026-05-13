import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from datetime import datetime
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Auto-Radar", page_icon="🛡️")

# --- 2. نظام الدخول الآمن ---
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
    # إدارة حالة الأنظمة (الرصد الآلي)
    if 'threats' not in st.session_state: st.session_state.threats = []
    if 'log_data' not in st.session_state: st.session_state.log_data = []
    if 'auto_mode' not in st.session_state: st.session_state.auto_mode = False

    # --- القائمة الجانبية ---
    with st.sidebar:
        st.header("🎮 تحكم الرادار الآلي")
        # المفتاح السحري لكسر الحلقة المفرغة
        st.session_state.auto_mode = st.toggle("🛰️ تشغيل المسح الآلي المستمر", value=st.session_state.auto_mode)
        
        thermal_on = st.toggle("🌡️ الرؤية الليلية")
        tracks_on = st.toggle("👣 ملاحقة المسارات", value=True)
        
        st.markdown("---")
        if st.session_state.auto_mode:
            st.success("الرادار الآن يقوم بمسح حي كل 10 ثوانٍ...")
        
        if st.button("🗑️ مسح السجل"):
            st.session_state.log_data = []
            st.session_state.threats = []
            st.rerun()

    # --- محرك التحديث الآلي ---
    # إذا تم تفعيل المسح الآلي، يقوم الكود بتحديث البيانات تلقائياً
    if st.session_state.auto_mode:
        import random
        # محاكاة رصد جديد
        new_loc = [random.uniform(19, 25), random.uniform(-2, 9)]
        new_entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "loc": [round(new_loc[0], 2), round(new_loc[1], 2)],
            "type": random.choice(["تحرك مشبوه", "إشارة حرارية", "تسلل حدودي"]),
            "status": "رصد آلي",
            "temp": f"{random.randint(35, 45)}°C"
        }
        st.session_state.threats = [new_entry]
        st.session_state.log_data.insert(0, new_entry)
        # تحديد المسارات المتغيرة آلياً
        st.session_state.dynamic_path = [[19 + random.random(), 3 + random.random()] for _ in range(4)]
        
        # التحديث التلقائي للصفحة (Hack بسيط لـ Streamlit ليعمل كـ Real-time)
        time.sleep(10)
        st.rerun()

    # --- الخريطة والواجهة ---
    if thermal_on:
        st.markdown("<style>.night-vision { filter: sepia(100%) hue-rotate(80deg) saturate(200%) brightness(0.6) contrast(1.2); }</style>", unsafe_allow_html=True)

    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="Esri World Imagery")
    m.add_child(plugins.MeasureControl(position='topleft'))

    # الحدود الوطنية الثابتة
    border = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.0, -8.5], [35.5, -2.0], [36.5, -1.0], [37.5, 2.0], [38.0, 5.0], [37.0, 8.5]]
    folium.PolyLine(border, color="#00FF00" if thermal_on else "yellow", weight=4).add_to(m)

    # المسارات المتغيرة (👣)
    if tracks_on and 'dynamic_path' in st.session_state:
        folium.PolyLine(st.session_state.dynamic_path, color="#00FFFF", weight=3, dash_array='5').add_to(m)

    # التهديدات
    for t in st.session_state.threats:
        folium.Marker(t['loc'], icon=folium.Icon(color='red', icon='circle', prefix='fa')).add_to(m)

    st.title("🛡️ GeoSentinel-DZ | الرصد المباشر")
    with st.container():
        if thermal_on: st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=500, key="radar_map")
        if thermal_on: st.markdown('</div>', unsafe_allow_html=True)

    # سجل النشاطات
    st.markdown("---")
    st.subheader("📋 سجل الرصد الآلي المباشر")
    if st.session_state.log_data:
        st.table(pd.DataFrame(st.session_state.log_data).head(10))
