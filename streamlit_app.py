import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import requests

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# تخصيص مظهر شريط التنبيهات الجانبي
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظيفة جلب بيانات الرادار (مع معالجة الأخطاء) ---
def get_flight_data():
    url = "https://opensky-network.org/api/states/all"
    # إحداثيات الجزائر للتصفية
    params = {'lamin': 18.9, 'lomin': -8.7, 'lamax': 37.1, 'lomax': 12.0}
    try:
        # قمنا بزيادة المهلة إلى 20 ثانية لتجنب الخطأ في الصورة 1000046494.jpg
        response = requests.get(url, params=params, timeout=20)
        if response.status_code == 200:
            return response.json().get('states', [])
    except Exception:
        # في حال فشل الاتصال، لا تظهر الخطأ الأحمر، بل أعد قائمة فارغة
        return None
    return []

# --- 3. الشريط الجانبي (أدوات الرصد المتقدمة) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    st.subheader("🗓️ المقارنة الزمنية")
    time_analysis = st.radio("نطاق البحث:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري (10 سنوات)"])
    
    st.divider()
    st.subheader("🚨 رادار التهديدات")
    osint_active = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)", value=True)
    radar_active = st.toggle("✈️🚢 رصد الملاحة الجوية والبحرية", value=True)
    thermal_active = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")
    
    if st.button("إجراء مسح شامل الآن"):
        st.toast("جاري تحديث البيانات الجغرافية...")

# --- 4. بناء العنوان والخريطة ---
st.title(f"🛡️ GeoSentinel-DZ | Live: {datetime.now().strftime('%H:%M:%S')}")

# إحداثيات مركزية (Bordj Badji Mokhtar وما حولها)
m = folium.Map(location=[24.0, 5.0], zoom_start=5, tiles="CartoDB dark_matter")

# رسم حدود النطاق الأحمر (كما في صورك السابقة)
boundary_coords = [[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]]
folium.PolyLine(boundary_coords, color="red", weight=3, opacity=0.8).add_to(m)

# --- 5. تشغيل الرادار وحماية التطبيق من الانهيار ---
if radar_active:
    flights = get_flight_data()
    if flights:
        for flight in flights:
            lat, lon = flight[6], flight[5]
            if lat and lon:
                folium.Marker(
                    location=[lat, lon],
                    popup=f"Flight: {flight[1]}",
                    icon=folium.Icon(color="blue", icon="plane", prefix="fa")
                ).add_to(m)
    elif flights is None:
        # عرض تنبيه هادئ بدلاً من الخطأ الضخم في الصورة 1000046494.jpg
        st.sidebar.warning("⚠️ خادم OpenSky لا يستجيب حالياً. جاري العرض بدون بيانات الرادار.")

# إضافة نقاط افتراضية للتهديدات (OSINT) لمحاكاة صورك الأصلية
if osint_active:
    folium.Marker(
        location=[22.5, 3.5], 
        popup="🚨 OSINT: تحرك حدودي مشبوه",
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
    ).add_to(m)

# --- 6. عرض الخريطة ---
st_folium(m, width="100%", height=600)

# تحديث تلقائي هادئ
time.sleep(30)
st.rerun()
