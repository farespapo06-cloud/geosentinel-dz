import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # حل مشكلة الصورة 1000046408.jpg
        # نحول البيانات إلى نص بصيغة JSON لكي يقبلها النظام كـ Bytes
        secret_data = st.secrets["GCP_SERVICE_ACCOUNT"]
        
        # إذا كانت البيانات قادمة كقاموس، نحولها لنص
        if isinstance(secret_data, dict):
            json_key = json.dumps(secret_data)
        else:
            json_key = str(secret_data)

        info = json.loads(json_key)
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=json_key)
        ee.Initialize(credentials)
        
        st.success("✅ تم تفعيل الرادار الحدودي بنجاح")

        # رسم كامل الحدود الجزائرية
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5}
        ).add_to(m)
        
        st_folium(m, width="100%", height=600)

    except Exception as e:
        st.error(f"❌ خطأ تقني: {e}")
else:
    st.warning("الرجاء إضافة المفتاح في Secrets")
