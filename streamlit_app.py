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
