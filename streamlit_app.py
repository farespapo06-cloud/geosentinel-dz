import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
import re

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

# وظيفة لتطهير البيانات من الرموز التي ظهرت في الصورة 1000046409.jpg
def sanitize_key(text):
    if not isinstance(text, str):
        text = json.dumps(text)
    # حذف الرمز 147 والرموز غير المرئية الأخرى
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        raw_key = st.secrets["GCP_SERVICE_ACCOUNT"]
        clean_key = sanitize_key(raw_key)
        
        info = json.loads(clean_key)
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=clean_key)
        ee.Initialize(credentials)
        
        st.success("✅ تم تفعيل المسح الشامل للحدود الوطنية")

        # جلب حدود الجزائر كاملة ورسمها باللون الأحمر العريض
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 6},
            name="الحدود الجزائرية"
        ).add_to(m)
        
        st_folium(m, width="100%", height=700)
        
    except Exception as e:
        st.error(f"❌ خطأ تقني في المفتاح: {e}")
else:
    st.info("الرجاء إدخال المفتاح في قسم Secrets لتشغيل الرادار")
