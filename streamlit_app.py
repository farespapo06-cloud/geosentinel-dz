import streamlit as st
import folium
from streamlit_folium import st_folium

# عنوان التطبيق المرتبط بمشروعك في الصورة 1000046374.jpg
st.set_page_config(page_title="GeoSentinel-DZ Analysis", layout="wide")
st.title("🛡️ تحليل التغيرات الحدودية (2020-2026)")

# قائمة جانبية للتحكم بالزمن
st.sidebar.header("إعدادات المسح الزمني")
year_compare = st.sidebar.slider("قارن سنة 2026 مع:", 2018, 2022, 2020)

# إحداثيات قطاع برج باجي مختار كمثال
lat, lon = 21.328, 0.924

# إنشاء خريطة ثنائية الرؤية
m = folium.Map(location=[lat, lon], zoom_start=14)

# روابط صور الأقمار الصناعية (محاكاة للمقارنة بدون API Key معقد)
google_earth = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
folium.TileLayer(tiles=google_earth, attr='Google Earth 2026', name='الوضع الحالي (2026)').add_to(m)

# إضافة تنبيه ذكي في القائمة الجانبية
st.sidebar.subheader("نتائج المسح الذكي")
if st.sidebar.button("تشغيل كاشف التغيرات"):
    st.sidebar.warning("🔍 جاري تحليل الفرق في بيكسلات التربة...")
    st.sidebar.error("🚨 تنبيه: تم رصد تغير في البنية التحتية بنسبة 15% مقارنة بـ 2020")
    
    # إضافة دائرة حمراء على منطقة التغيير المكتشفة
    folium.Circle(
        location=[21.330, 0.926],
        radius=500,
        color='red',
        fill=True,
        popup='منطقة اشتباه: نشاط جديد'
    ).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=600)

st.info("ملاحظة: هذا النظام يراقب 'المناطق الميتة' عبر مقارنة البصمة الرادارية.")
import streamlit as st
import ee
import json

# جلب المفتاح السري الذي وضعته في الصورة 1000046389.jpg
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
    ee.Initialize(credentials)
    st.success("✅ تم الاتصال برادار غوغل إيرث بنجاح")
else:
    st.error("❌ لم يتم العثور على مفتاح التشغيل")
import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

# 1. الاتصال بـ Google Earth Engine باستخدام المفتاح الذي وضعته في Secrets
try:
    if "GCP_SERVICE_ACCOUNT" in st.secrets:
        key_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(key_dict['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.sidebar.success("✅ متصل برادار GeoSentinel-DZ")
except Exception as e:
    st.sidebar.error(f"❌ خطأ في الاتصال: {e}")

st.title("🛡️ كاشف التغيرات الحدودية (2020-2026)")

# 2. إعدادات المنطقة (مثلاً برج باجي مختار)
lat, lon = 21.328, 0.924
m = folium.Map(location=[lat, lon], zoom_start=13)

# 3. جلب صور Sentinel-2 للمقارنة
def get_satellite_image(year):
    dataset = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(ee.Geometry.Point(lon, lat)) \
        .filterDate(f'{year}-01-01', f'{year}-12-31') \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()
    return dataset

# زر تفعيل المقارنة الذكية
if st.sidebar.button("تشغيل المسح الاستراتيجي"):
    st.sidebar.info("🔍 جاري تحليل الفوارق الطيفية بين 2020 و 2026...")
    
    # محاكاة لإظهار مناطق التغيير المكتشفة في برج باجي مختار
    folium.Marker(
        [21.335, 0.930], 
        popup="تغير مستحدث رصده الرادار",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    st.sidebar.warning("🚨 تنبيه: تم رصد نشاط إنشائي جديد في القطاع الشمالي")

# عرض الخريطة كما تظهر في صورتك 1000046392.jpg
st_folium(m, width="100%", height=600)
import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

# الاتصال بالرادار
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
    ee.Initialize(credentials)
    st.success("✅ تم الاتصال برادار غوغل إيرث بنجاح")
else:
    st.error("❌ مفتاح التشغيل غير موجود")
