"""
config_manager.py - Gestión de configuración del programa.
Lee y escribe config.json con las preferencias del usuario:
rutas de origen, destino, horarios de recordatorio, y datos del SSD.
"""

import json
import os
import sys

def get_app_data_dir():
    """Devuelve la carpeta de datos de la aplicación (AppData/Local)."""
    app_data = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "DarkPassengerBackup")
    os.makedirs(app_data, exist_ok=True)
    return app_data

def get_base_dir():
    """Devuelve el directorio base del ejecutable o script."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = get_app_data_dir()
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "source_folders": [],
    "destination_path": "",
    "ssd_volume_serial": "",
    "ssd_volume_label": "",
    "ssd_drive_letter": "",
    "schedule": {
        "enabled": True,
        "day": "Sunday",
        "hour": 12,
        "minute": 0
    },
    "reminder": {
        "enabled": True,
        "day": "Sunday",
        "hour": 12,
        "minute": 0
    },
    "robocopy_flags": "/MIR /FFT /Z /XA:H /W:5 /R:3",
    "auto_start_with_windows": False,
    "show_popup_on_ssd_connect": True,
    "last_backup_date": None,
    "theme": "dark"
}


def load_config():
    """Carga la configuración desde config.json. Si no existe, crea uno con valores por defecto."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Merge con defaults para que si hay campos nuevos, se añadan
        merged = DEFAULT_CONFIG.copy()
        _deep_merge(merged, config)
        return merged
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Guarda la configuración en config.json."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def _deep_merge(base, override):
    """Merge recursivo de diccionarios. Override tiene prioridad."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def add_source_folder(folder_path):
    """Añade una carpeta de origen a la configuración."""
    config = load_config()
    if folder_path not in config["source_folders"]:
        config["source_folders"].append(folder_path)
        save_config(config)
    return config


def remove_source_folder(folder_path):
    """Elimina una carpeta de origen de la configuración."""
    config = load_config()
    if folder_path in config["source_folders"]:
        config["source_folders"].remove(folder_path)
        save_config(config)
    return config


def set_destination(dest_path):
    """Establece la ruta de destino (en el SSD)."""
    config = load_config()
    config["destination_path"] = dest_path
    save_config(config)
    return config


def set_ssd_info(volume_serial, volume_label, drive_letter):
    """Guarda la información identificativa del SSD."""
    config = load_config()
    config["ssd_volume_serial"] = volume_serial
    config["ssd_volume_label"] = volume_label
    config["ssd_drive_letter"] = drive_letter
    save_config(config)
    return config


def update_last_backup():
    """Actualiza la fecha del último backup."""
    from datetime import datetime
    config = load_config()
    config["last_backup_date"] = datetime.now().isoformat()
    save_config(config)
    return config
