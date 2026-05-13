import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Configuration du Système
st.set_page_config(page_title="GeoSentinel-DZ Intelligence", layout="wide")

st.title("🛰️ GeoSentinel-DZ Intelligence")
st.sidebar.title("لوحة التحكم والعمليات")

# 2. Sélection du Mode de Vision
map_mode = st.sidebar.selectbox("نمط الرؤية (Vision Mode)", ["Satellite", "Standard Map"])
st.sidebar.markdown("---")

# 3. Radar des Menaces en Arabe (Threat Intelligence)
st.sidebar.subheader("🗞️ رادار التهديدات والأخبار")
st.sidebar.warning("⚠️ تنبيهات حدودية مباشرة")

# محاكاة لجلب الأخبار المتعلقة بالحدود الجزائرية
st.sidebar.error("🚩 تهديد محتمل: تحركات مشبوهة في منطقة الساحل")
st.sidebar.info("📌 تقرير: تعزيز الرقابة على الحدود الشرقية")
st.sidebar.write("- **رويترز:** تحليل صور الأقمار الصناعية يظهر مسارات جديدة.")
st.sidebar.write("- **الصحافة العالمية:** رصد نشاط لوجستي في المناطق الميتة.")

# 4. Initialisation de la Carte (Centrée sur l'Algérie)
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5)

# 5. Intégration de la couche Satellite Google
if map_mode == "Satellite":
    google_sat = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    folium.TileLayer(
        tiles=google_sat,
        attr='Google Satellite',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)

# 6. Points de Surveillance Stratégiques
# إضافة نقاط مراقبة على طول الحدود الجزائرية
border_points = [
    {"name": "قطاع مغنية (الغرب)", "coords": [34.845, -1.728]},
    {"name": "قطاع تندوف (الجنوب الغربي)", "coords": [27.671, -8.147]},
    {"name": "قطاع برج باجي مختار (الجنوب)", "coords": [21.328, 0.924]},
    {"name": "قطاع إن قزام (الجنوب الشرقي)", "coords": [19.572, 5.769]},
    {"name": "قطاع الدبداب (الشرق)", "coords": [30.151, 9.458]}
]

for point in border_points:
    folium.Marker(
        location=point["coords"], 
        popup=point["name"], 
        icon=folium.Icon(color='red', icon='eye-open')
    ).add_to(m)

# 7. Affichage de l'Application
st_folium(m, width="100%", height=600)

# 8. Note sur le développement futur
st.info("نظام التحليل الزمني (2020-2026) والكشف الحراري قيد التطوير عبر ربط API.")
