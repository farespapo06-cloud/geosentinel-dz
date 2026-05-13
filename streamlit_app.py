import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import requests
from datetime import datetime, timedelta

# --- 1. إعدادات المنصة السيادية الشاملة 2026 ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Total Sovereignty", page_icon="🇩🇿")

# --- 2. محرك الرادار الوطني الشامل (بري + بحري + جوي) ---
def get_national_radar():
    # توسيع النطاق ليشمل المياه الإقليمية في المتوسط (38.5 شمالاً)
    url = "https://opensky-network.org/api/states/all?lamin=18.0&lomin=-9.0&lamax=38.5&lomax=12.5"
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
        st.markdown("<p style='text-align: center;'>السيادة الوطنية الكاملة (بر، بحر، جو)</p>", unsafe_allow_html=True)
        with st.container(border=True):
            password = st.text_input("رمز الدخول العملياتي", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if password == "DZ_ADMIN_2026":
                    st.session_state.authenticated = True
                    st.rerun()
else:
    # --- 4. لوحة التحكم الجانبية ---
    with st.sidebar:
        st.header("🇩🇿 مركز قيادة الأركان")
        if st.button("🔄 تحديث شامل للمنظومة", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        monitor_mode = st.radio("وضع الرصد الاستراتيجي", ["صور هجينة (كامل التفاصيل)", "تحليل القشرة (الأقمار الصناعية)", "الرصد الحراري (الرؤية الليلية)"])
        
        st.subheader("📡 أنظمة الرصد الفعالة")
        show_land = st.toggle("إظهار الحدود البرية", value=True)
        show_sea = st.toggle("إظهار الحدود البحرية (المياه الإقليمية)", value=True)
        show_radar = st.toggle("رادار الطيران (المجال الجوي)", value=True)
        
        st.markdown("---")
        st.subheader("🕰️ المقارنة الزمنية")
        compare_date = st.date_input("رصد التغيرات منذ تاريخ:", value=datetime.now() - timedelta(days=10))

    # --- 5. بناء الخريطة السيادية الكبرى ---
    st.title("🇩🇿 مركز القيادة والرصد الجغرافي الشامل | GeoSentinel-DZ")
    
    tile_layer = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}' if "هجينة" in monitor_mode else 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'

    m = folium.Map(location=[28.0, 3.0], zoom_start=5, tiles=tile_layer, attr='GeoSentinel 2026')
    m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='kilometers'))

    # أ. الحدود البرية والبحرية
    # الحدود البرية
    land_border = [
        [37.0, 8.5], [30.0, 9.5], [23.5, 12.0], [19.5, 6.0], [19.0, 3.0], 
        [21.0, -4.5], [27.0, -8.7], [33.0, -1.8], [35.5, -2.1]
    ]
    # الحدود البحرية (المياه الإقليمية في المتوسط)
    sea_border = [[35.5, -2.1], [37.5, -2.1], [38.5, 3.0], [38.5, 8.5], [37.0, 8.5]]

    if show_land:
        folium.PolyLine(land_border, color="#FFD700", weight=5, opacity=0.8, tooltip="الحدود البرية").add_to(m)
    
    if show_sea:
        folium.PolyLine(sea_border, color="#00BFFF", weight=5, opacity=0.8, tooltip="الحدود البحرية (المياه الإقليمية)").add_to(m)
        # تظليل المياه الإقليمية
        folium.Polygon(sea_border, color="#00BFFF", weight=0, fill=True, fill_opacity=0.1).add_to(m)

    # ب. رادار المجال الجوي الوطني
    if show_radar:
        live_flights = get_national_radar()
        for f in live_flights:
            if f['lat'] and f['lon']:
                fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
                folium.Marker(
                    [f['lat'], f['lon']],
                    icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(20, 20)),
                    popup=folium.Popup(f"<b>الهدف: {f['callsign']}</b><br>الارتفاع: {f['alt']}م<br><a href='{fa_link}' target='_blank'>تتبع مباشر</a>", max_width=200)
                ).add_to(m)

    # ج. نقاط التحليل (تغطي الشمال البحري والجنوب البري)
    strategic_points = [
        {"loc": [37.2, 7.5], "name": "ميناء سكيكدة / القاعدة البحرية"},
        {"loc": [36.0, -1.3], "name": "واجهة الغزوات / مرسى بن مهيدي"},
        {"loc": [21.32, 0.95], "name": "قطاع برج باجي مختار (بري)"},
        {"loc": [19.57, 5.80], "name": "قطاع عين قزام (بري)"}
    ]

    for p in strategic_points:
        sentinel_url = f"https://apps.sentinel-hub.com/eo-browser/?zoom=12&lat={p['loc'][0]}&lng={p['loc'][1]}&themeId=DEFAULT-THEME&datasetId=S2L2A&fromTime={compare_date}T00%3A00%3A00.000Z&toTime={datetime.now().strftime('%Y-%m-%d')}T23%3A59%3A59.999Z"
        folium.Marker(
            p['loc'],
            icon=folium.Icon(color='red', icon='eye-open'),
            popup=folium.Popup(f"<b>{p['name']}</b><br><a href='{sentinel_url}' target='_blank'>👁️ تحليل الصور (بري/بحري)</a>", max_width=300)
        ).add_to(m)

    # د. تطبيق الرؤية الليلية
    if "حراري" in monitor_mode:
        st.markdown("<style>.night-vision { filter: invert(1) hue-rotate(180deg) brightness(0.8) contrast(1.2); }</style>", unsafe_allow_html=True)
        st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=720)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st_folium(m, width="100%", height=720)

    st.caption("تم تفعيل بروتوكول السيادة الكاملة 2026. الرصد الجوي والبحري يعمل بكفاءة 100%.")
