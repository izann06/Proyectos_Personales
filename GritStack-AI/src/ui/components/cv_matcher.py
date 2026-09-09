"""
Componente del Adaptador Curricular Inteligente (CV Tailor & ATS Matcher).
Procesa currículums reales en formato PDF, evalúa afinidad técnica con el puesto
con barra de progreso lineal en segundo plano, modal sin emojis y alta fidelidad técnica.
Permite navegación libre entre pestañas durante el análisis.
"""

import time
import math
import re
import threading
import textwrap
import streamlit as st
from src.core.pdf_extractor import extraer_texto_pdf
from src.core.curriculum_matcher import analizar_y_adaptar_cv
from src.core.pdf_generator import generar_pdf_cv
from src.ui.components.progress_bar import render_html_progress

@st.dialog("Currículum Requerido")
def popup_falta_cv():
    """Modal de aviso si el usuario no ha subido el archivo PDF."""
    html_dialog = """<div style="text-align: center; padding: 10px 0;">
<div style="margin-bottom: 14px; display: flex; justify-content: center;">
<div style="width: 52px; height: 52px; border-radius: 12px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center;">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
<polyline points="14 2 14 8 20 8"/>
<line x1="16" y1="13" x2="8" y2="13"/>
<line x1="16" y1="17" x2="8" y2="17"/>
<polyline points="10 9 9 9 8 9"/>
</svg>
</div>
</div>
<h3 style="color: #ffffff; margin-bottom: 8px; font-weight: 800; font-family: 'Outfit', sans-serif; font-size: 1.25rem;">
Falta adjuntar tu currículum
</h3>
<p style="color: #94a3b8; font-size: 0.92rem; line-height: 1.6; max-width: 440px; margin: 0 auto 18px auto;">
Para que el motor ATS pueda auditar los errores reales de tu currículum y optimizarlo para la vacante, debes subir primero tu archivo en formato PDF.
</p>
<div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; color: #cbd5e1; margin-bottom: 20px; text-align: left;">
<strong>Nota de prueba rápida:</strong> Si no dispones del PDF en este instante, pulsa en <strong>"Ver Auditoría con Proyectos de GitHub"</strong> para evaluar tu perfil de inmediato.
</div>
</div>"""
    st.markdown(textwrap.dedent(html_dialog).strip(), unsafe_allow_html=True)
    if st.button("Entendido, voy a adjuntarlo", type="primary", use_container_width=True):
        st.rerun()

def render_cv_matcher(datos_perfil: dict):
    """
    Renderiza la interfaz interactiva y funcional de optimización de CV.
    Soporta ejecución en segundo plano para permitir navegación libre entre pestañas.
    """
    header_html = """<div style="margin-bottom: 24px;" class="fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
<div>
<h3 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
TailorCV Studio • Auditoría & Optimizador Curricular Inteligente
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Audita los fallos de tu currículum frente a cualquier vacante técnica y genera una versión de élite adaptada rigurosamente al puesto.
</p>
</div>
<span class="badge-devops">ATS Adaptive Engine V3.0</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Estado de tarea en segundo plano para el análisis de CV
    if "cv_bg_task" not in st.session_state:
        st.session_state["cv_bg_task"] = None

    tarea_cv = st.session_state["cv_bg_task"]
    
    # Comprobar si la tarea en segundo plano ha finalizado
    if tarea_cv is not None and tarea_cv.get("terminado"):
        if tarea_cv.get("error"):
            st.error(f"Error al auditar el currículum: {tarea_cv['error']}")
        else:
            st.session_state["resultado_cv"] = tarea_cv.get("resultado")
            st.session_state["puesto_objetivo_actual"] = tarea_cv.get("puesto")
            st.session_state["desc_oferta_actual"] = tarea_cv.get("oferta")
        st.session_state["cv_bg_task"] = None
        st.rerun()

    en_ejecucion = tarea_cv is not None and not tarea_cv.get("terminado")

    # Parámetros y Formulario de Subida
    card_form_html = """<div class="solid-card" style="padding: 22px; margin-bottom: 24px;">
