import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# 1. إعدادات المنصة السيادية
st.set_page_config(page_title="GeoSentinel-DZ | Full Spectrum Intelligence", layout="wide")

if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# 2. لوحة التحكم الجانبية (Sidebar) - تضم كل القفلات السابقة والجديدة
with st.sidebar:
    st.title("⚙️ مركز القيادة والأركان")
    
    st.subheader("⏳ أرشيف التغيرات (منذ 2024)")
    time_node = st.select_slider("الفترة الزمنية:", options=["2024", "2025", "2026"])
    
    st.divider()
    
    st.subheader("🚨 أنظمة الرصد المتعددة")
    radar_active = st.toggle("🛰️ رادار مسح التغيرات (مطار/خندق)", value=True)
    thermal_active = st.toggle("🌡️ رصد ليلي حراري (للمركبات الكهربائية)", value=True)
    stealth_active = st.toggle("👣 تتبع المسارات المخفية (خارج الرادار)", value=True)
    
    st.divider()
    
    # أزرار الرصد التراكمي
    if st.button("🔍 إجراء مسح ميداني شامل", use_container_width=True):
        # مصفوفة التهديدات الشاملة (دول مجاورة، خنادق، مسارات خفية)
        threat_catalog = {
            "مطار عسكري حدودي (دولة مجاورة)": {"color": "darkred", "img": "https://img.freepik.com/free-photo/military-airbase_181624-1.jpg", "link": "https://twitter.com/search?q=border+military+base"},
            "خندق دفاعي مستحدث": {"color": "orange", "img": "https://img.freepik.com/free-photo/trench_181624-2.jpg", "link": "https://www.reuters.com/"},
            "مسار تسلل (خارج الرادار)": {"color": "purple", "img": "https://img.freepik.com/free-photo/secret-path_181624-3.jpg", "link": "https://www.lefigaro.fr/"},
            "مركبة كهربائية (رصد حراري ليلي)": {"color": "cyan", "img": "https://img.freepik.com/free-photo/thermal-car_181624-4.jpg", "link": "https://www.nytimes.com/"},
            "ثكنة تجمع قوات": {"color": "red", "img": "https://img.freepik.com/free-photo/military-camp_181624-5.jpg", "link": "https://www.aljazeera.net/"}
        }
        
        name, info = random.choice(list(threat_catalog.items()))
        # توزيع الإحداثيات ليشمل الدول المجاورة (خارج الحدود قليلاً)
        target = {
            "ID": f"OP-{random.randint(1000, 9999)}",
            "النوع": name,
            "LAT": round(random.uniform(19.0, 36.0), 4),
            "LON": round(random.uniform(-2.0, 10.0), 4),
            "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": info['color'],
            "image": info['img'],
            "news_link": info['link']
        }
        st.session_state.all_detections.append(target)
        st.rerun()

    if st.button("🗑️ تطهير السجل"):
        st.session_state.all_detections = []
        st.rerun()

# 3. واجهة العرض الرئيسية
st.success(f"✅ جميع الأنظمة نشطة | الرصد الحراري: {'مفعل' if thermal_active else 'معطل'} | تتبع المسارات: {'نشط' if stealth_active else 'معطل'}")

# تقسيم الشاشة لثلاثة أقسام (خريطة الميدان | رادار الطيران | رادار السفن)
main_col, side_col = st.columns([2, 1])

with main_col:
    st.subheader("🗺️ خريطة الرصد العملياتي الشامل")
    m = folium.Map(
        location=[28.0, 3.0], zoom_start=5,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite"
    )

    # الحدود السيادية
    algeria_borders = [[37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.0, 5.0], [21.0, -1.0], [27.0, -8.5], [35.5, -2.0], [37.0, 8.5]]
    folium.PolyLine(algeria_borders, color="white", weight=2, dash_array='5, 5').add_to(m)

    # عرض الأهداف (دوائر رادارية + صور + روابط)
    for d in st.session_state.all_detections:
        popup_html = f"""
        <div style="width: 200px; text-align: center; font-family: Arial;">
            <b style="color:{d['color']};">{d['النوع']}</b><br>
            <img src="{d['image']}" width="100%" style="border-radius: 8px; margin: 5px 0;"><br>
            <a href="{d['news_link']}" target="_blank">
                <button style="background-color:{d['color']}; color:white; border:none; padding:5px; border-radius:5px; cursor:pointer;">
                    فتح الرابط الاستخباري 🔗
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

    st_folium(m, width="100%", height=650, key="global_radar")

with side_col:
    st.subheader("✈️ الملاحة الجوية")
    st.components.v1.iframe("https://www.flightradar24.com/simple_index.php?lat=28.0&lon=3.0&z=5", height=300)
    
    st.divider()
    
    st.subheader("🚢 الملاحة البحرية")
    st.components.v1.iframe("https://www.marinetraffic.com/en/ais/embed/zoom:5/centery:37.0/centerx:4.0/maptype:4/show_menu:false", height=300)

# 4. سجل البيانات
if st.session_state.all_detections:
    st.markdown("---")
    st.subheader("📋 سجل الرصد الاستخباري الموحد")
    df = pd.DataFrame(st.session_state.all_detections)
    st.dataframe(df[['ID', 'النوع', 'LAT', 'LON', 'الوقت']], use_container_width=True)
