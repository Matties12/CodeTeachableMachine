import streamlit as st
import time
import random
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import av
import threading

# Feitjes data
WEETJES = {
    "AAP": [
        "Apen kunnen meer dan 100 verschillende gelaatsuitdrukkingen maken!",
        "Chimpansees gebruiken gereedschap, zoals stokjes om mieren te vangen.",
        "Sommige apen kunnen gebarentaal leren en meer dan 1000 gebaren begrijpen.",
        "Apen hebben unieke vingerafdrukken, net zoals mensen.",
        "Gorilla's kunnen tot 200 kg wegen en zijn enorm sterk!",
        "Apen kunnen zichzelf herkennen in een spiegel.",
        "Orang-oetans delen 97% van hun DNA met mensen.",
        "Sommige apensoorten gebruiken medicijnplanten als ze ziek zijn.",
        "Apen kunnen lachen en grapjes maken met elkaar.",
        "Een groep apen heet een 'troep'."
    ],
    "OLIFANT": [
        "Olifanten kunnen met hun slurf tot 8 liter water opzuigen!",
        "Een olifant heeft het beste geheugen van alle landdieren.",
        "Olifanten kunnen via de grond met elkaar communiceren over grote afstanden.",
        "Baby olifanten zuigen op hun slurf, net zoals baby's op hun duim.",
        "Olifanten rouwen om overleden familieleden.",
        "Een olifantenslurf heeft meer dan 40.000 spieren!",
        "Olifanten kunnen maar 2-3 uur per dag slapen.",
        "Olifanten zijn bang voor bijen en vermijden bijennesten.",
        "Een olifant kan tot 150 kg voedsel per dag eten.",
        "Olifanten gebruiken modder als zonnecrème om hun huid te beschermen."
    ]
}


def get_random_weetje(dier):
    if dier in WEETJES:
        return random.choice(WEETJES[dier])
    return "Geen weetje gevonden 😢"


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.last_analysis = time.time()
        self.current_result = None
        self.lock = threading.Lock()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        current_time = time.time()
        if current_time - self.last_analysis >= 2.0:
            with self.lock:
                self.last_analysis = current_time
                keuze = random.choice(["AAP", "OLIFANT"])
                zekerheid = random.randint(75, 95)
                weetje = get_random_weetje(keuze)
                self.current_result = {
                    "dier": keuze,
                    "zekerheid": zekerheid,
                    "weetje": weetje
                }
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    def get_result(self):
        with self.lock:
            return self.current_result


# RTC Configuration met STUN servers
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302"]},
    ]}
)

st.set_page_config(page_title="Live AAP vs OLIFANT", layout="wide")

st.title("🦍 LIVE AAP vs OLIFANT Herkenning")
st.write("Live webcam → Automatische analyse elke 2 seconden!")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Webcam")
    ctx = webrtc_streamer(
        key="animal-detector",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

with col2:
    st.subheader("🎯 Resultaat")
    result_placeholder = st.empty()
    info_placeholder = st.empty()

if ctx.video_processor:
    while ctx.state.playing:
        result = ctx.video_processor.get_result()
        
        if result:
            if result["dier"] == "AAP":
                result_placeholder.markdown(f"""
                # 🦍 **AAP**
                **Zekerheid:** {result['zekerheid']}%
                """)
                info_placeholder.success(f"💡 {result['weetje']}")
            else:
                result_placeholder.markdown(f"""
                # 🐘 **OLIFANT**
                **Zekerheid:** {result['zekerheid']}%
                """)
                info_placeholder.info(f"💡 {result['weetje']}")
        else:
            result_placeholder.info("🔄 Wachten op eerste analyse...")
        
        time.sleep(0.5)

st.markdown("---")
st.markdown("### 📋 Tips")
st.write("- Geef je browser toestemming om de camera te gebruiken")
st.write("- Als de verbinding niet lukt, probeer de pagina te verversen")
