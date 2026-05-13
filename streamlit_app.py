import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import random
import pandas as pd

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# تخصيص المظهر
st.markdown("""
    <style>
    .stTable { background-color: #1f2937; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات ---
def get_live_radar_data():
    targets = []
    for i in range(5):
        targets.append({
            "المعرف (ID)": f"DZ-{random.randint(1000, 9999)}",
            "خط العرض": round(random.uniform(20.0, 36.0), 4),
            "خط الطول": round(random.uniform(-2.0, 9.0), 4),
            "الارتفاع (قدم)": random.randint(15000, 35000),
            "الحالة": random.choice(["مستقر", "تحرك مشبوه", "رصد راداري"])
        })
    return targets

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم الاستراتيجي")
    time_mode = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    st.divider()
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT", value=True)
    radar_active = st.toggle("✈️ رصد الملاحة الجوية", value=True)
    thermal_active = st.toggle("🌡️ الرؤية الحرارية والليلي")

# --- 4. العرض الرئيسي والخريطة ---
st.title(f"🛡️ GeoSentinel-DZ | {datetime.now().strftime('%H:%M:%S')}")

m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles="CartoDB dark_matter")

# الحدود الحمراء
boundary = [[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]]
folium.PolyLine(boundary, color="red", weight=2).add_to(m)

current_targets = get_live_radar_data()

if radar_active:
    for target in current_targets:
        folium.CircleMarker(
            location=[target["خط العرض"], target["خط الطول"]],
            radius=10, color="cyan", fill=True, fill_opacity=0.2
        ).add_to(m)
        folium.Marker(
            location=[target["خط العرض"], target["خط الطول"]],
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(m)

st_folium(m, width="100%", height=500)

# --- 5. حل مشكلة الجدول (التصحيح هنا) ---
st.divider()
st.subheader("📋 سجل الأهداف المرصودة لحظياً")
df = pd.DataFrame(current_targets)

# دالة التلوين المحدثة لتعمل على كل النسخ
def style_status(val):
    color = 'red' if val == "تحرك مشبوه" else 'white'
    return f'color: {color}'

# استخدام الدالة المضمونة st.dataframe أو st.table مع التنسيق المبسط
st.table(df.style.map(style_status, subset=['الحالة']))

# تحديث تلقائي
time.sleep(15)
st.rerun()
