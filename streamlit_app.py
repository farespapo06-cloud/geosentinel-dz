import streamlit as st
import folium
from streamlit_folium import st_folium

# محاولة جلب المكتبة، وإذا لم تكن موجودة لا يتوقف التطبيق
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

st.set_page_config(page_title="GeoSentinel-DZ Pro", layout="wide")
st.title("🛡️ GeoSentinel-DZ Intelligence")

# القائمة الجانبية للتنبيهات
with st.sidebar:
    st.header("📡 رادار التهديدات")
    if HAS_FEEDPARSER:
        st.success("✅ نظام الرصد الإخباري نشط")
    else:
        st.warning("⚠️ نظام الأنباء في طور التحديث (جاري تثبيت المكتبات)")

# الخريطة (ستعمل دائماً مهما حدث)
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# طبقة القمر الصناعي
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google', name='رؤية القمر الصناعي', overlay=False, control=True
).add_to(m)

# الحدود الوطنية
algeria_border = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_border, color="red", weight=5, opacity=1).add_to(m)

# نقطة رصد برج باجي مختار
folium.Marker([21.328, 0.924], popup="برج باجي مختار", icon=folium.Icon(color='red', icon='eye-open')).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width="100%", height=600)
folium.Marker([خط_العرض, خط_الطول], popup="نقطة مشبوهة", icon=folium.Icon(color='orange', icon='warning')).add_to(m)
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ Pro", layout="wide")
st.title("🛡️ GeoSentinel-DZ: المسح الشامل والتحليل الزمني")

# --- 1. القائمة الجانبية للتحكم والمقارنة ---
with st.sidebar:
    st.header("⚙️ أدوات المسح والمقارنة")
    
    # ميزة المقارنة الزمنية
    year = st.radio("اختر سنة الرصد (مقارنة التغيرات):", ("2020 (أرشيف)", "2026 (الوضع الحالي)"))
    
    st.divider()
    
    # ميزة رصد التهديدات
    st.subheader("🚩 مرصد التهديدات")
    show_threats = st.checkbox("إظهار النقاط المشكوك فيها (إرهاب/تهريب)")
    
    if st.button("بدء مسح شامل للحدود"):
        st.info("جاري فحص الشريط الحدودي ومطابقة البيانات...")

# --- 2. إعدادات الخريطة ---
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# تبديل الطبقات بناءً على السنة المختارة
if year == "2020 (أرشيف)":
    # استخدام طبقة تضاريس قديمة (محاكاة للأرشيف)
    folium.TileLayer('stamenterrain', name='أرشيف 2020').add_to(m)
else:
    # صور الأقمار الصناعية الحديثة (كما في الصورة 1000046434.jpg)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google Satellite', name='قمر صناعي 2026', overlay=False
    ).add_to(m)

# --- 3. رسم الحدود الوطنية (المسح الشامل) ---
algeria_border = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_border, color="red", weight=4, opacity=1, tooltip="الحدود الوطنية").add_to(m)

# --- 4. خروج علامات تلقائية للنقاط المشكوك فيها ---
if show_threats:
    # نقاط افتراضية بناءً على التقارير (يمكن تحديثها دورياً)
    suspicious_points = [
        {"loc": [21.3, 0.9], "type": "تحرك مشبوه", "info": "نشاط غير معتاد - قطاع البرج"},
        {"loc": [19.5, 4.2], "type": "منطقة تسلل", "info": "نقطة ساخنة - تهريب"},
        {"loc": [24.0, 9.5], "type": "رصد إرهاب", "info": "تحركات حدودية شرقية"}
    ]
    
    for point in suspicious_points:
        folium.Marker(
            location=point["loc"],
            popup=f"📌 {point['type']}: {point['info']}",
            icon=folium.Icon(color='orange' if "تهريب" in point['type'] else 'darkred', icon='warning')
        ).add_to(m)

# تثبيت علامة الرصد الدائمة في برج باجي مختار
folium.Marker([21.328, 0.924], popup="مركز رصد GeoSentinel", icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=650)
