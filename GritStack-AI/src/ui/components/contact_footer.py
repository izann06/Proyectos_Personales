"""
Componente de Contacto y Cierre Profesional (Contact & Availability Footer).
Diseño Sólido de alta gama con enlaces verificados de LinkedIn y GitHub.
"""

import textwrap
import streamlit as st

def render_contact_footer(datos_perfil: dict):
    """
    Renderiza la sección de contacto final del dashboard con estética sólida,
    enlaces reales y tarjeta de disponibilidad profesional sin emojis.
    """
    usuario = datos_perfil.get("usuario", "izann06")
    nombre = datos_perfil.get("nombre", "Izan Marcos Martínez")
    ubicacion = datos_perfil.get("ubicacion", "España")
    url_perfil = datos_perfil.get("url_perfil", f"https://github.com/{usuario}")
    linkedin_url = "https://www.linkedin.com/in/izan-marcos-mart%C3%ADnez-913728369"

    html = f"""<div style="margin: 40px 0 20px 0;" class="fade-up-3">
<div class="solid-card" style="padding: 30px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 24px;">
<div>
<h3 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: #ffffff;">
Contacto & Oportunidades Profesionales
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #94a3b8;">
Abierto a roles técnicos en ingeniería Cloud, cultura DevOps, arquitectura Serverless y automatización.
</p>
</div>
<span class="badge-status">Disponible para Oportunidades</span>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px;">
<div style="background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 38px; height: 38px; border-radius: 8px; background: #0a66c2; display: flex; align-items: center; justify-content: center; color: #ffffff;">
<span style="font-weight: 900; font-size: 1.1rem;">in</span>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">LinkedIn Profesional</div>
<div style="font-size: 0.78rem; color: #94a3b8;">{nombre}</div>
</div>
</div>
<a href="{linkedin_url}" target="_blank" rel="noopener noreferrer" style="width: 100%; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; background: #0a66c2; border: 1px solid #0a66c2; color: #ffffff; padding: 10px 14px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; cursor: pointer; transition: all 0.2s ease;">
  <span>Conectar en LinkedIn</span>
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="7" y1="17" x2="17" y2="7"></line>
    <polyline points="7 7 17 7 17 17"></polyline>
  </svg>
</a>
</div>

<div style="background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 38px; height: 38px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #ffffff;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
</svg>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">Perfil de GitHub</div>
<div style="font-size: 0.78rem; color: #94a3b8;">@{usuario}</div>
</div>
</div>
<a href="{url_perfil}" target="_blank" rel="noopener noreferrer" style="width: 100%; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; background: #2563eb; border: 1px solid #2563eb; color: #ffffff; padding: 10px 14px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; cursor: pointer; transition: all 0.2s ease;">
  <span>Ver Repositorios</span>
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="7" y1="17" x2="17" y2="7"></line>
    <polyline points="7 7 17 7 17 17"></polyline>
  </svg>
</a>
</div>

<div style="background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 38px; height: 38px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #10b981;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></line>
  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
</svg>
</div>
<div>
<div style="font-size: 0.92rem; font-weight: 700; color: #ffffff;">Modalidad & Enfoque</div>
<div style="font-size: 0.78rem; color: #94a3b8;">Cloud / DevOps Engineer</div>
</div>
</div>
<div style="font-size: 0.82rem; color: #6ee7b7; font-weight: 600; background: #13241d; border: 1px solid #065f46; border-radius: 8px; padding: 8px 10px; text-align: center;">
{ubicacion} • Remoto / Híbrido
</div>
</div>
</div>

<div style="border-top: 1px solid #1e293b; padding-top: 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; font-size: 0.8rem; color: #64748b;">
<div>GritStack AI • Plataforma de Inteligencia Profesional & Portafolio Cloud</div>
<div>Construido con Python, Streamlit, Claude Sonnet 4.6 & AWS Bedrock</div>
</div>
</div>
</div>"""

    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
