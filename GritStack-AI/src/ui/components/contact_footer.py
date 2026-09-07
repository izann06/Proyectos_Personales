"""
Componente de Contacto y Cierre Profesional (Contact & Availability Footer).
Diseño Glassmorphic de alta gama con enlaces verificados de LinkedIn y GitHub.
"""

import textwrap
import streamlit as st

def render_contact_footer(datos_perfil: dict):
    """
    Renderiza la sección de contacto final del dashboard con estética premium,
    enlaces reales y tarjeta de disponibilidad profesional.
    """
    usuario = datos_perfil.get("usuario", "izann06")
    nombre = datos_perfil.get("nombre", "Izan Marcos Martínez")
    ubicacion = datos_perfil.get("ubicacion", "España")
    url_perfil = datos_perfil.get("url_perfil", f"https://github.com/{usuario}")
    linkedin_url = "https://www.linkedin.com/in/izan-marcos-mart%C3%ADnez-913728369"

    html = f"""<div style="margin: 40px 0 20px 0;" class="fade-up-3">
<div class="glass-card" style="padding: 30px; background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(11, 15, 25, 0.9) 100%);">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 24px;">
<div>
<h3 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: #ffffff;">
📫 Conecta Conmigo & Oportunidades Profesionales
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Abierto a roles técnicos en ingeniería Cloud, cultura DevOps, arquitectura Serverless y automatización.
</p>
</div>
<span class="badge-status">🟢 Disponible para Oportunidades</span>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px;">
<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 40px; height: 40px; border-radius: 10px; background: rgba(10, 102, 194, 0.2); border: 1px solid rgba(10, 102, 194, 0.4); display: flex; align-items: center; justify-content: center;">
<span style="font-weight: 900; color: #38bdf8; font-size: 1.2rem;">in</span>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">LinkedIn Profesional</div>
<div style="font-size: 0.78rem; color: #94a3b8;">{nombre}</div>
</div>
</div>
<a href="{linkedin_url}" target="_blank" rel="noopener noreferrer" style="width: 100%; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; background: rgba(10, 102, 194, 0.3); border: 1px solid rgba(10, 102, 194, 0.55); color: #bae6fd; padding: 10px 14px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; cursor: pointer; transition: all 0.2s ease;">
  <span>Conectar en LinkedIn</span> <span>↗</span>
</a>
</div>

<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 40px; height: 40px; border-radius: 10px; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.35); display: flex; align-items: center; justify-content: center;">
<span style="font-size: 1.2rem;">🐙</span>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">Perfil de GitHub</div>
<div style="font-size: 0.78rem; color: #94a3b8;">@{usuario}</div>
</div>
</div>
<a href="{url_perfil}" target="_blank" rel="noopener noreferrer" style="width: 100%; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; background: rgba(168, 85, 247, 0.25); border: 1px solid rgba(168, 85, 247, 0.45); color: #e9d5ff; padding: 10px 14px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; cursor: pointer; transition: all 0.2s ease;">
  <span>Ver Repositorios</span> <span>↗</span>
</a>
</div>


<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 40px; height: 40px; border-radius: 10px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); display: flex; align-items: center; justify-content: center;">
<span style="font-size: 1.2rem;">🚀</span>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">Modalidad & Enfoque</div>
<div style="font-size: 0.78rem; color: #94a3b8;">Cloud / DevOps Engineer</div>
</div>
</div>
<div style="font-size: 0.82rem; color: #6ee7b7; font-weight: 600; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 8px 10px; text-align: center;">
📍 {ubicacion} (Remoto / Híbrido)
</div>
</div>
</div>

<div style="border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; font-size: 0.8rem; color: #64748b;">
<div>GritStack AI • Plataforma de Inteligencia Profesional & Portafolio Cloud</div>
<div>Construido con Python, Streamlit, Claude Sonnet 4.6 & AWS Bedrock</div>
</div>
</div>
</div>"""

    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
