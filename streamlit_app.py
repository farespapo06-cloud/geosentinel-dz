import streamlit as st
import folium
from streamlit_folium import st_folium

# إعداد واجهة التطبيق
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title("🛡️ GeoSentinel-DZ")
st.subheader("نظام مراقبة الحدود - برج باجي مختار")

# إحداثيات المنطقة (برج باجي مختار)
m = folium.Map(location=[21.328, 0.924], zoom_start=10)
folium.Marker([21.328, 0.924], popup="نقطة مراقبة حدودية").add_to(m)

# عرض الخريطة
st_folium(m, width="100%", height=600)
