"""
Servicio de Extracción de Texto de Archivos PDF (Curriculum Vitae).
Utiliza PyPDF2 para procesamiento en memoria sin dependencias externas pesadas.
"""

import io
from PyPDF2 import PdfReader

def extraer_texto_pdf(archivo_bytes) -> str:
    """
    Extrae el texto plano de un archivo PDF subido a través de Streamlit.
    
    Args:
        archivo_bytes: Archivo o BytesIO de Streamlit (st.file_uploader)
        
    Returns:
        str: Texto extraído limpio del documento.
    """
    if not archivo_bytes:
        return ""
        
    try:
        # Asegurar puntero al inicio
        if hasattr(archivo_bytes, "seek"):
            archivo_bytes.seek(0)
            
        reader = PdfReader(archivo_bytes)
        paginas_texto = []
        
        for idx, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            if texto:
                paginas_texto.append(texto.strip())
                
        texto_completo = "\n\n".join(paginas_texto)
        return texto_completo.strip()
    except Exception as e:
        print(f"[Error PyPDF2] No se pudo procesar el PDF: {e}")
        return ""
