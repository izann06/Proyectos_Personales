"""
Módulo de Estilos y Sistema de Diseño Visual para GritStack AI
Estética: Dark Mode Inmersivo (#0b0f19) + Glassmorphism + React Bits Hover Glow
Acentos: Morado Neón (#a855f7 / #8b5cf6) y Azul Eléctrico (#38bdf8 / #6366f1)
"""

CSS_PRINCIPAL = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

:root {
    --bg-dark-void: #070a12;
    --bg-dark-base: #0b0f19;
    --bg-dark-card: rgba(15, 23, 42, 0.65);
    --bg-dark-elevated: rgba(22, 33, 62, 0.55);
    
    /* Acentos vibrantes */
    --accent-purple: #a855f7;
    --accent-purple-glow: rgba(168, 85, 247, 0.35);
    --accent-blue: #38bdf8;
    --accent-blue-glow: rgba(56, 189, 248, 0.35);
    --accent-indigo: #6366f1;
    --accent-emerald: #10b981;
    --accent-red: #ef4444;
    
    /* Gradientes */
    --grad-primary: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #38bdf8 100%);
    --grad-purple: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
    --grad-blue: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
    --grad-card-hover: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(56, 189, 248, 0.08) 100%);
    
    /* Bordes Glassmorphism */
    --border-glass: rgba(255, 255, 255, 0.07);
    --border-glass-bright: rgba(255, 255, 255, 0.16);
    --border-glow-purple: rgba(168, 85, 247, 0.5);
    --border-glow-blue: rgba(56, 189, 248, 0.5);

    /* Textos */
    --text-pure: #ffffff;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;

    /* Radios */
    --radius-xl: 20px;
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
}

/* ============================================================
   1. RESET Y TIPOGRAFÍA CUIDADA (SIN ROMPER FUENTES DE ICONOS)
   ============================================================ */
html, body {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: var(--text-primary);
}

