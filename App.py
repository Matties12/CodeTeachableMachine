import streamlit as st
import cv2
import numpy as np
import av
import tensorflow as tf
from PIL import Image, ImageOps
from streamlit_webrtc import webrtc_streamer
import random
import time

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

# Load Model
@st.cache_resource
def load_keras_model():
    model = tf.keras.models.load_model('keras_model.h5')
    return model

try:
    model = load_keras_model()
except Exception as e:
    st.error(f"Fout bij het laden van het model: {e}")
    model = None

# Labels mapping
LABELS = {0: "OLIFANT", 1: "AAP"}

st.set_page_config(page_title="AAP vs OLIFANT", layout="wide")

st.title("🦍 AAP vs OLIFANT Live Herkenning")
st.write("De camera herkent automatisch of het een aap of een olifant is!")

class VideoProcessor:
    def __init__(self):
        self.last_prediction = None
        self.frame_count = 0
        self.current_fact = ""
        self.fact_update_time = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Prepare for model
        input_shape = (224, 224)
        img_resized = cv2.resize(img, input_shape)
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize (Standard Teachable Machine preprocessing: (val / 127.5) - 1)
        img_normalized = (img_rgb.astype(np.float32) / 127.5) - 1
        data = np.expand_dims(img_normalized, axis=0)
        
        # Predict
        if model:
            prediction = model.predict(data)
            index = np.argmax(prediction)
            confidence = prediction[0][index]
            
            label = LABELS.get(index, "Onbekend")
            
            # Update display info
            color = (0, 255, 0) if label == "AAP" else (255, 0, 0)
            
            # Simple UI on video
            text = f"{label}: {int(confidence * 100)}%"
            cv2.putText(img, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Show a fact
            if confidence > 0.8:
                current_time = time.time()
                # Update fact every 5 seconds if label is stable or just show random
                if current_time - self.fact_update_time > 5 or self.last_prediction != label:
                    if label in WEETJES:
                        self.current_fact = random.choice(WEETJES[label])
                    self.fact_update_time = current_time
                
                self.last_prediction = label
                
                # Draw fact (wrapping text is hard in cv2, keeping it short or subtitle style)
                # Just draw first part of fact for simplicity on overlay
                cv2.putText(img, "Weetje:", (10, img.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Simple text wrapping for CV2
                max_width = img.shape[1] - 20
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                thickness = 1
                
                words = self.current_fact.split(' ')
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    cnt_size = cv2.getTextSize(' '.join(current_line), font, font_scale, thickness)[0]
                    if cnt_size[0] > max_width:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                lines.append(' '.join(current_line))
                
                y_offset = img.shape[0] - 30
                for i, line in enumerate(reversed(lines)): # Draw from bottom up
                     cv2.putText(img, line, (10, y_offset - (i * 25)), font, font_scale, (255, 255, 255), thickness)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Live Camera Feed")
    webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

with col2:
    st.markdown("### ℹ️ Instructies")
    st.write("1. Sta camera toegang toe.")
    st.write("2. Houd een foto of object van een **AAP** of **OLIFANT** voor de camera.")
    st.write("3. Het systeem herkent het automatisch!")
    
    st.info("💡 De 'weetjes' verschijnen direct op het camerabeeld!")
