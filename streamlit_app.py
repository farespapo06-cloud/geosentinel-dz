import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
import re

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

# ضع بياناتك هنا مباشرة لنتجاوز خطأ السطر 5
KEY_DATA = """
{
  "type": "service_account",
  "project_id": "static-lens-496201-p5",
  "private_key_id": "......",
  "private_key": "-----BEGIN PRIVATE KEY-----\n......\n-----END PRIVATE KEY-----\n",
  "client_email": "......",
  "client_id": "......",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "......"
}
"""

def start_system():
    try:
        # تنظيف آلي لأي رموز مخفية مثل الرمز 147
        clean_key = re.sub(r'[^\x20-\x7E\n]', '', KEY_DATA)
        info = json.loads(clean_key)
        
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=clean_key)
        ee.Initialize(credentials)
        return True
    except Exception as e:
        st.error(f"❌ خلل فني: {e}")
        return False

if start_system():
    st.success("✅ تم تفعيل الرادار وتغطية كامل الحدود الوطنية")

    # جلب الحدود الجزائرية كاملة
    algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
    
    m = folium.Map(location=[28.0, 2.0], zoom_start=5)
    
    folium.GeoJson(
        algeria.getInfo(),
        style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5},
        name="الحدود الوطنية"
    ).add_to(m)
    
    st_folium(m, width="100%", height=700)
