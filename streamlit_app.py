import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import random
import pandas as pd

# --- 1. إعدادات الصفحة المتقدمة ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

# تخصيص المظهر العام (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTable { background-color: #1f2937; border-radius: 10px; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الرادار الخفيف (Lightweight Radar Engine) ---
def get_live_radar_data():
    """توليد بيانات حية فورية لتجنب بطء الخوادم الخارجية"""
    targets = []
    # توليد أهداف في مناطق الاهتمام (الجنوب، الحدود، الوسط)
    for i in range(6):
        targets.append({
            "المعرف (ID)": f"DZ-{random.randint(1000, 9999)}",
            "خط العرض": round(random.uniform(20.0, 36.0), 4),
            "خط الطول": round(random.uniform(-2.0, 9.0), 4),
            "الارتفاع (قدم)": random.randint(15000, 35000),
            "السرعة (عقدة)": random.randint(300, 550),
            "الحالة": random.choice(["مستقر", "تحرك مشبوه", "رصد راداري"])
        })
    return targets

# --- 3. وظيفة الإنذار الصوتي ---
def trigger_alert_sound():
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(
        f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>',
        height=0,
    )

# --- 4. الشريط الجانبي للتحكم ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/584/584611.png", width=80)
    st.header("⚙️ لوحة التحكم الاستراتيجي")
    
    st.subheader("🗓️ التحليل الزمني")
    time_mode = st.radio("الفترة:", ["الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري"])
    
    st.divider()
    st.subheader("🚨 أنظمة الرصد")
    osint_active = st.toggle("🔗 تفعيل OSINT (التواصل الاجتماعي)", value=True)
    radar_active = st.toggle("✈️ رصد الملاحة الجوية", value=True)
    thermal_active = st.toggle("🌡️ الرؤية الحرارية والليلي")
    
    if st.button("🔄 تحديث المسح الشامل"):
        st.toast("جاري إعادة مسح المجال الجوي...")

# --- 5. واجهة العرض الرئيسية ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"🛡️ GeoSentinel-DZ")
with col2:
    st.write(f"**التوقيت المحلي:**\n{datetime.now().strftime('%H:%M:%S')}")

# إعداد الخريطة
tile_style = "CartoDB dark_matter"
if thermal_active:
    tile_style = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
    trigger_alert_sound()

m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tile_style, attr="GeoSentinel")

# رسم الحدود الحمراء (كما في تصميمك)
boundary = [[19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]]
folium.PolyLine(boundary, color="red", weight=2, opacity=0.7).add_to(m)

# معالجة بيانات الرادار وعرضها
current_targets = get_live_radar_data()

if radar_active:
    for target in current_targets:
        # إضافة تأثير النبض (Pulse) حول الهدف
        folium.CircleMarker(
            location=[target["خط العرض"], target["خط الطول"]],
            radius=10, color="cyan", fill=True, fill_opacity=0.2
        ).add_to(m)
        
        folium.Marker(
            location=[target["خط العرض"], target["خط الطول"]],
            popup=f"Target: {target['المعرف (ID)']}",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=500)

# --- 6. سجل الأهداف المرصودة (أسفل الخريطة) ---
st.divider()
st.subheader("📋 سجل الأهداف المرصودة لحظياً")
df = pd.DataFrame(current_targets)

# تلوين الحالة بناءً على نوع التنبيه
def color_status(val):
    color = 'red' if val == "تحرك مشبوه" else 'white'
    return f'color: {color}'

st.table(df.style.applymap(color_status, subset=['الحالة']))

# تحديث تلقائي هادئ
time.sleep(15)
st.rerun()
