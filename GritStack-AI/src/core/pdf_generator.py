"""
Generador de Currículum Vitae en formato PDF profesional de alta fidelidad.
Convierte el CV optimizado en Markdown a un documento PDF ejecutivo y compatible con ATS usando fpdf2.
"""

import os
import re
from fpdf import FPDF

class ModernCVPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(16, 16, 16)
        
        # Carga de fuentes TrueType de Windows si están disponibles
        font_dir = "C:/Windows/Fonts"
        arial = os.path.join(font_dir, "arial.ttf")
        arial_bd = os.path.join(font_dir, "arialbd.ttf")
        arial_it = os.path.join(font_dir, "ariali.ttf")
        
        if os.path.exists(arial):
            self.add_font("Arial", "", arial)
            self.add_font("Arial", "B", arial_bd)
            self.add_font("Arial", "I", arial_it)
            self.font_family_name = "Arial"
        else:
            self.font_family_name = "Helvetica"

    def clean_text(self, text: str) -> str:
        """Limpia emojis y caracteres incompatibles con fuentes TrueType estándar."""
        if not text:
            return ""
            
        reemplazos = {
            '🚀': '', '🛠️': '', '🎯': '', '💼': '', '🌐': '', '📍': '', '✅': '', '❌': '', '⚠️': '',
            '✨': '', '🎙️': '', '🐳': '', '⚙️': '', '📊': '', '📫': '', '👋': '', '💡': '', '🔥': '',
            '☁️': '', '⚡': '', '💻': '', '🔧': '', '🔍': '', '📄': '', '✓': 'v', '•': '-'
        }
        for k, v in reemplazos.items():
            text = text.replace(k, v)
            
        # Eliminar emojis y caracteres suplementarios Unicode
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        return text.strip()

    def footer(self):
        """Pie de página elegante y discreto."""
        self.set_y(-12)
        self.set_font(self.font_family_name, "I", 7.5)
        self.set_text_color(148, 163, 184) # Slate 400
        self.cell(0, 8, f"Currículum Vitae Optimizado • GritStack AI | Página {self.page_no()}", align="C")

