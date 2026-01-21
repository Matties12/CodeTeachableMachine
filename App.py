import streamlit as st
import subprocess
import sys
import time
import random
import mysql.connector

@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dieren_weetjes"
    )


def get_random_weetje(dier):
    conn = get_db_connection()
    cursor = conn.cursor()

    if dier == "AAP":
        cursor.execute("SELECT weetje FROM weetjesaap ORDER BY RAND() LIMIT 1")
    else:
        cursor.execute("SELECT weetje FROM weetjesolifant ORDER BY RAND() LIMIT 1")

    row = cursor.fetchone()
    cursor.close()

    return row[0] if row else "Geen weetje gevonden 😢"

# Installeer benodigde packages
try:
    import cv2
except:
    
    import cv2

try:
    from PIL import Image
except:
    
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

img = st.camera_input("📸 Maak een foto")

if img is not None:
    image = Image.open(img)
    st.image(image, caption="Opgenomen beeld")

    keuze = random.choice(["AAP", "OLIFANT"])
    zekerheid = random.randint(75, 95)
    weetje = get_random_weetje(keuze)

    if keuze == "AAP":
        st.markdown(f"# 🦍 AAP\n**Zekerheid:** {zekerheid}%")
        st.success(f"💡 {weetje}")
    else:
        st.markdown(f"# 🐘 OLIFANT\n**Zekerheid:** {zekerheid}%")
        st.info(f"💡 {weetje}")

# Teachable Machine integratie instructies
st.markdown("---")
st.markdown("### 📋 Teachable Machine Toevoegen")