<h4 style="margin: 0 0 14px 0; font-size: 1.15rem; font-weight: 700; color: #ffffff;">
1. Parámetros del Puesto Objetivo & Subida de CV
</h4>
</div>"""
    st.markdown(textwrap.dedent(card_form_html).strip(), unsafe_allow_html=True)

    c_puesto, c_oferta = st.columns([1, 1.2], gap="medium")
    with c_puesto:
        puesto_deseado = st.text_input(
            "Puesto de Trabajo Objetivo",
            value=st.session_state.get("puesto_objetivo_actual", "Cloud & DevOps Engineer / Junior SRE"),
            placeholder="Ej: Frontend Developer, Backend .NET, Cloud & DevOps, Data Engineer...",
            help="El título exacto del puesto al que te postulas (la IA adaptará las tecnologías y proyectos a este rol).",
            disabled=en_ejecucion
        )
    with c_oferta:
        descripcion_oferta = st.text_area(
            "Requisitos clave de la Oferta (Opcional)",
            value=st.session_state.get("desc_oferta_actual", "Experiencia en Docker, AWS (Serverless/Lambda), Terraform (IaC), CI/CD con GitHub Actions y entornos Linux."),
            height=68,
            placeholder="Pega aquí fragmentos o requisitos de la oferta...",
            help="Pega aquí fragmentos de la oferta para alinear palabras clave y requisitos específicos.",
            disabled=en_ejecucion
        )

    archivo_cv = st.file_uploader(
        "Sube tu currículum en formato PDF",
        type=["pdf"],
        help="Sube tu archivo PDF para que el motor ATS extraiga el texto y audite tus errores.",
        disabled=en_ejecucion
    )

    col_btn_analizar, col_btn_demo = st.columns([1.5, 1], gap="medium")
    with col_btn_analizar:
        btn_analizar = st.button("Analizar y Optimizar CV al Puesto", type="primary", use_container_width=True, disabled=en_ejecucion)
    with col_btn_demo:
        btn_demo = st.button("Ver Auditoría con Proyectos de GitHub", use_container_width=True, disabled=en_ejecucion)

    # ------------------------------------------------------------
    # VALIDACIÓN DE SUBIDA: POPUP SI FALTA EL CV
    # ------------------------------------------------------------
    if btn_analizar and archivo_cv is None:
        st.toast("Por favor, sube tu currículum en formato PDF antes de continuar.")
        popup_falta_cv()
        return

    # Iniciar tarea en segundo plano al pulsar botón
    if (btn_analizar and archivo_cv is not None) or btn_demo:
        texto_cv = ""
        if archivo_cv is not None and btn_analizar:
            texto_cv = extraer_texto_pdf(archivo_cv)

        nueva_tarea = {
            "terminado": False,
            "resultado": None,
            "error": None,
            "inicio": time.time(),
            "puesto": puesto_deseado,
            "oferta": descripcion_oferta
        }

        def worker_analisis(t_cv, p_des, d_ofe):
            try:
                res = analizar_y_adaptar_cv(
                    texto_cv=t_cv,
                    puesto_objetivo=p_des,
                    descripcion_oferta=d_ofe,
                    datos_perfil=datos_perfil
                )
                nueva_tarea["resultado"] = res
            except Exception as e:
                nueva_tarea["error"] = str(e)
            finally:
                nueva_tarea["terminado"] = True

        hilo = threading.Thread(
            target=worker_analisis,
            args=(texto_cv, puesto_deseado, descripcion_oferta),
            daemon=True
        )
        hilo.start()
        st.session_state["cv_bg_task"] = nueva_tarea
        st.rerun()

    # Si hay tarea activa en ejecución, renderizar barra de progreso viva no bloqueante
    if en_ejecucion:
        t_transcurrido = time.time() - tarea_cv["inicio"]
        progreso_actual = min(96.5, 96.5 * (1.0 - math.exp(-t_transcurrido / 22.0)))

        if t_transcurrido < 4.0:
            msg = "Extrayendo texto y procesando estructura del currículum..."
        elif t_transcurrido < 10.0:
            msg = f"Evaluando requisitos y palabras clave ATS para {puesto_deseado[:28]}..."
        elif t_transcurrido < 18.0:
            msg = "Auditando deficiencias, anti-patrones y riesgos de descarte..."
        elif t_transcurrido < 28.0:
            msg = "Cruzando competencias clave con proyectos reales de GitHub..."
        elif t_transcurrido < 40.0:
            msg = "Reestructurando experiencia técnica con fórmula Google X-Y-Z..."
        elif t_transcurrido < 54.0:
            msg = "Maximizando densidad semántica para directores técnicos y ATS..."
        else:
            msg = "Finalizando redacción ejecutiva y ensamblando el currículum..."

        html_bar = render_html_progress(
            progreso=progreso_actual,
            mensaje=msg,
            titulo="AUDITORÍA ATS EN TIEMPO REAL"
        )
        st.markdown(html_bar, unsafe_allow_html=True)
        
        info_bg = """<div style="font-size: 0.85rem; color: #94a3b8; margin: 12px 0 24px 0; display: flex; align-items: center; gap: 8px;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 2s linear infinite;">
