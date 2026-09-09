"""
Componente de Barra de Navegación Superior (Solid Topbar).
"""

import textwrap
import streamlit as st

def render_navbar(usuario: str = "izann06"):
    """
    Renderiza la barra de navegación superior con diseño sólido,
    indicador de estado y botón de gestión de sesión sin emojis.
    """
    col_logo, col_badge, col_btn = st.columns([3, 3, 2])
    
    with col_logo:
        html_logo = """<div style="display: flex; align-items: center; gap: 12px; padding: 6px 0;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: #2563eb; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="16 18 22 12 16 6"></polyline>
  <polyline points="8 6 2 12 8 18"></polyline>
</svg>
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
        if st.button("Cambiar Token", key="nav_token_btn", use_container_width=True):
            st.session_state["etapa"] = "onboarding"
            st.session_state["datos_perfil"] = None
            st.session_state["readme_generado"] = None
            st.rerun()
        
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
