"""
startup_watcher.py - Servicio ligero que corre al iniciar Windows.
Monitoriza la conexión del SSD en segundo plano sin abrir ninguna ventana.
Cuando detecta el SSD configurado, lanza la aplicación principal con el popup.
"""

import sys
import os
import time
import subprocess
import ctypes
import ctypes.wintypes
import json
import string

# ── Rutas ──
def get_app_data_dir():
    app_data = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        "DarkPassengerBackup"
    )
    os.makedirs(app_data, exist_ok=True)
    return app_data

CONFIG_FILE = os.path.join(get_app_data_dir(), "config.json")
LOCK_FILE = os.path.join(get_app_data_dir(), "watcher.lock")

# Determinar el directorio base del proyecto
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")


def load_config():
    """Carga la configuración."""
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def get_drive_serial(letter):
    """Obtiene el número de serie de un disco."""
    drive_path = f"{letter}:\\"
    serial_number = ctypes.wintypes.DWORD()
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        drive_path,
        None, 0,
        ctypes.byref(serial_number),
        None, None, None, 0
    )
    if result:
        return str(serial_number.value)
    return None


def is_target_ssd_connected(target_serial):
    """Comprueba si el SSD objetivo está conectado."""
    if not target_serial:
        return False
    
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i, letter in enumerate(string.ascii_uppercase):
        if bitmask & (1 << i):
            serial = get_drive_serial(letter)
            if serial == target_serial:
                return True
    return False


def is_app_running():
    """Comprueba si la aplicación principal ya está corriendo usando su lock file."""
    app_lock = os.path.join(get_app_data_dir(), "app.lock")
    if os.path.exists(app_lock):
        try:
            with open(app_lock, "r") as f:
                pid = int(f.read().strip())
            # Comprobar si el proceso de la app sigue vivo
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'],
                capture_output=True, text=True, timeout=5
            )
            if str(pid) in result.stdout:
                return True
        except Exception:
            pass
    return False


def acquire_lock():
    """Evita que se ejecuten múltiples instancias del watcher."""
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read().strip())
            # Comprobar si el proceso sigue vivo
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'],
                capture_output=True, text=True, timeout=5
            )
            if str(pid) in result.stdout:
                return False  # Ya hay otro watcher corriendo
        except (ValueError, subprocess.TimeoutExpired, OSError):
            pass
    
    # Escribir nuestro PID
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    """Libera el lock file."""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except OSError:
        pass


def launch_app(with_popup=False):
    """Lanza la aplicación principal."""
    python_exe = sys.executable  # pythonw.exe
    
    # Si estamos en pythonw.exe, usarlo para la app también
    if 'pythonw' not in python_exe.lower():
        # Intentar encontrar pythonw.exe
        pythonw = os.path.join(os.path.dirname(python_exe), "pythonw.exe")
        if os.path.exists(pythonw):
            python_exe = pythonw
    
    args = [python_exe, MAIN_SCRIPT]
    if with_popup:
        args.append("--ssd-popup")
    
    try:
        subprocess.Popen(
            args,
            cwd=BASE_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
    except Exception:
        pass


def main():
    """Bucle principal del watcher."""
    # Evitar múltiples instancias
    if not acquire_lock():
        sys.exit(0)
    
    try:
        ssd_was_connected = False
        
        while True:
            config = load_config()
            
            if config and config.get("show_popup_on_ssd_connect", True):
                target_serial = config.get("ssd_volume_serial", "")
                
                if target_serial:
                    ssd_connected = is_target_ssd_connected(target_serial)
                    
                    if ssd_connected and not ssd_was_connected:
                        # SSD acaba de conectarse y la app no está abierta
                        if not is_app_running():
                            launch_app(with_popup=True)
                        ssd_was_connected = True
                    
                    elif not ssd_connected and ssd_was_connected:
                        ssd_was_connected = False
            
            time.sleep(3)
    
    except KeyboardInterrupt:
        pass
    finally:
        release_lock()


if __name__ == "__main__":
    main()
