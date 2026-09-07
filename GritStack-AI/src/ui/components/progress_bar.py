"""
Componente Reutilizable de Barra de Progreso con Marcador de GitHub Móvil.
Diseño Glassmorphism animado en tiempo real con límite estricto en 100.0%.
"""

GITHUB_OCTOCAT_SVG = """<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>"""

def render_html_progress(progreso: float, mensaje: str, titulo: str = "PROGRESO DE INTELIGENCIA") -> str:
    """
    Genera el HTML puro de la barra de progreso con el Octocat móvil.
    Garantiza de forma estricta que el porcentaje jamás supere el 100% y que
    el icono quede perfectamente alineado al inicio y al final de la pista.
    """
    # Límite matemático infranqueable entre 0.0% y 100.0%
    progreso_clamped = max(0.0, min(100.0, float(progreso)))
    pct_int = int(progreso_clamped)
    
    # Posición geométrica del Octocat (2.5% a 97.5% para centrarlo exactamente en los bordes)
    posicion_icono = 2.5 + (progreso_clamped / 100.0) * 95.0
    
    html = f"""<div class="glass-card" style="max-width: 680px; margin: 0 auto; padding: 24px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<span style="font-size: 0.82rem; font-weight: 700; color: #a855f7; text-transform: uppercase; letter-spacing: 0.05em;">{titulo}</span>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: #38bdf8;">{pct_int}%</span>
</div>
<div class="grit-progress-track">
<div class="grit-progress-fill" style="width: {progreso_clamped:.1f}%;"></div>
<div class="grit-github-runner" style="left: {posicion_icono:.1f}%;">{GITHUB_OCTOCAT_SVG}</div>
</div>
<div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 14px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px #38bdf8;"></div>
<div style="font-size: 0.92rem; color: #f1f5f9; font-weight: 600;">{mensaje}</div>
</div>
</div>"""
    return html.strip()
