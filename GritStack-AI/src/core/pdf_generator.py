"""
Generador de Currículum Vitae en formato PDF profesional de alta fidelidad.
Convierte el CV optimizado en Markdown a un documento PDF ejecutivo moderno,
altamente estructurado y compatible con sistemas ATS usando fpdf2.
"""

import os
import re
from fpdf import FPDF

class ModernCVPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(16, 14, 16)
        
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
        """Limpia emojis y caracteres suplementarios manteniendo caracteres latinos y puntuación."""
        if not text:
            return ""
            
        reemplazos = {
            '🚀': '', '🛠️': '', '🎯': '', '💼': '', '🌐': '', '📍': '', '✅': '', '❌': '', '⚠️': '',
            '✨': '', '🎙️': '', '🐳': '', '⚙️': '', '📊': '', '📫': '', '👋': '', '💡': '', '🔥': '',
            '☁️': '', '⚡': '', '💻': '', '🔧': '', '🔍': '', '📄': '', '🎓': '', '✓': 'v', '•': '-'
        }
        for k, v in reemplazos.items():
            text = text.replace(k, v)
            
        # Eliminar emojis suplementarios Unicode
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        return text.strip()

    def draw_section_heading(self, title: str):
        """Dibuja un encabezado de sección ejecutivo con acento lateral y línea divisoria."""
        self.ln(3.5)
        curr_y = self.get_y()
        
        # Barra de acento vertical izquierda (Primary Cyan/Blue)
        self.set_fill_color(2, 132, 199) # Sky 600
        self.rect(16, curr_y + 0.5, 3.2, 5.0, style='F')
        
        # Texto de la sección
        self.set_x(21)
        self.set_font(self.font_family_name, "B", 10.5)
        self.set_text_color(15, 23, 42) # Slate 900
        self.cell(0, 6.0, title.upper(), new_x="LMARGIN", new_y="NEXT")
        
        # Línea divisoria horizontal sutil
        line_y = self.get_y() + 0.5
        self.set_draw_color(226, 232, 240) # Slate 200
        self.set_line_width(0.3)
        self.line(16, line_y, 210 - 16, line_y)
        self.ln(2.5)

    def footer(self):
        """Pie de página elegante con numeración y marca discreta."""
        self.set_y(-11)
        self.set_font(self.font_family_name, "I", 7.5)
        self.set_text_color(148, 163, 184) # Slate 400
        self.cell(0, 6, f"GritStack AI • Executive Portfolio & ATS Optimized CV | Página {self.page_no()}", align="C")

