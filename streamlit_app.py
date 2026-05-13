import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

# 1. التحقق من المفتاح السري
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
        ee.Initialize(credentials)
        st.success("✅ Connected to Earth Engine")
    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.error("❌ Key not found in Secrets")

# 2. إعداد الخريطة لبرج باجي مختار
lat, lon = 21.328, 0.924
m = folium.Map(location=[lat, lon], zoom_start=12)

# إضافة علامة الرصد
folium.Marker(
    [21.335, 0.930], 
    popup="New Activity Detected",
    icon=folium.Icon(color='red')
).add_to(m)

# 3. عرض الخريطة
st_folium(m, width=700, height=500)
