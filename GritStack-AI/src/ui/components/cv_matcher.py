"""
Componente del Adaptador Curricular Inteligente (CV Tailor & ATS Matcher).
Procesa currículums reales en formato PDF, evalúa afinidad técnica con el puesto
con barra de progreso lineal en tiempo real, popup de aviso si falta el PDF,
auditoría crítica en ROJO y versión optimizada en VERDE.
"""

import time
import threading
import textwrap
import streamlit as st
from src.core.pdf_extractor import extraer_texto_pdf
from src.core.curriculum_matcher import analizar_y_adaptar_cv
from src.core.pdf_generator import generar_pdf_cv
from src.ui.components.progress_bar import render_html_progress

@st.dialog("📄 Currículum Requerido")
def popup_falta_cv():
    """Modal popup que se abre si el usuario no ha subido el archivo PDF."""
    html_dialog = """<div style="text-align: center; padding: 10px 0;">
<div style="font-size: 3rem; margin-bottom: 12px;">📂</div>
<h3 style="color: #ffffff; margin-bottom: 8px; font-weight: 800; font-family: 'Outfit', sans-serif;">
¡Falta adjuntar tu currículum!
</h3>
<p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; max-width: 460px; margin: 0 auto 18px auto;">
Para que el motor ATS pueda auditar los errores reales de tu currículum y optimizarlo para el puesto, primero debes subir tu archivo en formato PDF en el campo superior.
</p>
<div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 10px; padding: 12px 16px; font-size: 0.85rem; color: #e9d5ff; margin-bottom: 20px;">
💡 <em>Tip: Si no tienes tu PDF a mano ahora mismo, puedes usar el botón <strong>"⚡ Ver Auditoría con Proyectos de GitHub"</strong> para probar la auditoría de inmediato.</em>
</div>
</div>"""
    st.markdown(textwrap.dedent(html_dialog).strip(), unsafe_allow_html=True)
    if st.button("Entendido, voy a adjuntarlo 🚀", type="primary", use_container_width=True):
        st.rerun()

def render_cv_matcher(datos_perfil: dict):
    """
    Renderiza la interfaz interactiva y funcional de optimización de CV.
    """
    header_html = """<div style="margin-bottom: 24px;" class="fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
<div>
<h3 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
🎯 TailorCV Studio • Auditoría & Optimizador Curricular Inteligente
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Audita los fallos de tu currículum original y genera una versión optimizada para roles de Cloud & DevOps.
</p>
</div>
<span class="badge-devops">ATS Engine V2.5</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # Parámetros y Formulario de Subida
    card_form_html = """<div class="glass-card" style="padding: 22px; margin-bottom: 24px;">
<h4 style="margin: 0 0 14px 0; font-size: 1.15rem; font-weight: 700; color: #ffffff;">
1. Parámetros del Puesto Objetivo & Subida de CV
</h4>
</div>"""
    st.markdown(textwrap.dedent(card_form_html).strip(), unsafe_allow_html=True)

    c_puesto, c_oferta = st.columns([1, 1.2], gap="medium")
    with c_puesto:
        puesto_deseado = st.text_input(
            "Puesto de Trabajo Deseado",
            value="Cloud & DevOps Engineer / Junior SRE",
            placeholder="Ej: Cloud & DevOps Engineer, SRE...",
            help="El título exacto del puesto al que te postulas."
        )
    with c_oferta:
        descripcion_oferta = st.text_area(
            "Requisitos clave de la Oferta (Opcional)",
            value="Experiencia en Docker, AWS (Serverless/Lambda), Terraform (IaC), CI/CD con GitHub Actions y entornos Linux.",
            height=68,
            help="Pega aquí fragmentos de la oferta para evaluar palabras clave específicas."
        )

    archivo_cv = st.file_uploader(
        "Sube tu currículum en formato PDF",
        type=["pdf"],
        help="Sube tu archivo PDF para que el motor ATS extraiga el texto y audite tus errores."
    )

    col_btn_analizar, col_btn_demo = st.columns([1.5, 1], gap="medium")
    with col_btn_analizar:
        btn_analizar = st.button("🚀 Analizar y Optimizar CV al Puesto", type="primary", use_container_width=True)
    with col_btn_demo:
        btn_demo = st.button("⚡ Ver Auditoría con Proyectos de GitHub", use_container_width=True)

    # ------------------------------------------------------------
    # VALIDACIÓN DE SUBIDA: POPUP SI FALTA EL CV
    # ------------------------------------------------------------
    if btn_analizar and archivo_cv is None:
        st.toast("⚠️ Por favor, sube tu currículum en formato PDF antes de continuar.", icon="📄")
        popup_falta_cv()
        return

    # Contenedor dinámico para la barra de progreso animada lineal
    placeholder_progreso = st.empty()

    if (btn_analizar and archivo_cv is not None) or btn_demo:
        texto_cv = ""
        if archivo_cv is not None and btn_analizar:
            texto_cv = extraer_texto_pdf(archivo_cv)

        # Estado compartido con el hilo de ejecución
        estado_worker = {
            "terminado": False,
            "error": None,
            "resultado": None
        }

        def tarea_analisis():
            try:
                res = analizar_y_adaptar_cv(
                    texto_cv=texto_cv,
                    puesto_objetivo=puesto_deseado,
                    descripcion_oferta=descripcion_oferta,
                    datos_perfil=datos_perfil
                )
                estado_worker["resultado"] = res
            except Exception as e:
                estado_worker["error"] = str(e)
            finally:
                estado_worker["terminado"] = True

        hilo = threading.Thread(target=tarea_analisis)
        hilo.start()

        progreso_lineal = 5.0

        # Barra de progreso lineal sincronizada en tiempo real
        while not estado_worker["terminado"] or progreso_lineal < 100.0:
            if estado_worker["terminado"] and estado_worker["error"]:
                break

            if not estado_worker["terminado"]:
                if progreso_lineal < 30.0:
                    progreso_lineal += 1.2
                    msg = "📄 Extrayendo texto y analizando estructura del currículum..."
                elif progreso_lineal < 60.0:
                    progreso_lineal += 0.9
                    msg = "🔍 Escaneando palabras clave ATS para Cloud & DevOps..."
                elif progreso_lineal < 85.0:
                    progreso_lineal += 0.7
                    msg = "❌ Auditando deficiencias, falta de métricas y riesgos de filtrado..."
                else:
                    # Avanza suavemente mientras la IA responde sin superar el 95%
                    progreso_lineal = min(95.0, progreso_lineal + 0.15)
                    msg = "✨ Reestructurando experiencia técnica con fórmula Google X-Y-Z..."
            else:
                # El análisis concluyó: completar rápidamente al 100% exacto
                progreso_lineal = min(100.0, progreso_lineal + 6.0)
                msg = "🚀 ¡Auditoría completada y CV optimizado listo!"

            html_bar = render_html_progress(
                progreso=min(100.0, progreso_lineal),
                mensaje=msg,
                titulo="AUDITORÍA ATS EN TIEMPO REAL"
            )
            placeholder_progreso.markdown(html_bar, unsafe_allow_html=True)
            time.sleep(0.06)

        if estado_worker["error"]:
            placeholder_progreso.empty()
            st.error(f"❌ Error al auditar el CV: {estado_worker['error']}")
            return

        # Mostrar el 100% durante 0.3 segundos para confirmación visual perfecta
        placeholder_progreso.markdown(
            render_html_progress(
                progreso=100.0,
                mensaje="🚀 ¡100% Completado! Desplegando informe de auditoría...",
                titulo="AUDITORÍA ATS EN TIEMPO REAL"
            ),
            unsafe_allow_html=True
        )
        time.sleep(0.3)
        placeholder_progreso.empty()
        st.session_state["resultado_cv"] = estado_worker["resultado"]
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
                f'<div style="background: rgba(239, 68, 68, 0.08); border-left: 3px solid #ef4444; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 0.86rem; color: #fca5a5; line-height: 1.4;">{err}</div>'
                for err in errores
            ])

            html_critico = f"""<div class="card-critique-red fade-up-1">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
