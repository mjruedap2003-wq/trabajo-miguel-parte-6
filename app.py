import json
import os

from deep_translator import GoogleTranslator
from PIL import Image
import streamlit as st
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración de la app
st.set_page_config(
    page_title="Evaluación de Bienestar Emocional",
    page_icon="🧠",
    layout="centered",
)


def load_lottiefile(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None


st.title("🧠 Evaluación de Estado de Ánimo y Bienestar")
st.write(
    "Parchate y responde con sinceridad. Recuerda que **no hay respuestas"
    " buenas ni malas**."
)

lottie_anim = load_lottiefile("Juggling ball.json")
if lottie_anim:
    st_lottie(lottie_anim, height=250, key="juggling")

st.divider()

st.subheader("📋 Campo de Expresión Emocional")
st.write("Escribe cómo te has sentido en estos últimos días o describe tu día a día:")

text = st.text_area(
    "Escribe tu respuesta aquí:",
    placeholder="Ejemplo: Hoy estoy deprimido, no estoy contento, necesito ayuda...",
    height=120,
)


# Función para traducir de forma ultra segura
def traducir_texto(texto_original):
    try:
        # Intento 1: Uso de deep-translator
        return GoogleTranslator(source="auto", target="en").translate(texto_original)
    except Exception:
        # Intento 2: Si la API de traducción se bloquea, devolvemos el texto limpio
        return texto_original


if st.button("🚀 Analizar Estado Emocional", type="primary"):
    if not text.strip():
        st.warning("Por favor escribe una frase o texto para analizar.")
    else:
        with st.spinner("Analizando respuesta..."):
            # 1. Traducir el texto al inglés para TextBlob
            texto_traducido = traducir_texto(text)

            # 2. Análisis de sentimiento mediante TextBlob
            blob = TextBlob(texto_traducido)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            # Ajuste manual por palabras clave en español en caso de que falle la traducción
            palabras_tristes = [
                "deprimido",
                "deprimida",
                "triste",
                "ayuda",
                "llorar",
                "mal",
                "solo",
                "sola",
                "horrible",
            ]
            contiene_palabras_tristes = any(
                p in text.lower() for p in palabras_tristes
            )

            # Fuerza polaridad negativa si contiene léxico explícito de depresión/tristeza
            if contiene_palabras_tristes and polarity >= 0:
                polarity = -0.5

            st.divider()
            st.subheader("📊 Resultados de la Evaluación")

            col1, col2 = st.columns(2)
            col1.metric(label="Nivel de Polaridad", value=polarity)
            col2.metric(label="Subjetividad", value=subjectivity)

            st.subheader("💬 Recomendación Psicopedagógica:")

            if polarity > 0.15:
                st.success("😊 **¡Excelente estado mental!**")
                st.write(
                    "Tus palabras reflejan una actitud positiva, balance"
                    " emocional y un estado de ánimo óptimo. ¡Sigue cultivando"
                    " esos hábitos saludables que te hacen bien!"
                )
                st.balloons()

            elif polarity < -0.10:
                st.error(
                    "😔 **Recomendación: Considera buscar acompañamiento"
                    " profesional.**"
                )
                st.write(
                    "Detectamos una carga de tensión, tristeza o malestar"
                    " emocional en lo que escribiste. **Ir al psicólogo o hablar"
                    " con un profesional de la salud mental** es un paso valioso"
                    " para cuidar de ti."
                )
                st.warning(
                    "📍 *Recuerda: Pedir ayuda no es síntoma de debilidad, sino"
                    " un acto de valentía y autocuidado.*"
                )

            else:
                st.info("😐 **Estado Neutro / Estable**")
                st.write(
                    "Tus palabras indican un punto de equilibrio o"
                    " neutralidad. Vas por buen camino; mantén la escucha de"
                    " tus emociones y procura realizar actividades que te"
                    " generen bienestar."
                )
