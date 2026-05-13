import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide", page_title="الرادار الحدودي الجزائري")

# الاتصال بنظام GeoSentinel-DZ
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # قراءة البيانات مع ضمان عدم وجود أخطاء في التنسيق
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.sidebar.success("✅ النظام متصل بكامل الحدود")
    except Exception as e:
        st.sidebar.error(f"❌ خلل في تنسيق المفتاح: {e}")

st.title("🛡️ نظام المسح الشامل للحدود الجزائرية")

# جلب ورسم حدود الجزائر بالكامل
algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))

# إعداد الخريطة لتشمل النطاق الوطني من تندوف إلى إن قزام
m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles="OpenStreetMap")

# رسم الخط الحدودي الوطني بلون أحمر بارز
folium.GeoJson(
    algeria.getInfo(),
    style_function=lambda x: {'fillColor': '#00ff0005', 'color': 'red', 'weight': 5},
    name="الحدود الوطنية"
).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=700)
