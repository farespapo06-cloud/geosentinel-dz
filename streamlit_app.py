import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime

# إعدادات الصفحة لتطابق الصورة 1000046567.jpg
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ")

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🚨 أنظمة الرصد المتقدمة")
    
    # مفاتيح التشغيل (Switches) كما في الصورة
    radar_scan = st.toggle("🛰️ رادار مسح الحدود (مطارات/خنادق)")
    thermal_detect = st.toggle("🌡️ كشف ليلي حراري (مركبات كهربائية)")
    track_hidden = st.toggle("👣 ملاحقة المسارات المخفية")
    
    st.markdown("---")
    
    # زر الإجراء الاستخباراتي
    if st.button("🔍 إجراء مسح استخباراتي شامل"):
        st.info("جاري تحليل المنطقة وجمع البيانات الحديثة...")

# --- منطق الخريطة والبيانات ---
# التركيز على إحداثيات مشابهة لما يظهر في الخريطة بالصورة
center = [28.0339, 1.6596] # إحداثيات عامة للجزائر
m = folium.Map(location=center, zoom_start=5, tiles="Esri World Imagery")

# إضافة تأثيرات بناءً على الاختيارات في الصورة 1000046567.jpg
if radar_scan:
    # إضافة دوائر المسح الراداري
    folium.Circle(
        location=[24.0, 2.0],
        radius=200000,
        color="cyan",
        fill=True,
        fill_opacity=0.2,
        popup="نطاق مسح الرادار"
    ).add_to(m)

if thermal_detect:
    # إضافة نقاط حرارية افتراضية
    folium.Marker(
        location=[26.0, 1.0],
        icon=folium.Icon(color='red', icon='fire', prefix='fa'),
        popup="تنبيه: بصمة حرارية مكتشفة"
    ).add_to(m)

if track_hidden:
    # رسم مسارات مخفية (خطوط متقطعة)
    points = [[22.0, 0.5], [24.0, 1.5], [26.0, 1.0]]
    folium.PolyLine(points, color="purple", weight=3, opacity=0.8, dash_array='5').add_to(m)

# --- عرض الخريطة ---
st.subheader("خريطة الرصد العملياتي")
st_folium(m, width="100%", height=600)

# إضافة زر الطيران وربطه كما طلبتم سابقاً
if st.sidebar.button("✈️ ربط الطيران (FlightRadar24)"):
    st.sidebar.markdown(f"[اضغط هنا لفتح الرادار المباشر](https://www.flightradar24.com/28.03,1.66/6)")
