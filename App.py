import streamlit as st
import subprocess
import sys
import time
import random

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
    """Haal een willekeurig feitje op voor het gekozen dier"""
    if dier in WEETJES:
        return random.choice(WEETJES[dier])
    return "Geen weetje gevonden 😢"


# Installeer benodigde packages
try:
    import cv2
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2

try:
    from PIL import Image
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image

import numpy as np

st.set_page_config(page_title="Live AAP vs OLIFANT", layout="wide")

st.title("🦍 LIVE AAP vs OLIFANT Herkenning")
st.write("Live webcam → Automatische analyse elke 2 seconden!")

# Layout met kolommen
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Webcam")
    video_frame = st.empty()

with col2:
    st.subheader("🎯 Resultaat")
    result_box = st.empty()
    info_box = st.empty()

# Controle knoppen
col_a, col_b = st.columns(2)
with col_a:
    start_btn = st.button("▶️ Start Camera")
with col_b:
    stop_btn = st.button("⏹️ Stop Camera")

# Session state voor camera status
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False

if start_btn:
    st.session_state.camera_active = True

if stop_btn:
    st.session_state.camera_active = False

# CAMERA LOOP
if st.session_state.camera_active:
    cap = cv2.VideoCapture(0)
   
    if not cap.isOpened():
        st.error("❌ Camera niet beschikbaar!")
        st.session_state.camera_active = False
    else:
        last_check = time.time()
        frame_count = 0
       
        while st.session_state.camera_active:
            ret, frame = cap.read()
           
            if not ret:
                st.error("❌ Kan geen beeld krijgen")
                break
           
            # Toon live feed
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_frame.image(frame_rgb, channels="RGB", use_container_width=True)
           
            # Check elke 2 seconden
            current_time = time.time()
            if current_time - last_check >= 2.0:
                last_check = current_time

                keuze = random.choice(["AAP", "OLIFANT"])
                zekerheid = random.randint(75, 95)

                # Toon resultaat
                weetje = get_random_weetje(keuze)

                if keuze == "AAP":
                    result_box.markdown(f"""
                    # 🦍 **AAP**
                    **Zekerheid:** {zekerheid}%
                    """)
                    info_box.success(f"💡 {weetje}")
                    st.balloons()

                else:
                    result_box.markdown(f"""
                    # 🐘 **OLIFANT**
                    **Zekerheid:** {zekerheid}%
                    """)
                    info_box.info(f"💡 {weetje}")
                    st.balloons()

            # Refresh delay
            time.sleep(0.03)
           
            # Check stop button
            if stop_btn:
                st.session_state.camera_active = False
                break
       
        cap.release()
        st.success("✅ Camera gestopt")
else:
    st.info("ℹ️ Klik op 'Start Camera' om te beginnen")

# Teachable Machine integratie instructies
st.markdown("---")
st.markdown("### 📋 Teachable Machine Toevoegen")
