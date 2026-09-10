import json
import os

from deep_translator import GoogleTranslator
from PIL import Image
import streamlit as st
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración básica de la aplicación
st.set_page_config(
    page_title="Evaluación de Bienestar Emocional",
    page_icon="🧠",
    layout="centered",
)


# Función para cargar el archivo Lottie local sin romper la app si no existe
def load_lottiefile(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None


st.title("🧠 Evaluación de Estado de Animo y Bienestar")
st.write(
    "Parchate y responde con sinceridad. Recuerda que **no hay respuestas"
    " buenas ni malas**."
)

# Cargar y mostrar la animación Lottie (JSON)
lottie_anim = load_lottiefile("Juggling ball.json")
if lottie_anim:
    st_lottie(lottie_anim, height=250, key="juggling")
else:
    st.info(
        "💡 Nota: Puedes agregar el archivo 'Juggling ball.json' para ver la"
        " animación."
    )

st.divider()

st.subheader("📋 Campo de Expresión Emocional")
st.write("Escribe cómo te has sentido en estos últimos días o describe tu día a día:")

# Entrada de texto del usuario
text = st.text_area(
    "Escribe tu respuesta aquí:",
    placeholder="Ejemplo: Hoy me he sentido un poco abrumado con las tareas y sin mucha energía...",
    height=120,
)

if st.button("🚀 Analizar Estado Emocional", type="primary"):
    if not text.strip():
        st.warning("Por favor escribe una frase o texto para analizar.")
    else:
        with st.spinner("Analizando respuesta..."):
            try:
                # 1. Traducción del texto de Español a Inglés para TextBlob
                translated_text = GoogleTranslator(
                    source="es", target="en"
                ).translate(text)

                # 2. Análisis de sentimiento mediante TextBlob
                blob = TextBlob(translated_text)
                polarity = round(blob.sentiment.polarity, 2)
                subjectivity = round(blob.sentiment.subjectivity, 2)

                st.divider()
                st.subheader("📊 Resultados de la Evaluación")

                # Mostrar métricas del análisis
                col1, col2 = st.columns(2)
                col1.metric(label="Nivel de Polaridad", value=polarity)
                col2.metric(label="Subjetividad", value=subjectivity)

                # 3. Interacción según el nivel de sentimiento detectado
                st.subheader("💬 Recomendación Psicopedagógica:")

                if polarity > 0.15:
                    st.success("😊 **¡Excelente estado mental!**")
                    st.write(
                        "Tus palabras reflejan una actitud positiva, balance"
                        " emocional y un estado de ánimo óptimo. ¡Sigue"
                        " cultivando esos hábitos saludables que te hacen"
                        " bien!"
                    )
                    st.balloons()

                elif polarity < -0.15:
                    st.error(
                        "😔 **Recomendación: Considera buscar acompañamiento"
                        " profesional.**"
                    )
                    st.write(
                        "Detectamos una carga de tensión, tristeza o malestar"
                        " emocional en lo que escribiste. **Ir al psicólogo o"
                        " hablar con un profesional de la salud mental** es"
                        " un paso valioso para cuidar de ti."
                    )
                    st.warning(
                        "📍 *Recuerda: Pedir ayuda no es síntoma de debilidad,"
                        " sino un acto de valentía y autocuidado.*"
                    )

                else:
                    st.info("😐 **Estado Neutro / Estable**")
                    st.write(
                        "Tus palabras indican un punto de equilibrio o"
                        " neutralidad. Vas por buen camino; mantén la escucha"
                        " de tus emociones y procura realizar actividades que"
                        " te generen bienestar."
                    )

            except Exception as e:
                st.error(f"Ocurrió un error durante el procesamiento: {e}")
