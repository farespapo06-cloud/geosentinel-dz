import streamlit as st
import folium
from streamlit_folium import st_folium
import feedparser # لمراقبة الصحف العالمية

st.set_page_config(page_title="GeoSentinel-DZ Pro", layout="wide")

# --- تنسيق الواجهة ---
st.title("🛡️ GeoSentinel-DZ: Intelligence & Monitoring")
st.sidebar.header("📡 مركز الإنذار المبكر")

# --- وظيفة مراقبة الصحف والتهديدات ---
def fetch_global_news():
    # هنا يمكن إضافة روابط RSS لصحف عالمية أو مواقع تحليلات عسكرية
    feeds = [
        "https://www.aljazeera.net/aljazeerarss/ad67301c-668b-47e0-94a1-09e45e54911d/154c1859-99c0-4354-9467-336717a61d10",
        "https://arabic.rt.com/rss/"
    ]
    news_items = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # جلب آخر 3 أخبار من كل مصدر
            if any(word in entry.title for word in ["الجزائر", "حدود", "تهديد", "مالي", "ليبيا"]):
                news_items.append(f"⚠️ **تنبيه:** {entry.title}")
    return news_items

# عرض التنبيهات في القائمة الجانبية
with st.sidebar:
    st.subheader("آخر التهديدات والتسريبات")
    alerts = fetch_global_news()
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("✅ لا توجد تهديدات مباشرة مرصودة حالياً")
    
    st.divider()
    st.info("ملاحظة: النظام يقارن التغيرات في المصادر المفتوحة OSINT")

# --- الخريطة الشاملة (كما في الصور السابقة) ---
col1, col2 = st.columns([3, 1])

with col1:
    m = folium.Map(location=[28.0, 2.0], zoom_start=5)
    
    # طبقة القمر الصناعي
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google', name='رؤية القمر الصناعي', overlay=False, control=True
    ).add_to(m)

    # رسم الحدود الوطنية الرسمية
    algeria_coords = [[37.0,-2.0],[37.0,8.5],[30.0,9.5],[23.5,12.0],[19.0,5.0],[21.0,-4.5],[27.5,-8.5],[33.0,-2.0],[37.0,-2.0]]
    folium.PolyLine(algeria_coords, color="red", weight=4, opacity=1).add_to(m)

    # علامات الرصد (برج باجي مختار وغيرها)
    folium.Marker([21.328, 0.924], popup="قطاع برج باجي مختار", icon=folium.Icon(color='red', icon='eye-open')).add_to(m)
    
    st_folium(m, width="100%", height=600)

with col2:
    st.subheader("📊 تحليل التغيرات")
    st.write("- **تغيرات التضاريس:** مستقرة")
    st.write("- **النشاط الحدودي:** رصد اعتيادي")
    if st.button("تحديث المسح الشامل"):
        st.write("🔄 جاري مقارنة الصور الفضائية...")