<line x1="12" y1="2" x2="12" y2="6"/>
<line x1="12" y1="18" x2="12" y2="22"/>
<line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/>
<line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/>
<line x1="2" y1="12" x2="6" y2="12"/>
<line x1="18" y1="12" x2="22" y2="12"/>
<line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/>
<line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/>
</svg>
<span>Procesando en segundo plano. Puedes navegar libremente por las demás pestañas mientras se completa.</span>
</div>"""
        st.markdown(textwrap.dedent(info_bg).strip(), unsafe_allow_html=True)

        time.sleep(1.0)
        st.rerun()

    # ============================================================
    # RENDERIZADO DE RESULTADOS: AUDITORÍA ROJA + MEJORAS VERDES + CV
    # ============================================================
    resultado = st.session_state.get("resultado_cv")

    if resultado:
        nombre = datos_perfil.get("nombre", datos_perfil.get("usuario", "Izan"))
        score_rojo = resultado.get("score_original_rojo", 34)
        diag_critico = resultado.get("diagnostico_critico", "")
        errores = resultado.get("errores_detectados", [])
        
        score_verde = resultado.get("score_optimizado_verde", 96)
        puntos_fuertes = resultado.get("puntos_fuertes_optimizados", [])
        perfil_opt = resultado.get("perfil_profesional_opt", "")
        cv_md = resultado.get("cv_markdown_completo") or ""

        col_rojo, col_verde = st.columns([1, 1], gap="large")

        # ------------------------------------------------------------
        # TARJETA 1: AUDITORÍA CRÍTICA DEL CV ORIGINAL (ROJO)
        # ------------------------------------------------------------
        with col_rojo:
            items_errores = "".join([
                f'<div style="background: #1e293b; border-left: 3px solid #ef4444; border: 1px solid #334155; border-left-width: 3px; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 0.86rem; color: #fca5a5; line-height: 1.4;">{err}</div>'
                for err in errores
            ])

            html_critico = f"""<div class="card-critique-red fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
<div>
<span style="font-size: 0.78rem; font-weight: 700; color: #f87171; text-transform: uppercase; letter-spacing: 0.05em;">
Evaluación del CV Original
</span>
<h4 style="margin: 2px 0 0 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">
Deficiencias & Errores Críticos
</h4>
</div>
<div style="background: #1e293b; border: 2px solid #ef4444; border-radius: 12px; padding: 8px 16px; text-align: center;">
<span style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #ef4444; line-height: 1;">
{score_rojo}%
</span>
<div style="font-size: 0.68rem; font-weight: 700; color: #fca5a5; text-transform: uppercase;">Filtro ATS</div>
</div>
</div>

<p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 16px;">
{diag_critico}
</p>

