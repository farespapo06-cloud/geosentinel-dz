import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime

# --- 1. الإعدادات الأساسية ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# --- 2. محرك توليد البيانات ---
def get_live_data():
    targets = []
    for i in range(5):
        targets.append({
            "المعرف (ID)": f"DZ-{random.randint(1000, 9999)}",
            "خط العرض": round(random.uniform(22.0, 34.0), 4),
            "خط الطول": round(random.uniform(0.0, 8.0), 4),
            "الحالة": random.choice(["مستقر", "تحرك مشبوه", "رصد راداري"])
        })
    return targets

# --- 3. القائمة الجانبية (ثابتة لا تتغير) ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    radar_active = st.toggle("✈️ رصد الملاحة الجوية", value=True)
    thermal_active = st.toggle("🌡️ الرؤية الحرارية")

# --- 4. الجزء الذكي (يحدث نفسه بدون وميض) ---
@st.fragment(run_every=15)
def update_dashboard():
    # تحديث الوقت
    st.title(f"🛡️ GeoSentinel-DZ | {datetime.now().strftime('%H:%M:%S')}")
    
    # بناء الخريطة
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles="CartoDB dark_matter")
    
    # الحدود (الخطوط الحمراء التي تظهر في صورتك 1000046508.jpg)
    folium.PolyLine([[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]], color="red", weight=2).add_to(m)

    data = get_live_data()
    
    if radar_active:
        for t in data:
            # تأثير النبض الاحترافي
            folium.CircleMarker(location=[t["خط العرض"], t["خط الطول"]], radius=8, color="cyan", fill=True).add_to(m)
            folium.Marker(location=[t["خط العرض"], t["خط الطول"]], icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(m)

    # عرض الخريطة
    st_folium(m, width="100%", height=500, key=f"map_{datetime.now().second}")

    # عرض الجدول بتنسيق ثابت
    st.divider()
    df = pd.DataFrame(data)
    st.table(df)

# تشغيل التحديث التلقائي
update_dashboard()
