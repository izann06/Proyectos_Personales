"""
ssd_detector.py - Detección en tiempo real de dispositivos USB/SSD.
Monitoriza la conexión de discos externos y compara con el SSD
configurado del usuario usando el número de serie del volumen.
"""

import subprocess
import string
import ctypes
import threading
import time
import ctypes.wintypes


def get_all_drives():
    """
    Devuelve información de todos los discos conectados al sistema.
    Retorna una lista de diccionarios con: letter, label, serial, type, size.
    """
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    
    for i, letter in enumerate(string.ascii_uppercase):
        if bitmask & (1 << i):
            drive_path = f"{letter}:\\"
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
            
            # 2 = Removable, 3 = Fixed, 5 = CDROM
            if drive_type in (2, 3):
                info = _get_drive_info(letter)
                if info:
                    info["drive_type"] = "Removable" if drive_type == 2 else "Fixed"
                    drives.append(info)
    
    return drives


def _get_drive_info(letter):
    """Obtiene la información detallada de un disco (label, serial, tamaño)."""
    drive_path = f"{letter}:\\"
    
    volume_name_buf = ctypes.create_unicode_buffer(256)
    serial_number = ctypes.wintypes.DWORD()
    max_component = ctypes.wintypes.DWORD()
    file_system_flags = ctypes.wintypes.DWORD()
    file_system_name = ctypes.create_unicode_buffer(256)
    
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        drive_path,
        volume_name_buf, 256,
        ctypes.byref(serial_number),
        ctypes.byref(max_component),
        ctypes.byref(file_system_flags),
        file_system_name, 256
    )
    
    if not result:
        return None
    
    # Obtener espacio en disco
    free_bytes = ctypes.c_ulonglong(0)
    total_bytes = ctypes.c_ulonglong(0)
    total_free_bytes = ctypes.c_ulonglong(0)
    
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        drive_path,
        ctypes.byref(free_bytes),
        ctypes.byref(total_bytes),
        ctypes.byref(total_free_bytes)
    )
    
    return {
        "letter": letter,
        "path": drive_path,
        "label": volume_name_buf.value or "Sin nombre",
        "serial": str(serial_number.value),
        "file_system": file_system_name.value,
        "total_bytes": total_bytes.value,
        "free_bytes": free_bytes.value,
        "total_display": _format_size(total_bytes.value),
        "free_display": _format_size(free_bytes.value)
    }


def get_removable_drives():
    """Devuelve solo los discos extraíbles (USB/SSD externos)."""
    return [d for d in get_all_drives() if d["drive_type"] == "Removable"]


def get_external_drives():
    """
    Devuelve todos los discos que podrían ser un SSD externo.
    Incluye extraíbles y fijos que no sean C: (por si el SSD se reconoce como fijo).
    """
    all_drives = get_all_drives()
    return [d for d in all_drives if d["letter"] != "C"]


def is_target_ssd_connected(config):
    """
    Comprueba si el SSD configurado del usuario está conectado.
    Lo identifica por el número de serie del volumen.
    
    Returns:
        dict con info del disco si está conectado, None si no.
    """
    target_serial = config.get("ssd_volume_serial", "")
    
    if not target_serial:
        return None
    
    for drive in get_all_drives():
        if drive["serial"] == target_serial:
            return drive
    
    return None


class SSDWatcher(threading.Thread):
    """
    Hilo que monitoriza la conexión/desconexión de discos USB en tiempo real.
    Llama a un callback cuando detecta que el SSD objetivo se conecta.
    """
    
    def __init__(self, config, on_ssd_connected=None, on_ssd_disconnected=None, check_interval=3):
        super().__init__(daemon=True)
        self.config = config
        self.on_ssd_connected = on_ssd_connected
        self.on_ssd_disconnected = on_ssd_disconnected
        self.check_interval = check_interval
        self._stop_event = threading.Event()
        self._ssd_was_connected = False
    
    def run(self):
        """Bucle principal de detección."""
        while not self._stop_event.is_set():
            try:
                ssd = is_target_ssd_connected(self.config)
                
                if ssd and not self._ssd_was_connected:
                    # SSD acaba de conectarse
                    self._ssd_was_connected = True
                    if self.on_ssd_connected:
                        self.on_ssd_connected(ssd)
                
                elif not ssd and self._ssd_was_connected:
                    # SSD acaba de desconectarse
                    self._ssd_was_connected = False
                    if self.on_ssd_disconnected:
                        self.on_ssd_disconnected()
                
            except Exception:
                pass  # Evitar que errores paren el watcher
            
            self._stop_event.wait(self.check_interval)
    
    def stop(self):
        """Detiene el watcher."""
        self._stop_event.set()
    
    def update_config(self, config):
        """Actualiza la configuración (ej: si el usuario cambia el SSD objetivo)."""
        self.config = config


def _format_size(size_bytes):
    """Convierte bytes a formato legible."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.1f} {units[i]}"
