import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
import re

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

def deep_clean_json(text):
    """حذف الرمز 147 وأي رموز تحكم مخفية تظهر في الصور"""
    if not isinstance(text, str):
        text = json.dumps(text)
    # حذف الرموز غير المرئية ورموز UTF-8 المزعجة
    clean = re.sub(r'[^\x20-\x7E]', '', text)
    return clean

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # قراءة وتطهير المفتاح
        raw_input = st.secrets["GCP_SERVICE_ACCOUNT"]
        cleaned_json = deep_clean_json(raw_input)
        
        # تحويل النص النظيف إلى JSON
        info = json.loads(cleaned_json)
        
        # تهيئة الاتصال بمحرك Google Earth
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=cleaned_json)
        ee.Initialize(credentials)
        
        st.success("✅ تم تطهير النظام وتفعيل رادار الحدود الوطنية")

        # جلب ورسم حدود الجزائر كاملة
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5},
            name="الحدود الوطنية"
        ).add_to(m)
        
        st_folium(m, width="100%", height=700)
        
    except Exception as e:
        st.error(f"❌ خطأ تقني مستمر: {e}")
else:
    st.info("الرجاء إدخال المفتاح في قسم Secrets لتشغيل الرادار")
