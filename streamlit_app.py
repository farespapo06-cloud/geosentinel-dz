import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

# 1. الاتصال بمحرك غوغل إيرث
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.success("✅ GeoSentinel-DZ: متصل بنظام الأقمار الصناعية")
    except Exception as e:
        st.error(f"❌ خطأ في قراءة المفتاح: {e}")
else:
    st.error("❌ المفتاح السري مفقود في Secrets")

st.title("🛡️ نظام مراقبة الحدود الجزائرية (2020-2026)")

# 2. تحديد حدود الجزائر كاملة من قاعدة بيانات غوغل
algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))

# 3. إعداد الخريطة لتشمل كامل الجزائر
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# رسم الحدود الوطنية باللون الأحمر
folium.GeoJson(
    algeria.getInfo(),
    style_function=lambda x: {'fillColor': 'none', 'color': 'red', 'weight': 3},
    name="الحدود الوطنية"
).add_to(m)

# 4. إضافة طبقة صور Sentinel-2 للمقارنة (تغطية شاملة)
st.sidebar.header("إعدادات الرادار")
year = st.sidebar.select_slider("اختر السنة للمسح:", options=[2020, 2026], value=2026)

st_folium(m, width="100%", height=600)
