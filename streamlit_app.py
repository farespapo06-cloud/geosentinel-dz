import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# 2. الحفاظ على البيانات حتى عند الوميض
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. دالة الخريطة - ثابتة تماماً (Static)
@st.cache_resource
def get_map():
    # استخدام خريطة بسيطة وسريعة التحميل
    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tiles, attr="Esri")
    return m

with st.sidebar:
    st.title("🛡️ رصد الحدود")
    if st.button("🛰️ مسح إضافي (تراكمي)"):
        # إضافة هدف واحد جديد في كل مرة لتقليل الضغط
        new_lat = random.uniform(22.0, 26.0)
        new_lon = random.uniform(2.0, 6.0)
        st.session_state.all_detections.append([new_lat, new_lon])
        st.rerun()
    
    if st.button("🗑️ تنظيف الخريطة"):
        st.session_state.all_detections = []
        st.rerun()

# 4. بناء الخريطة مع الأهداف بدون إعادة تحميل Tiles
m = get_map()

# إضافة الأهداف الحالية من الجلسة
for point in st.session_state.all_detections:
    folium.CircleMarker(
        location=point,
        radius=8,
        color="red",
        fill=True,
        fill_color="yellow",
        popup="Target Detected"
    ).add_to(m)

# السر هنا: استخدام key ثابت ومنع الـ return_on_hover لتقليل التواصل مع السيرفر
st_folium(
    m, 
    width="100%", 
    height=550, 
    key="fixed_geo_map", 
    returned_objects=[] # هذا يمنع التحديث عند تحريك الخريطة باللمس
)

# عرض الجدول أسفل الخريطة (كما في صورك)
if st.session_state.all_detections:
    st.write(f"✅ تم تثبيت {len(st.session_state.all_detections)} أهداف على الرادار.")
# إضافة سجل نصي أسفل الخريطة لتوثيق الأهداف المرصودة تراكمياً
import pandas as pd

if st.session_state.all_detections:
    st.markdown("### 📜 سجل الرصد الاستخباراتي")
    # تحويل البيانات إلى جدول منظم
    df = pd.DataFrame(st.session_state.all_detections, columns=['Latitude', 'Longitude'])
    df['Status'] = 'Active Scan'
    st.table(df) # يعرض الأهداف بشكل ثابت ومنظم
    
