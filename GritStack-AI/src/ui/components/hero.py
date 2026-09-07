"""
Componente Hero del Perfil (Senior UX Profile Banner).
"""

import textwrap
import streamlit as st

def render_hero(datos_perfil: dict):
    """
    Renderiza el Hero banner con tarjeta glassmorphism, avatar con resplandor neón,
    badges de especialidad Cloud & DevOps y estadísticas clave.
    """
    usuario = datos_perfil.get("usuario", "izann06")
    nombre = datos_perfil.get("nombre", usuario)
    
    # Avatar de alta resolución con fallback visual garantizado
    raw_avatar = datos_perfil.get("avatar_url", "")
    avatar_url = raw_avatar if raw_avatar else f"https://github.com/{usuario}.png"
    avatar_fallback = f"https://ui-avatars.com/api/?name={nombre.replace(' ', '+')}&background=7c3aed&color=fff&size=200&bold=true"
    
    bio = datos_perfil.get("bio", "Software Developer | AWS Cloud & DevOps Enthusiast | Docker & Terraform")
    ubicacion = datos_perfil.get("ubicacion", "España")
    url_perfil = datos_perfil.get("url_perfil", f"https://github.com/{usuario}")
    
    stats = datos_perfil.get("estadisticas", {})
    total_repos = stats.get("total_repositorios", len(datos_perfil.get("repositorios", [])))
    total_stars = stats.get("total_estrellas", 0)

    html = f"""<div class="glass-card fade-up-1" style="margin-bottom: 24px; padding: 26px 30px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
<div style="display: flex; align-items: center; gap: 24px;">
<div style="position: relative;">
<img src="{avatar_url}" 
     referrerpolicy="no-referrer" 
     crossorigin="anonymous"
     onerror="this.onerror=null; this.src='{avatar_fallback}';" 
     style="width: 84px; height: 84px; border-radius: 50%; border: 2px solid #a855f7; box-shadow: 0 0 25px rgba(168, 85, 247, 0.45); object-fit: cover; background: #1e1b4b;"
     alt="{nombre}">
<span style="position: absolute; bottom: 4px; right: 4px; width: 16px; height: 16px; background: #10b981; border: 3px solid #0b0f19; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></span>
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
<div style="display: flex; align-items: center; gap: 16px; margin-top: 10px; font-size: 0.82rem; color: #64748b;">
<span>📍 {ubicacion}</span>
<span>📦 <strong>{total_repos}</strong> repositorios</span>
<span>⭐ <strong>{total_stars}</strong> estrellas</span>
</div>
</div>
</div>
<div>
<a href="{url_perfil}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.18); color: #ffffff; padding: 10px 20px; border-radius: 12px; font-size: 0.88rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease;">
  <span>Ver en GitHub</span> <span>↗</span>
</a>
</div>
</div>
</div>"""

    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

