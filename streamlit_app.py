import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة التطبيق
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل للحدود الوطنية الجزائرية")

# إنشاء الخريطة (مركزة على وسط الجزائر لرؤية الحدود كاملة)
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# 1. إضافة طبقة القمر الصناعي الاحترافية
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='رؤية القمر الصناعي',
    overlay=False,
    control=True
).add_to(m)

# 2. إضافة طبقة الخريطة العادية كخيار ثانٍ
folium.TileLayer('OpenStreetMap', name='الخريطة العادية').add_to(m)

# 3. حل مشكلة الصورة 1000046422.jpg: رسم الحدود الوطنية
# استخدمنا إحداثيات مبسطة وموثوقة لضمان عدم حدوث خطأ JSON
algeria_border = [[37.0, -2.0], [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.5, 5.0], [21.0, -4.5], [27.5, -8.5], [35.0, -2.0]]

folium.PolyLine(
    locations=algeria_border,
    color="red",
    weight=5,
    opacity=0.8,
    tooltip="الحدود الوطنية الجزائرية"
).add_to(m)

# 4. علامة قطاع برج باجي مختار
folium.Marker(
    [21.328, 0.924], 
    popup="قطاع برج باجي مختار العملياتي",
    icon=folium.Icon(color='red', icon='screenshot')
).add_to(m)

# 5. أداة التبديل بين القمر الصناعي والخريطة (في أعلى اليمين)
folium.LayerControl().add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=700)
