"""
GritStack AI - Plataforma de Inteligencia Profesional para Desarrolladores
Punto de Entrada Principal (Streamlit App)
"""

import streamlit as st
from src.ui.styles import aplicar_estilos
from src.ui.onboarding import render_onboarding
from src.ui.pantalla_carga import render_pantalla_carga
from src.ui.dashboard import render_dashboard

# Configuración inicial de la página
st.set_page_config(
    page_title="GritStack AI | Developer Intelligence Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Inyectar estilos CSS maestros (Cyber Luxe / Obsidian Aurora)
    aplicar_estilos(st)

    # Inicialización limpia de estados de sesión
    if "etapa" not in st.session_state:
        st.session_state["etapa"] = "onboarding"

    if "token_github" not in st.session_state:
        st.session_state["token_github"] = ""

    if "datos_perfil" not in st.session_state:
        st.session_state["datos_perfil"] = None

    if "readme_generado" not in st.session_state:
        st.session_state["readme_generado"] = None

    # Enrutador de pantallas
    etapa_actual = st.session_state["etapa"]

    if etapa_actual == "onboarding":
        render_onboarding()

    elif etapa_actual == "cargando":
        token = st.session_state.get("token_github", "")
        if not token:
            st.session_state["etapa"] = "onboarding"
            st.rerun()
        else:
            render_pantalla_carga(token)

    elif etapa_actual == "dashboard":
        datos = st.session_state.get("datos_perfil")
        readme = st.session_state.get("readme_generado")

        if not datos or not readme:
            st.session_state["etapa"] = "onboarding"
            st.rerun()
        else:
            render_dashboard(datos, readme)

if __name__ == "__main__":
    main()
