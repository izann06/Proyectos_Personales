"""
Componente del Asistente Conversacional Inteligente (Staff Technical Mentor & Career Strategist).
"""

import textwrap
import streamlit as st
from src.core.analizador_ia import responder_chat_ia

def render_chat_assistant(datos_perfil: dict):
    """
    Renderiza la interfaz de chat con IA orientada a mentoría técnica multidisciplinar de nivel Staff.
    """
    nombre = datos_perfil.get("nombre", datos_perfil.get("usuario", "desarrollador"))
    
    header_html = """<div style="margin-bottom: 24px;" class="fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h3 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
💬 Mentor IA • Staff Technical Architect & Career Strategist
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Asesoramiento riguroso de nivel Senior para resolver dudas de arquitectura, preparar entrevistas, optimizar código y acelerar tu carrera.
</p>
</div>
<span class="badge-cloud">Staff Engineering AI</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Inicializar historial de chat si no existe
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "rol": "ia",
                "mensaje": f"¡Hola, {nombre}! He analizado todo tu repertorio de GitHub: desde tus proyectos en **AWS Serverless y Docker**, hasta tus repositorios en **C# (.NET), TypeScript y automatización**. Como tu mentor técnico de nivel Staff, estoy listo para debatir sobre arquitectura, preparar respuestas contundentes para entrevistas, analizar trade-offs técnicos o trazar tu hoja de ruta profesional. ¿Qué te gustaría consultar hoy?"
            }
        ]

    # Chips de Preguntas Sugeridas Multidisciplinares
    st.markdown("<p style='font-size: 0.8rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Preguntas Rápidas de Alto Impacto:</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    pregunta_click = None
    with c1:
        if st.button("🏛️ ¿Cómo defender mi arquitectura en entrevistas?", key="chip_chat_1", use_container_width=True):
            pregunta_click = "¿Cómo estructuro una respuesta contundente con el Método STAR y trade-offs técnicos al defender la arquitectura de mis proyectos en una entrevista técnica?"
    with c2:
        if st.button("🚀 ¿Qué stack priorizar para maximizar valor?", key="chip_chat_2", use_container_width=True):
            pregunta_click = "Analizando mi perfil actual entre Cloud, Backend y Frontend, ¿cuál es la ruta técnica que mayor valor y diferenciación aportará a mi perfil en los próximos 12 meses?"
    with c3:
        if st.button("🎯 ¿Cómo adaptar mi experiencia a un nuevo rol?", key="chip_chat_3", use_container_width=True):
            pregunta_click = "¿Qué estrategia debo seguir para postularme con éxito a un rol que solicita tecnologías que no domino al 100%, destacando mis fundamentos de ingeniería?"

    # Historial de Conversación
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    for msg in st.session_state["chat_history"]:
        if msg["rol"] == "user":
            user_bubble = f"""<div class="chat-bubble-user">
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #c084fc; display: block; margin-bottom: 4px;">Tú</span>
{msg['mensaje']}
</div>"""
            st.markdown(textwrap.dedent(user_bubble).strip(), unsafe_allow_html=True)
        else:
            ai_bubble = f"""<div class="chat-bubble-ai">
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #38bdf8; display: block; margin-bottom: 4px;">⚡ GritStack Mentor (Staff Architect)</span>
{msg['mensaje']}
</div>"""
            st.markdown(textwrap.dedent(ai_bubble).strip(), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Formulario de entrada
    with st.form(key="form_chat_mentor", clear_on_submit=True):
        col_txt, col_send = st.columns([5, 1])
        with col_txt:
            user_input = st.text_input(
                "Pregunta a la IA...",
                placeholder="Pregunta sobre diseño de sistemas, backend .NET, Cloud, React, entrevistas técnicas...",
                label_visibility="collapsed"
            )
        with col_send:
            enviado = st.form_submit_button("Enviar 💬", use_container_width=True)

    mensaje_final = pregunta_click or (user_input.strip() if enviado and user_input.strip() else None)

    if mensaje_final:
        st.session_state["chat_history"].append({"rol": "user", "mensaje": mensaje_final})
        with st.spinner("Razonando respuesta con el mentor de IA..."):
            respuesta = responder_chat_ia(mensaje_final, datos_perfil, st.session_state["chat_history"])
        st.session_state["chat_history"].append({"rol": "ia", "mensaje": respuesta})
        st.rerun()

