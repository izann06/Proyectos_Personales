"""
Dashboard Principal de GritStack AI (Arquitectura Modular y Estabilidad Estricta).
Orquestador limpio que ensambla componentes desacoplados de alto rendimiento.
"""

import streamlit as st
from src.ui.components.navbar import render_navbar
from src.ui.components.hero import render_hero
from src.ui.components.projects_showcase import render_projects_showcase
from src.ui.components.readme_studio import render_readme_studio
from src.ui.components.cv_matcher import render_cv_matcher
from src.ui.components.chat_assistant import render_chat_assistant
from src.ui.components.contact_footer import render_contact_footer

def render_dashboard(datos_perfil: dict, readme_md: str):
    """
    Renderiza el Dashboard completo integrando componentes modulares
    con estética Glassmorphism, animaciones fade-up y cero código duplicado.
    """
    usuario = datos_perfil.get("usuario", "izann06")
    
    # 1. Barra de navegación superior
    render_navbar(usuario)

    # 2. Hero del perfil con avatar, bio y stats
    render_hero(datos_perfil)

    # 3. Navegación en 3 Pestañas Principales (Full-Width y Tipografía Moderna)
    tab_perfil, tab_chat, tab_cv = st.tabs([
        "🚀 Perfil & README Studio",
        "💬 Mentor IA (Staff Architect)",
        "🎯 TailorCV Studio (ATS Matcher)"
    ])


    # ------------------------------------------------------------
    # PESTAÑA 1: PERFIL, TOP 3 PROYECTOS & README
    # ------------------------------------------------------------
    with tab_perfil:
        # Top 3 Proyectos Insignia
        render_projects_showcase(datos_perfil)

        # Visor de README limpio (con alternador de vista renderizada vs markdown)
        render_readme_studio(readme_md, usuario)

        # Sección de Contacto final y disponibilidad
        render_contact_footer(datos_perfil)

    # ------------------------------------------------------------
    # PESTAÑA 2: MENTOR IA (CHATBOT ORIENTADO A DEVOPS & CLOUD)
    # ------------------------------------------------------------
    with tab_chat:
        render_chat_assistant(datos_perfil)

    # ------------------------------------------------------------
    # PESTAÑA 3: ADAPTADOR DE CV REAL (ATS MATCHER)
    # ------------------------------------------------------------
    with tab_cv:
        render_cv_matcher(datos_perfil)
