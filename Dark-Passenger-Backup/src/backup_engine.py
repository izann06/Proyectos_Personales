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
        
        on_progress(percent, current_file, current_count, total_count): Progreso de la copia
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
        
        self.config = config_manager.load_config()
        
        sources = source_folders or self.config.get("source_folders", [])
        dest = destination or self.config.get("destination_path", "")
        flags = robocopy_flags or self.config.get("robocopy_flags", "/MIR /FFT /Z /XA:H /W:5 /R:3")
        
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
    
    def cancel_backup(self, rollback=False):
        """Cancela el backup en curso."""
        self._cancel_event.set()
        if self._current_process:
            try:
                import subprocess
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self._current_process.pid)], 
                               creationflags=0x08000000 if os.name == 'nt' else 0,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                try:
                    self._current_process.terminate()
                except Exception:
                    pass
        
        if rollback and hasattr(self, 'files_copied_this_session'):
            import time
            time.sleep(0.5)  # Esperar a que el SO libere los handles
            
            dirs_to_check = set()
            
            for file_path in self.files_copied_this_session:
                try:
                    if os.path.exists(file_path):
                        import stat
                        os.chmod(file_path, stat.S_IWRITE)
                        os.remove(file_path)
                        dirs_to_check.add(os.path.dirname(file_path))
                except Exception as e:
                    print(f"Error borrando {file_path}: {e}")
                    
            # Eliminar carpetas que hayan quedado vacías subiendo hacia la raíz
            for d in dirs_to_check:
                curr = d
                while curr and os.path.exists(curr):
                    try:
                        if not os.listdir(curr):
                            os.chmod(curr, stat.S_IWRITE)
                            os.rmdir(curr)
                            curr = os.path.dirname(curr)
                        else:
                            break
                    except Exception:
                        break
                        
            # Si era un backup de carpetas completamente nuevas, aniquilarlas enteras
            if hasattr(self, '_new_folders_created'):
                import shutil
                def on_rm_error(func, path, exc_info):
                    try:
                        os.chmod(path, stat.S_IWRITE)
                        func(path)
                    except: pass
                for d in self._new_folders_created:
                    try:
                        if os.path.exists(d):
                            shutil.rmtree(d, onerror=on_rm_error)
                    except: pass
                self._new_folders_created.clear()
                    
            self.files_copied_this_session.clear()
    
    def _run_backup(self, sources, destination, flags):
        """Ejecuta el backup para todas las carpetas de origen."""
        self.is_running = True
        try:
            self._run_backup_inner(sources, destination, flags)
        except Exception as e:
            # Asegurar que SIEMPRE se llame al callback de completado
            self.is_running = False
            error_entry = {
                "id": "error",
                "status": "error",
                "files_copied": 0,
                "bytes_copied": 0,
                "size_display": "0 B",
                "duration_display": "0s",
                "errors": [str(e)]
            }
            self._emit_status(f"❌ Error inesperado: {e}")
            self._emit_progress(100, "Error", 0, 0)
            if self._completion_callback:
                self._completion_callback(False, error_entry)

    def _run_backup_inner(self, sources, destination, flags):
        """Lógica interna del backup."""
        start_time = time.time()
        
        total_files_copied = 0
        total_files_skipped = 0
        total_bytes = 0
        errors = []
        overall_success = True
        
        self._emit_status("🔍 Escaneando archivos...")
        total_files = 0
        for source in sources:
            for root, dirs, files in os.walk(source):
                total_files += len(files)
        
        self.total_files = total_files
        self.files_copied_so_far = 0
        self.files_copied_this_session = []
        self._new_folders_created = []
        
        self._emit_status("🔪 Iniciando protocolo de backup...")
        
        for i, source in enumerate(sources):
            if self._cancel_event.is_set():
                self._emit_status("❌ Backup cancelado por el usuario.")
                overall_success = False
                break
            
            folder_name = os.path.basename(source)
            dest_path = os.path.join(destination, folder_name)
            
            if not os.path.exists(dest_path) or not os.listdir(dest_path):
                self._new_folders_created.append(dest_path)
            
            self._emit_status(f"📂 [{i+1}/{len(sources)}] Procesando: {folder_name}")
            
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
            total_files_copied = 0
            total_bytes = 0
        elif errors and overall_success:
            status = "partial"
        elif overall_success:
            status = "success"
        else:
            status = "error"
        
        # Si está al día o cancelado, no guardar en historial para no inflar los contadores
        if (status == "success" and total_files_copied == 0) or status == "cancelled":
            entry = {
                "id": "ignored",
                "status": status,
                "files_copied": 0,
                "files_skipped": 0,
                "bytes_copied": 0,
                "bytes": 0,
                "size_display": "0 B",
                "duration_display": "0s"
            }
            if status == "success":
                config_manager.update_last_backup()
                self._emit_status("✅ Estás al día. No había archivos nuevos que copiar.")
            else:
                self._emit_status("❌ Backup cancelado.")
        else:
            # Guardar en historial
            ssd_name = self.config.get("ssd_volume_label", "SSD")
            entry = history_manager.add_entry(
                status=status,
                source_folders=sources,
                destination=destination,
                files_copied=total_files_copied,
                files_skipped=total_files_skipped,
                bytes_copied=total_bytes,
                duration_seconds=int(duration),
                errors=errors,
                destination_name=ssd_name
            )
            
            if status == "success":
                config_manager.update_last_backup()
                self._emit_status(f"✅ Backup completado. {total_files_copied} archivos copiados en {entry['duration_display']}.")
            elif status == "partial":
                self._emit_status(f"⚠️ Backup parcial completado. {total_files_copied} archivos copiados.")
            else:
                self._emit_status("❌ Error crítico en el backup.")
        
        self._emit_progress(100, "Completado", self.files_copied_so_far, self.total_files)
        
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
        
        # Eliminamos /NFL y /NDL para poder ver los archivos, usamos /NP para evitar % rotos
        cmd = f'robocopy "{source}" "{destination}" {flags} /NP /BYTES /NJH /NJS'
        
        result = {
            "files_copied": 0,
            "files_skipped": 0,
            "bytes_copied": 0,
            "errors": []
        }
        
        try:
            import subprocess
            self._current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=0x08000000 if os.name == 'nt' else 0
            )
            
            files_in_this_folder = 0
            current_source_dir = source
            
            while True:
                if self._cancel_event.is_set():
                    break
                    
                line = self._current_process.stdout.readline()
                if not line and self._current_process.poll() is not None:
                    break
                
                if line:
                    line = line.strip()
                    if not line:
                        continue
                        
                    parts = line.split('\t')
                    text_part = parts[-1].strip() if parts else line.strip()
                    
                    if os.path.isdir(text_part) and text_part.startswith(source):
                        current_source_dir = text_part
                    
                    if "Nuevo arch" in line or "New File" in line or "mismo" in line or "Same" in line or "Extra File" in line or "arch extra" in line:
                        self.files_copied_so_far += 1
                        files_in_this_folder += 1
                        
                        # Extraer nombre del archivo y tamaño
                        file_name = text_part
                        if len(parts) >= 2:
                            try:
                                size_str = parts[-2].strip()
                                result["bytes_copied"] += int(size_str)
                            except ValueError:
                                pass
                                
                        # Registrar archivo si es nuevo para posible rollback
                        if "Nuevo arch" in line or "New File" in line:
                            try:
                                rel_path = os.path.relpath(current_source_dir, source)
                                dest_dir = destination if rel_path == "." else os.path.join(destination, rel_path)
                                dest_file_path = os.path.join(dest_dir, file_name)
                                self.files_copied_this_session.append(dest_file_path)
                            except Exception:
                                pass
                        
                        if self.total_files > 0:
                            percent = int((self.files_copied_so_far / self.total_files) * 100)
                            percent = min(100, percent)
                        else:
                            percent = 100
                            
                        self._emit_progress(percent, f"Procesando: {file_name}", self.files_copied_so_far, self.total_files)

            self._current_process.wait()
            exit_code = self._current_process.returncode
            self._current_process = None
            
            result["files_copied"] = files_in_this_folder
            
            if exit_code is not None and exit_code >= 8:
                result["errors"] = [f"Robocopy error (exit code {exit_code})"]
            
            return result
            
        except Exception as e:
            self._current_process = None
            result["errors"] = [str(e)]
            return result
    
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
    
    def _emit_progress(self, percent, current_file, current_count=None, total_count=None):
        """Emite progreso a la UI."""
        if self._progress_callback:
            self._progress_callback(percent, current_file, current_count, total_count)
    
    def _emit_status(self, message):
        """Emite un mensaje de estado a la UI."""
        if self._status_callback:
            self._status_callback(message)
