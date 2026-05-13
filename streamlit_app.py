import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# إعداد الصفحة وتصميم الواجهة
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | المركز الوطني للرصد")

# إدارة حالة التهديدات لضمان بقائها عند تحديث الصفحة
if 'threats' not in st.session_state:
    st.session_state.threats = []

# --- القائمة الجانبية (Sidebar) مطابقة لصورك الأخيرة ---
with st.sidebar:
    st.title("🛡️ نظام GeoSentinel")
    st.header("أجهزة الرصد المتقدمة")
    
    radar_scan = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)", value=True)
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية", value=True)
    
    st.markdown("---")
    
    # تنفيذ المسح الاستخباراتي الشامل
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        # توليد نقاط تهديد استراتيجية على الحدود البرية والبحرية
        st.session_state.threats = [
            {"loc": [21.32, 0.95], "type": "تحرك بري مشبوه - برج باجي مختار", "icon": "truck"},
            {"loc": [25.10, 9.10], "type": "نشاط غير قانوني - جانت", "icon": "user-secret"},
            {"loc": [37.20, 7.50], "type": "هدف بحري م
