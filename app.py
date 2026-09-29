from PIL import Image
from googletrans import Translator
import pandas as pd
import streamlit as st
from textblob import TextBlob

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Sentimiento - NLP",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- ESTILOS CSS ESTILO DARK PSYCHOLOGY ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general oscuro estilo noche profunda */
    .stApp {
        background-color: #0A0A0C;
        color: #E2E8F0;
    }

    /* Banner de Encabezado Psicología Oscura */
    .hero-container {
        background: linear-gradient(135deg, #111116 0%, #1A102F 50%, #0A0A0C 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #2D1B4E;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 15px rgba(139, 92, 246, 0.15);
        margin-bottom: 2rem;
    }
    .hero-container h1 {
        color: #F8FAFC !important;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .hero-container p {
        color: #94A3B8;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Barra Lateral Estilizada */
    [data-testid="stSidebar"] {
        background-color: #0F0F14;
        border-right: 1px solid #1E1E28;
    }

    /* Tarjetas de Métricas */
    .metric-card {
        background: #13131A;
        border: 1px solid #27273A;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card .label {
        color: #A0AEC0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        color: #8B5CF6;
        font-size: 2rem;
        font-weight: 700;
    }

    /* Ajustes visuales de Inputs y Expanders */
    .stTextInput > div > div > input {
        background-color: #13131A !important;
        color: #F8FAFC !important;
        border: 1px solid #27273A !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 8px rgba(139, 92, 246, 0.4) !important;
    }

    /* Modificación de alertas/mensajes */
    .stAlert {
        background-color: #13131A !important;
        border: 1px solid #27273A !important;
        color: #E2E8F0 !important;
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

try:
    image = Image.open("emoticones.jpg")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

translator = Translator()

# --- BARRA LATERAL CON INFORMACIÓN ---
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
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        polarity_val = round(blob.sentiment.polarity, 2)
        subjectivity_val = round(blob.sentiment.subjectivity, 2)

        # Visualización elegante de métricas en 2 columnas
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

        x = polarity_val
        if x > 0.0 and x <= 1.0:
            st.success("Es un sentimiento Positivo 😊")
        elif x >= -1 and x <= 0:
            st.error("Es un sentimiento Negativo 😔")
        else:
            st.info("Es un sentimiento Neutral 😐")
