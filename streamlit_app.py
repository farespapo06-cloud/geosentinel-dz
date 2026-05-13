import streamlit as st
import folium
from streamlit_folium import st_folium
import feedparser

st.set_page_config(page_title="GeoSentinel-DZ Elite", layout="wide")

# --- الواجهة الرئيسية ---
st.title("🛡️ GeoSentinel-DZ: الرصد السيادي")

# --- القائمة الجانبية (نفس تنسيق الصورة 1000046437.jpg مع إضافات) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    
    # 1. المقارنة الزمنية
    st.subheader("🗓️ المقارنة الزمنية")
    time_travel = st.radio("اختر سنة المسح:", ("الوضع الحالي (2026)", "الأرشيف (2020)"))
    
    st.divider()
    
    # 2. رادار التهديدات (إضافة الخوارزميات والربط الاجتماعي)
    st.subheader("🚨 رادار التهديدات")
    threat_detection = st.toggle("تفعيل رصد النقاط المشكوك فيها")
    terror_monitor = st.toggle("رصد نشاط الجماعات الإرهابية والتهريب")
    
    # الإضافات الجديدة المطلوبة:
    social_monitor = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)")
    thermal_view = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")

    if st.button("إجراء مسح شامل الآن"):
        st.write("🔄 جاري تطبيق خوارزميات التهديدات...")

# --- منطق الخريطة والطبقات ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# تفعيل الطبقة الليلية/الحرارية إذا تم اختيارها
if thermal_view:
    folium.TileLayer('CartoDB dark_matter', name='Night/Thermal View').add_to(m)
    st.warning("⚠️ وضع الرؤية الليلية نشط - يتم الآن محاكاة الرصد الحراري.")
else:
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google Satellite', name='Satellite', overlay=False
    ).add_to(m)

# رسم الحدود الوطنية الكاملة
algeria_border = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_border, color="red", weight=5, opacity=1).add_to(m)

# إظهار التهديدات بناءً على خوارزميات الربط الاجتماعي والخبري
if social_monitor:
    # محاكاة لنقاط تم رصدها عبر الأخبار (الطلب رقم 5)
    folium.Marker([22.0, 5.0], popup="تنبيه: نشاط مشبوه رصدته الصحف العالمية", icon=folium.Icon(color='red', icon='rss', prefix='fa')).add_to(m)

st_folium(m, width="100%", height=650)
