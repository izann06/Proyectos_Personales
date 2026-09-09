"""
Módulo de Estilos y Sistema de Diseño Visual para GritStack AI
Estética: Dark Mode de Alta Ingeniería + Paleta Sólida (#2563eb / #0f172a)
Sin degradados morado-azul, sin texto con gradiente, sin glassmorphism, alto contraste.
"""

CSS_PRINCIPAL = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

:root {
    /* Fondos Sólidos de Alto Contraste */
    --bg-canvas: #090d16;
    --bg-card: #0f172a;
    --bg-card-elevated: #1e293b;
    --bg-card-subtle: #111827;
    
    /* Color Primario Sólido y Acentos de Precisión */
    --primary-solid: #2563eb;
    --primary-hover: #1d4ed8;
    --primary-light: #3b82f6;
    --accent-cyan: #0284c7;
    --accent-emerald: #10b981;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    
    /* Bordes Nítidos de Alto Contraste (Sin desenfoque difuso) */
    --border-subtle: #1e293b;
    --border-contrast: #334155;
    --border-active: #2563eb;
    --border-bright: #475569;

    /* Jerarquía de Texto en Blanco Puro de Máxima Claridad */
    --text-pure: #ffffff;
    --text-primary: #ffffff;
    --text-body: #ffffff;
    --text-secondary: #f8fafc;
    --text-muted: #e2e8f0;

    /* Radios */
    --radius-xl: 18px;
    --radius-lg: 14px;
    --radius-md: 10px;
    --radius-sm: 6px;
}

/* ============================================================
   1. RESET Y TIPOGRAFÍA CUIDADA (ALTO CONTRASTE)
   ============================================================ */
html, body {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: var(--text-primary);
    background-color: var(--bg-canvas);
}

