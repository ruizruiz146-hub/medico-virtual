import asyncio
import os
import sys
import time
import json
import base64
import google.generativeai as genai
import edge_tts
import streamlit as st
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA FUTURISTA DE ELITE
st.set_page_config(
    page_title="MED-VIRTUAL PRO | Consola Holográfica",
    page_icon="👨‍⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FUNCIÓN MAESTRA: Lee tu imagen 'fondo' PNG/JPG local de forma nativa
def cargar_fondo_local():
    for nombre in ["fondo", "fondo.png", "fondo.jpg"]:
        if os.path.exists(nombre):
            with open(nombre, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    return ""

fondo_b64 = cargar_fondo_local()

# 2. DISEÑO CSS AVANZADO: TEXTOS EN BLANCO NEÓN + PANEL CRÍTICO VITTAL
if fondo_b64:
    estilo_fondo = f"""
    .stApp {{
        background-image: linear-gradient(rgba(0, 11, 24, 0.40), rgba(0, 11, 24, 0.55)), url('data:image/png;base64,{fondo_b64}');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    """
else:
    estilo_fondo = """
    .stApp {{
        background-color: #000B18;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    """

st.markdown(f"""
<style>
    {estilo_fondo}

    /* Títulos Principales con Brillo de Neón Cian Intenso */
    h1, h2, h3, h4 {{
        color: #00F2FF !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: bold;
    }}

    /* Paneles de Control de Cristal Optimizado */
    [data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlock"] {{
        background-color: rgba(0, 11, 24, 0.82) !important;
        border: 2px solid rgba(0, 242, 255, 0.5);
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(14px);
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2), inset 0 0 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 20px;
    }}

    /* CLASE PREMIUM: Fuerza el Blanco Neón en las líneas métricas del System Monitor */
    .texto-neon-blanco {{
        color: #FFFFFF !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: bold !important;
        font-size: 15px !important;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6), 0 0 15px rgba(255, 255, 255, 0.5);
        display: block;
        margin-bottom: 10px;
        line-height: 1.4;
    }}

    /* Panel de Alerta Crítica Vittal (Estilo Alarma Médica Roja) */
    .contenedor-vittal {{
        background-color: rgba(40, 0, 5, 0.90) !important;
        border: 2px solid #FF3333 !important;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 0 25px rgba(255, 51, 51, 0.4);
    }}
    .titulo-vittal {{
        color: #FF3333 !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.8);
        font-size: 18px;
        margin-bottom: 10px;
    }}
    .texto-vittal {{
        color: #FFFFFF !important;
        font-size: 15px !important;
        line-height: 1.5;
    }}

    /* Respuestas de la IA y Mensajes de Chat */
    .stChatMessage {{
        background-color: rgba(0, 18, 41, 0.88) !important;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 255, 0.4);
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
    }}
    
    .stChatMessage .stMarkdown p {{
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
    }}

    /* Alertas de Streamlit */
    .stAlert {{
        background-color: rgba(0, 30, 15, 0.85) !important;
        border: 1px solid #39FF14 !important;
    }}
    
    /* Input de Escritura Táctil (Chat Input) */
    .stChatInputContainer {{
        border-radius: 20px;
        border: 2px solid #00F2FF !important;
        background-color: rgba(0, 11, 24, 0.95) !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}

    /* Módulo del Lector de Laboratorios Clínicos */
    .stFileUploader {{
        border: 2px dashed rgba(0, 242, 255, 0.7) !important;
        border-radius: 12px;
        padding: 15px;
        background-color: rgba(0, 11, 24, 0.90);
    }}

    /* Botones Interactivos del Panel */
    .stButton>button {{
        background-color: rgba(0, 26, 61, 0.8);
        color: #00F2FF;
        border: 2px solid #00F2FF;
        border-radius: 8px;
        text-transform: uppercase;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
    }}
    .stButton>button:hover {{
        background-color: #00F2FF;
        color: #000B18;
        box-shadow: 0 0 25px #00F2FF;
    }}
    
    /* Botón especial de Llamada de Emergencia */
    .boton-emergencia-vittal>button {{
        background-color: #FF3333 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        text-shadow: 0 0 5px rgba(255,255,255,0.5);
        box-shadow: 0 0 15px rgba(255, 51, 51, 0.6) !important;
    }}
    .boton-emergencia-vittal>button:hover {{
        background-color: #FFFFFF !important;
        color: #FF3333 !important;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.9) !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. CONFIGURACIÓN DEL CEREBRO (Gemini Flash)
API_KEY = "AIzaSyBBG_bOP94Y9WHIKMUi2_fm2v6zz2AnjwA"
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error al configurar la IA: {e}")

SYSTEM_PROMPT = """
Sos el "Médico Virtual Pro", el asistente de salud e inteligencia artificial número 1.
Hablas siempre de "vos" (voseo rioplatense de Argentina). Tu tono es cordial, cálido y profesional.

REGLA PARA ESTUDIOS MÉDICOS (LABORATORIOS / IMÁGENES):
Si el paciente te sube una foto o PDF de un laboratorio o estudio clínico, analizá detalladamente los valores.
Identificá con precisión matemática qué parámetros están fuera de rango (altos o bajos) y explicale al paciente qué significan de forma clara, empática y sin tecnicismos innecesarios.
Planteá posibles causas clínicas de forma orientativa pero recordale siempre la importancia de que lo evalúe su médico de cabecera.
"""

VOZ_ARGENTINA = "es-AR-TomasNeural"
ARCHIVO_AUDIO = "respuesta_medico.mp3"
ARCHIVO_DB = "historial_persistente.json"

# 4. ALGORITMO DE SEGURIDAD MEJORADO (TRIAGE DE CRÍTICOS)
def evaluar_emergencia(texto_usuario):
    if not texto_usuario:
        return False
    texto = texto_usuario.lower()
    palabras_criticas = [
        "pecho", "opresion", "oprime", "braz", "bras", 
        "respirar", "falta el aire", "asfixia", "ahogo", "no tengo aire",
        "duerme el cuerp", "no puedo hablar", "cara caida", "paralisis",
        "hemorragia", "mucha sangre", "desmay", "perdi el conocimiento",
        "infarto", "paro", "inconsciente", "dolor fuerte"
    ]
    for palabra in palabras_criticas:
        if palabra in texto:
            return True
    return False

# 5. GESTOR DE MEMORIA PERSISTENTE
def guardar_en_memoria_permanente(usuario, respuesta):
    registro = {"usuario": usuario, "medico": respuesta, "timestamp": time.time()}
    historial = []
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except:
            historial = []
    historial.append(registro)
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def recuperar_contexto_relevante(consulta_actual):
    if not os.path.exists(ARCHIVO_DB):
        return ""
    try:
        with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
            historial = json.load(f)
        palabras_clave = [p for p in consulta_actual.lower().split() if len(p) > 3]
        fragmentos_utiles = []
        for h in historial:
            coincidencias = sum(1 for p in palabras_clave if p in h["usuario"].lower() or p in h["medico"].lower())
            if modificaciones_locales := (coincidencias > 0 or len(historial) <= 3):
                fragmentos_utiles.append(f"• Paciente: '{h['usuario']}'\n• Respuesta previa: '{h['medico']}'")
        if fragmentos_utiles:
            return "\n[ANTECEDENTES ANTERIORES DETECTADOS EN EL DISCO DURO]:\n" + "\n".join(fragmentos_utiles[-2:])
    except Exception as e:
        print("Error al recuperar memoria:", e)
    return ""

# MODULO DE AUDIO BLINDADO PARA INTERNET (NATIVO DE STREAMLIT)
async def generar_y_reproducir_audio(texto):
    texto_limpio = texto.replace("*", "")
    try:
        communicate = edge_tts.Communicate(texto_limpio, VOZ_ARGENTINA)
        await communicate.save(ARCHIVO_AUDIO)
        st.audio(ARCHIVO_AUDIO, format="audio/mp3", autoplay=True)
    except Exception as audio_error:
        print("Error en el módulo de audio de la nube:", audio_error)

# Inicialización de estados de Streamlit
if "historial_clinico" not in st.session_state:
    st.session_state.historial_clinico = []
if "mensajes_pantalla" not in st.session_state:
    st.session_state.mensajes_pantalla = []
if "estado_critico" not in st.session_state:
    st.session_state.estado_critico = False

# 6. INTERFAZ GRÁFICA (Frontend Sincronizado)
st.markdown("<h1>🤖 MED-VIRTUAL PRO <span style='font-size:16px; color:#BAE6FD;'>v1.5 ES-AR</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00F2FF; font-weight:bold; margin-top:-15px; margin-bottom:25px;'>Sistema de Inteligencia Clínica Multimodal y Empática</p>", unsafe_allow_html=True)
st.markdown("---")

col_izquierda, col_derecha = st.columns([1.9, 1.1])

archivo_subido = None

# COLUMNA DERECHA: MONITOR DE SISTEMA MÓVIL
with col_derecha:
    st.write("### 📊 SYSTEM MONITOR")
    
    st.markdown("""
        <span class='texto-neon-blanco'>STATUS: PERSISTENTE</span>
        <span class='texto-neon-blanco'>MONITOR BIOMÉTRICO ACTIVO</span>
    """, unsafe_allow_html=True)
    
    st.write("#### 🛡️ ESTADO DE SEGURIDAD:")
    if st.session_state.estado_critico:
        st.markdown("<h3 style='color:#FF4B4B; text-shadow: 0 0 15px #FF4B4B;'>⚠️ RIESGO CRÍTICO DETECTADO</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:#39FF14; text-shadow: 0 0 15px #39FF14;'>✅ ESTABLE</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("### 📂 DIGITALIZAR ESTUDIO MÉDICO")
    archivo_subido = st.file_uploader(
        "Arrastrá o subí el reporte clínico aquí:", 
        type=["png", "jpg", "jpeg", "pdf"],
        help="Soportado: Análisis de sangre, orina, informes, etc."
    )
    if archivo_subido:
        st.success(f"Estudio cargado con éxito.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Cerrar Sesión Actual (Mantener Historial)"):
        st.session_state.historial_clinico = []
        st.session_state.mensajes_pantalla = []
        st.session_state.estado_critico = False
        st.rerun()

# COLUMNA IZQUIERDA: CONSOLA DE CHAT HOLOGRÁFICO
with col_izquierda:
    st.write("### 💬 CONSOLA DE CHAT MÉDICO")

    chat_placeholder = st.container()

    with chat_placeholder:
        for mensaje in st.session_state.mensajes_pantalla:
            with st.chat_message(mensaje["role"]):
                st.write(mensaje["content"])

    # ENTRADA DE TEXTO
    if pregunta := st.chat_input("Escribí tu consulta acá... (Ej: ¿Cómo dio mi análisis?)"):
        st.session_state.mensajes_pantalla.append({"role": "user", "content": pregunta})
        
        contexto_antiguo = recuperar_contexto_relevante(pregunta)
        prompt_completo = pregunta
        if contexto_antiguo:
            prompt_completo += f"\n\n{contexto_antiguo}"
        
        if evaluar_emergencia(pregunta):
            st.session_state.estado_critico = True
            st.session_state.historial_clinico.append({"role": "user", "parts": [prompt_completo]})
        else:
            st.session_state.estado_critico = False
            
            if archivo_subido:
                try:
                    if archivo_subido.type in ["image/png", "image/jpeg", "image/jpg"]:
                        imagen_pil = Image.open(archivo_subido)
                        st.session_state.historial_clinico.append({
                            "role": "user", 
                            "parts": [imagen_pil, f"[El paciente adjuntó este estudio médico]. Consulta: {prompt_completo}"]
                        })
                    elif archivo_subido.type == "application/pdf":
                        pdf_bytes = archivo_subido.read()
                        st.session_state.historial_clinico.append({
                            "role": "user",
                            "parts": [
                                {"mime_type": "application/pdf", "data": pdf_bytes},
                                f"[El paciente adjuntó este PDF clínico]. Consulta: {prompt_completo}"
                            ]
                        })
                except Exception as ex:
                    st.error(f"Error al procesar el archivo: {ex}")
            else:
                st.session_state.historial_clinico.append({"role": "user", "parts": [prompt_completo]})
                
        st.rerun()

    # DETECCIÓN DE ESTADO CRÍTICO: PANEL + AUDIO DE RECOMENDACIÓN COMPLETO
    if st.session_state.estado_critico:
        st.markdown("""
            <div class='contenedor-vittal'>
                <div class='titulo-vittal'>🚨 ALERTA ROJA: ACTIVACIÓN DE CÓDIGO ROJO S.O.S.</div>
                <div class='texto-vittal'>
                    <strong>Atención:</strong> Los síntomas ingresados son compatibles con un síndrome coronario agudo en curso. 
                    <br><br>
                    <strong>¿Por qué recomendamos el despacho inmediato de Vittal?</strong>
                    <ul>
                        <li><strong>Liderazgo prehospitalario:</strong> Es el sistema de emergencias médicas privadas más grande del país, especializado en soporte vital avanzado.</li>
                        <li><strong>Infraestructura de alta complejidad:</strong> Sus Unidades de Terapia Intensiva Móvil operan como shock-rooms sobre ruedas con médicos emergentólogos capacitados.</li>
                        <li><strong>Tratamiento a bordo:</strong> Cuentan con equipamiento de desfibrilación y monitoreo crítico para prevenir complicaciones cardíacas mayores en tránsito.</li>
                    </ul>
                    <strong>Recomendaciones operativas para la llamada (Línea Directa: 4005-5555):</strong>
                    <ol>
                        <li>Informá la dirección exacta y la localidad de inmediato.</li>
                        <li>Decile al despachador: <strong>"Paciente con dolor opresivo de pecho irradiado al brazo, sospecha de infarto en curso"</strong>.</li>
                        <li>No cortes la comunicación y facilitá un teléfono de contacto rápido.</li>
                    </ol>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón de acción con estilo de alarma roja
        st.markdown("<div class='boton-emergencia-vittal'>", unsafe_allow_html=True)
        if st.button("📞 LLAMAR DE INMEDIATO A VITTAL (CÓDIGO ROJO)"):
            st.markdown("<script>window.open('tel:40055555');</script>", unsafe_allow_html=True)
            st.toast("Iniciando llamada de emergencia al 4005-5555...", icon="🚨")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # TEXTO EXPANDIDO DE AUDIO AUTOMÁTICO EN LA NUBE
        script_audio_emergencia = (
            "Atención. Estás manifestando síntomas de alarma críticos. "
            "Mientras iniciás la llamada, escuchá con atención las siguientes recomendaciones operativas. "
            "Elegimos el sistema prehospitalario de Vittal porque es la red de emergencias médicas más grande del país, "
            "especializada en soporte vital avanzado. Sus ambulancias operan como terapias intensivas móviles y están "
            "tripuladas por médicos emergentólogos preparados para la estabilización coronaria en viaje. "
            "Al comunicarte a la línea directa, cuatro cero cero cinco, cinco cinco cinco cinco, mantené la calma e informá la dirección exacta. "
            "Decile claramente al despachador la frase: Paciente adulto con dolor opresivo de pecho irradiado al brazo, sospecha de infarto en curso. "
            "Esto asegura la prioridad absoluta de despacho. No cuelgues el teléfono y seguí las indicaciones."
        )
        asyncio.run(generar_y_reproducir_audio(script_audio_emergencia))

    # Generación de la respuesta médica estándar si no es crítico
    elif st.session_state.mensajes_pantalla and st.session_state.mensajes_pantalla[-1]["role"] == "user":
        ultimo_texto_usuario = st.session_state.mensajes_pantalla[-1]["content"]
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analizando rastro e interpretando valores..."):
                try:
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        system_instruction=SYSTEM_PROMPT
                    )
                    response = model.generate_content(st.session_state.historial_clinico)
                    respuesta_texto = response.text

                    st.write(respuesta_texto)
                    st.session_state.mensajes_pantalla.append({"role": "assistant", "content": respuesta_texto})
                    guardar_en_memoria_permanente(ultimo_texto_usuario, respuesta_texto)
                    asyncio.run(generar_y_reproducir_audio(respuesta_texto))
                    
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        respuesta_texto = "Disculpame che, tengo el consultorio colapsado de consultas en este instante. Aguantame un minuto y volveme a preguntar, ¿dale?"
                    else:
                        respuesta_texto = "Disculpame che, se me complicó la conexión para leer este archivo. ¿Me lo podrás volver a subir?"
                    st.warning(respuesta_texto)
                    st.session_state.mensajes_pantalla.append({"role": "assistant", "content": respuesta_texto})
                    asyncio.run(generar_y_reproducir_audio(respuesta_texto))
