import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import requests
from datetime import datetime, timedelta

# --- 1. إعدادات المنصة السيادية الشاملة 2026 ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Integrated Command", page_icon="🛡️")

# --- 2. محرك جلب الطائرات الحقيقي (المجال الجوي الجزائري) ---
def get_live_flights():
    # إحداثيات تغطي كامل جغرافيا الجزائر من الشمال للجنوب
    url = "https://opensky-network.org/api/states/all?lamin=18.0&lomin=-9.0&lamax=38.0&lomax=12.5"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        flights = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                flights.append({
                    "callsign": s[1].strip() if s[1] else "UNKNOWN",
                    "lat": s[6], "lon": s[5],
                    "alt": s[7] if s[7] else 0,
                    "velocity": s[9] if s[9] else 0
                })
        return flights
    except:
        return []

# --- 3. نظام الدخول ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🛡️ GeoSentinel-DZ</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            password = st.text_input("رمز الدخول العملياتي", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if password == "DZ_ADMIN_2026":
                    st.session_state.authenticated = True
                    st.rerun()
else:
    # --- 4. لوحة التحكم الجانبية (كل الأدوات السابقة) ---
    with st.sidebar:
        st.header("🎮 لوحة التحكم المركزية")
        if st.button("🔄 تحديث يدوي فوري", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        monitor_mode = st.radio("نظام الرصد", ["رصد نهار (Hybrid)", "رصد حراري (Night)", "تحليل القشرة (Sentinel)"])
        
        show_tracks = st.toggle("👣 إظهار مسارات التهريب", value=True)
        show_flights = st.toggle("✈️ تفعيل رادار الطيران", value=True)
        
        st.markdown("---")
        st.subheader("🕰️ المقارنة التاريخية (حتى اليوم)")
        compare_date = st.date_input("تاريخ المقارنة ضد اليوم", value=datetime.now() - timedelta(days=30))
        
        if st.button("🗑️ مسح الجلسة"):
            st.session_state.authenticated = False
            st.rerun()

    # --- 5. بناء الخريطة المدمجة ---
    st.title("🛡️ مركز القيادة والرصد الجغرافي | GeoSentinel-DZ")
    
    # تحديد الطبقة الأساسية
    if "تحليل القشرة" in monitor_mode:
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}' # Satellite Pure
    else:
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}' # Hybrid

    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles=tiles, attr='GeoSentinel Hybrid 2026')
    m.add_child(plugins.MeasureControl(position='topleft'))

    # أ. رسم الحدود الوطنية (الأصلية)
    border = [[37.0, 8.5], [19.0, 5.0], [21.0, -4.5], [37.0, 8.5]]
    folium.PolyLine(border, color="yellow", weight=4, opacity=0.4, tooltip="الحدود").add_to(m)

    # ب. إدماج رادار الطيران الحي (FlightAware Link)
    if show_flights:
        live_flights = get_live_flights()
        for f in live_flights:
            if f['lat'] and f['lon']:
                fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
                folium.Marker(
                    [f['lat'], f['lon']],
                    icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(20, 20)),
                    popup=folium.Popup(f"<b>{f['callsign']}</b><br>رابط التتبع الحقيقي:<br><a href='{fa_link}' target='_blank'>FlightAware Live</a>", max_width=250)
                ).add_to(m)

    # ج. المسارات ونقاط مقارنة القشرة الأرضية (Sentinel 2026)
    if show_tracks:
        # مسار حدودي مرسوم
        path_coords = [[19.2, 3.5], [20.5, 1.8], [21.3, 0.95]]
        folium.PolyLine(path_coords, color="cyan", weight=3, dash_array='5').add_to(m)
        
        # نقاط تحليل التغيرات (خنادق ومطارات)
        hotspots = [
            {"loc": [21.32, 0.95], "label": "رصد تغيرات الخنادق (برج باجي مختار)"},
            {"loc": [24.50, 9.30], "label": "تحليل مسارات التهريب (جانت)"}
        ]
        for h in hotspots:
            # رابط المقارنة الزمنية المباشر لليوم ضد التاريخ المختار
            sentinel_url = f"https://apps.sentinel-hub.com/eo-browser/?zoom=13&lat={h['loc'][0]}&lng={h['loc'][1]}&themeId=DEFAULT-THEME&datasetId=S2L2A&fromTime={compare_date}T00%3A00%3A00.000Z&toTime={datetime.now().strftime('%Y-%m-%d')}T23%3A59%3A59.999Z"
            folium.Marker(
                h['loc'],
                icon=folium.Icon(color='red', icon='eye', prefix='fa'),
                popup=folium.Popup(f"<b>{h['label']}</b><br><a href='{sentinel_url}' target='_blank'>👁️ قارن القشرة (اليوم ضد السابق)</a>", max_width=300)
            ).add_to(m)

    # د. تطبيق الرؤية الليلية
    if "حراري" in monitor_mode:
        st.markdown("<style>.night-vision { filter: invert(1) hue-rotate(180deg) brightness(0.9); }</style>", unsafe_allow_html=True)
        st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=650)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st_folium(m, width="100%", height=650)

    st.success(f"✅ تم دمج كافة الأنظمة بنجاح. المجال الجوي والقشرة الأرضية قيد الرصد المباشر تحديث {datetime.now().year}.")
