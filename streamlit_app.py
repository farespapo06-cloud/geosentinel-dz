import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل - قمر صناعي + حدود وطنية")

# إحداثيات مركز الخريطة (الجزائر)
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# طبقة القمر الصناعي الأساسية
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google',
    name='رؤية القمر الصناعي (Hybrid)',
    overlay=False,
    control=True
).add_to(m)

# حدود الجزائر الرسمية
algeria_border_url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries/DZA.geojson"

try:
    folium.GeoJson(
        algeria_border_url,
        name="الحدود الوطنية",
        style_function=lambda x: {'color': 'red', 'weight': 4, 'fillColor': 'none'}
    ).add_to(m)
except:
    st.error("تنبيه: تأكد من اتصال الإنترنت لجلب إحداثيات الحدود")

# نقطة رصد برج باجي مختار (كما في الصورة 1000046421.jpg)
folium.Marker(
    [21.328, 0.924], 
    popup="برج باجي مختار",
    icon=folium.Icon(color='red', icon='eye-open')
).add_to(m)

folium.LayerControl().add_to(m)

# عرض الخريطة - تأكد من نسخ هذا السطر الأخير كاملاً
st_folium(m, width="100%", height=700)