def generar_pdf_cv(cv_markdown: str) -> bytes:
    """
    Parsea el contenido Markdown del currículum vitae y genera un PDF ejecutivo en memoria.
    
    Args:
        cv_markdown (str): Texto en Markdown del CV.
        
    Returns:
        bytes: Archivo PDF listo para descargar.
    """
    if not cv_markdown or not cv_markdown.strip():
        cv_markdown = "# Currículum Vitae\n**Cloud & DevOps Engineer**\nNo se proporcionó contenido."
        
    pdf = ModernCVPDF()
    pdf.add_page()
    
    lineas = cv_markdown.split("\n")
    i = 0
    en_cabecera = True
    
    while i < len(lineas):
        linea = lineas[i].strip()
        i += 1
        
        if not linea:
            continue
            
        # 1. Línea divisoria horizontal (--- o ***)
        if linea.startswith("---") or linea.startswith("***"):
            pdf.ln(1.5)
            pdf.set_draw_color(226, 232, 240) # Slate 200
            pdf.set_line_width(0.3)
            pdf.line(16, pdf.get_y(), 210 - 16, pdf.get_y())
            pdf.ln(2.5)
            continue
            
        # 2. Nombre completo (# Título)
        if linea.startswith("# "):
            nombre = pdf.clean_text(linea.replace("# ", ""))
            pdf.set_font(pdf.font_family_name, "B", 18)
            pdf.set_text_color(15, 23, 42) # Slate 900
            pdf.cell(0, 7.5, nombre, new_x="LMARGIN", new_y="NEXT")
            en_cabecera = True
            continue
            
        # 3. Subtítulo / Especialidad en cabecera (**Especialidad**)
        if en_cabecera and (linea.startswith("**") and linea.endswith("**")):
            headline = pdf.clean_text(linea.replace("**", ""))
            pdf.set_font(pdf.font_family_name, "B", 10.5)
            pdf.set_text_color(14, 116, 144) # Cyan 700
            pdf.cell(0, 5.5, headline, new_x="LMARGIN", new_y="NEXT")
            continue
            
        # 4. Datos de contacto en cabecera
        if en_cabecera and ("GitHub" in linea or "LinkedIn" in linea or "España" in linea or "@" in linea or "📍" in linea):
            # Formatear enlaces markdown: [Texto](URL) -> Texto: URL
            contacto = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', linea)
            contacto = pdf.clean_text(contacto)
            pdf.set_font(pdf.font_family_name, "", 8.5)
            pdf.set_text_color(100, 116, 139) # Slate 500
            pdf.cell(0, 4.5, contacto, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            en_cabecera = False
            continue
            
        # 5. Encabezado de Sección (## o ###)
        if linea.startswith("## ") or linea.startswith("### "):
            en_cabecera = False
            seccion = pdf.clean_text(re.sub(r'^#+\s*', '', linea))
            pdf.ln(2.5)
            # Fondo de sección elegante
            pdf.set_fill_color(241, 245, 249) # Slate 100
            pdf.set_font(pdf.font_family_name, "B", 10.5)
            pdf.set_text_color(30, 41, 59) # Slate 800
            pdf.cell(0, 6.0, f"  {seccion.upper()}", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1.5)
            continue
            
        # 6. Subsección (#### Nombre del Proyecto o Puesto)
        if linea.startswith("#### "):
            subsec = pdf.clean_text(linea.replace("#### ", ""))
            pdf.ln(1.5)
            pdf.set_font(pdf.font_family_name, "B", 9.5)
            pdf.set_text_color(15, 23, 42) # Slate 900
            pdf.cell(0, 5.0, subsec, new_x="LMARGIN", new_y="NEXT")
            continue
            
        # 7. Línea de Repositorio o Link (*Repositorio:* [URL])
        if linea.startswith("*Repositorio:*") or linea.startswith("*Link:*") or linea.startswith("*GitHub:*"):
            repo_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\2', linea)
            repo_text = pdf.clean_text(repo_text.replace("*", ""))
            pdf.set_font(pdf.font_family_name, "I", 8.2)
            pdf.set_text_color(14, 116, 144) # Cyan 700
            pdf.cell(0, 4.0, repo_text, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.8)
            continue
            
        # 8. Viñetas / Bullets (- o *)
        if linea.startswith("- ") or linea.startswith("* "):
            bullet_raw = re.sub(r'^[-*]\s*', '', linea)
            match_bold = re.match(r'^\*\*(.*?)\*\*(.*)', bullet_raw)
            pdf.set_text_color(51, 65, 85) # Slate 700
            
            # Sangría y viñeta
            pdf.set_left_margin(21)
            pdf.set_x(16)
            pdf.set_font(pdf.font_family_name, "", 8.5)
            pdf.cell(5, 4.4, "\u2022", new_x="RIGHT")
            
            if match_bold:
                bold_part = pdf.clean_text(match_bold.group(1))
                rest_part = pdf.clean_text(match_bold.group(2)).replace("**", "")
                texto_completo = f"{bold_part}: {rest_part}" if not rest_part.startswith(":") else f"{bold_part}{rest_part}"
                pdf.set_font(pdf.font_family_name, "", 8.8)
                pdf.multi_cell(0, 4.4, texto_completo, new_x="LMARGIN", new_y="NEXT")
            else:
                texto_limpio = pdf.clean_text(bullet_raw).replace("**", "")
                pdf.set_font(pdf.font_family_name, "", 8.8)
                pdf.multi_cell(0, 4.4, texto_limpio, new_x="LMARGIN", new_y="NEXT")
                
            pdf.set_left_margin(16)
            pdf.ln(0.5)
            continue
            
        # 9. Párrafo general descriptivo
        texto_p = pdf.clean_text(linea).replace("**", "")
        pdf.set_font(pdf.font_family_name, "", 8.8)
        pdf.set_text_color(51, 65, 85) # Slate 700
        pdf.multi_cell(0, 4.5, texto_p, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        
    return bytes(pdf.output())
