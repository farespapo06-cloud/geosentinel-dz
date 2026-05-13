import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة النظام
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل - الحدود الوطنية والأقمار الصناعية")

# إنشاء الخريطة (مركزة على الجزائر)
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# 1. إضافة طبقة القمر الصناعي (Google Hybrid) لرؤية الأرض والأسماء معاً
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='رؤية القمر الصناعي (Hybrid)',
    overlay=False,
    control=True
).add_to(m)

# 2. رسم الحدود الرسمية للجزائر (الخط الأحمر المتعرج الدقيق)
# ملاحظة: هذا الرابط يوفر إحداثيات الحدود الجزائرية الرسمية بدقة عالية
algeria_border_geojson = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries/DZA.geojson"

try:
    folium.GeoJson(
        algeria_border_geojson,
        name="الحدود الوطنية الجزائرية",
        style_function=lambda x: {
            'fillColor': 'none',
            'color': '#FF0000', # أحمر فاقع
            'weight': 4,
            'opacity': 1
        }
    ).add_to(m)
except:
    st.warning("تنبيه: جاري جلب تفاصيل الحدود الرسمية من قاعدة البيانات...")

# 3. تثبيت نقطة الرصد في برج باجي مختار (كما ظهرت في الصورة 1000046424.jpg)
folium.Marker(
    [21.328, 0.924], 
    popup="نقطة مراقبة: قطاع برج باجي مختار",
    icon=folium.Icon(color='red', icon='eye-open')
).add_to(m)

# 4. أداة التبديل بين الطبقات
folium.LayerControl(position='topright').add_to(m)

# عرض الخريطة النهائية
st_folium(m, width="100%", height=700)
