"""
Componente de Visualización y Exportación de README.md (README Studio).
Diseño tipo Ventana Terminal MacOS con selector de vista (Renderizada vs Código Limpio).
"""

import re
import textwrap
import streamlit as st

def sanitizar_y_mejorar_readme(readme_md: str, usuario: str = "izann06") -> str:
    """
    Normaliza y asegura que los títulos de proyectos, badges de Terraform
    y métricas de ingeniería de GitHub se muestren impecables y 100% funcionales.
    """
    if not readme_md:
        return ""

    # 1. Corrección del badge de Terraform (garantizar que siempre cargue en shields.io)
    readme_md = re.sub(
        r'<img[^>]*src="[^"]*shields\.io/badge/Terraform[^"]*"[^>]*>',
        '<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />',
        readme_md,
        flags=re.IGNORECASE
    )
    readme_md = re.sub(
        r'!\[Terraform\]\([^)]+\)',
        '<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />',
        readme_md,
        flags=re.IGNORECASE
    )

    # 2. Asegurar que los números de proyectos tengan el título y enlace INMEDIATAMENTE en la misma línea
    # Proyecto 1: AWS Serverless Text-to-Speech
    p1_title = "🎙️ AWS Serverless Text-to-Speech (IaC con Terraform)"
    p1_url = f"https://github.com/{usuario}/aws-serverless-text-to-speech"
    readme_md = re.sub(
        r'(?m)^(?:#+\s*)?1\.(?:(?!\(https://github\.com).)*$',
        f"#### 1. [{p1_title}]({p1_url})",
        readme_md
    )

    # Proyecto 2: Docker Labs
    p2_title = "🐳 Docker Labs & Homelab Infrastructure (Orquestación & Zero-Trust)"
    p2_url = f"https://github.com/{usuario}/Docker-Labs"
    readme_md = re.sub(
        r'(?m)^(?:#+\s*)?2\.(?:(?!\(https://github\.com).)*$',
        f"#### 2. [{p2_title}]({p2_url})",
        readme_md
    )

    # Proyecto 3: DevOps Proyectos & Linux Automation
    p3_title = "⚙️ DevOps Proyectos & Linux Systems Automation"
    p3_url = f"https://github.com/{usuario}/DevOps-Proyectos-RoadMap"
    readme_md = re.sub(
        r'(?m)^(?:#+\s*)?3\.(?:(?!\(https://github\.com).)*$',
        f"#### 3. [{p3_title}]({p3_url})",
        readme_md
    )

    # 3. Métricas de ingeniería de GitHub 100% fiables sin caracteres no ASCII en URLs
    metricas_html = """<div align="center">
  <img src="https://img.shields.io/badge/Repositorios_Publicos-16-232F3E?style=for-the-badge&logo=github&logoColor=white" alt="repos" />
  <img src="https://img.shields.io/badge/Estrellas_Totales-1-f59e0b?style=for-the-badge&logo=apachespark&logoColor=white" alt="stars" />
  <img src="https://img.shields.io/badge/Especialidad-Cloud_%26_DevOps-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="focus" />
  <img src="https://img.shields.io/badge/Infraestructura-AWS_%26_Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="docker" />
</div>"""

    # Limpiar servidores externos caídos
    if "github-readme-stats" in readme_md or "metrics" in readme_md:
        readme_md = re.sub(
            r'<img[^>]*github-readme-stats[^>]*>',
            '',
            readme_md
        )

    # Reemplazar de forma integral y robusta la sección de métricas
    patron_metricas = r'(?is)(#{1,4}\s*[^\n]*(?:métricas|metrics)[^\n]*\n)(?:.*?)(?=\n#{1,4}\s|\Z)'
    if re.search(patron_metricas, readme_md):
        readme_md = re.sub(
            patron_metricas,
            r'### 📊 Métricas de Ingeniería en GitHub\n\n' + metricas_html + '\n\n',
            readme_md
        )
    else:
        readme_md += f"\n\n---\n\n### 📊 Métricas de Ingeniería en GitHub\n\n{metricas_html}\n"

    return readme_md

def render_readme_studio(readme_md: str, usuario: str = "izann06"):
    """
    Renderiza el README generado con terminal MacOS perfectamente cohesionada
    sin bloques sueltos ni espacios muertos.
    """
    readme_md = sanitizar_y_mejorar_readme(readme_md, usuario)

    header_html = """<div style="margin: 28px 0 16px 0;" class="fade-up-2">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h3 style="margin: 0; font-size: 1.45rem; font-weight: 800; color: #ffffff;">
📑 README.md de Perfil Profesional
</h3>
<p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">
Generado a medida para tu perfil de GitHub con enfoque en Cloud, DevOps e Infraestructura.
</p>
</div>
<span class="badge-status">Listo para Publicar</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)

    # 1. Barra de controles y descarga (situada limpiamente ANTES de la ventana de terminal)
    col_vistas, col_dl = st.columns([2.5, 1.2])
    
    with col_vistas:
        modo_vista = st.radio(
            "Modo de Visualización",
            options=["👁️ Vista Previa Formateada", "💻 Código Markdown Fuente (.md)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
    with col_dl:
        st.download_button(
            label="📥 Descargar README.md",
            data=readme_md,
            file_name="README.md",
            mime="text/markdown",
            use_container_width=True
        )

    # 2. Ventana Terminal MacOS integrada de una sola pieza (cabecera + cuerpo)
    terminal_header_html = """<div class="terminal-header" style="border-top-left-radius: 16px; border-top-right-radius: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
<div class="terminal-dots">
<span class="dot-red"></span>
<span class="dot-yellow"></span>
<span class="dot-green"></span>
</div>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8;">
README.md • GritStack Intelligence Engine
</div>
<div>
<span style="font-size: 0.75rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">UTF-8 Markdown</span>
</div>
</div>"""
    st.markdown(textwrap.dedent(terminal_header_html).strip(), unsafe_allow_html=True)

    # Contenedor del cuerpo de la terminal (adherido directamente sin huecos)
    st.markdown('<div class="glass-card" style="border-top: none; border-top-left-radius: 0; border-top-right-radius: 0; border-bottom-left-radius: 16px; border-bottom-right-radius: 16px; padding: 28px; margin-bottom: 24px; margin-top: 0;">', unsafe_allow_html=True)

    if modo_vista == "👁️ Vista Previa Formateada":
        st.markdown(readme_md, unsafe_allow_html=True)
    else:
        st.code(readme_md, language="markdown")

    st.markdown("</div>", unsafe_allow_html=True)