<div>
<span style="font-size: 0.78rem; font-weight: 700; color: #f87171; text-transform: uppercase; letter-spacing: 0.05em;">
Evaluación del CV Original
</span>
<h4 style="margin: 2px 0 0 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">
⚠️ Deficiencias & Errores Críticos
</h4>
</div>
<div style="background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; border-radius: 12px; padding: 8px 16px; text-align: center;">
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
        # TARJETA 2: MEJORAS Y CV OPTIMIZADO (VERDE NEÓN)
        # ------------------------------------------------------------
        with col_verde:
            items_mejoras = "".join([
                f'<div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid #10b981; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; font-size: 0.86rem; color: #6ee7b7; line-height: 1.4;">{pts}</div>'
                for pts in puntos_fuertes
            ])

            html_optimizado = f"""<div class="card-optimized-green fade-up-2">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
<div>
<span style="font-size: 0.78rem; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 0.05em;">
Versión Optimizada para el Puesto
</span>
<h4 style="margin: 2px 0 0 0; font-size: 1.25rem; font-weight: 800; color: #ffffff;">
✨ Correcciones & Puntos Fuertes
</h4>
</div>
<div style="background: rgba(16, 185, 129, 0.2); border: 2px solid #10b981; border-radius: 12px; padding: 8px 16px; text-align: center;">
<span style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #34d399; line-height: 1;">
{score_verde}%
</span>
<div style="font-size: 0.68rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase;">Top Match</div>
</div>
</div>

<div style="background: rgba(10, 15, 28, 0.6); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 14px; margin-bottom: 16px;">
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
        col_cv_ctrl, col_cv_pdf, col_cv_md = st.columns([1.8, 1.4, 1.4], gap="medium")
        with col_cv_ctrl:
            vista_cv = st.radio(
                "Vista de CV",
                options=["👁️ Vista Formateada del CV", "💻 Código Markdown Fuente (.md)"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with col_cv_pdf:
            pdf_bytes = generar_pdf_cv(cv_md)
            st.download_button(
                label="📄 Descargar CV en PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"Curriculum_{nombre.replace(' ', '_')}_DevOps.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_cv_md:
            st.download_button(
                label="📥 Descargar CV (.md)",
                data=cv_md,
                file_name=f"Curriculum_{nombre.replace(' ', '_')}_DevOps.md",
                mime="text/markdown",
                use_container_width=True
            )

        # Encabezado visual de la terminal
        cv_header_html = """<div class="terminal-header" style="border-top-left-radius: 16px; border-top-right-radius: 16px; margin-top: 14px;">
<div class="terminal-dots">
<span class="dot-red"></span>
<span class="dot-yellow"></span>
<span class="dot-green"></span>
</div>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; color: #94a3b8;">
Curriculum_Vitae_Cloud_DevOps.md • Listo para Postulaciones
</div>
<div>
<span class="badge-status">100% Optimizado</span>
</div>
</div>"""
        st.markdown(textwrap.dedent(cv_header_html).strip(), unsafe_allow_html=True)

        # Contenedor del documento CV (unido a la cabecera sin huecos)
        if vista_cv == "👁️ Vista Formateada del CV":
            st.markdown(
                f'<div class="cv-document-sheet fade-up-2">\n\n{cv_md}\n\n</div>',
                unsafe_allow_html=True
            )
        else:
            st.code(cv_md, language="markdown")

