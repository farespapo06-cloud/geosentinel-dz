import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# --- 1. بروتوكول GeoSentinel-Auth ---
def check_security():
    if "auth_ok" not in st.session_state:
        st.sidebar.warning("🔐 نظام مؤمن: ادخل مفتاح العبور")
        key = st.sidebar.text_input("Security Key:", type="password")
        if key == "DZ_ELITE_2026":
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.stop()

check_security()

st.title("🛡️ GeoSentinel-DZ: الرصد البحري والجوي الشامل")

# --- القائمة الجانبية (بناءً على الصورة 1000046448.jpg) ---
with st.sidebar:
    st.header("⚙️ أدوات الرصد المتقدمة")
    
    st.subheader("🗓️ المقارنة الزمنية")
    time_mode = st.radio("نطاق البحث:", 
                        ("الوضع الحالي (2026)", "الأرشيف (2020)", "التحليل العشري (10 سنوات)"), index=2)
    
    st.divider()
    
    st.subheader("🚨 رادار التهديدات")
    osint = st.toggle("🔗 ربط الصحف ومواقع التواصل (OSINT)", value=True)
    # إضافة رصد الطيران والبحر
    air_sea_monitor = st.toggle("✈️🚢 رصد الملاحة الجوية والبحرية", value=True)
    thermal = st.toggle("🌡️ تفعيل الرصد الحراري والليلي")

    if st.button("إجراء مسح شامل الآن"):
        with st.status("جاري مسح الحدود البحرية والبرية وتحليل حركة الطيران..."):
            time.sleep(2)
            st.success("تم تحديث خارطة التهديدات الجوية والبحرية.")

# --- منطق الخريطة ---
m = folium.Map(location=[32.0, 2.0], zoom_start=5)

# طبقات الخريطة
if thermal:
    folium.TileLayer('CartoDB dark_matter').add_to(m)
else:
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                     attr='Google', name='Satellite').add_to(m)

# --- 2. رسم الحدود الوطنية والبحرية (المسح الشامل) ---
# إضافة الإحداثيات البحرية للشمال الجزائري
algeria_full_border = [
    [37.0,-2.0],[38.0,2.0],[38.5,5.0],[37.5,8.5], # الحدود البحرية
    [30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]
]
folium.PolyLine(algeria_full_border, color="red", weight=4).add_to(m)

# --- 3. خوارزمية التغيرات العشارية (الدوائر الصفراء التفاعلية) ---
if time_mode == "التحليل العشري (10 سنوات)":
    yellow_points = [
        {"loc": [21.5, 1.5], "type": "حفر خنادق جديد", "date": "2016 vs 2026"},
        {"loc": [36.8, 3.0], "type": "تجمع بحري مشبوه", "date": "رصد حديث"},
        {"loc": [19.5, 4.2], "type": "تغير في التضاريس (مطار ترابي)", "date": "مكتشف بـ AI"}
    ]
    
    for p in yellow_points:
        html_yellow = f"""
        <div style='width:200px; font-family: Arial;'>
        <h4 style='color:#E6B800;'>🟡 تنبيه التغيير العشري</h4>
        <p><b>النوع:</b> {p['type']}</p>
        <p><b>الفترة:</b> {p['date']}</p>
        <hr>
        <a href='https://www.google.com/maps/@{p['loc'][0]},{p['loc'][1]},15z/data=!3m1!1e3' target='_blank' 
           style='background:#E6B800; color:black; padding:5px; text-decoration:none; border-radius:3px; font-weight:bold;'>
           👁️ رؤية صور القمر الصناعي
        </a>
        </div>
        """
        folium.CircleMarker(
            location=p["loc"], radius=10, color="#E6B800", fill=True,
            popup=folium.Popup(html_yellow, max_width=250)
        ).add_to(m)

# --- 4. رصد الطيران والبحر (الربط الملاحي) ---
if air_sea_monitor:
    # محاكاة لرصد طائرة أو سفينة تقترب من المياه الإقليمية
    folium.Marker(
        [38.2, 4.0], popup="🚢 سفينة غير معرفة - قبالة السواحل",
        icon=folium.Icon(color='blue', icon='ship', prefix='fa')
    ).add_to(m)
    folium.Marker(
        [35.0, -1.0], popup="✈️ طائرة رصد أجنبية - القطاع الغربي",
        icon=folium.Icon(color='black', icon='plane', prefix='fa')
    ).add_to(m)

# التنبيه الأحمر (OSINT) كما في الصورة 1000046446.jpg
if osint:
    html_red = """
    <div style='width:200px; font-family: Arial;'>
    <h4 style='color:red;'>🔴 إنذار OSINT</h4>
    <p><b>النوع:</b> تحرك حدودي مشبوه</p>
    <a href='https://google.com/search?q=border+security' target='_blank' 
       style='background:red; color:white; padding:5px; text-decoration:none; border-radius:3px;'>
       👁️ رؤية صور التهديد والمصدر
    </a>
    </div>
    """
    folium.Marker([22.5, 3.0], popup=folium.Popup(html_red), 
                  icon=folium.Icon(color='red', icon='warning')).add_to(m)

st_folium(m, width="100%", height=650)
