import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import requests
from datetime import datetime, timedelta

# --- 1. إعدادات المنصة السيادية الشاملة 2026 ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | National Sovereignty", page_icon="🇩🇿")

# --- 2. محرك الرادار الشامل (كامل المجال الجوي الجزائري) ---
def get_national_radar():
    # إحداثيات تغطي كامل مساحة الجزائر بدقة (من الشمال 37 إلى الجنوب 18)
    url = "https://opensky-network.org/api/states/all?lamin=18.0&lomin=-9.0&lamax=38.0&lomax=12.0"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        flights = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                flights.append({
                    "callsign": s[1].strip() if s[1] else "DZ-RADAR",
                    "lat": s[6], "lon": s[5],
                    "alt": s[7] if s[7] else 0,
                    "velocity": s[9] if s[9] else 0
                })
        return flights
    except:
        return []

# --- 3. نظام الدخول العملياتي ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🛡️ GeoSentinel-DZ</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>نظام الرصد المتكامل لكامل التراب الوطني</p>", unsafe_allow_html=True)
        with st.container(border=True):
            password = st.text_input("رمز الدخول العملياتي", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if password == "DZ_ADMIN_2026":
                    st.session_state.authenticated = True
                    st.rerun()
else:
    # --- 4. لوحة التحكم (خيارات السيطرة الكاملة) ---
    with st.sidebar:
        st.header("🇩🇿 التحكم الوطني")
        if st.button("🔄 تحديث شامل (Full Refresh)", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        monitor_mode = st.radio("وضع الرؤية", ["صور هجينة (Google Hybrid)", "تحليل طبقات الأرض (Satellite)", "رصد حراري لليلي"])
        
        st.subheader("🔍 رصد المناطق الاستراتيجية")
        show_borders = st.toggle("إظهار الحدود الوطنية", value=True)
        show_flights = st.toggle("رادار الطيران الحي", value=True)
        
        st.markdown("---")
        st.subheader("🕰️ مقارنة القشرة الأرضية")
        compare_date = st.date_input("تاريخ المقارنة (رصد الخنادق)", value=datetime.now() - timedelta(days=15))

    # --- 5. بناء الخريطة الوطنية الكبرى ---
    st.title("🇩🇿 مركز القيادة والرصد الجغرافي الشامل | GeoSentinel-DZ")
    
    # اختيار نوع القشرة الأرضية
    tile_layer = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}' if "Hybrid" in monitor_mode else 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'

    # مركز الخريطة في قلب الجزائر (عين صالح تقريبا) لتغطية كاملة
    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tile_layer, attr='GeoSentinel National 2026')
    
    # إضافة أدوات القياس لرصد مسافات التحرك
    m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='kilometers'))

    # أ. رسم حدود التراب الوطني بالكامل (أصفر استخباراتي)
    if show_borders:
        # إحداثيات دقيقة لحدود الجزائر
        dz_border = [
            [37.0, 8.5], [36.5, 9.5], [30.0, 9.5], [23.5, 12.0], [19.5, 6.0], 
            [19.0, 3.0], [21.0, -4.5], [27.0, -8.7], [33.0, -1.8], [35.5, -2.1], 
            [36.6, 1.2], [37.0, 8.5]
        ]
        folium.PolyLine(dz_border, color="#FFD700", weight=5, opacity=0.8, tooltip="الحدود الوطنية الجزائرية").add_to(m)

    # ب. رادار الطيران للتراب الوطني (FlightAware Integration)
    if show_flights:
        live_flights = get_national_radar()
        for f in live_flights:
            if f['lat'] and f['lon']:
                fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
                folium.Marker(
                    [f['lat'], f['lon']],
                    icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(20, 20)),
                    popup=folium.Popup(f"<b>الهدف: {f['callsign']}</b><br><a href='{fa_link}' target='_blank'>تتبع حي</a>", max_width=200)
                ).add_to(m)

    # ج. نقاط التحليل الاستراتيجي (تنوع المثلث ليشمل كل الحدود)
    # نقاط موزعة على كامل القشرة الأرضية الحدودية لرصد الخنادق والتحركات
    strategic_points = [
        {"loc": [21.32, 0.95], "name": "قطاع برج باجي مختار"},
        {"loc": [24.50, 9.30], "name": "قطاع جانت / تينزاوتين"},
        {"loc": [19.57, 5.80], "name": "قطاع عين قزام"},
        {"loc": [27.30, -8.60], "name": "قطاع تيندوف / الحدود الغربية"},
        {"loc": [36.80, 8.40], "name": "القطاع الشمالي الشرقي (القالة)"}
    ]

    for p in strategic_points:
        # رابط Sentinel-2 المحدث يومياً لمقارنة الصور 2026
        sentinel_url = f"https://apps.sentinel-hub.com/eo-browser/?zoom=12&lat={p['loc'][0]}&lng={p['loc'][1]}&themeId=DEFAULT-THEME&datasetId=S2L2A&fromTime={compare_date}T00%3A00%3A00.000Z&toTime={datetime.now().strftime('%Y-%m-%d')}T23%3A59%3A59.999Z"
        folium.Marker(
            p['loc'],
            icon=folium.Icon(color='red', icon='eye-open'),
            popup=folium.Popup(f"<b>{p['name']}</b><br><a href='{sentinel_url}' target='_blank'>👁️ تحليل تغير القشرة اليوم</a>", max_width=300)
        ).add_to(m)

    # د. نظام الرؤية الليلية الحراري
    if "حراري" in monitor_mode:
        st.markdown("<style>.night-vision { filter: invert(1) hue-rotate(180deg) brightness(0.8) contrast(1.2); }</style>", unsafe_allow_html=True)
        st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=700)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st_folium(m, width="100%", height=700)

    st.caption("تنبيه: البيانات الجوية والساتلية يتم تحديثها دورياً لضمان دقة الرصد الاستخباراتي لعام 2026.")
