"""
Pantalla de Carga Interactiva con Barra de Progreso y Marcador de GitHub Móvil
"""

import time
import math
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

    t_inicio = time.time()
    t_inicio_bedrock = None
    progreso_visual = 2.0
    
    # Progresión asintótica temporal continua sin atascos en 48% ni en 95%
    while not estado_worker["terminado"]:
        fase_actual = estado_worker["fase"]
        t_total = time.time() - t_inicio
        
        if fase_actual == "github":
            # Progresión suave durante fase GitHub (0% hacia ~45% sin atascarse)
            meta_progreso = 45.0 * (1.0 - math.exp(-t_total / 8.0))
            if meta_progreso > progreso_visual:
                progreso_visual += (meta_progreso - progreso_visual) * 0.25
            else:
                progreso_visual = min(46.0, progreso_visual + 0.04)
                
            if t_total < 3.5:
                mensaje = "📡 Conectando con GitHub API y autenticando credenciales..."
            elif t_total < 8.0:
                mensaje = "📦 Indexando repositorios, historial de commits y tecnologías..."
            else:
                mensaje = "📊 Calculando métricas de ingeniería y distribución de lenguajes..."
                
        elif fase_actual == "bedrock":
            if t_inicio_bedrock is None:
                t_inicio_bedrock = time.time()
                base_bedrock = max(45.0, progreso_visual)
            else:
                base_bedrock = 45.0
                
            t_bedrock = time.time() - t_inicio_bedrock
            # Progresión suave durante fase Bedrock (45% hacia ~96.5% sin frenazos)
            meta_progreso = base_bedrock + (96.5 - base_bedrock) * (1.0 - math.exp(-t_bedrock / 14.0))
            
            if meta_progreso > progreso_visual:
                progreso_visual += (meta_progreso - progreso_visual) * 0.25
            else:
                progreso_visual = min(96.5, progreso_visual + 0.04)
                
            if t_bedrock < 4.0:
                mensaje = "🧠 Conectando con Claude Sonnet 4.6 en AWS Bedrock..."
            elif t_bedrock < 10.0:
                mensaje = "⚡ Analizando decisiones de diseño y arquitecturas insignia..."
            elif t_bedrock < 18.0:
                mensaje = "📐 Sintetizando topologías Zero-Trust y diagramas de flujo..."
            elif t_bedrock < 28.0:
                mensaje = "✨ Redactando README técnico con pensamiento crítico..."
            else:
                mensaje = "🚀 Optimizando insignias de producción y estructura ejecutiva..."
        else:
            progreso_visual = min(96.5, progreso_visual + 0.2)
            mensaje = "✨ Ensamblando métricas de ingeniería y proyectos..."

        html_barra = render_html_progress(
            progreso=progreso_visual,
            mensaje=mensaje,
            titulo="PROGRESO DE INTELIGENCIA DEVOPS"
        )
        placeholder.markdown(html_barra, unsafe_allow_html=True)
        time.sleep(0.08)

    if estado_worker["error"]:
        placeholder.empty()
        st.error(f"❌ Error al conectar o analizar: {estado_worker['error']}")
        if st.button("⬅️ Intentar de nuevo con otro Token"):
            st.session_state["etapa"] = "onboarding"
            st.rerun()
        return

    # Animación de cierre suave hasta el 100% exacto
    while progreso_visual < 100.0:
        progreso_visual = min(100.0, progreso_visual + 3.5)
        html_barra = render_html_progress(
            progreso=progreso_visual,
            mensaje="🚀 ¡100% Completado! Abriendo tu Centro de Mando...",
            titulo="PROGRESO DE INTELIGENCIA DEVOPS"
        )
        placeholder.markdown(html_barra, unsafe_allow_html=True)
        time.sleep(0.03)

    time.sleep(0.35)
    st.session_state["datos_perfil"] = estado_worker["datos_perfil"]
    st.session_state["readme_generado"] = estado_worker["readme"]
    st.session_state["etapa"] = "dashboard"
    st.rerun()
    st.rerun()
