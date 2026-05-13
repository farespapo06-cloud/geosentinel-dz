import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

st.title("🛰️ GeoSentinel-DZ")
st.subheader("نظام مراقبة الحدود الإقليمية - برج باجي مختار")

# إحداثيات المنطقة الجغرافية
m = folium.Map(location=[21.328, 0.924], zoom_start=10)
folium.Marker([21.328, 0.924], popup="نقطة مراقبة حدودية").add_to(m)

# عرض الخريطة
st_folium(m, width=700)
