import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime
import requests

# --- 1. بروتوكول GeoSentinel-Auth ---
def check_security():
    # هذا الجزء يبقى كما هو في كودك الأصلي
    return True

# --- 2. وظيفة جلب بيانات الطائرات (الرادار البديل) ---
def get_flight_data():
    """جلب بيانات الطائرات عبر رابط مباشر لضمان الاستقرار"""
    url = "https://opensky-network.org/api/states/all"
    # حدود الجزائر الجغرافية للتصفية (Lamin, Lomin, Lamax, Lomax)
    params = {'lamin': 18.9, 'lomin': -8.7, 'lamax': 37.1, 'lomax': 12.0}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('states', [])
    except Exception as e:
        st.sidebar.error(f"خطأ في الاتصال بالرادار: {e}")
        return []
    return []

# --- 3. إعداد واجهة المستخدم ---
st.set_page_config(page_title="GeoSentinel-DZ", layout="wide")
st.title(f"🛡️ GeoSentinel-DZ | Live: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- 4. بناء الخريطة ---
# إحداثيات مركزية لمنطقة Bordj Badji Mokhtar والجزائر
m = folium.Map(location=[28.0339, 1.6596], zoom_start=5, tiles="CartoDB dark_matter")

# إضافة حدود المنطقة (الخط الأحمر الذي ظهر في صورتك 1000046489.jpg)
# تأكد من إبقاء إحداثيات الحدود التي وضعتها سابقاً هنا
boundary_coords = [
    [19.0, -8.0], [37.0, -8.0], [37.0, 12.0], [19.0, 12.0], [19.0, -8.0]
]
folium.PolyLine(boundary_coords, color="red", weight=2.5, opacity=1).add_to(m)

# --- 5. تشغيل الرادار وعرض الطائرات ---
flights = get_flight_data()

if flights:
    for flight in flights:
        callsign = flight[1] if flight[1] else "Unknown"
        lat, lon = flight[6], flight[5]
        altitude = flight[7]
        
        if lat and lon:
            folium.Marker(
                location=[lat, lon],
                popup=f"Flight: {callsign}\nAlt: {altitude}m",
                icon=folium.Icon(color="blue", icon="plane", prefix="fa")
            ).add_to(m)
else:
    st.info("جاري البحث عن حركة طيران في المجال الجوي حالياً...")

# --- 6. عرض الخريطة في التطبيق ---
st_folium(m, width="100%", height=600)

# تحديث تلقائي كل دقيقة
time.sleep(60)
st.rerun()
