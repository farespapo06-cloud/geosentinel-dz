import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. الإعدادات الأساسية للنظام
st.set_page_config(page_title="GeoSentinel-DZ | Command Center", layout="wide")

# 2. إدارة ذاكرة الرصد (تثبيت الأهداف)
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. لوحة التحكم الجانبية (Strategic Sidebar)
with st.sidebar:
    st.title("⚙️ غرفة العمليات")
    st.subheader("📅 الإطار الزمني")
    period = st.radio("الفترة المحددة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد النشطة")
    osint_active = st.toggle("🔗 تفعيل OSINT", value=True)
    air_active = st.toggle("✈️ رصد الملاحة الجوية", value=True)
    thermal_active = st.toggle("🌡️ تفعيل المسح الحراري")
    
    st.divider()
    
    # إجراءات المسح اليدوي
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        # توليد هدف في مناطق الجنوب (مثل برج باجي مختار أو إن قزام)
        new_target = {
            "ID": len(st.session_state.all_detections) + 1,
            "LAT": round(random.uniform(21.0, 24.5), 4), 
            "LON": round(random.uniform(0.0, 4.0), 4),
            "TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": "Detected" if not thermal_active else "Heat Alert"
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

    if st.button("🗑️ مسح سجل الرادار"):
        st.session_state.all_detections = []
        st.rerun()

# 4. واجهة العرض الرئيسية (Main Interface)
if air_active:
    st.warning("⚠️ تحذير: خادم OpenSky غير مستجيب. يتم العرض بناءً على الرصد المحلي.")

st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

# إعداد الخريطة بناءً على صورة 1000046554.jpg
m = folium.Map(
    location=[28.0, 3.0], 
    zoom_start=5, 
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
    attr="Esri Satellite"
)

# طبقة الحدود السيادية (الدقة الجيوسياسية)
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, opacity=0.8, dash_array='5, 5').add_to(m)

# عرض الأهداف المثبتة
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["LAT"], d["LON"]],
        radius=12,
        color="red",
        fill=True,
        fill_color="yellow",
        popup=f"Target: {d['ID']}\nTime: {d['TIME']}"
    ).add_to(m)

# معالجة عرض الخريطة (Flicker Fix)
st_folium(m, width="100%", height=500, key="operational_map_vFinal", returned_objects=[])

# 5. إدارة البيانات وتصدير السجل
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الاستخباري")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df, use_container_width=True)
    
    # ميزة التصدير للحفظ (Download Feature)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل السجل العملياتي (CSV)",
        data=csv,
        file_name=f"GeoSentinel_Log_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime='text/csv',
        use_container_width=True
    )
