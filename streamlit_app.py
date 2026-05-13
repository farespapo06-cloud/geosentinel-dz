import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات المنصة السيادية - GeoSentinel-DZ
st.set_page_config(page_title="GeoSentinel-DZ | Regional Intelligence", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. لوحة التحكم الجانبية (Sidebar) - التراكم لا الحذف
with st.sidebar:
    st.title("⚙️ مركز العمليات الإقليمي")
    
    st.subheader("⏳ تحليل التغيرات (منذ 2024)")
    time_node = st.select_slider("الإطار الزمني:", options=["2024", "2025", "2026"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد والملاحقة")
    radar_active = st.toggle("🛰️ رادار مسح التغيرات الميدانية", value=True)
    thermal_active = st.toggle("🌡️ رصد ليلي (مركبات كهربائية صامتة)", value=True)
    stealth_active = st.toggle("👣 تتبع المسارات المخفية (خارج الرادار)", value=True)
    
    st.divider()
    
    # أزرار الرصد الميداني والحدودي
    if st.button("🔍 إجراء مسح استخباراتي شامل", use_container_width=True):
        # تصنيفات دقيقة تشمل الحدود والتهديدات الحديثة
        threat_catalog = {
            "مطار عسكري مستحدث (منطقة حدودية)": {"color": "darkred", "img": "https://img.freepik.com/free-photo/military-airbase_181624-1.jpg", "link": "https://www.reuters.com/world/africa/"},
            "خندق دفاعي / سواتر ترابية": {"color": "orange", "img": "https://img.freepik.com/free-photo/trench_181624-2.jpg", "link": "https://twitter.com/search?q=Border+Security"},
            "مسار تسلل (خارج نطاق الرادار)": {"color": "purple", "img": "https://img.freepik.com/free-photo/secret-path_181624-3.jpg", "link": "https://www.aljazeera.net/"},
            "نشاط ليلي (مركبات كهربائية صامتة)": {"color": "cyan", "img": "https://img.freepik.com/free-photo/thermal-car_181624-4.jpg", "link": "https://www.lemonde.fr/afrique/"},
            "ثكنة تجمع / قاعدة إمداد": {"color": "red", "img": "https://img.freepik.com/free-photo/military-camp_181624-5.jpg", "link": "https://www.bbc.com/arabic"}
        }
        
        name, info = random.choice(list(threat_catalog.items()))
        
        # تركيز الإحداثيات داخل الجزائر وعلى الحدود المجاورة مباشرة
        target = {
            "ID": f"OP-{random.randint(1000, 9999)}",
            "النوع": name,
            "LAT": round(random.uniform(20.0, 35.0), 4),
            "LON": round(random.uniform(1.0, 8.0), 4),
            "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": info['color'],
            "image": info['img'],
            "news_link": info['link']
        }
        st.session_state.all_detections.append(target)
        st.rerun()

    if st.button("🗑️ تطهير السجل الميداني"):
        st.session_state.all_detections = []
        st.rerun()

# 3. واجهة العرض الرئيسية
st.success(f"✅ جميع الأنظمة نشطة ومستجيبة | الرصد الحراري والمسارات الخفية مفعلة")

# تقسيم الشاشة: خريطة الميدان (يسار) | رادارات الملاحة الحية (يمين)
col_main, col_live = st.columns([2, 1])

with col_main:
    st.subheader("🗺️ خريطة الرصد وتغيرات الأرض (إقليمي)")
    # الخريطة بنمط الدوائر الرادارية كما في 1000046564.jpg
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite"
    )

    # الحدود السيادية (الخط المقطع)
    algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

    # عرض التهديدات (دوائر رادارية + صور + روابط صحف)
    for d in st.session_state.all_detections:
        popup_html = f"""
        <div style="width: 200px; text-align: center; font-family: Arial;">
            <b style="color:{d['color']}; font-size: 14px;">{d['النوع']}</b><br>
            <img src="{d['image']}" width="100%" style="border-radius: 8px; margin: 5px 0;"><br>
            <a href="{d['news_link']}" target="_blank">
                <button style="background-color:{d['color']}; color:white; border:none; padding:6px; border-radius:5px; cursor:pointer; width:100%;">
                    المصدر الاستخباري 🔗
                </button>
            </a><br>
            <small style="color:grey;">ID: {d['ID']} | {d['الوقت']}</small>
        </div>
        """
        folium.CircleMarker(
            location=[d["LAT"], d["LON"]],
            radius=12, color=d["color"], weight=3,
            fill=True, fill_color=d["color"], fill_opacity=0.4,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    st_folium(m, width="100%", height=600, key="v_final_sovereign")

with col_live:
    # تتبع الطائرات الحي (FlightRadar24)
    st.subheader("✈️ تتبع الطيران الحي")
    st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5", height=300)
    
    st.divider()
    
    # تتبع الملاحة البحرية (Marine Traffic)
    st.subheader("🚢 تتبع الملاحة البحرية")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:37.0/centerx:4.0/maptype:4/show_menu:false", height=300)

# 4. سجل البيانات
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الاستخباري الموحد")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['ID', 'النوع', 'LAT', 'LON', 'الوقت']], use_container_width=True)
