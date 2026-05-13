import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import random
import pandas as pd

# --- 1. إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# تصميم خاص للجدول ليتناسب مع الرؤية الليلية
st.markdown("""
    <style>
    .stTable { background-color: #1a1c23; border-radius: 10px; color: #00ffcc; }
    thead tr th { background-color: #2d2f39 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الرادار (توليد بيانات مستقرة) ---
def fetch_radar_targets():
    targets = []
    # توليد 5 أهداف في النطاق الجغرافي الجزائري
    for i in range(5):
        targets.append({
            "المعرف (ID)": f"DZ-{random.randint(100, 999)}",
            "خط العرض": round(random.uniform(22.0, 35.0), 4),
            "خط الطول": round(random.uniform(0.0, 8.0), 4),
            "الارتفاع": f"{random.randint(18, 38)}k ft",
            "السرعة": f"{random.randint(400, 520)} kn",
            "الحالة": random.choice(["مستقر", "رصد نشط"])
        })
    return targets

# --- 3. الشريط الجانبي (أدوات التحكم) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2561/2561374.png", width=70)
    st.header("لوحة التحكم")
    radar_active = st.toggle("تفعيل الرادار الجوي", value=True)
    thermal_view = st.toggle("وضع الرؤية الحرارية")
    st.divider()
    st.info("نظام GeoSentinel يعمل الآن بأحدث بروتوكول استقرار لعام 2026.")

# --- 4. العرض الرئيسي (الخريطة والوقت) ---
st.title(f"🛡️ GeoSentinel-DZ | {datetime.now().strftime('%H:%M:%S')}")

# اختيار نمط الخريطة
map_tiles = "CartoDB dark_matter"
if thermal_view:
    map_tiles = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"

# إنشاء الخريطة وتثبيت الموقع
m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=map_tiles, attr="GeoSentinel")

# رسم الحدود الحمراء (كما في تصميمك الأصلي)
folium.PolyLine([[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]], 
                color="red", weight=2, opacity=0.8).add_to(m)

# جلب وعرض البيانات
current_data = fetch_radar_targets()

if radar_active:
    for target in current_data:
        # إضافة أيقونة الطائرة مع دائرة نبضية حولها
        folium.CircleMarker([target["خط العرض"], target["خط الطول"]], 
                            radius=10, color="#00ffff", fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([target["خط العرض"], target["خط الطول"]], 
                      icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(m)

# عرض الخريطة (استخدام مفتاح ثابت يمنع البياض)
st_folium(m, width="100%", height=500, key="geosentinel_final_map")

# --- 5. جدول البيانات المحدث ---
st.subheader("📋 سجل الأهداف المرصودة")
df = pd.DataFrame(current_data)
st.table(df)

# --- 6. آلية التحديث الصامت ---
# تحديث كل 30 ثانية لضمان أعلى درجات الاستقرار على الهاتف
time.sleep(30)
st.rerun()