def generar_pdf_cv(cv_markdown: str) -> bytes:
    """
    Parsea el contenido Markdown del currículum vitae y genera un PDF ejecutivo en memoria.
    
    Args:
        cv_markdown (str): Texto en Markdown del CV.
        
    Returns:
        bytes: Archivo PDF compilado listo para descargar.
    """
    if not cv_markdown or not cv_markdown.strip():
        cv_markdown = "# Currículum Vitae\n**Software Engineer**\nNo se proporcionó contenido."
        
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
            pdf.ln(1)
            pdf.set_draw_color(226, 232, 240)
            pdf.set_line_width(0.3)
            pdf.line(16, pdf.get_y(), 210 - 16, pdf.get_y())
            pdf.ln(2)
            continue
            
        # 2. Nombre del candidato (# Título)
        if linea.startswith("# "):
            nombre = pdf.clean_text(linea.replace("# ", ""))
            pdf.set_font(pdf.font_family_name, "B", 18.5)
            pdf.set_text_color(15, 23, 42) # Slate 900
            pdf.cell(0, 8.0, nombre, new_x="LMARGIN", new_y="NEXT")
            en_cabecera = True
            continue
            
        # 3. Subtítulo / Rol objetivo (**Headline**)
        if en_cabecera and (linea.startswith("**") and linea.endswith("**")):
            headline = pdf.clean_text(linea.replace("**", ""))
            pdf.set_font(pdf.font_family_name, "B", 10.5)
            pdf.set_text_color(2, 132, 199) # Sky 600
            pdf.cell(0, 5.5, headline, new_x="LMARGIN", new_y="NEXT")
            continue
            
        # 4. Datos de contacto y redes en cabecera
        if en_cabecera and any(k in linea for k in ["GitHub", "LinkedIn", "España", "Spain", "@", "📍", "🌐", "💼"]):
            # Extraer enlaces
            contacto_limpio = pdf.clean_text(re.sub(r'\[(.*?)\]\((.*?)\)', r'\1: \2', linea))
            pdf.set_font(pdf.font_family_name, "", 8.3)
            pdf.set_text_color(100, 116, 139) # Slate 500
            pdf.cell(0, 4.5, contacto_limpio, new_x="LMARGIN", new_y="NEXT")
            
            # Barra divisoria superior con acento
            pdf.ln(1.5)
            pdf.set_draw_color(2, 132, 199)
            pdf.set_line_width(0.8)
            pdf.line(16, pdf.get_y(), 210 - 16, pdf.get_y())
            pdf.ln(2.0)
            en_cabecera = False
            continue
            
        # 5. Encabezado de Sección (## o ###)
        if linea.startswith("## ") or linea.startswith("### "):
            en_cabecera = False
            seccion = pdf.clean_text(re.sub(r'^#+\s*', '', linea))
            pdf.draw_section_heading(seccion)
            continue
            
        # 6. Subsección (#### Proyecto o Cargo)
        if linea.startswith("#### "):
            subsec_raw = linea.replace("#### ", "")
            # Detectar enlace: [Nombre](URL) o 1. [Nombre](URL)
            match_link = re.search(r'\[(.*?)\]\((.*?)\)', subsec_raw)
            if match_link:
                title_link = pdf.clean_text(match_link.group(1))
                url_link = match_link.group(2).strip()
                prefix = pdf.clean_text(subsec_raw[:match_link.start()])
                full_title = f"{prefix} {title_link}".strip()
                
                pdf.ln(1.8)
                pdf.set_font(pdf.font_family_name, "B", 9.8)
                pdf.set_text_color(15, 23, 42)
                pdf.cell(0, 5.0, full_title, new_x="LMARGIN", new_y="NEXT")
                
                # Renderizar URL pequeña clicable
                pdf.set_font(pdf.font_family_name, "I", 8.0)
                pdf.set_text_color(2, 132, 199)
                pdf.cell(0, 3.8, f"Repo: {url_link}", link=url_link, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(0.5)
            else:
                subsec = pdf.clean_text(subsec_raw)
                pdf.ln(1.8)
                pdf.set_font(pdf.font_family_name, "B", 9.8)
                pdf.set_text_color(15, 23, 42)
                pdf.cell(0, 5.0, subsec, new_x="LMARGIN", new_y="NEXT")
            continue
            
        # 7. Línea de Repositorio o Link (*Repositorio:* [URL])
        if linea.startswith("*Repositorio:*") or linea.startswith("*Link:*") or linea.startswith("*GitHub:*"):
            match_r = re.search(r'\((.*?)\)', linea)
            url_r = match_r.group(1).strip() if match_r else ""
            repo_text = pdf.clean_text(re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', linea).replace("*", ""))
            pdf.set_font(pdf.font_family_name, "I", 8.0)
            pdf.set_text_color(2, 132, 199)
            pdf.cell(0, 4.0, repo_text, link=url_r if url_r else None, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.5)
            continue
            
        # 8. Viñetas / Bullets (- o *)
        if linea.startswith("- ") or linea.startswith("* "):
            bullet_raw = re.sub(r'^[-*]\s*', '', linea)
            
            # Detectar formato bold inicial: - **Categoría:** contenido
            match_bold = re.match(r'^\*\*(.*?)\*\*(.*)', bullet_raw)
            
            pdf.set_left_margin(21)
            pdf.set_x(16)
            
            # Icono viñeta estilizado
            pdf.set_font(pdf.font_family_name, "B", 9.0)
            pdf.set_text_color(2, 132, 199) # Sky 600
            pdf.cell(5, 4.3, "-", new_x="RIGHT")
            
            pdf.set_text_color(51, 65, 85) # Slate 700
            if match_bold:
                bold_part = pdf.clean_text(match_bold.group(1))
                rest_part = pdf.clean_text(match_bold.group(2)).replace("**", "")
                texto_linea = f"{bold_part}: {rest_part}" if not rest_part.startswith(":") else f"{bold_part}{rest_part}"
                
                pdf.set_font(pdf.font_family_name, "", 8.6)
                pdf.multi_cell(0, 4.3, texto_linea, new_x="LMARGIN", new_y="NEXT")
            else:
                texto_limpio = pdf.clean_text(bullet_raw).replace("**", "")
                pdf.set_font(pdf.font_family_name, "", 8.6)
                pdf.multi_cell(0, 4.3, texto_limpio, new_x="LMARGIN", new_y="NEXT")
                
            pdf.set_left_margin(16)
            pdf.ln(0.4)
            continue
            
        # 9. Párrafo general descriptivo (Perfil profesional, etc.)
        texto_p = pdf.clean_text(linea).replace("**", "")
        pdf.set_font(pdf.font_family_name, "", 8.8)
        pdf.set_text_color(51, 65, 85) # Slate 700
        pdf.multi_cell(0, 4.5, texto_p, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.0)
        
    return bytes(pdf.output())
