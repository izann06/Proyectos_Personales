"""
Pantalla de Carga Interactiva con Barra de Progreso y Marcador de GitHub Móvil
"""

import time
import threading
import streamlit as st
from src.data.github_parser import obtener_perfil_github
from src.core.analizador_ia import generar_readme_ia
from src.ui.components.progress_bar import render_html_progress

def render_pantalla_carga(token: str):
    """
    Ejecuta el pipeline de extracción e IA mientras proyecta una barra de progreso
    viva donde el icono de GitHub se desplaza a través de la pista en tiempo real.
    Garantiza que el progreso llegue al 100% exacto sin pasarse jamás.
    """
    st.markdown(
        """<div style="text-align: center; margin-top: 30px; margin-bottom: 25px;">
<div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 12px;">
<span class="badge-cloud">⚡ Procesamiento en Tiempo Real</span>
</div>
<h2 style="font-size: 2.3rem; font-weight: 800; color: #ffffff; margin: 0 0 10px 0;">
Analizando tu Universo de Código
</h2>
<p style="color: #94a3b8; font-size: 1rem; max-width: 540px; margin: 0 auto;">
Conectando con GitHub API y el motor de IA de AWS Bedrock para decodificar tu perfil técnico.
</p>
</div>""",
        unsafe_allow_html=True
    )

    placeholder = st.empty()

    estado_worker = {
        "terminado": False,
        "error": None,
        "datos_perfil": None,
        "readme": None,
        "fase": "github"
    }

    def tarea_segundo_plano():
        try:
            # 1. Extraer datos de GitHub
            estado_worker["fase"] = "github"
            datos = obtener_perfil_github(token)
            estado_worker["datos_perfil"] = datos

            # 2. Sintetizar README con Claude
            estado_worker["fase"] = "bedrock"
            readme = generar_readme_ia(datos)
            estado_worker["readme"] = readme

            estado_worker["fase"] = "completado"
        except Exception as err:
            estado_worker["error"] = str(err)
        finally:
            estado_worker["terminado"] = True

    hilo = threading.Thread(target=tarea_segundo_plano)
    hilo.start()

    progreso_visual = 5.0
    
    # Animación fluida con distribución uniforme del tiempo y tope estricto en 100%
    while not estado_worker["terminado"] or progreso_visual < 100.0:
        if estado_worker["terminado"] and estado_worker["error"]:
            break

        fase_actual = estado_worker["fase"]
        
        if not estado_worker["terminado"]:
            if fase_actual == "github":
                if progreso_visual < 45.0:
                    progreso_visual = min(45.0, progreso_visual + 1.2)
                else:
                    progreso_visual = min(48.0, progreso_visual + 0.1)
                mensaje = "📡 Conectando con GitHub API e indexando repositorios y tecnologías..."
            elif fase_actual == "bedrock":
                if progreso_visual < 85.0:
                    progreso_visual = min(85.0, progreso_visual + 1.0)
                else:
                    # Durante la inferencia con Claude en Bedrock, avanza sutilmente sin pasar jamás del 95%
                    progreso_visual = min(95.0, progreso_visual + 0.15)
                mensaje = "🧠 Analizando arquitectura y sintetizando README con Claude Sonnet 4.6..."
            else:
                progreso_visual = min(96.0, progreso_visual + 0.2)
                mensaje = "✨ Optimizando métricas y organizando proyectos insignia..."
        else:
            # Al terminar el worker, completar suavemente hasta el 100% exacto
            progreso_visual = min(100.0, progreso_visual + 5.0)
            mensaje = "🚀 ¡Todo listo! Desplegando tu Centro de Mando..."

        # Renderizar la barra usando la función con límite estricto de 100%
        html_barra = render_html_progress(
            progreso=min(100.0, progreso_visual),
            mensaje=mensaje,
            titulo="PROGRESO DE INTELIGENCIA DEVOPS"
        )
        placeholder.markdown(html_barra, unsafe_allow_html=True)
        time.sleep(0.06)

    if estado_worker["error"]:
        placeholder.empty()
        st.error(f"❌ Error al conectar o analizar: {estado_worker['error']}")
        if st.button("⬅️ Intentar de nuevo con otro Token"):
            st.session_state["etapa"] = "onboarding"
            st.rerun()
        return

    # Mostrar el 100% completo durante un instante para una experiencia visual perfecta
    placeholder.markdown(
        render_html_progress(
            progreso=100.0,
            mensaje="🚀 ¡100% Completado! Abriendo tu Centro de Mando...",
            titulo="PROGRESO DE INTELIGENCIA DEVOPS"
        ),
        unsafe_allow_html=True
    )
    time.sleep(0.4)

    st.session_state["datos_perfil"] = estado_worker["datos_perfil"]
    st.session_state["readme_generado"] = estado_worker["readme"]
    st.session_state["etapa"] = "dashboard"
    st.rerun()
