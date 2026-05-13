import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
import re

# إعدادات الواجهة
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام رصد الحدود الجزائرية الشامل")

def clean_json_string(json_str):
    """حذف الرموز المخفية التي تسبب أعطالاً في الهواتف"""
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str)

# محاولة الاتصال بالنظام
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        raw_key = st.secrets["GCP_SERVICE_ACCOUNT"]
        clean_key = clean_json_string(raw_key)
        info = json.loads(clean_key)
        
        # تسجيل الدخول لـ Google Earth Engine
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=clean_key)
        ee.Initialize(credentials)
        st.success("✅ الرادار متصل الآن بنطاق الحدود الوطنية")

        # جلب حدود الجزائر بالكامل
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        # إنشاء الخريطة (مركزة على الجزائر)
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        
        # رسم الحدود باللون الأحمر
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5},
            name="الحدود الجزائرية"
        ).add_to(m)
        
        # عرض الخريطة
        st_folium(m, width="100%", height=700)
        
    except Exception as e:
        st.error(f"❌ خطأ في الإعدادات: {e}")
else:
    st.warning("الرجاء إضافة المفتاح السري في إعدادات Secrets لتفعيل النظام.")
        
