import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام الرصد الشامل للحدود الجزائرية")

# 1. الدخول الإجباري للنظام (Authentication)
def start_engine():
    if "GCP_SERVICE_ACCOUNT" in st.secrets:
        try:
            info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
            credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=st.secrets["GCP_SERVICE_ACCOUNT"])
            ee.Initialize(credentials)
            return True
        except Exception as e:
            st.error(f"❌ خلل في تشفير المفتاح: {e}")
            return False
    else:
        st.error("❌ لم يتم العثور على مفتاح التشغيل في Secrets")
        return False

# 2. تشغيل الخريطة فقط إذا تم الاتصال بنجاح
if start_engine():
    st.success("✅ الرادار متصل الآن بكامل الحدود الوطنية")
    
    # جلب حدود الجزائر الرسمية
    algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
    
    # إعداد خريطة الجزائر (مركزة على الهضاب العليا لتشمل الشمال والجنوب)
    m = folium.Map(location=[28.0, 2.0], zoom_start=5)
    
    # رسم الحدود باللون الأحمر لمنع أي تداخل
    folium.GeoJson(
        algeria.getInfo(),
        style_function=lambda x: {'fillColor': 'none', 'color': 'red', 'weight': 4},
        name="الحدود الجزائرية"
    ).add_to(m)
    
    st_folium(m, width="100%", height=700)
