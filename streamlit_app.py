import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="GeoSentinel-DZ | Strategic Command", layout="wide")

# 2. تهيئة مخازن البيانات
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    st.subheader("📅 التحليل الزمني")
    period = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT", value=True)
    air_active = st.toggle("✈️ رصد الملاحة", value=True)
    thermal_active = st.toggle("🌡️ الرصد الحراري")
    
    st.divider()
    
    # أزرار التشغيل اليدوي
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        new_target = {
            "id": len(st.session_state.all_detections) + 1,
            "lat": random.uniform(21.5, 24.0), 
            "lon": random.uniform(0.5, 3.0),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Border Activity" if not thermal_active else "Heat Signature"
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

    if st.button("🗑️ تنظيف السجل"):
        st.session_state.all_detections = []
        st.rerun()

# 4. الواجهة الرئيسية والخريطة
if air_active:
    st.warning("⚠️ خادم OpenSky لا يستجيب حالياً. جاري العرض بدون بيانات الرادار الحي.")

st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

m = folium.Map(
    location=[28.0, 3.0], zoom_start=5, 
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
    attr="Esri Satellite"
)

# رسم الحدود (كما تظهر في صورتك 1000046553.jpg)
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, opacity=0.8, dash_array='5, 5').add_to(m)

# وضع الأهداف
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["lat"], d["lon"]], radius=12, color="red", fill=True, fill_color="yellow",
        popup=f"ID: {d['id']}\nTime: {d['time']}"
    ).add_to(m)

st_folium(m, width="100%", height=500, key="v4_map", returned_objects=[])

# 5. نظام تصدير البيانات (الجديد)
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الاستخباري")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df, use_container_width=True)
    
    # ميزة الحفظ: تحويل الجدول إلى ملف نصي قابل للتحميل
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل السجل كملف (CSV/Text)",
        data=csv,
        file_name=f"GeoSentinel_Log_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
