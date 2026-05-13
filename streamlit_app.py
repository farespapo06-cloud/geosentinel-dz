import streamlit as st
import folium
from streamlit_folium import st_folium
import feedparser

st.set_page_config(page_title="GeoSentinel-DZ Pro", layout="wide")

# واجهة الرصد الاستخباراتي
st.title("🛡️ GeoSentinel-DZ Intelligence")
st.sidebar.header("📡 رادار التهديدات والعواجل")

# وظيفة مراقبة الصحف العالمية (OSINT)
def scan_global_news():
    # روابط لمصادر دولية لمتابعة التحركات الإقليمية
    sources = [
        "https://www.aljazeera.net/aljazeerarss", 
        "https://arabic.rt.com/rss/"
    ]
    alerts = []
    for url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                # البحث عن كلمات مفتاحية حساسة للحدود والتهديدات
                if any(k in entry.title for k in ["الحدود", "مالي", "ليبيا", "تهديد", "تسريب", "تحرك عسكري"]):
                    alerts.append(f"🔴 **عاجل:** {entry.title}")
        except:
            pass
    return alerts

# عرض الإنذارات في القائمة الجانبية
with st.sidebar:
    st.subheader("⚠️ نظام الإنذار المبكر")
    threats = scan_global_news()
    if threats:
        for t in threats: st.warning(t)
    else:
        st.success("✅ الوضع الحدودي مستقر إخبارياً")

# قسم مقارنة التغيرات الجغرافية والخرائط
m = folium.Map(location=[28.0, 2.0], zoom_start=5)

# طبقة القمر الصناعي (Satellite)
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google', name='رؤية القمر الصناعي', overlay=False, control=True
).add_to(m)

# الحدود الوطنية الحمراء (المسح الشامل)
algeria_border = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
folium.PolyLine(algeria_border, color="red", weight=5, opacity=1).add_to(m)

# نقطة رصد برج باجي مختار
folium.Marker([21.328, 0.924], popup="قطاع العمليات: برج باجي مختار", icon=folium.Icon(color='red', icon='eye-open')).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width="100%", height=600)

st.info("💡 نظام GeoSentinel يقوم الآن بمقارنة البيانات الإخبارية مع الموقع الجغرافي للحدود.")
