"""
Pantalla de Inicio / Onboarding para GritStack AI
Estilo: Dark Mode de Alta Ingeniería + Paleta Sólida + Alto Contraste
"""

import os
import textwrap
import streamlit as st
from dotenv import load_dotenv

def render_onboarding():
    """
    Renderiza la pantalla inicial solicitando el Token de GitHub sin emojis y con diseño sólido.
    """
    load_dotenv()
    token_por_defecto = os.getenv("GITHUB_TOKEN", "")

    header_html = """<div style="text-align: center; margin-top: 20px; margin-bottom: 35px;" class="fade-up-1">
<div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 16px;">
<span class="badge-devops">GritStack AI v2.5</span>
<span class="badge-cloud">Cloud & DevOps Focus</span>
<span class="badge-status">Conexión Segura</span>
</div>
<h1 style="font-size: 2.8rem; font-weight: 800; margin: 0 0 12px 0; color: #ffffff; letter-spacing: -0.03em; line-height: 1.15;">
Tu Talento Técnico,<br>Decodificado por IA
</h1>
<p style="font-size: 1.05rem; color: #94a3b8; max-width: 640px; margin: 0 auto; line-height: 1.6;">
Conecta tu cuenta de GitHub para transformar tus proyectos y arquitecturas en un portafolio de alto impacto, optimizado para roles de <strong>Cloud & DevOps</strong>.
</p>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    
    with col_centro:
        card_start = """<div class="solid-card fade-up-2" style="padding: 32px;">
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 20px;">
<div style="width: 42px; height: 42px; border-radius: 10px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #38bdf8;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
<path d="M7 11V7a5 5 0 0 1 10 0v4"/>
</svg>
</div>
<div>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #ffffff;">Conectar con GitHub</h3>
<p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">Personal Access Token (PAT) seguro</p>
</div>
</div>"""
        st.markdown(textwrap.dedent(card_start).strip(), unsafe_allow_html=True)

        token_input = st.text_input(
            "GitHub Personal Access Token",
            value=token_por_defecto,
            type="password",
            placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Introduce tu token con permisos 'repo' y 'read:user'. Se almacena solo en memoria.",
            label_visibility="collapsed"
        )

        card_info = """<p style="font-size: 0.78rem; color: #64748b; margin-top: 6px; margin-bottom: 20px;">
Tu token solo se utiliza en memoria para consultar la API oficial de GitHub y jamás se almacena externamente.
</p>"""
        st.markdown(textwrap.dedent(card_info).strip(), unsafe_allow_html=True)

        boton_conectar = st.button("Iniciar Análisis Inteligente", type="primary", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if boton_conectar:
            token_limpio = token_input.strip()
            if not token_limpio:
                st.error("Por favor, introduce un Token de GitHub válido para continuar.")
            else:
                st.session_state["token_github"] = token_limpio
                st.session_state["etapa"] = "cargando"
                st.rerun()

    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        c1_html = """<div class="solid-card fade-up-1" style="padding: 22px;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #38bdf8; margin-bottom: 12px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="8"></circle>
  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
</svg>
</div>
<div style="font-family: 'Outfit'; font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 6px;">
Extracción Profunda de Repos
</div>
<p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.5; margin: 0;">
Escaneamos arquitecturas de infraestructura, contenedores, commits y lenguajes reales evitando métricas engañosas.
</p>
</div>"""
        st.markdown(textwrap.dedent(c1_html).strip(), unsafe_allow_html=True)

    with c2:
        c2_html = """<div class="solid-card fade-up-2" style="padding: 22px;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #38bdf8; margin-bottom: 12px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
</svg>
</div>
<div style="font-family: 'Outfit'; font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 6px;">
Top 3 Proyectos & README
</div>
<p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.5; margin: 0;">
Selección inteligente de tus mejores proyectos (AWS, Docker, CI/CD) y generación de README listo para publicar.
</p>
</div>"""
        st.markdown(textwrap.dedent(c2_html).strip(), unsafe_allow_html=True)

    with c3:
        c3_html = """<div class="solid-card fade-up-3" style="padding: 22px;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #38bdf8; margin-bottom: 12px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
  <polyline points="14 2 14 8 20 8"></polyline>
  <line x1="16" y1="13" x2="8" y2="13"></line>
  <line x1="16" y1="17" x2="8" y2="17"></line>
  <polyline points="10 9 9 9 8 9"></polyline>
</svg>
</div>
<div style="font-family: 'Outfit'; font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 6px;">
Adaptador de CV ATS en PDF
</div>
<p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.5; margin: 0;">
Optimiza tu currículum para ofertas de Cloud & DevOps, alineando tus proyectos para superar filtros ATS.
</p>
</div>"""
        st.markdown(textwrap.dedent(c3_html).strip(), unsafe_allow_html=True)
