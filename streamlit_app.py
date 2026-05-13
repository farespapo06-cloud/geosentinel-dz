import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة التطبيق
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام مراقبة الحدود - برج باجي مختار")

# إحداثيات المنطقة (برج باجي مختار)
m = folium.Map(location=[21.328, 0.924], zoom_start=10)
folium.Marker([21.328, 0.924], popup="نقطة مراقبة حدودية").add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=600)
import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة التطبيق
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل للحدود الوطنية الجزائرية")

# إنشاء الخريطة مع تفعيل خيار القمر الصناعي
# سنبدأ بالخريطة العادية ونضيف خيار التبديل (LayerControl)
m = folium.Map(location=[28.0, 2.0], zoom_start=5, control_scale=True)

# إضافة طبقة القمر الصناعي (Google Satellite)
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google',
    name='القمر الصناعي (Satellite)',
    overlay=False,
    control=True
).add_to(m)

# إضافة طبقة الخريطة العادية
folium.TileLayer('OpenStreetMap', name='الخريطة العادية').add_to(m)

# جلب حدود الجزائر (GeoJSON) ورسمها بخط أحمر
# هذا الرابط يحتوي على إحداثيات حدود الجزائر بدقة
algeria_border_url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries/DZA.geojson"

folium.GeoJson(
    algeria_border_url,
    name="الحدود الوطنية",
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'red',
        'weight': 4,
        'opacity': 0.7
    }
).add_to(m)

# إضافة علامة برج باجي مختار كما في الصورة 1000046421.jpg
folium.Marker(
    [21.328, 0.924], 
    popup="قطاع برج باجي مختار",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# إضافة أداة التحكم للتبديل بين القمر الصناعي والخريطة العادية
folium.LayerControl(position='topright').add_to(m)

# عرض الخريطة بكامل عرض الشاشة
st_folium(m, width="100%", height=700)
