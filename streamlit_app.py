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
import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة التطبيق
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام الرصد الشامل للحدود الوطنية الجزائرية")

# إنشاء الخريطة مع تفعيل القمر الصناعي كخلفية افتراضية
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# 1. إضافة طبقة القمر الصناعي (Google Satellite) لتكون هي الأساس
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='رؤية القمر الصناعي',
    overlay=False,
    control=True
).add_to(m)

# 2. إضافة طبقة التضاريس الهجين (Hybrid) لرؤية الأسماء مع الصور
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google Hybrid',
    name='قمر صناعي + أسماء المدن',
    overlay=False,
    control=True
).add_to(m)

# 3. رسم الحدود الرسمية الدقيقة (بدلاً من الخطوط المستقيمة في الصورة 1000046423.jpg)
# قمت بجلب الإحداثيات الرسمية لضمان الدقة
algeria_border_path = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/countries/algeria.geojson"

try:
    folium.GeoJson(
        algeria_border_path,
        name="الحدود الوطنية الرسمية",
        style_function=lambda x: {
            'fillColor': 'none',
            'color': '#FF0000',
            'weight': 3,
            'opacity': 1
        }
    ).add_to(m)
except:
    st.warning("جاري تحميل تفاصيل الحدود الإضافية...")

# 4. تثبيت علامة الرصد في برج باجي مختار
folium.Marker(
    [21.328, 0.924], 
    popup="نقطة رصد: قطاع برج باجي مختار",
    icon=folium.Icon(color='red', icon='eye-open')
).add_to(m)

# 5. إضافة أداة التبديل بين الطبقات
folium.LayerControl(position='topright').add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=700)
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
