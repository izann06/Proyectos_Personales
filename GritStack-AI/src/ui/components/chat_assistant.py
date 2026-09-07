"""
Componente del Asistente Conversacional Inteligente (Cloud & DevOps Career Coach).
"""

import textwrap
import streamlit as st
from src.core.analizador_ia import responder_chat_ia

def render_chat_assistant(datos_perfil: dict):
    """
    Renderiza la interfaz de chat con IA orientada a mentoría DevOps y Cloud.
    """
    nombre = datos_perfil.get("nombre", datos_perfil.get("usuario", "desarrollador"))
    
    header_html = """<div style="margin-bottom: 24px;" class="fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h3 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
💬 Mentor IA • Cloud & DevOps Career Coach
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Asesoramiento de nivel Senior para defender tus proyectos de Terraform y Docker, preparar entrevistas y evolucionar tu stack.
</p>
</div>
<span class="badge-cloud">Enfoque: DevOps & SRE</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Inicializar historial de chat si no existe
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "rol": "ia",
                "mensaje": f"¡Hola, {nombre}! He analizado a fondo tus repositorios de **AWS Serverless con Terraform**, **Docker Labs** y tus prácticas de **automatización en Linux**. Tu perfil tiene un gran potencial hacia **Cloud & DevOps**. ¿Qué te gustaría consultar hoy? Puedo ayudarte a preparar respuestas para entrevistas, recomendarte siguientes retos (como Kubernetes) o revisar tus proyectos."
            }
        ]

    # Chips de Preguntas Sugeridas (DevOps)
    st.markdown("<p style='font-size: 0.8rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Preguntas Rápidas Sugeridas:</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    pregunta_click = None
    with c1:
        if st.button("🔥 ¿Cuáles son mis puntos fuertes en DevOps?", key="chip_devops_1", use_container_width=True):
            pregunta_click = "¿Cuáles son mis 3 mayores fortalezas técnicas en Cloud y DevOps según mis repositorios?"
    with c2:
        if st.button("🎙️ ¿Cómo defender mi proyecto de Terraform?", key="chip_devops_2", use_container_width=True):
            pregunta_click = "¿Cómo debería explicar mi proyecto 'aws-serverless-text-to-speech' con Terraform ante un entrevistador técnico?"
    with c3:
        if st.button("🚀 ¿Qué debería aprender tras dominar Docker?", key="chip_devops_3", use_container_width=True):
            pregunta_click = "Ya manejo Docker Compose y Linux. ¿Cuál es la ruta recomendada para dominar Kubernetes y Observabilidad?"

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
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #38bdf8; display: block; margin-bottom: 4px;">⚡ GritStack Mentor (DevOps & Cloud)</span>
{msg['mensaje']}
</div>"""
            st.markdown(textwrap.dedent(ai_bubble).strip(), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Formulario de entrada
    with st.form(key="form_chat_devops", clear_on_submit=True):
        col_txt, col_send = st.columns([5, 1])
        with col_txt:
            user_input = st.text_input(
                "Pregunta a la IA...",
                placeholder="Pregunta sobre arquitecturas cloud, CI/CD, preparación de entrevistas...",
                label_visibility="collapsed"
            )
        with col_send:
            enviado = st.form_submit_button("Enviar 💬", use_container_width=True)

    mensaje_final = pregunta_click or (user_input.strip() if enviado and user_input.strip() else None)

    if mensaje_final:
        st.session_state["chat_history"].append({"rol": "user", "mensaje": mensaje_final})
        with st.spinner("Consultando con el motor de IA..."):
            respuesta = responder_chat_ia(mensaje_final, datos_perfil, st.session_state["chat_history"])
        st.session_state["chat_history"].append({"rol": "ia", "mensaje": respuesta})
        st.rerun()
