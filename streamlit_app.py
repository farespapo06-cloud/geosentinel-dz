import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
import re

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

def clean_json_string(raw_str):
    # إزالة أي حرف ليس رقماً أو حرفاً إنجليزياً أو رمزاً برمجياً أساسياً
    # هذا يقتل الرمز 148 الظاهر في الصورة 1000046418.jpg فوراً
    printable = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[{]};:\'",<.>/? \n\r\t')
    return ''.join(filter(lambda x: x in printable, raw_str))

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        # استلام النص وتنظيفه من "مخلفات" النسخ واللصق
        raw_input = st.secrets["GCP_SERVICE_ACCOUNT"]
        if isinstance(raw_input, dict):
            raw_input = json.dumps(raw_input)
            
        cleaned_json = clean_json_string(raw_input)
        
        # تحويل النص المنظف إلى قاموس برمجياً
        info = json.loads(cleaned_json)
        
        # تسجيل الدخول إلى Google Earth Engine
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=cleaned_json)
        ee.Initialize(credentials)
        
        st.success("✅ تم تطهير النظام بنجاح وتفعيل رصد الحدود")

        # رسم الخريطة الرسمية للحدود الجزائرية
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5},
            name="حدود الجمهورية الجزائرية"
        ).add_to(m)
        
        st_folium(m, width="100%", height=600)

    except Exception as e:
        st.error(f"❌ خطأ تقني مستمر في البيانات: {e}")
else:
    st.info("يرجى وضع المفتاح في إعدادات Secrets لتشغيل النظام")