p, div, label, input, textarea {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

h1, h2, h3, h4, h5, h6, .font-heading {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.025em;
    color: var(--text-pure) !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: unset !important;
}

h1 {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
}

h2 {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

h3 {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
}

h4 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}

/* ============================================================
   1.1 BLOQUES DE CÓDIGO Y ELEMENTOS PREFORMATEADOS (CERO FONDO BLANCO)
   ============================================================ */
code, pre, .font-mono {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Bloques de código multilínea (ASCII Art, esquemas, YAML, configs) */
div[data-testid="stMarkdownContainer"] pre,
.stMarkdown pre,
.readme-viewer-sheet pre,
.cv-document-sheet pre,
pre {
    background-color: #0c1222 !important;
    background: #0c1222 !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.86rem !important;
    line-height: 1.55 !important;
    overflow-x: auto !important;
    margin: 16px 0 !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4) !important;
}

div[data-testid="stMarkdownContainer"] pre code,
.stMarkdown pre code,
.readme-viewer-sheet pre code,
.cv-document-sheet pre code,
pre code {
    background-color: transparent !important;
    background: transparent !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0 !important;
    font-size: inherit !important;
    line-height: inherit !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Código en línea (Pills de tecnologías, rutas, variables, tags) */
div[data-testid="stMarkdownContainer"] :not(pre) > code,
.stMarkdown :not(pre) > code,
.readme-viewer-sheet :not(pre) > code,
.cv-document-sheet :not(pre) > code,
:not(pre) > code {
    background-color: #1e293b !important;
    background: #1e293b !important;
    color: #38bdf8 !important;
    border: 1px solid #334155 !important;
    border-radius: 6px !important;
    padding: 2px 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85em !important;
    font-weight: 500 !important;
}

/* Tablas Markdown */
div[data-testid="stMarkdownContainer"] table,
.stMarkdown table,
.readme-viewer-sheet table,
.cv-document-sheet table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 16px 0 !important;
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

div[data-testid="stMarkdownContainer"] th,
.stMarkdown th,
.readme-viewer-sheet th,
.cv-document-sheet th {
    background-color: #1e293b !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: 1px solid #334155 !important;
    padding: 10px 14px !important;
    text-align: left !important;
}

div[data-testid="stMarkdownContainer"] td,
.stMarkdown td,
.readme-viewer-sheet td,
.cv-document-sheet td {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
    padding: 9px 14px !important;
}

/* Blockquotes en Markdown */
div[data-testid="stMarkdownContainer"] blockquote,
.stMarkdown blockquote,
.readme-viewer-sheet blockquote,
.cv-document-sheet blockquote {
    background: #0f172a !important;
    border-left: 3px solid #2563eb !important;
    border-top: 1px solid #1e293b !important;
    border-right: 1px solid #1e293b !important;
    border-bottom: 1px solid #1e293b !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 12px 18px !important;
    margin: 16px 0 !important;
    color: #ffffff !important;
}

/* Forzar Párrafos y Listas Generales a Blanco Puro */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    color: #ffffff !important;
}

/* Bloques de código nativos de Streamlit (st.code) */
div[data-testid="stCode"],
div[data-testid="stCodeBlock"],
div[data-testid="stCodeBlock"] pre {
    background-color: #0c1222 !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

div[data-testid="stCodeBlock"] code {
    color: #e2e8f0 !important;
    background-color: transparent !important;
}

/* ============================================================
   2. ELIMINAR ICONOS DE CLIP / ENLACES DE ANCLA EN ENCABEZADOS
   ============================================================ */
[data-testid="stHeaderActionElements"],
.header-anchor,
a.header-anchor,
a.anchor-link,
[data-testid="stMarkdownContainer"] a.anchor-link,
[data-testid="stMarkdownContainer"] a[href^="#"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Enlaces legítimos de contenido */
h1 a:not([href^="#"]), 
h2 a:not([href^="#"]), 
h3 a:not([href^="#"]), 
h4 a:not([href^="#"]), 
h5 a:not([href^="#"]), 
h6 a:not([href^="#"]) {
    display: inline !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    color: var(--primary-light) !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
}

h1 a:not([href^="#"]):hover, 
h2 a:not([href^="#"]):hover, 
h3 a:not([href^="#"]):hover, 
h4 a:not([href^="#"]):hover {
    color: #93c5fd !important;
    text-decoration: underline !important;
}

/* ============================================================
   3. BOTÓN DE OJO (PASSWORD VISIBILITY)
   ============================================================ */
[data-testid="stTextInput"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    padding: 6px 10px !important;
    margin: auto 4px !important;
    min-width: 38px !important;
    height: 38px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextInput"] button:hover {
    color: var(--primary-light) !important;
    background: rgba(37, 99, 235, 0.1) !important;
}

[data-testid="stTextInput"] button span,
[data-testid="stTextInput"] button svg,
[data-testid="stTextInput"] button [class*="material"],
[class*="material-symbols"],
[class*="material-icons"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-size: 20px !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased !important;
}

/* ============================================================
   4. FILE UPLOADER
   ============================================================ */
[data-testid="stFileUploader"] span[data-testid*="Icon"],
[data-testid="stFileUploader"] [class*="material"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-size: 22px !important;
    line-height: 1 !important;
    display: inline-block !important;
}

[data-testid="stFileUploader"] section button {
    background: var(--bg-card-elevated) !important;
    border: 1px solid var(--border-contrast) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] section button:hover {
    background: var(--primary-solid) !important;
    border-color: var(--primary-solid) !important;
}

/* ============================================================
   5. FONDO SÓLIDO Y LIMPIO (SIN DEGRADADOS LAVADOS)
   ============================================================ */
.stApp {
    background-color: var(--bg-canvas) !important;
    background-image: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ============================================================
   6. ANIMACIONES SUAVES
   ============================================================ */
@keyframes fadeUp {
    0% {
        opacity: 0;
        transform: translateY(14px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-up-1 { animation: fadeUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.fade-up-2 { animation: fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.fade-up-3 { animation: fadeUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

/* ============================================================
   7. TARJETAS SÓLIDAS DE ALTO CONTRASTE (ADIÓS GLASSMORPHISM)
   ============================================================ */
.solid-card, .glass-card {
    background: var(--bg-card) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: 1px solid var(--border-contrast) !important;
    border-radius: var(--radius-lg) !important;
    padding: 24px !important;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5) !important;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.solid-card::before, .glass-card::before {
    display: none !important;
}

.solid-card:hover, .glass-card:hover {
    transform: translateY(-2px) !important;
    border-color: var(--border-bright) !important;
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.65) !important;
}

/* Tarjeta de Diagnóstico Crítico (ROJO SÓLIDO ALTO CONTRASTE) */
.card-critique-red {
    background: #181216 !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: 1px solid #7f1d1d !important;
    border-left: 4px solid #ef4444 !important;
    border-radius: var(--radius-lg) !important;
    padding: 24px !important;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5) !important;
    position: relative !important;
    overflow: hidden !important;
    margin-bottom: 20px !important;
}

.card-critique-red::before {
    display: none !important;
}

/* Tarjeta de Diagnóstico Optimizado (VERDE SÓLIDO ALTO CONTRASTE) */
.card-optimized-green {
    background: #0d1a16 !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: 1px solid #065f46 !important;
    border-left: 4px solid #10b981 !important;
    border-radius: var(--radius-lg) !important;
    padding: 24px !important;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5) !important;
    position: relative !important;
    overflow: hidden !important;
    margin-bottom: 20px !important;
}

.card-optimized-green::before {
    display: none !important;
}

/* ============================================================
   8. BADGES Y PILLS SÓLIDOS
   ============================================================ */
.badge-devops {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: #1e293b;
    border: 1px solid #334155;
    color: #93c5fd;
}

.badge-cloud {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: #1e293b;
    border: 1px solid #334155;
    color: #38bdf8;
}

.badge-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    background: #1e293b;
    border: 1px solid #334155;
    color: #6ee7b7;
}

.badge-status::before {
    content: '';
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
}

.badge-red {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    background: #1e293b;
    border: 1px solid #7f1d1d;
    color: #fca5a5;
}

/* ============================================================
   9. VENTANA TERMINAL MACOS
   ============================================================ */
.terminal-header {
    background: var(--bg-card);
    padding: 12px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid var(--border-contrast);
    border-bottom: none;
}

.terminal-dots {
    display: flex;
    gap: 7px;
}

.terminal-dots span {
    width: 11px;
    height: 11px;
    border-radius: 50%;
}
.dot-red { background: #ef4444; }
.dot-yellow { background: #f59e0b; }
.dot-green { background: #10b981; }

/* ============================================================
   10. BOTONES E INPUTS DE STREAMLIT (SÓLIDOS DE ALTO CONTRASTE)
   ============================================================ */
.stButton button[kind="primary"], .stButton button[data-testid="baseButton-primary"] {
    background: var(--primary-solid) !important;
    border: 1px solid var(--primary-solid) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    transition: all 0.2s ease !important;
}

.stButton button[kind="primary"]:hover, .stButton button[data-testid="baseButton-primary"]:hover {
    background: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5) !important;
}

.stButton button[kind="secondary"], .stButton button[data-testid="baseButton-secondary"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-contrast) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton button[kind="secondary"]:hover, .stButton button[data-testid="baseButton-secondary"]:hover {
    background: var(--bg-card-elevated) !important;
    border-color: var(--border-bright) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

.stTextInput input, .stTextArea textarea {
    background: var(--bg-canvas) !important;
    border: 1px solid var(--border-contrast) !important;
    border-radius: var(--radius-md) !important;
    color: #ffffff !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary-solid) !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.35) !important;
}

/* ============================================================
   11. BARRA DE PROGRESO CON OCTOCAT MÓVIL
   ============================================================ */
.grit-progress-track, .progress-track {
    width: 100%;
    height: 12px;
    background: var(--bg-card-elevated);
    border: 1px solid var(--border-contrast);
    border-radius: 999px;
    position: relative;
    overflow: visible;
    margin: 18px 0;
}

.grit-progress-fill, .progress-fill {
    height: 100%;
    background: var(--primary-solid);
    border-radius: 999px;
    transition: width 0.15s ease;
}

.grit-github-runner, .progress-icon {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 34px;
    height: 34px;
    background: var(--bg-card);
    border: 2px solid var(--primary-light);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    color: #ffffff;
    transition: left 0.1s ease;
    z-index: 10;
}

/* Chat Bubbles (Sólidas y de Alto Contraste) */
.chat-bubble-user {
    background: var(--bg-card-elevated);
    border: 1px solid var(--border-contrast);
    border-radius: 14px 14px 4px 14px;
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 82%;
    margin-left: auto;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}

.chat-bubble-ai {
    background: var(--bg-card);
    border: 1px solid var(--border-contrast);
    border-radius: 14px 14px 14px 4px;
    padding: 16px 20px;
    margin: 10px 0;
    max-width: 88%;
    margin-right: auto;
    color: var(--text-body);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    line-height: 1.6;
}

/* ============================================================
   12. TABS DE NAVEGACIÓN FULL-WIDTH (DOCK SÓLIDO DE ALTO CONTRASTE)
   ============================================================ */
[data-testid="stTabs"],
.stTabs {
    width: 100% !important;
    margin-bottom: 30px !important;
}

/* Dock contenedor exterior */
[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-testid="stTabs"] [role="tablist"],
[data-baseweb="tab-list"],
div[role="tablist"] {
    display: flex !important;
    width: 100% !important;
    gap: 12px !important;
    background: var(--bg-card) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 8px 10px !important;
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--border-contrast) !important;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5) !important;
    align-items: center !important;
    justify-content: space-between !important;
}

/* Todas las pestañas base */
[data-testid="stTabs"] [role="tab"],
[data-testid="stTabs"] div[role="tab"],
[data-testid="stTabs"] button[role="tab"],
[data-testid="stTabs"] [data-baseweb="tab"],
div[role="tab"],
button[role="tab"],
[role="tab"] {
    flex: 1 1 0% !important;
    min-height: 52px !important;
    height: auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.02em !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--bg-card-subtle) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    white-space: nowrap !important;
    box-sizing: border-box !important;
    outline: none !important;
    overflow: visible !important;
}

/* Contenido textual dentro de la pestaña */
[data-testid="stTabs"] [role="tab"] *,
div[role="tab"] *,
button[role="tab"] *,
[role="tab"] * {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.98rem !important;
    line-height: 1.3 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Pestaña inactiva */
[data-testid="stTabs"] [role="tab"]:not([aria-selected="true"]),
div[role="tab"]:not([aria-selected="true"]),
button[role="tab"]:not([aria-selected="true"]) {
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--bg-card-subtle) !important;
}

/* Efecto hover */
[data-testid="stTabs"] [role="tab"]:hover,
[data-testid="stTabs"] div[role="tab"]:hover,
[data-testid="stTabs"] button[role="tab"]:hover,
div[role="tab"]:hover,
button[role="tab"]:hover,
[role="tab"]:hover {
    color: #ffffff !important;
    background: var(--bg-card-elevated) !important;
    border-color: var(--border-bright) !important;
    transform: translateY(-1px) !important;
}

/* Pestaña activa seleccionada: Color primario sólido de alta visibilidad */
[data-testid="stTabs"] [role="tab"][aria-selected="true"],
[data-testid="stTabs"] div[role="tab"][aria-selected="true"],
[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
div[role="tab"][aria-selected="true"],
button[role="tab"][aria-selected="true"],
[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    font-weight: 700 !important;
    background: var(--primary-solid) !important;
    border: 1px solid var(--primary-solid) !important;
    border-bottom: 1px solid var(--primary-solid) !important;
    border-bottom-color: var(--primary-solid) !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* Quitar pseudo-elementos */
[data-testid="stTabs"] [role="tab"]::before,
[data-testid="stTabs"] [role="tab"]::after,
div[role="tab"]::before,
div[role="tab"]::after {
    display: none !important;
    content: none !important;
}

/* ELIMINAR COMPLETAMENTE LA LÍNEA ROJA INFERIOR */
[data-testid="stTabs"] [role="tab"] > div:nth-child(2),
[data-testid="stTabs"] div[role="tab"] > div:nth-child(2),
[role="tab"] > div:nth-child(2),
div[role="tab"] > div:nth-child(2),
[data-testid="stTabs"] [role="tab"] > div:last-child:not(:first-child),
div[role="tab"] > div:last-child:not(:first-child),
[data-baseweb="tab-highlight"],
div[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"],
div[data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] div[style*="background-color: rgb(255, 75, 75)"],
div[data-testid="stTabs"] div[style*="background-color:#ff4b4b"],
div[data-testid="stTabs"] div[style*="rgb(255, 75, 75)"],
div[role="tablist"] ~ div[style*="rgb(255, 75, 75)"],
div[role="tablist"] div[style*="rgb(255, 75, 75)"],
[data-testid="stTabs"] div[class*="highlight"],
[data-testid="stTabs"] hr {
    display: none !important;
    height: 0 !important;
    width: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    background: transparent !important;
    border: none !important;
}

/* ============================================================
   13. HOJA DE ESTILO EJECUTIVA PARA VISTA DEL CURRÍCULUM (CV)
   ============================================================ */
.cv-document-sheet {
    background: var(--bg-card) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: 1px solid var(--border-contrast) !important;
    border-top: none !important;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
    border-bottom-left-radius: 14px !important;
    border-bottom-right-radius: 14px !important;
    padding: 38px 46px !important;
    margin-bottom: 28px !important;
    box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6) !important;
    position: relative !important;
}

.cv-document-sheet h1 {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: unset !important;
    letter-spacing: -0.025em !important;
    margin-bottom: 4px !important;
    line-height: 1.2 !important;
}

.cv-document-sheet > p:first-of-type strong {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--primary-light) !important;
    letter-spacing: 0.03em !important;
    background: transparent !important;
    padding: 0 !important;
    display: inline-block !important;
    margin-bottom: 6px !important;
}

.cv-document-sheet h2,
.cv-document-sheet h3 {
    font-size: 1.12rem !important;
    font-weight: 800 !important;
    color: var(--primary-light) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    border-left: 4px solid var(--primary-solid) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding-left: 12px !important;
    padding-bottom: 8px !important;
    margin-top: 30px !important;
    margin-bottom: 16px !important;
    text-shadow: none !important;
}

.cv-document-sheet h4 {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #f8fafc !important;
    margin-top: 22px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.cv-document-sheet p,
.cv-document-sheet li,
.cv-document-sheet span {
    font-size: 0.94rem !important;
    line-height: 1.72 !important;
    color: #ffffff !important;
}

.cv-document-sheet ul {
    margin-top: 8px !important;
    margin-bottom: 20px !important;
    padding-left: 20px !important;
}

.cv-document-sheet li {
    margin-bottom: 8px !important;
}

.cv-document-sheet strong {
    color: #ffffff !important;
    font-weight: 700 !important;
    background: rgba(37, 99, 235, 0.12) !important;
    padding: 1px 6px !important;
    border-radius: 4px !important;
    border: 1px solid rgba(37, 99, 235, 0.25) !important;
}

.cv-document-sheet hr {
    border: none !important;
    height: 1px !important;
    background: var(--border-contrast) !important;
    margin: 24px 0 !important;
}

.cv-document-sheet a {
    color: var(--primary-light) !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    border-bottom: 1px dotted rgba(59, 130, 246, 0.6) !important;
    transition: all 0.2s ease !important;
}

.cv-document-sheet a:hover {
    color: #93c5fd !important;
    border-bottom-color: #93c5fd !important;
}

/* ============================================================
   15. ESTILOS DEDICADOS PARA README STUDIO
   ============================================================ */
.readme-viewer-sheet,
.readme-markdown-body {
    background: var(--bg-card) !important;
    color: #ffffff !important;
}

.readme-markdown-body h1,
.readme-markdown-body h2,
.readme-markdown-body h3,
.readme-markdown-body h4 {
    color: #ffffff !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
}

.readme-markdown-body p,
.readme-markdown-body li,
.readme-markdown-body span,
.readme-markdown-body div {
    font-size: 0.94rem !important;
    line-height: 1.72 !important;
    color: #ffffff !important;
}

.readme-markdown-body strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.readme-markdown-body hr {
    border: none !important;
    height: 1px !important;
    background: var(--border-contrast) !important;
    margin: 24px 0 !important;
}

.readme-markdown-body a {
    color: var(--primary-light) !important;
    text-decoration: none !important;
    font-weight: 600 !important;
}

.readme-markdown-body a:hover {
    color: #93c5fd !important;
    text-decoration: underline !important;
}

</style>
"""


def aplicar_estilos(st):
    """Inyecta la hoja de estilos global en la sesión de Streamlit."""
    st.markdown(CSS_PRINCIPAL, unsafe_allow_html=True)
