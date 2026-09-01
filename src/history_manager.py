"""
history_manager.py - Gestión del historial de copias de seguridad.
Guarda y lee registros de cada backup realizado con fecha, estado,
cantidad de archivos y tamaño.
"""

import json
import os
from datetime import datetime
from src.config_manager import CONFIG_DIR

HISTORY_FILE = os.path.join(CONFIG_DIR, "history.json")


def load_history():
    """Carga el historial de backups desde history.json."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history):
    """Guarda el historial completo en history.json."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def add_entry(status, source_folders, destination, files_copied=0, 
              files_skipped=0, bytes_copied=0, duration_seconds=0, errors=None, destination_name=""):
    """
    Añade una nueva entrada al historial de backups.
    
    Args:
        status: "success", "partial", "error", "cancelled"
        source_folders: lista de carpetas origen
        destination: ruta destino
        files_copied: número de archivos copiados
        files_skipped: número de archivos omitidos (ya existían)
        bytes_copied: bytes totales copiados
        duration_seconds: duración del backup en segundos
        errors: lista de errores (si los hay)
    """
    history = load_history()
    
    entry = {
        "id": len(history) + 1,
        "timestamp": datetime.now().isoformat(),
        "date_display": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": status,
        "source_folders": source_folders,
        "destination": destination,
        "destination_name": destination_name,
        "files_copied": files_copied,
        "files_skipped": files_skipped,
        "bytes_copied": bytes_copied,
        "size_display": _format_bytes(bytes_copied),
        "duration_seconds": duration_seconds,
        "duration_display": _format_duration(duration_seconds),
        "errors": errors or []
    }
    
    history.insert(0, entry)  # Más reciente primero
    
    # Mantener máximo 100 entradas
    if len(history) > 100:
        history = history[:100]
    
    save_history(history)
    return entry


def get_last_backup():
    """Devuelve la información del último backup realizado."""
    history = load_history()
    if history:
        return history[0]
    return None


def get_stats():
    """Devuelve estadísticas generales del historial."""
    history = load_history()
    
    if not history:
        return {
            "total_backups": 0,
            "successful": 0,
            "failed": 0,
            "total_bytes": 0,
            "total_files": 0,
            "last_backup": None
        }
    
    successful = sum(1 for h in history if h.get("status") == "success")
    failed = sum(1 for h in history if h.get("status") == "error")
    total_bytes = sum(h.get("bytes_copied", 0) for h in history)
    total_files = sum(h.get("files_copied", 0) for h in history)
    
    return {
        "total_backups": len(history),
        "successful": successful,
        "failed": failed,
        "total_bytes": total_bytes,
        "total_bytes_display": _format_bytes(total_bytes),
        "total_files": total_files,
        "last_backup": history[0].get("date_display", "Nunca")
    }


def clear_history():
    """Borra todo el historial."""
    save_history([])


def _format_bytes(size_bytes):
    """Convierte bytes a formato legible (KB, MB, GB)."""
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.1f} {units[i]}"


def _format_duration(seconds):
    """Convierte segundos a formato legible."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
