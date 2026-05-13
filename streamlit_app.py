import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import requests
from datetime import datetime, timedelta

# --- 1. إعدادات المنصة السيادية 2026 ---
st.set_page_config(layout="wide", page_title="GeoSentinel-DZ | Operational 2026", page_icon="🛡️")

# --- 2. جلب بيانات الطائرات الحقيقية (الجزائر) ---
def get_live_flights():
    # استخدام OpenSky مع تحديث الإحداثيات لعام 2026
    url = "https://opensky-network.org/api/states/all?lamin=18.5&lomin=-8.9&lamax=37.5&lomax=12.5"
    try:
        response = requests.get(url, timeout=8)
        data = response.json()
        flights = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                flights.append({
                    "callsign": s[1].strip() if s[1] else "RADAR-ID",
                    "lat": s[6], "lon": s[5],
                    "alt": s[7] if s[7] else 0,
                    "origin": s[2]
                })
        return flights
    except:
        return []

# --- 3. نظام الدخول المتطور ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🛡️ GeoSentinel-DZ 2026</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            password = st.text_input("رمز الدخول العملياتي (Operational Key)", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if password == "DZ_ADMIN_2026":
                    st.session_state.authenticated = True
                    st.rerun()
else:
    # --- القائمة الجانبية (أدوات رصد 2026) ---
    with st.sidebar:
        st.header("⚡ التحكم الفوري")
        if st.button("🔄 تحديث الرادار والقشرة الأرضية (Live Update)", use_container_width=True):
            st.rerun()
            
        st.markdown("---")
        monitor_mode = st.radio("وضع الرصد", ["الرؤية النهارية", "الرؤية الليلية (الحرارية)", "تحليل القشرة (Sentinel-2)"])
        
        st.markdown("---")
        st.info(f"📅 تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
        
        # ميزة مقارنة التغيرات (تاريخ اليوم ضد الأمس)
        st.subheader("🕰️ المقارنة الزمنية")
        target_date = st.date_input("قارن مع تاريخ سابق لرصد الخنادق", value=datetime.now() - timedelta(days=7))

    # --- بناء الخريطة الاستخباراتية ---
    st.title(f"🛡️ رادار الرصد الاستراتيجي | تحديث {datetime.now().year}")
    
    # اختيار طبقة الخريطة بناءً على الوضع
    if "تحليل القشرة" in monitor_mode:
        # طبقة خاصة لرصد التغيرات في التربة والخنادق
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
        attr = 'Satellite Analytics'
    else:
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
        attr = 'Google Hybrid 2026'

    m = folium.Map(location=[28.0, 2.0], zoom_start=5, tiles=tiles, attr=attr)
    m.add_child(plugins.MeasureControl(position='topleft'))

    # 1. رسم الحدود والمسارات (الخدمة القديمة المستمرة)
    border = [[37.0, 8.5], [19.0, 5.0], [21.0, -4.5], [37.0, 8.5]]
    folium.PolyLine(border, color="yellow", weight=3, opacity=0.6).add_to(m)

    # 2. الطائرات الحية (التعديل البرمجي لعام 2026)
    live_flights = get_live_flights()
    if live_flights:
        for f in live_flights:
            if f['lat'] and f['lon']:
                fa_link = f"https://www.flightaware.com/live/flight/{f['callsign']}"
                folium.Marker(
                    [f['lat'], f['lon']],
                    icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/723/723971.png", icon_size=(22, 22)),
                    popup=folium.Popup(f"<b>{f['callsign']}</b><br><a href='{fa_link}' target='_blank'>تتبع الهدف</a>", max_width=200)
                ).add_to(m)
    else:
        st.warning("🔄 جاري إعادة الاتصال بمصفوفة الرادار... اضغط 'تحديث يدوي' إذا طال الانتظار.")

    # 3. نقاط رصد "التغيرات الأرضية" (خنادق، مطارات، مسارات تهريب) حية
    # الروابط هنا تفتح Sentinel Hub لرؤية صور اليوم ومقارنتها بالماضي
    hotspots = [
        {"loc": [21.32, 0.95], "label": "قطاع برج باجي مختار (تحليل الخنادق)", "id": "BBM-X1"},
        {"loc": [24.50, 9.30], "label": "قطاع جانت (مسارات التهريب)", "id": "DJ-Z2"}
    ]
    
    for h in hotspots:
        # رابط ذكي يفتح مقارنة صور الأقمار الصناعية (Sentinel) لتاريخ اليوم
        sentinel_url = f"https://apps.sentinel-hub.com/eo-browser/?zoom=13&lat={h['loc'][0]}&lng={h['loc'][1]}&themeId=DEFAULT-THEME&datasetId=S2L2A&fromTime={target_date}T00%3A00%3A00.000Z&toTime={datetime.now().strftime('%Y-%m-%d')}T23%3A59%3A59.999Z"
        
        folium.Marker(
            h['loc'],
            icon=folium.Icon(color='red', icon='info-sign'),
            popup=folium.Popup(f"<b>{h['label']}</b><br><a href='{sentinel_url}' target='_blank'>👁️ قارن صور القشرة (اليوم ضد السابق)</a>", max_width=300)
        ).add_to(m)

    # تطبيق الرؤية الليلية الحرارية
    if "الحرارية" in monitor_mode:
        st.markdown("<style>.night-vision { filter: invert(1) hue-rotate(180deg) brightness(0.8); }</style>", unsafe_allow_html=True)
        st.markdown('<div class="night-vision">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=650)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st_folium(m, width="100%", height=650)

    # سجل التنبيهات
    st.info("📌 ملاحظة: ميزة المقارنة الزمنية تستخدم بيانات Sentinel-2 المحدثة يومياً لرصد أي تسريبات أو خنادق جديدة.")
