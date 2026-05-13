import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")

st.title("🛰️ GeoSentinel-DZ: نظام مراقبة الحدود الوطنية")
st.write("عرض شامل لكامل الشريط الحدودي للجمهورية الجزائرية")

# ضبط الخريطة لتشمل كامل الجزائر (إحداثيات مركزية وزووم مناسب)
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5, tiles="OpenStreetMap")

# قائمة ببعض النقاط الحدودية الاستراتيجية (يمكنك إضافة المزيد)
border_points = [
    {"name": "الحدود الغربية (مغنية)", "loc": [34.845, -1.728]},
    {"name": "الحدود الجنوبية الغربية (تندوف)", "loc": [27.671, -8.147]},
    {"name": "الحدود الجنوبية (برج باجي مختار)", "loc": [21.328, 0.924]},
    {"name": "الحدود الجنوبية الشرقية (إن قزام)", "loc": [19.572, 5.769]},
    {"name": "الحدود الشرقية (الدبداب)", "loc": [30.151, 9.458]},
    {"name": "الحدود الشمالية الشرقية (القالة)", "loc": [36.895, 8.443]}
]

# إضافة النقاط إلى الخريطة
for point in border_points:
    folium.Marker(
        location=point["loc"],
        popup=point["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# رسم خط تقريبي يمثل الحدود (اختياري لتعزيز الرؤية)
# ملاحظة: هذه إحداثيات توضيحية فقط
folium.PolyLine(
    locations=[p["loc"] for p in border_points],
    color="blue",
    weight=2,
    opacity=0.7
).add_to(m)

# عرض الخريطة في Streamlit
st_folium(m, width="100%", height=500)
