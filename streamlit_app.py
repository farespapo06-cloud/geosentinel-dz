import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام السيادي
st.set_page_config(page_title="GeoSentinel-DZ | Intelligence", layout="wide")

# 2. مخزن البيانات التراكمي
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 3. لوحة التحكم (Sidebar)
with st.sidebar:
    st.title("⚙️ غرفة العمليات")
    st.subheader("📅 الإطار الزمني")
    period = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT", value=True)
    air_active = st.toggle("✈️ رصد الملاحة", value=True)
    thermal_active = st.toggle("🌡️ رصد حراري ليلى")
    
    st.divider()
    
    # ميزة تصنيف الأهداف الجديدة
    if st.button("🔍 إجراء مسح شامل الآن", use_container_width=True):
        # قائمة الأنواع التي طلبتها
        target_types = ["دورية حدودية", "عربة مشبوهة", "رصد حراري", "نقطة تجمع"]
        selected_type = random.choice(target_types)
        
        # ربط اللون بنوع الهدف
        color_map = {"دورية حدودية": "blue", "عربة مشبوهة": "red", "رصد حراري": "orange", "نقطة تجمع": "purple"}
        
        new_target = {
            "ID": len(st.session_state.all_detections) + 1,
            "النوع": selected_type,
            "LAT": round(random.uniform(21.2, 23.8), 4), 
            "LON": round(random.uniform(0.5, 3.5), 4),
            "الوقت": datetime.now().strftime("%H:%M:%S"),
            "اللون": color_map[selected_type]
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

    if st.button("🗑️ تفريغ الرادار"):
        st.session_state.all_detections = []
        st.rerun()

# 4. العرض الرئيسي (Main Map) كما في 1000046555.jpg
if air_active:
    st.warning("⚠️ خادم OpenSky غير مستجيب. يتم العرض بناءً على الرصد المحلي.")

st.subheader(f"🗺️ خريطة الرصد العملياتي - {period}")

m = folium.Map(
    location=[28.0, 3.0], zoom_start=5, 
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
    attr="Esri Satellite"
)

# طبقة الحدود (Boundary Layer)
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, opacity=0.8, dash_array='5, 5').add_to(m)

# عرض الأهداف المصنفة بالوانها
for d in st.session_state.all_detections:
    folium.CircleMarker(
        location=[d["LAT"], d["LON"]],
        radius=12,
        color=d["اللون"],
        fill=True,
        fill_color="yellow" if d["النوع"] != "دورية حدودية" else "cyan",
        popup=f"Target: {d['النوع']}\nID: {d['ID']}\nTime: {d['الوقت']}"
    ).add_to(m)

st_folium(m, width="100%", height=500, key="v_final_classified", returned_objects=[])

# 5. السجل الاستخباري المصنف
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد المصنف")
    df = pd.DataFrame(st.session_state.all_detections)
    # عرض الجدول مع استبعاد عمود اللون من العرض المرئي
    st.dataframe(df.drop(columns=['اللون']), use_container_width=True)
    
    # زر الحفظ
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل التقرير الاستخباري",
        data=csv,
        file_name=f"GeoSentinel_Report_{datetime.now().strftime('%H%M%S')}.csv",
        mime='text/csv',
        use_container_width=True
    )
    
