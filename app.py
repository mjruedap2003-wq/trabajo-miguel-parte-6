import json
import os
import pandas as pd
from PIL import Image
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
from streamlit_lottie import st_lottie

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Sentimientos - NLP",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- FUNCIÓN PARA CARGAR LA ANIMACIÓN LOTTIE (JSON) ---
def load_lottie_file(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# --- ESTILOS CSS ESTILO DARK PSYCHOLOGY & ALTO CONTRASTE ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0A0A0C;
        color: #FFFFFF !important;
    }

    p, span, label, .stMarkdown, div {
        color: #FFFFFF !important;
    }

    .hero-container {
        background: linear-gradient(135deg, #111116 0%, #1A102F 50%, #0A0A0C 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #3B206E;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 15px rgba(139, 92, 246, 0.25);
        margin-bottom: 2rem;
    }
    .hero-container h1 {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .hero-container p {
        color: #E2E8F0 !important;
        font-size: 1.05rem;
        margin: 0;
    }

    [data-testid="stSidebar"] {
        background-color: #0F0F14;
        border-right: 1px solid #1E1E28;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    .metric-card {
        background: #13131A;
        border: 1px solid #3B206E;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card .label {
        color: #FFFFFF !important;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        color: #A78BFA !important;
        font-size: 2.2rem;
        font-weight: 700;
    }

    .stTextInput label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    .stTextInput > div > div > input {
        background-color: #13131A !important;
        color: #FFFFFF !important;
        border: 1px solid #3B206E !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5) !important;
    }

    .stAlert {
        background-color: #13131A !important;
        border: 1px solid #3B206E !important;
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DICCIONARIOS DE PALABRAS PREDETERMINADAS EN ESPAÑOL ---
PALABRAS_POSITIVAS = [
    "feliz", "contento", "entusiasmado", "alegre", "optimista", 
    "animado", "radiante", "excelente", "genial", "bien", "encantado"
]

PALABRAS_NEUTRALES = [
    "normal", "serio", "transparente", "regular", "indiferente", 
    "tranquilo", "estable", "imparcial", "sin novedad", "ok"
]

PALABRAS_NEGATIVAS = [
    "triste", "aburrido", "decaido", "decaído", "deprimido", "maricon", 
    "maricón", "malo", "enojado", "molesto", "desanimado", "solo", 
    "frustrado", "ansioso", "agobiado", "estresado", "rabia"
]

# --- CABECERA ---
st.markdown(
    """
    <div class="hero-container">
        <h1>🧠 Análisis de Sentimiento</h1>
        <p>Procesamiento del Lenguaje Natural & Diagnóstico Emocional</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- CÁRGAR Y MOSTRAR LA ANIMACIÓN LOTTIE (JSON) ---
lottie_juggling = load_lottie_file("Juggling ball.json")

if lottie_juggling:
    st_lottie(lottie_juggling, height=220, key="juggling_anim")

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# --- BARRA LATERAL ---
with st.sidebar:
    st.subheader("📊 Polaridad y Subjetividad")
    """
    **Polaridad:** Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
    Su valor oscila entre **-1** (muy negativo) y **1** (muy positivo), con **0** representando un sentimiento neutral.

    ---
    
    **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
    (hechos). Va de **0** a **1**, donde **0** es completamente objetivo y **1** es completamente subjetivo.
    """

# --- SECCIÓN DE ANÁLISIS ---
with st.expander("🔍 Analizar texto", expanded=True):
    text = st.text_input("Escribe por favor:")
    if text:
        text_lower = text.lower().strip()
        
        # 1. DETECCIÓN POR PALABRAS CLAVE PREDETERMINADAS
        categoria_manual = None
        if any(palabra in text_lower for palabra in PALABRAS_POSITIVAS):
            categoria_manual = "positiva"
            polarity_val = 0.80
            subjectivity_val = 0.75
        elif any(palabra in text_lower for palabra in PALABRAS_NEGATIVAS):
            categoria_manual = "negativa"
            polarity_val = -0.80
            subjectivity_val = 0.85
        elif any(palabra in text_lower for palabra in PALABRAS_NEUTRALES):
            categoria_manual = "neutral"
            polarity_val = 0.00
            subjectivity_val = 0.10

        # 2. SI NO COINCIDE CON NINGUNA PALABRA CLAVE, USA TEXTBLOB + TRADUCCIÓN
        if not categoria_manual:
            try:
                trans_text = GoogleTranslator(source="auto", target="en").translate(text)
            except Exception:
                trans_text = text

            blob = TextBlob(trans_text)
            polarity_val = round(blob.sentiment.polarity, 2)
            subjectivity_val = round(blob.sentiment.subjectivity, 2)

            if polarity_val > 0.1:
                categoria_manual = "positiva"
            elif polarity_val < -0.1:
                categoria_manual = "negativa"
            else:
                categoria_manual = "neutral"

        # MÓDULO VISUAL DE MÉTRICAS
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="label">Polaridad</div>
                    <div class="value">{polarity_val}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="label">Subjetividad</div>
                    <div class="value">{subjectivity_val}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("---")

        # EVALUACIÓN FINAL Y RECOMENDACIÓN
        if categoria_manual == "positiva":
            st.success("Es un sentimiento Positivo 😊")
            st.markdown(
                """
                > **Resumen del Diagnóstico:** Expresas un estado emocional favorable u optimista.  
                > **Recomendación:** ¡Sigue así! Mantén esa mentalidad y continúa cultivando actividades que refuercen tu bienestar emocional.
                """
            )
        elif categoria_manual == "negativa":
            st.error("Es un sentimiento Negativo 😔")
            st.markdown(
                """
                > **Resumen del Diagnóstico:** Se detecta una carga emocional de malestar, tristeza o frustración en tu mensaje.  
                > **Recomendación:** Es totalmente normal atravesar momentos difíciles. Sin embargo, si estos sentimientos de tristeza o desánimo persisten en tu día a día, **se recomienda acudir a consulta con un psicólogo o profesional de salud mental** para recibir el acompañamiento adecuado.
                """
            )
        else:
            st.info("Es un sentimiento Neutral 😐")
            st.markdown(
                """
                > **Resumen del Diagnóstico:** Tu estado emocional se percibe en equilibrio o de carácter descriptivo/objetivo.  
                > **Recomendación:** Te encuentras en un punto neutro. Continúa con tus actividades manteniendo esa estabilidad.
                """
            )