p, div, label, input, textarea {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

h1, h2, h3, h4, h5, h6, .font-heading {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.025em;
}

code, pre, .font-mono {
    font-family: 'JetBrains Mono', monospace !important;
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

/* Enlaces legítimos de contenido dentro de títulos */
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
    color: #38bdf8 !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
}

h1 a:not([href^="#"]):hover, 
h2 a:not([href^="#"]):hover, 
h3 a:not([href^="#"]):hover, 
h4 a:not([href^="#"]):hover {
    color: #c084fc !important;
    text-shadow: 0 0 12px rgba(168, 85, 247, 0.5) !important;
}


/* ============================================================
   3. CORRECCIÓN DEL BOTÓN DE OJO (PASSWORD VISIBILITY)
   ============================================================ */
[data-testid="stTextInput"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    padding: 6px 10px !important;
    margin: auto 4px !important;
    min-width: 38px !important;
    height: 38px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextInput"] button:hover {
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.1) !important;
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
   4. CORRECCIÓN DEL FILE UPLOADER (QUITAR TEXTO SOLAPADO UPLOADPLOAD)
   ============================================================ */
[data-testid="stFileUploader"] span[data-testid*="Icon"],
[data-testid="stFileUploader"] [class*="material"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-size: 22px !important;
    line-height: 1 !important;
    display: inline-block !important;
}

[data-testid="stFileUploader"] section button {
    background: rgba(168, 85, 247, 0.2) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
}

/* ============================================================
   5. FONDO INMERSIVO Y BASE VISUAL
   ============================================================ */
.stApp {
    background-color: var(--bg-dark-base) !important;
    background-image: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15) 0%, transparent 60%),
        radial-gradient(circle at 10% 20%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 60%, rgba(56, 189, 248, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(11, 15, 25, 1) 0%, var(--bg-dark-void) 100%);
    background-attachment: fixed !important;
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
        transform: translateY(18px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-up-1 { animation: fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.fade-up-2 { animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.fade-up-3 { animation: fadeUp 0.75s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

/* ============================================================
   7. CARDS GLASSMORPHISM & REACT BITS HOVER GLOW
   ============================================================ */
.glass-card {
    background: var(--bg-dark-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: 0 12px 36px -12px rgba(0, 0, 0, 0.6);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.25) 50%, transparent 100%);
}

.glass-card:hover {
    transform: translateY(-4px);
    border-color: var(--border-glow-purple);
    box-shadow: 
        0 18px 45px -10px rgba(168, 85, 247, 0.25),
        0 0 0 1px rgba(168, 85, 247, 0.3),
        inset 0 0 20px rgba(168, 85, 247, 0.05);
}

/* Tarjeta de Diagnóstico Crítico (ROJO) */
.card-critique-red {
    background: rgba(239, 68, 68, 0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: 0 12px 36px -12px rgba(239, 68, 68, 0.2);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.card-critique-red::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ef4444, transparent);
}

/* Tarjeta de Diagnóstico Optimizado (VERDE NEÓN) */
.card-optimized-green {
    background: rgba(16, 185, 129, 0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: 0 12px 36px -12px rgba(16, 185, 129, 0.25);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.card-optimized-green::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #10b981, transparent);
}

/* ============================================================
   8. BADGES Y PILLS
   ============================================================ */
.badge-devops {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: rgba(168, 85, 247, 0.12);
    border: 1px solid rgba(168, 85, 247, 0.35);
    color: #e9d5ff;
}

.badge-cloud {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #bae6fd;
}

.badge-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
}

.badge-status::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
}

.badge-red {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
}

/* ============================================================
   9. VENTANA TERMINAL MACOS
   ============================================================ */
.terminal-header {
    background: rgba(15, 23, 42, 0.95);
    padding: 12px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid var(--border-glass-bright);
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
   10. PESTAÑAS, BOTONES E INPUTS DE STREAMLIT
   ============================================================ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    padding: 6px !important;
    gap: 8px !important;
    margin-bottom: 24px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.25s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    box-shadow: 0 4px 18px -4px rgba(168, 85, 247, 0.3) !important;
}

.stButton button[kind="primary"], .stButton button[data-testid="baseButton-primary"] {
    background: var(--grad-primary) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    box-shadow: 0 8px 24px -6px rgba(168, 85, 247, 0.45) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton button[kind="primary"]:hover, .stButton button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px -4px rgba(56, 189, 248, 0.6) !important;
}

.stButton button[kind="secondary"], .stButton button[data-testid="baseButton-secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--border-glass-bright) !important;
    color: #f1f5f9 !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
}

.stButton button[kind="secondary"]:hover, .stButton button[data-testid="baseButton-secondary"]:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent-purple) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

.stTextInput input, .stTextArea textarea {
    background: rgba(10, 15, 28, 0.75) !important;
    border: 1px solid var(--border-glass-bright) !important;
    border-radius: var(--radius-md) !important;
    color: #ffffff !important;
    padding: 12px 16px !important;
    transition: all 0.25s ease !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.25) !important;
}

/* ============================================================
   11. BARRA DE PROGRESO CON OCTOCAT MÓVIL
   ============================================================ */
.grit-progress-track, .progress-track {
    width: 100%;
    height: 14px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid var(--border-glass-bright);
    border-radius: 999px;
    position: relative;
    overflow: visible;
    margin: 18px 0;
}

.grit-progress-fill, .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #38bdf8 100%);
    border-radius: 999px;
    transition: width 0.15s ease;
    box-shadow: 0 0 16px rgba(168, 85, 247, 0.5);
}

.grit-github-runner, .progress-icon {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 36px;
    height: 36px;
    background: #0b0f19;
    border: 2px solid #38bdf8;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.7);
    color: #ffffff;
    transition: left 0.1s ease;
    z-index: 10;
}

/* Chat Bubbles */
.chat-bubble-user {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 82%;
    margin-left: auto;
    color: #ffffff;
    box-shadow: 0 4px 20px -5px rgba(0,0,0,0.4);
}

