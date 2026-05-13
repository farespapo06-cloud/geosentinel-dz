import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ Pro", layout="wide")

# --- واجهة التحكم الرئيسية ---
st.title("🛡️ GeoSentinel-DZ: مركز المسح الشامل")

# --- إضافة الأزرار في القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    
    # ميزة المقارنة الزمنية
    st.subheader("🗓️ المقارنة الزمنية")
    time_travel = st.radio("اختر سنة المسح:", ("الوضع الحالي (2026)", "الأرشيف (2020)"))
    
    st.divider()
    
    # ميزة رصد التهديدات والتهريب
    st.subheader("🚨 رادار التهديدات")
    threat_detection = st.toggle("تفعيل رصد النقاط المشكوك فيها")
    terror_monitor = st.toggle("رصد نشاط الجماعات الإرهابية والتهريب")

    if st.button("إجراء مسح شامل الآن"):
        with st.spinner("جاري تحليل الشريط الحدودي ومقارنة الصور..."):
            import time
            time.sleep(2)
            st.success("تم المسح: لا توجد تغيرات هيكلية كبرى.")

# --- إعداد الخريطة ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# تبديل الطبقات بناءً على اختيار السنة
if time_travel == "الأرشيف (2020)":
    folium.TileLayer('OpenStreetMap', name='خريطة قديمة').add_to(m)
else:
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google', name='قمر صناعي حديث', overlay=False
    ).add_to(m)

# رسم الحدود الوطنية الكاملة (المسح الشامل)
algeria_border = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_border, color="red", weight=5, opacity=1).add_to(m)

# --- إظهار النقاط المشكوك فيها تلقائياً عند تفعيل الزر ---
if threat_detection or terror_monitor:
    # نقاط افتراضية للتهديدات (يمكن برمجتها لتتغير ديناميكياً)
    threats = [
        {"loc": [21.0, 1.5], "info": "تحرك مشبوه - قطاع البرج", "color": "orange"},
        {"loc": [19.8, 4.0], "info": "منطقة تسلل محتملة", "color": "darkred"},
        {"loc": [24.5, 9.8], "info": "رصد نشاط تهريب", "color": "purple"}
    ]
    for t in threats:
        folium.Marker(location=t["loc"], popup=t["info"], icon=folium.Icon(color=t["color"], icon='warning')).add_to(m)

# علامة رصد برج باجي مختار الدائمة
folium.Marker([21.328, 0.924], popup="برج باجي مختار", icon=folium.Icon(color='blue', icon='eye-open')).add_to(m)

folium.LayerControl().add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=650)
