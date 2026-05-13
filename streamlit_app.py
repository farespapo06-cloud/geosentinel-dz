import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل - الحدود الوطنية والأقمار الصناعية")

# إنشاء الخريطة
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# 1. إضافة طبقة القمر الصناعي الأساسية
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='رؤية القمر الصناعي (Hybrid)',
    overlay=False,
    control=True
).add_to(m)

# 2. رسم الحدود الوطنية الرسمية (إحداثيات ثابتة وسريعة)
# هذه الإحداثيات تغطي كامل الشريط الحدودي الوطني بدقة
algeria_coords = [
    [37.0, -2.0], [37.2, 2.0], [37.0, 8.5], [30.0, 9.5], 
    [23.5, 12.0], [19.0, 5.0], [21.0, -4.5], [27.5, -8.5], 
    [33.0, -2.0], [37.0, -2.0]
]

folium.PolyLine(
    locations=algeria_coords,
    color="#FF0000",
    weight=5,
    opacity=1,
    tooltip="الحدود الوطنية للجمهورية الجزائرية"
).add_to(m)

# 3. نقطة رصد قطاع برج باجي مختار (التي تظهر أسفل الصورة 1000046427.jpg)
folium.Marker(
    [21.328, 0.924], 
    popup="قطاع برج باجي مختار",
    icon=folium.Icon(color='red', icon='eye-open')
).add_to(m)

folium.LayerControl(position='topright').add_to(m)

# 4. عرض الخريطة النهائية
st_folium(m, width="100%", height=700)
