import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="GeoSentinel-DZ | Strategic Command", layout="wide")

# 1. تهيئة مخازن البيانات (التراكم اليدوي)
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. القائمة الجانبية: لوحة التحكم الاستراتيجية (كما في 1000046506_2.jpg)
with st.sidebar:
    st.title("⚙️ لوحة التحكم الاستراتيجي")
    
    st.subheader("📅 التحليل الزمني")
    period = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT (التواصل الاجتماعي)", value=True)
    air_active = st.toggle("✈️ رصد الملاحة الجوية والبحرية", value=True)
    thermal_active = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")
    
    st.divider()
    
    # زر المسح اليدوي (كما طلبت)
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        # إضافة هدف افتراضي لمحاكاة الرصد اليدوي
        new_target = {
            "id": len(st.session_state.all_detections) + 1,
            "lat": random.uniform(21.0, 26.0),
            "lon": random.uniform(0.0, 5.0),
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": "Target Detected"
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

    if st.button("🗑️ تنظيف سجل الرادار"):
        st.session_state.all_detections = []
        st.rerun()

# 3. عرض حالة الخادم (كما في 1000046496_2.jpg)
if air_active:
    st.warning("⚠️ لا يستجيب حالياً OpenSky خادم. جاري العرض بدون بيانات الرادار الحي.")

# 4. بناء الخريطة وتثبيت الأهداف (تطوير صور 1000046544.jpg)
st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

# استخدام إحداثيات الجزائر كمركز
m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri")

# تثبيت الأهداف التراكمية
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["lat"], d["lon"]],
        radius=10,
        color="red",
        fill=True,
        fill_color="yellow",
        popup=f"ID: {d['id']} | Time: {d['time']}"
    ).add_to(m)

# عرض الخريطة مع منع الوميض الأبيض
st_folium(m, width="100%", height=500, key="strategic_map", returned_objects=[])

# 5. سجل الأهداف (Table View)
if st.session_state.all_detections:
    st.markdown("### 📋 سجل الأهداف المرصودة")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['id', 'time', 'lat', 'lon', 'type']], use_container_width=True)
# هذا الكود يضاف داخل حلقة (for d in st.session_state.all_detections)
for d in st.session_state.all_detections:
    # تخصيص لون بناءً على نوع الرصد (OSINT أو حراري)
    marker_color = "red" if not thermal_active else "orange"
    
    folium.CircleMarker(
        location=[d["lat"], d["lon"]],
        radius=12,
        color=marker_color,
        fill=True,
        fill_color="yellow",
        # إضافة معلومات تفصيلية تظهر عند النقر (Popup)
        popup=folium.Popup(f"""
            <b>Target ID:</b> {d['id']}<br>
            <b>Time:</b> {d['time']}<br>
            <b>Coordinates:</b> {round(d['lat'],2)}, {round(d['lon'],2)}<br>
            <b>Status:</b> Verified via OSINT
        """, max_width=200)
    ).add_to(m)
   # 1. إضافة إحداثيات الحدود التقريبية (أو استخدام ملف GeoJSON)
# سنرسم خطاً يوضح الحدود لتعزيز الطابع الاستراتيجي
algeria_borders = [
    [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], 
    [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]
]

# 2. رسم الحدود على الخريطة بلون مميز (أبيض أو ذهبي ليظهر فوق الساتلايت)
folium.PolyLine(
    algeria_borders, 
    color="white", 
    weight=2, 
    opacity=0.8,
    dash_array='5, 5' # خط مقطع ليعطي طابع الخرائط العسكرية
).add_to(m)

# 3. تعديل منطق "إجراء مسح شامل الآن" ليركز على الحدود الجنوبية
if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
    # محاكاة رصد في منطقة برج باجي مختار (إحداثيات حقيقية تقريبية)
    new_target = {
        "id": len(st.session_state.all_detections) + 1,
        "lat": random.uniform(21.3, 22.5), # منطقة حدودية جنوبية
        "lon": random.uniform(0.8, 1.5),
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": "Border Activity Detected"
    }
    st.session_state.all_detections.append(new_target)
    st.rerun()
               
