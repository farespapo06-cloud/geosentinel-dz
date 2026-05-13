import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام - GeoSentinel-DZ
st.set_page_config(page_title="GeoSentinel-DZ | Intelligence", layout="wide")

# 2. مخزن البيانات المستمر
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.title("⚙️ غرفة العمليات")
    st.subheader("📅 الإطار الزمني")
    period = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    # تم تعطيل التنبيه المزعج بجعله يعمل محلياً فقط
    radar_mode = st.toggle("🛰️ تفعيل الرادار المحلي (مستجيب)", value=True)
    thermal_active = st.toggle("🌡️ رصد حراري ليلي")
    
    st.divider()
    
    # ميزة تصنيف الأهداف وتوليدها
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        types = ["دورية حدودية", "عربة مشبوهة", "رصد حراري", "تحرك مشاة"]
        selected_type = random.choice(types)
        
        # توزيع الألوان حسب الخطورة
        colors = {"دورية حدودية": "blue", "عربة مشبوهة": "red", "رصد حراري": "orange", "تحرك مشاة": "purple"}
        
        target = {
            "ID": f"DZ-{random.randint(100, 999)}",
            "النوع": selected_type,
            "LAT": round(random.uniform(21.5, 24.0), 4), # التركيز على المناطق الجنوبية
            "LON": round(random.uniform(0.5, 3.5), 4),
            "الوقت": datetime.now().strftime("%H:%M:%S"),
            "color": colors[selected_type]
        }
        st.session_state.all_detections.append(target)
        st.rerun()

    if st.button("🗑️ تفريغ سجل الرادار"):
        st.session_state.all_detections = []
        st.rerun()

# 4. العرض الرئيسي (حل مشكلة التنبيه الأصفر)
if not radar_mode:
    st.warning("⚠️ الرادار في وضع الاستعداد. قم بتفعيل الرادار المحلي لبدء الرصد.")
else:
    st.success("✅ النظام متصل - الرصد المحلي نشط ومستجيب.")

st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

# إعداد الخريطة بناءً على صورة 1000046557.jpg
m = folium.Map(
    location=[28.0, 3.0], zoom_start=5, 
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
    attr="Esri Satellite"
)

# رسم الحدود السيادية (الخط المقطع في صورتك)
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, opacity=0.8, dash_array='5, 5').add_to(m)

# عرض الأهداف المصنفة
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["LAT"], d["LON"]],
        radius=10,
        color=d["color"],
        fill=True,
        fill_color="yellow",
        popup=f"Target: {d['النوع']}\nID: {d['ID']}"
    ).add_to(m)

st_folium(m, width="100%", height=500, key="v_radar_fixed")

# 5. جدول البيانات والتصدير
if st.session_state.all_detections:
    st.markdown("---")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df.drop(columns=['color']), use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل التقرير الاستخباري", csv, "GeoSentinel_Report.csv", "text/csv", use_container_width=True)
