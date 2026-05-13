import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        secret_content = st.secrets["GCP_SERVICE_ACCOUNT"]
        
        # علاج مشكلة الصورة 1000046416.jpg
        # إذا وصل المفتاح كقاموس، نحوله لنص JSON
        if isinstance(secret_content, dict):
            json_key = json.dumps(secret_content)
        else:
            json_key = str(secret_content)

        # تحويل النص لقاموس للتحقق، ثم استخدامه في تسجيل الدخول
        info = json.loads(json_key)
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=json_key)
        ee.Initialize(credentials)
        
        st.success("✅ تم تفعيل الرادار الحدودي بنجاح")

        # جلب الحدود الجزائرية كاملة من قاعدة بيانات LSIB
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        # خريطة تغطي كامل القطر الوطني
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        
        # رسم الحدود باللون الأحمر العريض (السمك: 5)
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000005', 'color': 'red', 'weight': 5},
            name="الحدود الوطنية الجزائرية"
        ).add_to(m)
        
        # عرض الخريطة لتملأ الشاشة
        st_folium(m, width="100%", height=600)

    except Exception as e:
        st.error(f"❌ خلل في قراءة البيانات: {e}")
else:
    st.info("الرجاء التأكد من وجود المفتاح في إعدادات Secrets")
