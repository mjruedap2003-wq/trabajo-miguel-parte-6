from PIL import Image
from deep_translator import GoogleTranslator
import pandas as pd
import streamlit as st
from textblob import TextBlob

# --- INTERFAZ PRINCIPAL ORIGINAL ---
st.title("Análisis de Sentimiento")

try:
    image = Image.open("emoticones.jpg")
    st.image(image)
except FileNotFoundError:
    pass

st.subheader(
    "Por favor escribe en el campo de texto la frase que deseas analizar"
)

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    """
    Polaridad: Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
    Su valor oscila entre -1 (muy negativo) y 1 (muy positivo), con 0 representando un sentimiento neutral.
    
    Subjetividad: Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
    (hechos). Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """

with st.expander("Analizar texto"):
    text = st.text_input("Escribe por favor: ")
    if text:
        # Traducción usando deep-translator para mayor estabilidad en GitHub
        trans_text = GoogleTranslator(source="es", target="en").translate(text)
        blob = TextBlob(trans_text)

        st.write("Polarity: ", round(blob.sentiment.polarity, 2))
        st.write("Subjectivity: ", round(blob.sentiment.subjectivity, 2))

        x = round(blob.sentiment.polarity, 2)
        if x > 0.0 and x <= 1.0:
            st.write("Es un sentimiento Positivo 😊")
        elif x >= -1 and x <= 0:
            st.write("Es un sentimiento Negativo 😔")
        else:
            st.write("Es un sentimiento Neutral 😐")
