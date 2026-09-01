"""
backup_engine.py - Motor de copia de seguridad usando robocopy.
Ejecuta las copias, parsea la salida de robocopy y reporta progreso.
"""

import subprocess
import os
import time
import threading
import re
from datetime import datetime
from src import config_manager, history_manager


class BackupEngine:
    """Motor de copia de seguridad que envuelve robocopy."""
    
    def __init__(self):
        self.is_running = False
        self._cancel_event = threading.Event()
        self._current_process = None
        self._progress_callback = None
        self._status_callback = None
        self._completion_callback = None
    
    def set_callbacks(self, on_progress=None, on_status=None, on_complete=None):
        """
        Configura callbacks para la UI.
        
        on_progress(percent, current_file): Progreso de la copia
        on_status(message): Mensajes de estado
        on_complete(success, entry): Cuando termina el backup
        """
        self._progress_callback = on_progress
        self._status_callback = on_status
        self._completion_callback = on_complete
    
    def start_backup(self, source_folders=None, destination=None, robocopy_flags=None):
        """
        Inicia el backup en un hilo separado.
        Si no se pasan parámetros, usa los de la configuración.
        """
        if self.is_running:
            return False
        
        config = config_manager.load_config()
        
        sources = source_folders or config.get("source_folders", [])
        dest = destination or config.get("destination_path", "")
        flags = robocopy_flags or config.get("robocopy_flags", "/MIR /FFT /Z /XA:H /W:5 /R:3")
        
        if not sources:
            self._emit_status("⚠ No hay carpetas de origen configuradas.")
            return False
        
        if not dest:
            self._emit_status("⚠ No hay ruta de destino configurada.")
            return False
        
        self._cancel_event.clear()
        thread = threading.Thread(
            target=self._run_backup,
            args=(sources, dest, flags),
            daemon=True
        )
        thread.start()
        return True
    
    def cancel_backup(self):
        """Cancela el backup en curso."""
        self._cancel_event.set()
        if self._current_process:
            try:
                self._current_process.terminate()
            except Exception:
                pass
    
    def _run_backup(self, sources, destination, flags):
        """Ejecuta el backup para todas las carpetas de origen."""
        self.is_running = True
        start_time = time.time()
        
        total_files_copied = 0
        total_files_skipped = 0
        total_bytes = 0
        errors = []
        overall_success = True
        
        self._emit_status("🔪 Iniciando protocolo de backup...")
        
        for i, source in enumerate(sources):
            if self._cancel_event.is_set():
                self._emit_status("❌ Backup cancelado por el usuario.")
                overall_success = False
                break
            
            folder_name = os.path.basename(source)
            dest_path = os.path.join(destination, folder_name)
            
            self._emit_status(f"📂 [{i+1}/{len(sources)}] Procesando: {folder_name}")
            self._emit_progress(int((i / len(sources)) * 100), folder_name)
            
            result = self._run_robocopy(source, dest_path, flags)
            
            if result:
                total_files_copied += result.get("files_copied", 0)
                total_files_skipped += result.get("files_skipped", 0)
                total_bytes += result.get("bytes_copied", 0)
                
                if result.get("errors"):
                    errors.extend(result["errors"])
                    overall_success = False
        
        duration = time.time() - start_time
        
        # Determinar estado
        if self._cancel_event.is_set():
            status = "cancelled"
        elif errors and overall_success:
            status = "partial"
        elif overall_success:
            status = "success"
        else:
            status = "error"
        
        # Guardar en historial
        entry = history_manager.add_entry(
            status=status,
            source_folders=sources,
            destination=destination,
            files_copied=total_files_copied,
            files_skipped=total_files_skipped,
            bytes_copied=total_bytes,
            duration_seconds=int(duration),
            errors=errors
        )
        
        if status == "success":
            config_manager.update_last_backup()
            self._emit_status(f"✅ Backup completado. {total_files_copied} archivos copiados en {entry['duration_display']}.")
        elif status == "cancelled":
            self._emit_status("❌ Backup cancelado.")
        else:
            self._emit_status(f"⚠ Backup finalizado con errores. Archivos copiados: {total_files_copied}.")
        
        self._emit_progress(100, "Completado")
        
        self.is_running = False
        
        if self._completion_callback:
            self._completion_callback(status == "success", entry)
    
    def _run_robocopy(self, source, destination, flags):
        """
        Ejecuta robocopy para una carpeta específica y parsea la salida.
        
        Códigos de salida de robocopy:
        0 = No hay cambios
        1 = Archivos copiados
        2 = Archivos extras en destino
        3 = 1+2
        4 = Mismatched files/dirs
        8+ = Error
        """
        # Asegurar que el directorio destino existe
        os.makedirs(destination, exist_ok=True)
        
        cmd = f'robocopy "{source}" "{destination}" {flags} /NP /NFL /NDL /NJH /BYTES'
        
        try:
            self._current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            stdout, stderr = self._current_process.communicate()
            exit_code = self._current_process.returncode
            
            self._current_process = None
            
            result = self._parse_robocopy_output(stdout)
            
            # Robocopy exit codes < 8 son éxito o parcial
            if exit_code >= 8:
                result["errors"] = [f"Robocopy error (exit code {exit_code}): {stderr.strip() or stdout.strip()}"]
            
            return result
            
        except Exception as e:
            self._current_process = None
            return {
                "files_copied": 0,
                "files_skipped": 0,
                "bytes_copied": 0,
                "errors": [str(e)]
            }
    
    def _parse_robocopy_output(self, output):
        """Parsea la salida de robocopy para extraer estadísticas."""
        result = {
            "files_copied": 0,
            "files_skipped": 0,
            "bytes_copied": 0,
            "errors": []
        }
        
        if not output:
            return result
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Buscar líneas de resumen de robocopy
            # El formato con /BYTES es: Files : 100 50 0 50 0 0
            if line.startswith("Files :") or line.startswith("Archivos :"):
                parts = line.split(':')[1].strip().split()
                if len(parts) >= 3:
                    try:
                        result["files_copied"] = int(parts[1])  # Copied
                        result["files_skipped"] = int(parts[2])  # Skipped
                    except (ValueError, IndexError):
                        pass
            
            elif line.startswith("Bytes :") or line.startswith("Bytes"):
                parts = line.split(':')[1].strip().split()
                if len(parts) >= 2:
                    try:
                        result["bytes_copied"] = int(parts[1])  # Copied bytes
                    except (ValueError, IndexError):
                        pass
        
        return result
    
    def _emit_progress(self, percent, current_file):
        """Emite progreso a la UI."""
        if self._progress_callback:
            self._progress_callback(percent, current_file)
    
    def _emit_status(self, message):
        """Emite un mensaje de estado a la UI."""
        if self._status_callback:
            self._status_callback(message)