<div style="font-size: 0.8rem; font-weight: 700; color: #f87171; text-transform: uppercase; margin-bottom: 10px;">
Fallos Detectados que Provocan el Descarte:
</div>
<div>
{items_errores}
</div>
</div>"""
            st.markdown(textwrap.dedent(html_critico).strip(), unsafe_allow_html=True)

        # ------------------------------------------------------------
        # TARJETA 2: MEJORAS Y CV OPTIMIZADO (VERDE SÓLIDO)
        # ------------------------------------------------------------
        with col_verde:
            items_mejoras = "".join([
                f'<div style="background: #1e293b; border-left: 3px solid #10b981; border: 1px solid #334155; border-left-width: 3px; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 0.86rem; color: #6ee7b7; line-height: 1.4;">{pts}</div>'
                for pts in puntos_fuertes
            ])

            html_optimizado = f"""<div class="card-optimized-green fade-up-2">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
<div>
<span style="font-size: 0.78rem; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">
Versión Optimizada para el Puesto
</span>
<h4 style="margin: 2px 0 0 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">
Correcciones & Puntos Fuertes
</h4>
</div>
<div style="background: #1e293b; border: 2px solid #10b981; border-radius: 12px; padding: 8px 16px; text-align: center;">
<span style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #34d399; line-height: 1;">
{score_verde}%
</span>
<div style="font-size: 0.68rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase;">Top Match</div>
</div>
</div>

<div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 14px; margin-bottom: 16px;">
<div style="font-size: 0.75rem; font-weight: 700; color: #34d399; text-transform: uppercase; margin-bottom: 4px;">
Nuevo Perfil Profesional para el CV:
</div>
<div style="font-size: 0.86rem; color: #f1f5f9; line-height: 1.5; font-style: italic;">
"{perfil_opt}"
</div>
</div>

<div style="font-size: 0.8rem; font-weight: 700; color: #34d399; text-transform: uppercase; margin-bottom: 10px;">
Transformaciones Clave Aplicadas:
</div>
<div>
{items_mejoras}
</div>
</div>"""
            st.markdown(textwrap.dedent(html_optimizado).strip(), unsafe_allow_html=True)

        # ------------------------------------------------------------
        # SECCIÓN 3: EL CURRÍCULUM ENTERO CORREGIDO & DESCARGAS
        # ------------------------------------------------------------
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        
        # Barra de herramientas y descargas del CV
        puesto_actual = st.session_state.get("puesto_objetivo_actual", "Ingeniero")
        rol_slug = re.sub(r'[^a-zA-Z0-9]+', '_', puesto_actual).strip('_')[:25] or "Profesional"
        
        col_cv_ctrl, col_cv_pdf, col_cv_md = st.columns([1.8, 1.4, 1.4], gap="medium")
        with col_cv_ctrl:
            vista_cv = st.radio(
                "Vista de CV",
                options=["Vista Formateada del CV", "Código Markdown Fuente (.md)"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with col_cv_pdf:
            pdf_bytes = generar_pdf_cv(cv_md)
            st.download_button(
                label="Descargar CV en PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"Curriculum_{nombre.replace(' ', '_')}_{rol_slug}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_cv_md:
            st.download_button(
                label="Descargar CV (.md)",
                data=cv_md,
                file_name=f"Curriculum_{nombre.replace(' ', '_')}_{rol_slug}.md",
                mime="text/markdown",
                use_container_width=True
            )

        # Encabezado visual de la terminal
        cv_header_html = f"""<div class="terminal-header" style="border-top-left-radius: 16px; border-top-right-radius: 16px; margin-top: 14px;">
<div class="terminal-dots">
<span class="dot-red"></span>
<span class="dot-yellow"></span>
<span class="dot-green"></span>
</div>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; color: #94a3b8;">
Curriculum_{rol_slug}.md • Adaptado rigurosamente para {puesto_actual}
</div>
<div>
<span class="badge-status">100% Optimizado</span>
</div>
</div>"""
        st.markdown(textwrap.dedent(cv_header_html).strip(), unsafe_allow_html=True)

        # Contenedor del documento CV
        if vista_cv == "Vista Formateada del CV":
            st.markdown(
                f'<div class="cv-document-sheet fade-up-2">\n\n{cv_md}\n\n</div>',
                unsafe_allow_html=True
            )
        else:
            st.code(cv_md, language="markdown")
