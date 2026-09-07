"""
Componente de Barra de Navegación Superior (Glassmorphic Topbar).
"""

import textwrap
import streamlit as st

def render_navbar(usuario: str = "izann06"):
    """
    Renderiza la barra de navegación superior con efecto cristal,
    indicador de estado y botón sutil de gestión de sesión.
    """
    col_logo, col_badge, col_btn = st.columns([3, 3, 2])
    
    with col_logo:
        html_logo = """<div style="display: flex; align-items: center; gap: 12px; padding: 6px 0;">
<div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 16px rgba(168, 85, 247, 0.5);">
<span style="font-size: 1.2rem;">⚡</span>
</div>
<div>
<span style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">
GritStack<span style="color: #38bdf8;">.AI</span>
</span>
<span style="font-size: 0.72rem; color: #64748b; margin-left: 6px; font-weight: 600; text-transform: uppercase;">PRO</span>
</div>
</div>"""
        st.markdown(textwrap.dedent(html_logo).strip(), unsafe_allow_html=True)
        
    with col_badge:
        html_badge = """<div style="display: flex; align-items: center; justify-content: center; height: 100%; padding-top: 6px;">
<span class="badge-status">
Cloud & DevOps Architecture Hub
</span>
</div>"""
        st.markdown(textwrap.dedent(html_badge).strip(), unsafe_allow_html=True)
        
    with col_btn:
        if st.button("🔄 Cambiar Token", key="nav_token_btn", use_container_width=True):
            st.session_state["etapa"] = "onboarding"
            st.session_state["datos_perfil"] = None
            st.session_state["readme_generado"] = None
            st.rerun()
        
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
