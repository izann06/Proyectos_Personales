"""
scheduler.py - Sistema de recordatorios y programación de backups.
Comprueba si toca hacer backup y lanza recordatorios si el SSD no está conectado.
"""

import threading
import time
from datetime import datetime, timedelta
from src import config_manager


# Mapeo de días en inglés a número de día de la semana (0=Lunes, 6=Domingo)
DAY_MAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

DAY_NAMES_ES = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}


class BackupScheduler(threading.Thread):
    """
    Hilo que comprueba si hay un backup pendiente y lanza recordatorios.
    
    Lógica:
    1. Si llega el día/hora programado y no se ha hecho backup → lanza recordatorio.
    2. Si el SSD se conecta y hay backup pendiente → lanza popup (gestionado por SSDWatcher).
    3. Si el PC estaba apagado y se enciende después → detecta que hay backup pendiente.
    """
    
    def __init__(self, on_reminder=None, on_backup_due=None, check_interval=60):
        super().__init__(daemon=True)
        self.on_reminder = on_reminder
        self.on_backup_due = on_backup_due
        self.check_interval = check_interval
        self._stop_event = threading.Event()
        self._last_reminder_date = None
        self._already_triggered_today = False
    
    def run(self):
        """Bucle principal del scheduler."""
        while not self._stop_event.is_set():
            try:
                self._check_schedule()
            except Exception:
                pass
            
            self._stop_event.wait(self.check_interval)
    
    def stop(self):
        """Detiene el scheduler."""
        self._stop_event.set()
    
    def _check_schedule(self):
        """Comprueba si toca hacer backup o lanzar recordatorio."""
        config = config_manager.load_config()
        schedule = config.get("schedule", {})
        reminder = config.get("reminder", {})
        
        if not schedule.get("enabled", False):
            return
        
        now = datetime.now()
        
        # ¿Hay un backup pendiente?
        if self.is_backup_overdue(config):
            # Comprobar si es hora de recordatorio
            if reminder.get("enabled", False) and self._should_remind(now, reminder):
                if self.on_reminder:
                    last_backup = config.get("last_backup_date", "Nunca")
                    self.on_reminder(
                        f"⏰ Tienes un backup pendiente. Último backup: {last_backup}\n"
                        f"Conecta tu SSD para iniciar la copia."
                    )
                    self._last_reminder_date = now.date()
            
            # Notificar que hay backup pendiente
            if self.on_backup_due and not self._already_triggered_today:
                self.on_backup_due()
                self._already_triggered_today = True
        
        # Resetear flag si cambia el día
        if self._last_reminder_date and self._last_reminder_date != now.date():
            self._already_triggered_today = False
    
    def _should_remind(self, now, reminder_config):
        """Comprueba si se debe lanzar un recordatorio ahora."""
        target_day = DAY_MAP.get(reminder_config.get("day", "Sunday"), 6)
        target_hour = reminder_config.get("hour", 12)
        target_minute = reminder_config.get("minute", 0)
        
        if now.weekday() != target_day:
            return False
        
        if now.hour != target_hour or now.minute != target_minute:
            return False
        
        # No repetir recordatorio el mismo día
        if self._last_reminder_date == now.date():
            return False
        
        return True
    
    @staticmethod
    def is_backup_overdue(config=None):
        """
        Comprueba si el backup está pendiente (retrasado).
        Retorna True si no se ha hecho backup desde la última fecha programada.
        """
        if config is None:
            config = config_manager.load_config()
        
        schedule = config.get("schedule", {})
        if not schedule.get("enabled", False):
            return False
        
        last_backup_str = config.get("last_backup_date")
        
        if not last_backup_str:
            return True  # Nunca se ha hecho backup
        
        try:
            last_backup = datetime.fromisoformat(last_backup_str)
        except (ValueError, TypeError):
            return True
        
        # Comprobar si ha pasado más de 7 días desde el último backup
        now = datetime.now()
        days_since = (now - last_backup).days
        
        if days_since >= 7:
            return True
        
        # Comprobar si hemos pasado el día/hora programado sin hacer backup
        target_day = DAY_MAP.get(schedule.get("day", "Sunday"), 6)
        target_hour = schedule.get("hour", 12)
        
        # Buscar el último día programado
        days_back = (now.weekday() - target_day) % 7
        last_scheduled = now - timedelta(days=days_back)
        last_scheduled = last_scheduled.replace(hour=target_hour, minute=0, second=0, microsecond=0)
        
        # Si la última hora programada es posterior al último backup
        if last_scheduled > last_backup and last_scheduled <= now:
            return True
        
        return False
    
    @staticmethod
    def get_next_backup_time(config=None):
        """Calcula la próxima fecha/hora programada de backup."""
        if config is None:
            config = config_manager.load_config()
        
        schedule = config.get("schedule", {})
        target_day = DAY_MAP.get(schedule.get("day", "Sunday"), 6)
        target_hour = schedule.get("hour", 12)
        target_minute = schedule.get("minute", 0)
        
        now = datetime.now()
        
        # Calcular días hasta el próximo día objetivo
        days_ahead = (target_day - now.weekday()) % 7
        
        next_date = now + timedelta(days=days_ahead)
        next_date = next_date.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        
        # Si ya pasó hoy, saltar a la semana siguiente
        if next_date <= now:
            next_date += timedelta(weeks=1)
        
        return next_date
    
    @staticmethod
    def get_next_backup_display(config=None):
        """Devuelve el próximo backup en formato legible."""
        next_time = BackupScheduler.get_next_backup_time(config)
        day_es = DAY_NAMES_ES.get(
            list(DAY_MAP.keys())[next_time.weekday()], 
            "Desconocido"
        )
        return f"{day_es} {next_time.strftime('%d/%m/%Y')} a las {next_time.strftime('%H:%M')}"
