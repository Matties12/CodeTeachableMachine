import streamlit as st
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


st.set_page_config(page_title="Live AAP vs OLIFANT", layout="wide")

st.title("🦍 LIVE AAP vs OLIFANT Herkenning")
st.write("Maak een foto met je camera!")

# Layout met kolommen
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Camera")
    # Streamlit's ingebouwde camera widget
    camera_photo = st.camera_input("Maak een foto")

with col2:
    st.subheader("🎯 Resultaat")
    
    if camera_photo is not None:
        # Simuleer analyse
        with st.spinner("Analyzing..."):
            time.sleep(1)
        
        keuze = random.choice(["AAP", "OLIFANT"])
        zekerheid = random.randint(75, 95)
        weetje = get_random_weetje(keuze)

        if keuze == "AAP":
            st.markdown(f"""
            # 🦍 **AAP**
            **Zekerheid:** {zekerheid}%
            """)
            st.success(f"💡 {weetje}")
            st.balloons()
        else:
            st.markdown(f"""
            # 🐘 **OLIFANT**
            **Zekerheid:** {zekerheid}%
            """)
            st.info(f"💡 {weetje}")
            st.balloons()
    else:
        st.info("📷 Maak een foto om te beginnen")

# Teachable Machine integratie instructies
st.markdown("---")
st.markdown("### 📋 Teachable Machine Toevoegen")
st.write("Later kunnen we hier echte AI-herkenning toevoegen!")
