import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")
st.title("🛡️ نظام رصد الحدود الجزائرية الشامل")

if "GCP_SERVICE_ACCOUNT" in st.secrets:
    try:
        secret_data = st.secrets["GCP_SERVICE_ACCOUNT"]
        
        # حل مشكلة الصورة 1000046413.jpg (تحويل القاموس إلى نص)
        if isinstance(secret_data, dict):
            json_key = json.dumps(secret_data)
        else:
            json_key = str(secret_data)

        # تهيئة النظام
        info = json.loads(json_key)
        credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=json_key)
        ee.Initialize(credentials)
        
        st.success("✅ تم تفعيل الرادار وتغطية كامل الحدود الوطنية")

        # جلب الحدود الجزائرية كاملة من قاعدة البيانات الرسمية
        algeria = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', 'Algeria'))
        
        # إعداد الخريطة لتشمل كامل القطر الوطني
        m = folium.Map(location=[28.0, 2.0], zoom_start=5)
        
        # رسم الحدود باللون الأحمر العريض لتكون واضحة
        folium.GeoJson(
            algeria.getInfo(),
            style_function=lambda x: {'fillColor': '#ff000011', 'color': 'red', 'weight': 5},
            name="الحدود الجزائرية"
        ).add_to(m)
        
        st_folium(m, width="100%", height=600)

    except Exception as e:
        st.error(f"❌ خطأ تقني في قراءة المفتاح: {e}")
else:
    st.info("الرجاء التأكد من حفظ المفتاح في قسم Secrets")
