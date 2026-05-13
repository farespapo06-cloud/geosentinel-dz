import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام مراقبة الحدود الجزائرية (2020-2026)")

# الاتصال بمشروع GeoSentinel-DZ
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.success("✅ تم تفعيل الرادار الحدودي بنجاح")
    except Exception as e:
        st.error(f"❌ خطأ في المفتاح: {e}")

# جلب حدود الجزائر كاملة ورسمها
algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5, tiles="CartoDB positron")

# رسم الخط الحدودي الوطني باللون الأحمر العريض
folium.GeoJson(
    algeria.getInfo(),
    style_function=lambda x: {'fillColor': '#ff000022', 'color': 'red', 'weight': 4},
    name="الحدود الوطنية الجزائرية"
).add_to(m)

# عرض الخريطة الشاملة
st_folium(m, width="100%", height=700)