.chat-bubble-ai {
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass-bright);
    border-radius: 16px 16px 16px 4px;
    padding: 16px 20px;
    margin: 10px 0;
    max-width: 88%;
    margin-right: auto;
    color: #e2e8f0;
    box-shadow: 0 4px 20px -5px rgba(0,0,0,0.4);
    line-height: 1.6;
}

/* ============================================================
   TABS DE NAVEGACIÓN FULL-WIDTH & SIMÉTRICOS (CYBER LUXE)
   ============================================================ */
[data-testid="stTabs"],
.stTabs {
    width: 100% !important;
    margin-bottom: 28px !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-baseweb="tab-list"],
div[role="tablist"] {
    display: flex !important;
    width: 100% !important;
    gap: 14px !important;
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    padding: 8px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6) !important;
    justify-content: space-between !important;
}

[data-testid="stTabs"] [data-baseweb="tab"],
[data-baseweb="tab"],
button[role="tab"] {
    flex: 1 1 0% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    border-radius: 12px !important;
    padding: 14px 22px !important;
    color: #94a3b8 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.96rem !important;
    letter-spacing: 0.03em !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    white-space: nowrap !important;
}

/* Efecto hover distintivo al pasar el cursor */
[data-testid="stTabs"] [data-baseweb="tab"]:hover,
[data-baseweb="tab"]:hover,
button[role="tab"]:hover {
    color: #ffffff !important;
    background: rgba(168, 85, 247, 0.14) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    box-shadow: 0 8px 24px -4px rgba(168, 85, 247, 0.35) !important;
    transform: translateY(-2px) !important;
}

/* Pestaña activa seleccionada */
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
[data-baseweb="tab"][aria-selected="true"],
button[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(168, 85, 247, 0.45) 100%) !important;
    border: 1px solid rgba(168, 85, 247, 0.7) !important;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
    transform: translateY(-1px) !important;
}

/* Quitar la línea roja y el borde por defecto de Streamlit */
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] {
    display: none !important;
}

/* ============================================================
   15. HOJA DE ESTILO EJECUTIVA PARA VISTA DEL CURRÍCULUM (CV)
   ============================================================ */
.cv-document-sheet {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: none !important;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
    border-bottom-left-radius: 16px !important;
    border-bottom-right-radius: 16px !important;
    padding: 36px 42px !important;
    margin-bottom: 28px !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5) !important;
}

.cv-document-sheet h1 {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 6px !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5) !important;
}

.cv-document-sheet h2,
.cv-document-sheet h3 {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #38bdf8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid rgba(56, 189, 248, 0.22) !important;
    padding-bottom: 8px !important;
    margin-top: 28px !important;
    margin-bottom: 14px !important;
}

.cv-document-sheet h4 {
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    margin-top: 20px !important;
    margin-bottom: 6px !important;
}

.cv-document-sheet p,
.cv-document-sheet li {
    font-size: 0.93rem !important;
    line-height: 1.68 !important;
    color: #cbd5e1 !important;
}

.cv-document-sheet ul {
    margin-top: 6px !important;
    margin-bottom: 16px !important;
    padding-left: 20px !important;
}

.cv-document-sheet li {
    margin-bottom: 6px !important;
}

.cv-document-sheet strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.cv-document-sheet hr {
    border: none !important;
    height: 1px !important;
    background: rgba(255, 255, 255, 0.1) !important;
    margin: 22px 0 !important;
}

.cv-document-sheet a {
    color: #38bdf8 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.cv-document-sheet a:hover {
    color: #c084fc !important;
    text-decoration: underline !important;
    text-shadow: 0 0 10px rgba(168, 85, 247, 0.4) !important;
}

</style>
"""


def aplicar_estilos(st):
    """Inyecta la hoja de estilos global en la sesión de Streamlit."""
    st.markdown(CSS_PRINCIPAL, unsafe_allow_html=True)
