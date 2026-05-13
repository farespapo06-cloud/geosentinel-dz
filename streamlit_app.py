import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية (2020-2026)")

# التأكد من وجود المفتاح
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # تحويل النص إلى قاموس برمجياً
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.success("✅ تم الاتصال بنجاح")

        # رسم كامل الحدود الجزائرية
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        folium.GeoJson(algeria.getInfo(), style_function=lambda x: {'color': 'red', 'weight': 4}).add_to(m)
        
        st_folium(m, width="100%", height=600)
    except Exception as e:
        st.error(f"❌ خطأ في التنسيق داخل Secrets: {e}")
