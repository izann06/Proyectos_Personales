"""
Componente de Proyectos Destacados (Top 3 Projects Showcase).
Muestra únicamente los 3 proyectos insignia de mayor calidad técnica con tarjetas Glassmorphism.
"""

import textwrap
import streamlit as st
from src.core.projects_curator import seleccionar_top_proyectos

def render_projects_showcase(datos_perfil: dict):
    """
    Renderiza los 3 proyectos más representativos del perfil,
    orientados a Cloud, DevOps, contenedores y automatización.
    """
    top_proyectos = seleccionar_top_proyectos(datos_perfil)
    if not top_proyectos:
        return

    header_html = """<div style="margin: 32px 0 16px 0;" class="fade-up-2">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h3 style="margin: 0; font-size: 1.45rem; font-weight: 800; color: #ffffff;">
🏆 Proyectos Insignia Destacados <span style="font-size: 0.9rem; font-weight: 600; color: #38bdf8;">(Top 3)</span>
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">
Selección curada de arquitecturas reales: Cloud Serverless, Infraestructura como Código (IaC), contenedores y pipelines CI/CD.
</p>
</div>
<span class="badge-cloud">Filtro de Excelencia Activo</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    cols = [col1, col2, col3]

    for i, proj in enumerate(top_proyectos[:3]):
        with cols[i]:
            tags_html = "".join([
                f'<span style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); color: #cbd5e1; font-size: 0.74rem; font-weight: 600; padding: 3px 8px; border-radius: 6px;">{t}</span>'
                for t in proj.get("stack", [])[:4]
            ])
            
            card_html = f"""<div class="glass-card fade-up-{i+1}" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 290px;">
<div>
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
<span style="font-size: 1.6rem;">{proj.get('icono', '🚀')}</span>
<span class="badge-devops" style="font-size: 0.72rem;">{proj.get('categoria', 'Cloud')}</span>
</div>
<h4 style="margin: 0 0 6px 0; font-size: 1.15rem; font-weight: 700; color: #ffffff;">
{proj.get('nombre')}
</h4>
<div style="font-size: 0.8rem; font-weight: 600; color: #38bdf8; margin-bottom: 10px;">
{proj.get('tagline', '')}
</div>
<p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.5; margin-bottom: 16px;">
{proj.get('descripcion')}
</p>
</div>
<div>
<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px;">
{tags_html}
</div>
<a href="{proj.get('url')}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.3) 100%); border: 1px solid rgba(168, 85, 247, 0.45); color: #ffffff; padding: 10px 14px; border-radius: 10px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.25s ease;">
  <span>Explorar Repositorio en GitHub</span> <span>↗</span>
</a>
</div>
</div>"""
            st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)

