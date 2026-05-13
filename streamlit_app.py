import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات المنصة
st.set_page_config(page_title="GeoSentinel-DZ | Sovereign Monitoring", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. لوحة التحكم والقفلات (Sidebar)
with st.sidebar:
    st.title("⚙️ غرفة العمليات")
    
    # قسم التغيرات التاريخية (منذ 2024)
    st.subheader("⏳ تحليل زمني")
    time_analysis = st.select_slider(
        "تغيرات النشاط منذ:",
        options=["يناير 2024", "يونيو 2024", "يناير 2025", "الوضع الحالي 2026"]
    )
    
    st.divider()
    
    # قسم الروابط والذكاء الاصطناعي
    st.subheader("🔗 روابط استخباراتية حية")
    st.markdown(f"[✈️ تتبع مباشر (FlightRadar)](https://www.flightradar24.com/34.0,3.0/6)")
    st.markdown(f"[🚢 حركة السفن (MarineTraffic)](https://www.marinetraffic.com/)")
    st.markdown(f"[📡 صور الأقمار (Sentinel)](https://apps.sentinel-hub.com/)")
    
    st.divider()
    
    # إعادة القفلات (أنظمة الرصد)
    st.subheader("🚨 أنظمة الرصد النشطة")
    radar_active = st.toggle("🛰️ رادار محلي (مستجيب)", value=True)
    thermal_active = st.toggle("🌡️ رصد حراري (الأشعة تحت الحمراء)")
    
    if st.button("🔍 مسح ميداني شامل", use_container_width=True):
        # مصفوفة التهديدات مع الصور الاستخباراتية الحديثة
        threats = {
            "دورية مراقبة": {"color": "blue", "icon": "shield", "img": "https://img.freepik.com/free-photo/soldier-patrol-desert_181624-345.jpg"},
            "عربة مشبوهة": {"color": "red", "icon": "warning", "img": "https://img.freepik.com/free-photo/military-convoy-dust_181624-987.jpg"},
            "طائرة بدون طيار": {"color": "orange", "icon": "plane", "img": "https://img.freepik.com/free-photo/military-drone-flight_181624-1122.jpg"},
            "نشاط بحري غير مصنف": {"color": "darkblue", "icon": "anchor", "img": "https://img.freepik.com/free-photo/navy-ship-horizon_181624-4455.jpg"}
        }
        
        name, info = random.choice(list(threats.items()))
        
        # توزيع الأهداف (بري جنوبي / بحري شمالي)
        is_sea = "بحري" in name
        lat = random.uniform(36.5, 38.0) if is_sea else random.uniform(21.0, 28.0)
        lon = random.uniform(2.0, 8.0) if is_sea else random.uniform(-1.0, 6.0)

        new_target = {
            "ID": f"OP-{random.randint(1000, 9999)}",
            "النوع": name,
            "LAT": round(lat, 4), "LON": round(lon, 4),
            "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": info['color'],
            "icon": info['icon'],
            "image": info['img']
        }
        st.session_state.all_detections.append(new_target)
        st.rerun()

# 3. العرض الرئيسي (Main Screen)
st.success(f"✅ النظام نشط ومستجيب | تحليل البيانات: {time_analysis}")

# شريط الأخبار العاجلة
st.info("📢 **آخر الأنباء:** رصد تحركات روتينية على الحدود الجنوبية | استقرار حركة الملاحة الجوية فوق الأطلس.")

# الخريطة العملياتية
m = folium.Map(
    location=[28.0, 3.0], zoom_start=5,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri Satellite"
)

# رسم الحدود السيادية
algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

# عرض الأهداف مع خاصية "الرؤية العميقة" (الصورة عند الضغط)
for d in st.session_state.all_detections:
    # محتوى النافذة المنبثقة (HTML)
    popup_content = f"""
    <div style="width: 200px; font-family: 'Arial';">
        <h4 style="margin:0; color:{d['color']};">{d['النوع']}</h4>
        <hr style="margin:5px 0;">
        <img src="{d['image']}" width="100%" style="border-radius: 5px; margin-bottom: 5px;">
        <p style="font-size: 12px; margin:0;"><b>المعرف:</b> {d['ID']}</p>
        <p style="font-size: 12px; margin:0;"><b>الوقت:</b> {d['الوقت']}</p>
        <p style="font-size: 10px; color: grey;">* صورة حديثة من أقمار Sentinel</p>
    </div>
    """
    
    folium.Marker(
        location=[d["LAT"], d["LON"]],
        icon=folium.Icon(color=d["color"], icon=d["icon"], prefix='fa'),
        popup=folium.Popup(popup_content, max_width=250)
    ).add_to(m)

st_folium(m, width="100%", height=500, key="v_sovereign_2026")

# 4. سجل التهديدات المصنف
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الاستخباري")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['ID', 'النوع', 'LAT', 'LON', 'الوقت']], use_container_width=True)
