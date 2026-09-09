"""
Componente Hero del Perfil (Senior UX Profile Banner).
"""

import textwrap
import streamlit as st

def render_hero(datos_perfil: dict):
    """
    Renderiza el Hero banner con tarjeta sólida de alto contraste,
    avatar nítido, badges y métricas clave sin emojis.
    """
    usuario = datos_perfil.get("usuario", "izann06")
    nombre = datos_perfil.get("nombre", usuario)
    
    # Avatar de alta resolución con fallback visual garantizado
    raw_avatar = datos_perfil.get("avatar_url", "")
    avatar_url = raw_avatar if raw_avatar else f"https://github.com/{usuario}.png"
    avatar_fallback = f"https://ui-avatars.com/api/?name={nombre.replace(' ', '+')}&background=2563eb&color=fff&size=200&bold=true"
    
    bio = datos_perfil.get("bio", "Software Developer | AWS Cloud & DevOps Enthusiast | Docker & Terraform")
    ubicacion = datos_perfil.get("ubicacion", "España")
    url_perfil = datos_perfil.get("url_perfil", f"https://github.com/{usuario}")
    
    stats = datos_perfil.get("estadisticas", {})
    total_repos = stats.get("total_repositorios", len(datos_perfil.get("repositorios", [])))
    total_stars = stats.get("total_estrellas", 0)

    html = f"""<div class="solid-card fade-up-1" style="margin-bottom: 24px; padding: 26px 30px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
<div style="display: flex; align-items: center; gap: 24px;">
<div style="position: relative;">
<img src="{avatar_url}" 
     referrerpolicy="no-referrer" 
     crossorigin="anonymous"
     onerror="this.onerror=null; this.src='{avatar_fallback}';" 
     style="width: 80px; height: 80px; border-radius: 50%; border: 2px solid #2563eb; object-fit: cover; background: #1e293b;"
     alt="{nombre}">
<span style="position: absolute; bottom: 2px; right: 2px; width: 14px; height: 14px; background: #10b981; border: 2.5px solid #0f172a; border-radius: 50%;"></span>
</div>
<div>
<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
<h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #ffffff;">{nombre}</h1>
<span class="badge-devops">DevOps & Cloud</span>
<span class="badge-cloud">@{usuario}</span>
</div>
<p style="margin: 6px 0 0 0; font-size: 0.94rem; color: #94a3b8; max-width: 680px; line-height: 1.5;">
{bio}
</p>
<div style="display: flex; align-items: center; gap: 20px; margin-top: 12px; font-size: 0.84rem; color: #94a3b8;">
<span>Ubicación: <strong style="color: #f1f5f9;">{ubicacion}</strong></span>
<span>Repositorios: <strong style="color: #f1f5f9;">{total_repos}</strong></span>
<span>Estrellas: <strong style="color: #f1f5f9;">{total_stars}</strong></span>
</div>
</div>
</div>
<div>
<a href="{url_perfil}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; background: #1e293b; border: 1px solid #334155; color: #ffffff; padding: 10px 20px; border-radius: 10px; font-size: 0.88rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease;">
  <span>Ver en GitHub</span>
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <line x1="7" y1="17" x2="17" y2="7"></line>
    <polyline points="7 7 17 7 17 17"></polyline>
  </svg>
</a>
</div>
</div>
</div>"""

    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
