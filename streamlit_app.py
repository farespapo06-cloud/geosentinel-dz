import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

# 1. الاتصال برادار غوغل إيرث
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # قراءة المفتاح الذي وضعته في الإعدادات
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.success("✅ Connected to GeoSentinel Engine")
    except Exception as e:
        st.error(f"❌ JSON Key Error: {e}")
else:
    st.error("❌ Secret Key Missing")

# 2. إعداد خريطة منطقة برج باجي مختار
lat, lon = 21.328, 0.924
m = folium.Map(location=[lat, lon], zoom_start=12)

# إضافة نقطة الرصد في الموقع المحدد
folium.Marker(
    [21.335, 0.930], 
    popup="Monitoring Site",
    icon=folium.Icon(color='red')
).add_to(m)

# 3. عرض الخريطة
st_folium(m, width=700, height=500)
