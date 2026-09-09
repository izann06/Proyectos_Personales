"""
Componente del Asistente Conversacional Inteligente (Staff Technical Mentor & Career Strategist).
Ejecución no bloqueante en segundo plano con soporte para navegación libre entre pestañas.
"""

import time
import threading
import textwrap
import streamlit as st
from src.core.analizador_ia import responder_chat_ia

def render_chat_assistant(datos_perfil: dict):
    """
    Renderiza la interfaz de chat con IA orientada a mentoría técnica multidisciplinar de nivel Staff.
    Soporta generación en segundo plano sin congelar la navegación de la aplicación.
    """
    nombre = datos_perfil.get("nombre", datos_perfil.get("usuario", "desarrollador"))
    
    header_html = """<div style="margin-bottom: 24px;" class="fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h3 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
Mentor IA • Staff Technical Architect & Career Strategist
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
                "mensaje": f"Hola, {nombre}. He analizado todo tu repertorio de GitHub: desde tus proyectos en **AWS Serverless y Docker**, hasta tus repositorios en **C# (.NET), TypeScript y automatización**. Como tu mentor técnico de nivel Staff, estoy listo para debatir sobre arquitectura, preparar respuestas para entrevistas con métricas cuantificables, analizar trade-offs técnicos o trazar tu hoja de ruta profesional. ¿Qué te gustaría consultar hoy?"
            }
        ]

    if "chat_bg_task" not in st.session_state:
        st.session_state["chat_bg_task"] = None

    # Comprobar si la tarea en segundo plano ha finalizado
    tarea_activa = st.session_state["chat_bg_task"]
    if tarea_activa is not None and tarea_activa.get("terminado"):
        if tarea_activa.get("error"):
            st.session_state["chat_history"].append({
                "rol": "ia",
                "mensaje": f"Error al generar la respuesta técnica: {tarea_activa['error']}"
            })
        else:
            st.session_state["chat_history"].append({
                "rol": "ia",
                "mensaje": tarea_activa.get("resultado", "No se pudo obtener respuesta.")
            })
        st.session_state["chat_bg_task"] = None
        st.rerun()

    # Chips de Preguntas Sugeridas Multidisciplinares
    st.markdown("<p style='font-size: 0.8rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Preguntas Rápidas de Alto Impacto:</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    pregunta_click = None
    with c1:
        if st.button("¿Cómo defender mi arquitectura en entrevistas?", key="chip_chat_1", use_container_width=True):
            pregunta_click = "¿Cómo estructuro una respuesta contundente con el Método STAR y trade-offs técnicos al defender la arquitectura de mis proyectos en una entrevista técnica?"
    with c2:
        if st.button("¿Qué stack priorizar para maximizar valor?", key="chip_chat_2", use_container_width=True):
            pregunta_click = "Analizando mi perfil actual entre Cloud, Backend y Frontend, ¿cuál es la ruta técnica que mayor valor y diferenciación aportará a mi perfil en los próximos 12 meses?"
    with c3:
        if st.button("¿Cómo adaptar mi experiencia a un nuevo rol?", key="chip_chat_3", use_container_width=True):
            pregunta_click = "¿Qué estrategia debo seguir para postularme con éxito a un rol que solicita tecnologías que no domino al 100%, destacando mis fundamentos de ingeniería?"

    # Historial de Conversación
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    for msg in st.session_state["chat_history"]:
        if msg["rol"] == "user":
            user_bubble = f"""<div class="chat-bubble-user">
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #93c5fd; display: block; margin-bottom: 4px;">Tú</span>
{msg['mensaje']}
</div>"""
            st.markdown(textwrap.dedent(user_bubble).strip(), unsafe_allow_html=True)
        else:
            ai_bubble = f"""<div class="chat-bubble-ai">
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #38bdf8; display: block; margin-bottom: 4px;">GritStack Mentor (Staff Architect)</span>
{msg['mensaje']}
</div>"""
            st.markdown(textwrap.dedent(ai_bubble).strip(), unsafe_allow_html=True)

    # Indicador dinámico si la IA está pensando en segundo plano
    if tarea_activa is not None and not tarea_activa.get("terminado"):
        ai_thinking_bubble = """<div class="chat-bubble-ai" style="border-left: 3px solid #38bdf8;">
<span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #38bdf8; display: block; margin-bottom: 6px;">GritStack Mentor (Staff Architect)</span>
<div style="display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 0.88rem;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 1.5s linear infinite;">
<path d="M21 12a9 9 0 1 1-6.219-8.56"/>
</svg>
<span>Razonando respuesta técnica en segundo plano... Puedes navegar libremente por otras pestañas.</span>
</div>
</div>"""
        st.markdown(textwrap.dedent(ai_thinking_bubble).strip(), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Formulario de entrada
    deshabilitar_envio = tarea_activa is not None and not tarea_activa.get("terminado")
    with st.form(key="form_chat_mentor", clear_on_submit=True):
        col_txt, col_send = st.columns([5, 1])
        with col_txt:
            user_input = st.text_input(
                "Pregunta a la IA...",
                placeholder="Pregunta sobre diseño de sistemas, backend .NET, Cloud, React, entrevistas técnicas...",
                label_visibility="collapsed",
                disabled=deshabilitar_envio
            )
        with col_send:
            enviado = st.form_submit_button("Enviar", use_container_width=True, disabled=deshabilitar_envio)

    mensaje_final = pregunta_click or (user_input.strip() if enviado and user_input.strip() else None)

    if mensaje_final and not deshabilitar_envio:
        st.session_state["chat_history"].append({"rol": "user", "mensaje": mensaje_final})
        
        # Iniciar worker en hilo secundario daemon
        nueva_tarea = {
            "terminado": False,
            "resultado": None,
            "error": None,
            "inicio": time.time()
        }
        
        def worker_chat(historial_copia, msg):
            try:
                res = responder_chat_ia(msg, datos_perfil, historial_copia)
                nueva_tarea["resultado"] = res
            except Exception as e:
                nueva_tarea["error"] = str(e)
            finally:
                nueva_tarea["terminado"] = True

        hilo = threading.Thread(
            target=worker_chat,
            args=(list(st.session_state["chat_history"]), mensaje_final),
            daemon=True
        )
        hilo.start()
        st.session_state["chat_bg_task"] = nueva_tarea
        st.rerun()

    # Si hay tarea en curso, esperar un breve ciclo no bloqueante y refrescar
    if st.session_state["chat_bg_task"] is not None and not st.session_state["chat_bg_task"].get("terminado"):
        time.sleep(1.0)
        st.rerun()
