"""
app.py - Interfaz gráfica principal de Dark Passenger Backup.
Diseño temático inspirado en la serie Dexter:
- Paleta oscura con acentos rojo sangre
- Tipografía quirúrgica/limpia
- Vocabulario inmersivo
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import sys

from src import config_manager, history_manager
from src.ssd_detector import SSDWatcher, get_external_drives, is_target_ssd_connected, get_all_drives
from src.backup_engine import BackupEngine
from src.scheduler import BackupScheduler, DAY_NAMES_ES, DAY_MAP

# ═══════════════════════════════════════════════════════
#  DEXTER COLOR PALETTE - "The Kill Room"
# ═══════════════════════════════════════════════════════
COLORS = {
    "bg_dark":          "#0D0D0D",      # Fondo principal - negro profundo
    "bg_card":          "#1A1A1A",      # Tarjetas/paneles
    "bg_card_hover":    "#222222",      # Hover sobre tarjetas
    "bg_input":         "#141414",      # Campos de entrada
    "border":           "#2A2A2A",      # Bordes sutiles
    "border_light":     "#333333",      # Bordes más visibles
    
    "blood_red":        "#8B0000",      # Rojo sangre oscuro
    "blood_bright":     "#C41E3A",      # Rojo carmesí (acento primario)
    "blood_glow":       "#E63946",      # Rojo brillante (hover/alertas)
    "blood_dim":        "#5C0A0A",      # Rojo apagado (estados inactivos)
    
    "text_primary":     "#E8E8E8",      # Texto principal
    "text_secondary":   "#888888",      # Texto secundario
    "text_dim":         "#555555",      # Texto muy tenue
    "text_accent":      "#C41E3A",      # Texto de acento
    
    "success":          "#2ECC71",      # Verde éxito
    "warning":          "#F39C12",      # Amarillo advertencia
    "error":            "#E74C3C",      # Rojo error
    
    "progress_bg":      "#1A1A1A",      # Fondo barra de progreso
    "progress_fill":    "#8B0000",      # Relleno barra de progreso
    
    "sidebar_bg":       "#111111",      # Fondo sidebar
    "sidebar_active":   "#1E1E1E",      # Item activo del sidebar
}

FONTS = {
    "title":            ("Consolas", 28, "bold"),
    "subtitle":         ("Consolas", 16),
    "heading":          ("Segoe UI", 18, "bold"),
    "body":             ("Segoe UI", 13),
    "body_bold":        ("Segoe UI", 13, "bold"),
    "small":            ("Segoe UI", 11),
    "tiny":             ("Consolas", 10),
    "mono":             ("Consolas", 12),
    "mono_large":       ("Consolas", 14),
    "stat_number":      ("Consolas", 32, "bold"),
    "stat_label":       ("Segoe UI", 11),
    "button":           ("Segoe UI", 13, "bold"),
    "nav_item":         ("Segoe UI", 13),
    "nav_active":       ("Segoe UI", 13, "bold"),
}


class DarkPassengerApp(ctk.CTk):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        
        # ── Configuración de ventana ──
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("Dark Passenger Backup")
        self.geometry("1100x720")
        self.minsize(950, 600)
        self.configure(fg_color=COLORS["bg_dark"])
        
        # ── Icono y Barra de Tareas (Windows) ──
        try:
            import ctypes
            import sys
            import os
            
            # Forzar a Windows a usar un icono propio en la barra de tareas en lugar del de Python
            myappid = 'dexter.darkpassenger.backup.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
            if os.name == 'nt':
                icon_path = os.path.join(base_dir, "assets", "images", "app_hd.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.winfo_screenheight() // 2) - (720 // 2)
        self.geometry(f"+{x}+{y}")
        
        # ── Estado de la app ──
        self.config = config_manager.load_config()
        self.backup_engine = BackupEngine()
        self.ssd_watcher = None
        self.scheduler = None
        self.current_page = "dashboard"
        self.ssd_connected = False
        self.ssd_info = None
        
        # ── Registrar PID para el watcher ──
        self._acquire_app_lock()
        
        # ── Cargar Recursos Gráficos ──
        try:
            from PIL import Image
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            knife_path = os.path.join(base_dir, "assets", "images", "knife.png")
            
            self.knife_image = ctk.CTkImage(light_image=Image.open(knife_path), dark_image=Image.open(knife_path), size=(48, 48)) if os.path.exists(knife_path) else None
            
            # Cargar assets adicionales
            boat_path = os.path.join(base_dir, "assets", "images", "boat.jpg")
            desk_path = os.path.join(base_dir, "assets", "images", "desk.jpg")
            wrap_path = os.path.join(base_dir, "assets", "images", "plastic_wrap.jpg")
            slide_path = os.path.join(base_dir, "assets", "images", "blood_slide.jpg")
            hand_path = os.path.join(base_dir, "assets", "images", "prosthetic_hand.jpg")
            tools_path = os.path.join(base_dir, "assets", "images", "tools_case.jpg")
            
            self.img_boat = ctk.CTkImage(light_image=Image.open(boat_path), dark_image=Image.open(boat_path), size=(120, 120)) if os.path.exists(boat_path) else None
            self.img_dashboard = ctk.CTkImage(light_image=Image.open(desk_path), dark_image=Image.open(desk_path), size=(48, 48)) if os.path.exists(desk_path) else None
            self.img_folders = ctk.CTkImage(light_image=Image.open(wrap_path), dark_image=Image.open(wrap_path), size=(48, 48)) if os.path.exists(wrap_path) else None
            self.img_history = ctk.CTkImage(light_image=Image.open(slide_path), dark_image=Image.open(slide_path), size=(48, 48)) if os.path.exists(slide_path) else None
            self.img_trophies = ctk.CTkImage(light_image=Image.open(hand_path), dark_image=Image.open(hand_path), size=(48, 48)) if os.path.exists(hand_path) else None
            self.img_settings = ctk.CTkImage(light_image=Image.open(tools_path), dark_image=Image.open(tools_path), size=(48, 48)) if os.path.exists(tools_path) else None
            
            # Iconos para stat cards
            path_total = os.path.join(base_dir, "assets", "images", "icon_total.png")
            path_success = os.path.join(base_dir, "assets", "images", "icon_success.png")
            path_data = os.path.join(base_dir, "assets", "images", "icon_data.png")
            path_files = os.path.join(base_dir, "assets", "images", "icon_files.png")
            
            self.icon_splatter = ctk.CTkImage(light_image=Image.open(path_total), dark_image=Image.open(path_total), size=(64, 64)) if os.path.exists(path_total) else None
            self.icon_drop = ctk.CTkImage(light_image=Image.open(path_success), dark_image=Image.open(path_success), size=(64, 64)) if os.path.exists(path_success) else None
            self.icon_knife = ctk.CTkImage(light_image=Image.open(path_data), dark_image=Image.open(path_data), size=(64, 64)) if os.path.exists(path_data) else None
            self.icon_folder = ctk.CTkImage(light_image=Image.open(path_files), dark_image=Image.open(path_files), size=(64, 64)) if os.path.exists(path_files) else None
            
            # Cuchillo grande para el popup
            self.img_knife_large = ctk.CTkImage(light_image=Image.open(knife_path), dark_image=Image.open(knife_path), size=(100, 100)) if os.path.exists(knife_path) else None
            
        except Exception as e:
            print("No se pudo cargar la imagen:", e)
            self.knife_image = None

        # Estado para borrado en segundo plano
        self.is_deleting = False
        self.cancel_delete_flag = False
        self.delete_stats = {"percent": 0, "current_file": "", "deleted": 0, "total": 0}

        # ── Construir UI ──
        self._build_layout()
        self._show_dashboard()
        
        # ── Iniciar servicios en segundo plano ──
        self._start_background_services()
        
        # ── Comprobar si hay backup pendiente al iniciar ──
        self.after(2000, self._check_startup_state)
        
        # ── Manejar cierre ──
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    # ═══════════════════════════════════════════════════════
    #  LAYOUT PRINCIPAL
    # ═══════════════════════════════════════════════════════
    
    def _build_layout(self):
        """Construye el layout principal: sidebar + área de contenido."""
        
        # ── Sidebar (navegación lateral) ──
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0,
            fg_color=COLORS["sidebar_bg"],
            border_width=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo / Título en sidebar
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=15, pady=(25, 5))
        
        ctk.CTkLabel(
            logo_frame, text="🔪",
            font=("Segoe UI Emoji", 36),
            text_color=COLORS["blood_bright"]
        ).pack()
        
        ctk.CTkLabel(
            logo_frame, text="DARK PASSENGER",
            font=("Consolas", 15, "bold"),
            text_color=COLORS["blood_bright"]
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            logo_frame, text="B A C K U P",
            font=("Consolas", 10),
            text_color=COLORS["text_dim"]
        ).pack()
        
        # Separador
        sep = ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"])
        sep.pack(fill="x", padx=20, pady=(20, 15))
        
        # Botones de navegación
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "◉  Dashboard", self._show_dashboard),
            ("folders",   "📁  Carpetas",  self._show_folders),
            ("history",   "📋  Historial",  self._show_history),
            ("trophies",  "🩸  Trofeos",    self._show_destination_files),
            ("settings",  "⚙  Ajustes",    self._show_settings),
        ]
        
        for key, text, command in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=text, anchor="w",
                font=FONTS["nav_item"],
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["text_secondary"],
                height=42, corner_radius=8,
                command=command
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = btn
        
        # ── Indicador SSD en sidebar (parte inferior) ──
        self.ssd_status_frame = ctk.CTkFrame(
            self.sidebar, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1,
            border_color=COLORS["border"]
        )
        self.ssd_status_frame.pack(side="bottom", fill="x", padx=12, pady=(5, 15))
        
        # Boat image
        if hasattr(self, 'img_boat') and self.img_boat:
            boat_label = ctk.CTkLabel(self.sidebar, text="", image=self.img_boat)
            boat_label.pack(side="bottom", pady=(10, 5))
            
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        self.ssd_status_icon = ctk.CTkLabel(
            self.ssd_status_frame, text="⬤",
            font=("Segoe UI", 12),
            text_color=COLORS["blood_dim"]
        )
        self.ssd_status_icon.pack(side="left", padx=(12, 5), pady=10)
        
        self.ssd_status_label = ctk.CTkLabel(
            self.ssd_status_frame, text="SSD Desconectado",
            font=FONTS["small"],
            text_color=COLORS["text_dim"]
        )
        self.ssd_status_label.pack(side="left", padx=(0, 12), pady=10)
        
        # ── Área de contenido principal ──
        self.content_area = ctk.CTkFrame(
            self, fg_color=COLORS["bg_dark"],
            corner_radius=0
        )
        self.content_area.pack(side="right", fill="both", expand=True)
    
    def _set_active_nav(self, active_key):
        """Resalta el botón de navegación activo."""
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(
                    fg_color=COLORS["sidebar_active"],
                    text_color=COLORS["blood_bright"],
                    font=FONTS["nav_active"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                    font=FONTS["nav_item"]
                )
    
    def _clear_content(self):
        """Limpia el área de contenido para cargar una nueva página."""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    # ═══════════════════════════════════════════════════════
    #  PÁGINA: DASHBOARD
    # ═══════════════════════════════════════════════════════
    
    def _show_dashboard(self):
        """Muestra la página principal del Dashboard."""
        self._clear_content()
        self._set_active_nav("dashboard")
        self.current_page = "dashboard"
        
        # Contenedor scrollable
        scroll = ctk.CTkScrollableFrame(
            self.content_area, fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ── Header ──
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Imagen
        if hasattr(self, 'img_dashboard') and self.img_dashboard:
            ctk.CTkLabel(header, text="", image=self.img_dashboard).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(
            header, text="Tonight's the night.",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(side="left")
        
        is_running = self.backup_engine.is_running
        
        # Botón principal de Backup
        self.btn_backup = ctk.CTkButton(
            header, 
            text="✕  DETENER BACKUP" if is_running else "▶  INICIAR BACKUP",
            font=FONTS["button"],
            fg_color=COLORS["border"] if is_running else COLORS["blood_red"],
            hover_color=COLORS["blood_dim"] if is_running else COLORS["blood_bright"],
            text_color="white",
            height=42, width=200,
            corner_radius=8,
            command=self._on_cancel_backup if is_running else self._on_backup_click
        )
        self.btn_backup.pack(side="right")
        
        # ── Tarjetas de estado ──
        stats = history_manager.get_stats()
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="card")
        
        self._create_stat_card(cards_frame, 0, "TOTAL BACKUPS", str(stats["total_backups"]), getattr(self, "icon_splatter", "🩸"))
        self._create_stat_card(cards_frame, 1, "SUCCESSFUL", f'{stats["successful"]}', getattr(self, "icon_drop", "✅"))
        self._create_stat_card(cards_frame, 2, "DATA COPIED", stats.get("total_bytes_display", "0 B"), getattr(self, "icon_knife", "💾"))
        self._create_stat_card(cards_frame, 3, "FILES", str(stats["total_files"]), getattr(self, "icon_folder", "📄"))
        
        # ── Panel de estado actual ──
        status_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        status_card.pack(fill="x", pady=(0, 15))
        
        status_inner = ctk.CTkFrame(status_card, fg_color="transparent")
        status_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            status_inner, text="Estado del Sistema",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(anchor="w")
        
        # Estado del SSD
        ssd_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
        ssd_frame.pack(fill="x", pady=(15, 5))
        
        ssd_connected = is_target_ssd_connected(self.config)
        ssd_color = COLORS["success"] if ssd_connected else COLORS["text_dim"]
        ssd_text = f"SSD Conectado ({ssd_connected['label']} - {ssd_connected['letter']}:)" if ssd_connected else "SSD No Detectado"
        
        ctk.CTkLabel(
            ssd_frame, text=f"⬤  {ssd_text}",
            font=FONTS["body"],
            text_color=ssd_color,
            anchor="w"
        ).pack(side="left")
        
        # Próximo backup
        next_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
        next_frame.pack(fill="x", pady=(5, 5))
        
        next_backup = BackupScheduler.get_next_backup_display(self.config)
        ctk.CTkLabel(
            next_frame, text=f"📅  Próximo backup: {next_backup}",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(side="left")
        
        # Último backup
        last_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
        last_frame.pack(fill="x", pady=(5, 5))
        
        last_backup = stats.get("last_backup", "Nunca")
        ctk.CTkLabel(
            last_frame, text=f"🕐  Último backup: {last_backup}",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(side="left")
        
        # Backup pendiente?
        # Solo mostrar si realmente ha pasado el tiempo (1 semana, etc), NO simplemente porque el SSD esté conectado o desconectado
        # Usamos is_backup_overdue que ya calcula si han pasado los días configurados.
        if BackupScheduler.is_backup_overdue(self.config):
            stats = history_manager.get_stats()
            # Si NUNCA se ha hecho un backup, también está pendiente
            is_never = stats.get("total_backups", 0) == 0
            if is_never or not self.backup_engine.is_running:
                overdue_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
                overdue_frame.pack(fill="x", pady=(5, 0))
                ctk.CTkLabel(
                    overdue_frame, text="⚠  ¡Backup pendiente! Conecta tu SSD o inícialo.",
                    font=FONTS["body_bold"],
                    text_color=COLORS["warning"],
                    anchor="w"
                ).pack(side="left")
        
        # ── Barra de progreso (oculta por defecto) ──
        self.progress_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["blood_dim"]
        )
        
        progress_inner = ctk.CTkFrame(self.progress_card, fg_color="transparent")
        progress_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            progress_inner, text="🔪 Progreso del Ritual",
            font=FONTS["heading"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(anchor="w")
        
        # Contenedor para barra y cuchillo
        self.progress_container = ctk.CTkFrame(progress_inner, fg_color="transparent", height=40)
        self.progress_container.pack(fill="x", pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_container,
            fg_color=COLORS["progress_bg"],
            progress_color=COLORS["blood_red"],
            height=12, corner_radius=6
        )
        # Colocamos la barra centrada verticalmente
        self.progress_bar.place(relx=0, rely=0.5, relwidth=1.0, anchor="w")
        self.progress_bar.set(0)
        
        # El cuchillo
        if hasattr(self, 'knife_image') and self.knife_image:
            self.knife_label = ctk.CTkLabel(self.progress_container, text="", image=self.knife_image)
            self.knife_label.place(relx=0, rely=0.5, anchor="center")
        else:
            self.knife_label = ctk.CTkLabel(self.progress_container, text="🔪", font=("Segoe UI Emoji", 24), text_color=COLORS["blood_bright"])
            self.knife_label.place(relx=0, rely=0.5, anchor="center")
        
        info_frame = ctk.CTkFrame(progress_inner, fg_color="transparent")
        info_frame.pack(fill="x", pady=(5, 0))
        
        self.progress_percentage = ctk.CTkLabel(
            info_frame, text="0%",
            font=FONTS["heading"],
            text_color=COLORS["blood_bright"]
        )
        self.progress_percentage.pack(side="right")
        
        self.progress_label = ctk.CTkLabel(
            info_frame, text="Preparando...",
            font=FONTS["mono"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        self.progress_label.pack(side="left")
        
        self.files_count_label = ctk.CTkLabel(
            progress_inner, text="Archivos: 0 / 0",
            font=FONTS["small"],
            text_color=COLORS["text_dim"],
            anchor="w"
        )
        self.files_count_label.pack(anchor="w")
        
        self.progress_status = ctk.CTkLabel(
            progress_inner, text="",
            font=FONTS["small"],
            text_color=COLORS["text_dim"],
            anchor="w"
        )
        self.progress_status.pack(anchor="w")
        
        btn_cancel = ctk.CTkButton(
            progress_inner, text="✕  Cancelar",
            font=FONTS["small"],
            fg_color=COLORS["border"],
            hover_color=COLORS["blood_dim"],
            text_color=COLORS["text_secondary"],
            height=30, width=100, corner_radius=6,
            command=self._on_cancel_backup
        )
        btn_cancel.pack(anchor="e", pady=(10, 0))
        
        # Solo mostrar si hay backup en curso
        if self.backup_engine.is_running:
            self.progress_card.pack(fill="x", pady=(0, 15))
            
            # Restaurar estado visual
            copied = getattr(self.backup_engine, 'files_copied_so_far', 0)
            total = getattr(self.backup_engine, 'total_files', 0)
            if total > 0:
                percent = int((copied / total) * 100)
                fraction = percent / 100.0
                self.progress_bar.set(fraction)
                safe_relx = max(0.02, min(0.98, fraction))
                if hasattr(self, 'knife_label'):
                    self.knife_label.place(relx=safe_relx, rely=0.5, anchor="center")
                self.progress_percentage.configure(text=f"{percent}%")
                self.files_count_label.configure(text=f"Archivos guardados: {copied} / {total}")
                self.progress_label.configure(text="Continuando con el ritual...")
        
        # ── Últimos backups (mini historial) ──
        recent_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        recent_card.pack(fill="x", pady=(0, 15))
        
        recent_inner = ctk.CTkFrame(recent_card, fg_color="transparent")
        recent_inner.pack(fill="x", padx=25, pady=20)
        
        recent_header = ctk.CTkFrame(recent_inner, fg_color="transparent")
        recent_header.pack(fill="x")
        
        ctk.CTkLabel(
            recent_header, text="Víctimas Recientes",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkButton(
            recent_header, text="Ver todo →",
            font=FONTS["small"],
            fg_color="transparent",
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["blood_bright"],
            height=28, width=80,
            command=self._show_history
        ).pack(side="right")
        
        history = history_manager.load_history()[:5]
        
        if not history:
            ctk.CTkLabel(
                recent_inner,
                text="Aún no hay víctimas... El pasajero oscuro espera.",
                font=FONTS["body"],
                text_color=COLORS["text_dim"]
            ).pack(pady=15)
        else:
            for entry in history:
                self._create_history_row(recent_inner, entry)
    
    def _create_stat_card(self, parent, col, label, value, icon):
        """Crea una tarjeta de estadística."""
        card = ctk.CTkFrame(
            parent, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        card.grid(row=0, column=col, padx=(0 if col == 0 else 5, 5 if col < 3 else 0), sticky="nsew")
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=18, pady=18)
        
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        
        if isinstance(icon, str):
            ctk.CTkLabel(
                top, text=icon,
                font=("Segoe UI Emoji", 18)
            ).pack(side="left")
        else:
            ctk.CTkLabel(
                top, text="", image=icon
            ).pack(side="left")
        
        ctk.CTkLabel(
            inner, text=value,
            font=FONTS["stat_number"],
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(anchor="w", pady=(8, 0))
        
        ctk.CTkLabel(
            inner, text=label,
            font=FONTS["stat_label"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w")
    
    def _create_history_row(self, parent, entry):
        """Crea una fila de historial."""
        row = ctk.CTkFrame(
            parent, fg_color=COLORS["bg_input"],
            corner_radius=8, height=45
        )
        row.pack(fill="x", pady=(8, 0))
        row.pack_propagate(False)
        
        inner = ctk.CTkFrame(row, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=8)
        
        status = entry.get("status", "")
        status_icons = {
            "success": ("✅", COLORS["success"]),
            "error": ("❌", COLORS["error"]),
            "partial": ("⚠", COLORS["warning"]),
            "cancelled": ("⊘", COLORS["text_dim"]),
        }
        icon, color = status_icons.get(status, ("?", COLORS["text_dim"]))
        
        ctk.CTkLabel(
            inner, text=icon, font=("Segoe UI Emoji", 14),
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            inner, text=entry.get("date_display", ""),
            font=FONTS["mono"], text_color=COLORS["text_primary"]
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            inner, text=f"{entry.get('files_copied', 0)} archivos",
            font=FONTS["small"], text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=(0, 15))
        
        dest = entry.get("destination_name", "")
        if dest:
            ctk.CTkLabel(
                inner, text=f"💾 {dest}",
                font=FONTS["small"], text_color=COLORS["text_dim"]
            ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            inner, text=entry.get("size_display", ""),
            font=FONTS["small"], text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            inner, text=entry.get("duration_display", ""),
            font=FONTS["tiny"], text_color=COLORS["text_dim"]
        ).pack(side="right")
    
    # ═══════════════════════════════════════════════════════
    #  PÁGINA: CARPETAS
    # ═══════════════════════════════════════════════════════
    
    def _show_folders(self):
        """Página de gestión de carpetas de origen y destino."""
        self._clear_content()
        self._set_active_nav("folders")
        self.current_page = "folders"
        
        scroll = ctk.CTkScrollableFrame(
            self.content_area, fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        if hasattr(self, 'img_folders') and self.img_folders:
            ctk.CTkLabel(header, text="", image=self.img_folders).pack(side="left", padx=(0, 15))
            
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame, text="La Mesa de Trabajo",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            title_frame, text="Selecciona las carpetas que el pasajero oscuro debe proteger.",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 20))
        
        # ── Carpetas de origen ──
        source_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        source_card.pack(fill="x", pady=(0, 15))
        
        source_inner = ctk.CTkFrame(source_card, fg_color="transparent")
        source_inner.pack(fill="x", padx=25, pady=20)
        
        source_header = ctk.CTkFrame(source_inner, fg_color="transparent")
        source_header.pack(fill="x")
        
        ctk.CTkLabel(
            source_header, text="📂  Carpetas de Origen",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        ctk.CTkButton(
            source_header, text="+ Añadir Carpeta",
            font=FONTS["small"],
            fg_color=COLORS["blood_red"],
            hover_color=COLORS["blood_bright"],
            text_color="white",
            height=32, width=130, corner_radius=6,
            command=self._add_source_folder
        ).pack(side="right")
        
        # Lista de carpetas configuradas
        self.source_list_frame = ctk.CTkFrame(source_inner, fg_color="transparent")
        self.source_list_frame.pack(fill="x", pady=(15, 0))
        
        self._refresh_source_list()
        
        # ── Destino (SSD) ──
        dest_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        dest_card.pack(fill="x", pady=(0, 15))
        
        dest_inner = ctk.CTkFrame(dest_card, fg_color="transparent")
        dest_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            dest_inner, text="💀  Destino (SSD Externo)",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            dest_inner,
            text="Selecciona tu SSD externo. El programa recordará su identidad.",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", pady=(5, 15))
        
        # Info del SSD configurado actual
        dest_path = self.config.get("destination_path", "")
        ssd_label = self.config.get("ssd_volume_label", "")
        
        if dest_path:
            current_frame = ctk.CTkFrame(dest_inner, fg_color=COLORS["bg_input"], corner_radius=8)
            current_frame.pack(fill="x", pady=(0, 10))
            
            ctk.CTkLabel(
                current_frame,
                text=f"📍  {ssd_label} → {dest_path}",
                font=FONTS["mono"],
                text_color=COLORS["text_primary"]
            ).pack(side="left", padx=15, pady=10)
        
        # Botones para configurar SSD
        btn_frame = ctk.CTkFrame(dest_inner, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame, text="🔍  Detectar SSD Conectado",
            font=FONTS["body"],
            fg_color=COLORS["blood_red"],
            hover_color=COLORS["blood_bright"],
            text_color="white",
            height=38, corner_radius=8,
            command=self._detect_ssd
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame, text="📂  Seleccionar Carpeta Manual",
            font=FONTS["body"],
            fg_color=COLORS["border_light"],
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_primary"],
            height=38, corner_radius=8,
            command=self._select_destination_manual
        ).pack(side="left")
    
    def _refresh_source_list(self):
        """Actualiza la lista visual de carpetas de origen."""
        for widget in self.source_list_frame.winfo_children():
            widget.destroy()
        
        folders = self.config.get("source_folders", [])
        
        if not folders:
            ctk.CTkLabel(
                self.source_list_frame,
                text="No hay carpetas configuradas. Añade una para empezar.",
                font=FONTS["body"],
                text_color=COLORS["text_dim"]
            ).pack(pady=10)
            return
        
        for folder in folders:
            row = ctk.CTkFrame(
                self.source_list_frame,
                fg_color=COLORS["bg_input"],
                corner_radius=8
            )
            row.pack(fill="x", pady=3)
            
            # Icono de carpeta
            ctk.CTkLabel(
                row, text="📁", font=("Segoe UI Emoji", 14)
            ).pack(side="left", padx=(12, 5), pady=8)
            
            # Ruta
            ctk.CTkLabel(
                row, text=folder,
                font=FONTS["mono"],
                text_color=COLORS["text_primary"],
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=5, pady=8)
            
            # Botón eliminar
            ctk.CTkButton(
                row, text="✕", width=30, height=28,
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color=COLORS["blood_dim"],
                text_color=COLORS["text_dim"],
                corner_radius=6,
                command=lambda f=folder: self._remove_source_folder(f)
            ).pack(side="right", padx=8, pady=6)
    
    def _add_source_folder(self):
        """Abre diálogo para seleccionar una carpeta de origen."""
        folder = filedialog.askdirectory(title="Selecciona una carpeta para backup")
        if folder:
            self.config = config_manager.add_source_folder(folder)
            self._refresh_source_list()
    
    def _remove_source_folder(self, folder):
        """Elimina una carpeta de la lista de orígenes."""
        self.config = config_manager.remove_source_folder(folder)
        self._refresh_source_list()
    
    def _detect_ssd(self):
        """Detecta discos externos y permite seleccionar uno como SSD destino."""
        drives = get_external_drives()
        
        if not drives:
            messagebox.showinfo(
                "Sin discos externos",
                "No se detectaron discos externos.\nConecta tu SSD e inténtalo de nuevo."
            )
            return
        
        # Crear ventana de selección
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar SSD")
        select_window.geometry("500x400")
        select_window.configure(fg_color=COLORS["bg_dark"])
        select_window.transient(self)
        select_window.grab_set()
        
        # Centrar
        select_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 250
        y = self.winfo_y() + (self.winfo_height() // 2) - 200
        select_window.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(
            select_window, text="Selecciona tu SSD",
            font=FONTS["heading"],
            text_color=COLORS["blood_bright"]
        ).pack(pady=(20, 15))
        
        for drive in drives:
            drive_frame = ctk.CTkFrame(
                select_window, fg_color=COLORS["bg_card"],
                corner_radius=10, border_width=1,
                border_color=COLORS["border"],
                cursor="hand2"
            )
            drive_frame.pack(fill="x", padx=20, pady=5)
            
            inner = ctk.CTkFrame(drive_frame, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)
            
            ctk.CTkLabel(
                inner,
                text=f"💾  {drive['label']} ({drive['letter']}:)",
                font=FONTS["body_bold"],
                text_color=COLORS["text_primary"]
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                inner,
                text=f"   {drive['total_display']} total · {drive['free_display']} libre · {drive['file_system']}",
                font=FONTS["small"],
                text_color=COLORS["text_secondary"]
            ).pack(anchor="w")
            
            ctk.CTkButton(
                inner, text="Seleccionar",
                font=FONTS["small"],
                fg_color=COLORS["blood_red"],
                hover_color=COLORS["blood_bright"],
                text_color="white",
                height=28, width=100, corner_radius=6,
                command=lambda d=drive, w=select_window: self._select_ssd(d, w)
            ).pack(anchor="e", pady=(5, 0))
    
    def _select_ssd(self, drive, window):
        """Configura el SSD seleccionado como destino."""
        dest_path = os.path.join(f"{drive['letter']}:\\", "DarkPassenger_Backup")
        
        config_manager.set_ssd_info(
            drive["serial"],
            drive["label"],
            drive["letter"]
        )
        config_manager.set_destination(dest_path)
        self.config = config_manager.load_config()
        
        # Reiniciar watcher con nueva config
        if self.ssd_watcher:
            self.ssd_watcher.update_config(self.config)
        
        window.destroy()
        self._show_folders()  # Refrescar la página
    
    def _select_destination_manual(self):
        """Selección manual de carpeta destino."""
        folder = filedialog.askdirectory(title="Selecciona la carpeta de destino en tu SSD")
        if folder:
            config_manager.set_destination(folder)
            self.config = config_manager.load_config()
            self._show_folders()
    
    # ═══════════════════════════════════════════════════════
    #  PÁGINA: HISTORIAL
    # ═══════════════════════════════════════════════════════
    
    def _show_history(self):
        """Muestra el historial completo de backups."""
        self._clear_content()
        self._set_active_nav("history")
        self.current_page = "history"
        
        scroll = ctk.CTkScrollableFrame(
            self.content_area, fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        if hasattr(self, 'img_history') and self.img_history:
            ctk.CTkLabel(header, text="", image=self.img_history).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(
            header, text="Las Víctimas",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkButton(
            header, text="🗑  Limpiar Historial",
            font=FONTS["small"],
            fg_color=COLORS["border_light"],
            hover_color=COLORS["blood_dim"],
            text_color=COLORS["text_secondary"],
            height=32, width=140, corner_radius=6,
            command=self._clear_history
        ).pack(side="right")
        
        # Stats rápidos
        stats = history_manager.get_stats()
        stats_text = (
            f"📊 {stats['total_backups']} backups  ·  "
            f"✅ {stats['successful']} exitosos  ·  "
            f"❌ {stats['failed']} fallidos  ·  "
            f"💾 {stats.get('total_bytes_display', '0 B')} total"
        )
        ctk.CTkLabel(
            scroll, text=stats_text,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))
        
        # Lista de entradas
        history = history_manager.load_history()
        
        if not history:
            empty_frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=12)
            empty_frame.pack(fill="x", pady=20)
            ctk.CTkLabel(
                empty_frame,
                text="🔪\n\nEl ritual aún no ha comenzado.\nRealiza tu primer backup.",
                font=FONTS["body"],
                text_color=COLORS["text_dim"],
                justify="center"
            ).pack(pady=40)
        else:
            for entry in history:
                self._create_history_detail_row(scroll, entry)
    
    def _create_history_detail_row(self, parent, entry):
        """Crea una fila detallada de historial."""
        status = entry.get("status", "")
        status_map = {
            "success":   ("✅ Completado", COLORS["success"]),
            "error":     ("❌ Error", COLORS["error"]),
            "partial":   ("⚠ Parcial", COLORS["warning"]),
            "cancelled": ("⊘ Cancelado", COLORS["text_dim"]),
        }
        status_text, status_color = status_map.get(status, ("?", COLORS["text_dim"]))
        
        card = ctk.CTkFrame(
            parent, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1,
            border_color=COLORS["border"]
        )
        card.pack(fill="x", pady=4)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=12)
        
        # Fila superior: fecha + estado
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        
        ctk.CTkLabel(
            top, text=entry.get("date_display", ""),
            font=FONTS["mono_large"],
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            top, text=status_text,
            font=FONTS["body_bold"],
            text_color=status_color
        ).pack(side="right")
        
        # Fila inferior: detalles
        bottom = ctk.CTkFrame(inner, fg_color="transparent")
        bottom.pack(fill="x", pady=(5, 0))
        
        details = (
            f"📄 {entry.get('files_copied', 0)} copiados  ·  "
            f"⏭ {entry.get('files_skipped', 0)} omitidos  ·  "
            f"💾 {entry.get('size_display', '0 B')}  ·  "
            f"⏱ {entry.get('duration_display', '0s')}"
        )
        
        ctk.CTkLabel(
            bottom, text=details,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        # Mostrar errores si los hay
        errors = entry.get("errors", [])
        if errors:
            for err in errors[:3]:  # Máximo 3 errores visibles
                ctk.CTkLabel(
                    inner, text=f"   ⚠ {err}",
                    font=FONTS["tiny"],
                    text_color=COLORS["error"],
                    anchor="w"
                ).pack(anchor="w", pady=(2, 0))
    
    def _clear_history(self):
        """Limpia todo el historial."""
        if messagebox.askyesno("Limpiar Historial", "¿Seguro que quieres eliminar todo el historial de backups?"):
            history_manager.clear_history()
            self._show_history()
    
    # ═══════════════════════════════════════════════════════
    #  PÁGINA: TROFEOS (DESTINO)
    # ═══════════════════════════════════════════════════════
    
    def _show_destination_files(self):
        """Muestra las carpetas respaldadas en el SSD de destino."""
        self._clear_content()
        self._set_active_nav("trophies")
        self.current_page = "trophies"
        
        # Header
        header = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        if hasattr(self, 'img_trophies') and self.img_trophies:
            ctk.CTkLabel(header, text="", image=self.img_trophies).pack(side="left", padx=(0, 15))
            
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            title_frame, text="La Colección de Trofeos",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(side="left")
        
        btn_refresh = ctk.CTkButton(
            header, text="⟳ Actualizar",
            font=FONTS["small"],
            fg_color=COLORS["border"],
            hover_color=COLORS["blood_dim"],
            text_color=COLORS["text_secondary"],
            height=30, width=100, corner_radius=6,
            command=self._refresh_destination_files
        )
        btn_refresh.pack(side="right")
        
        # Contenedor principal scrollable
        self.trophies_container = ctk.CTkScrollableFrame(
            self.content_area, fg_color=COLORS["bg_dark"]
        )
        self.trophies_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        self._refresh_destination_files()
        
    def _refresh_destination_files(self):
        """Recarga la lista de carpetas en el SSD."""
        if not hasattr(self, 'trophies_container') or not self.trophies_container.winfo_exists():
            return
            
        for widget in self.trophies_container.winfo_children():
            widget.destroy()
            
        # Si está borrando, restaurar la interfaz de borrado y no mostrar la lista
        if getattr(self, 'is_deleting', False):
            self._create_delete_progress_ui()
            stats = self.delete_stats
            self._do_update_delete_progress(stats["percent"], stats["current_file"], stats["deleted"], stats["total"])
            return
            
        config = config_manager.load_config()
        ssd = is_target_ssd_connected(config)
        
        if not ssd:
            # SSD No conectado
            empty_frame = ctk.CTkFrame(self.trophies_container, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=50)
            
            ctk.CTkLabel(
                empty_frame, text="⚠", font=("Segoe UI Emoji", 48), text_color=COLORS["warning"]
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                empty_frame, text="El SSD no está conectado.",
                font=FONTS["heading"], text_color=COLORS["text_primary"]
            ).pack()
            
            ctk.CTkLabel(
                empty_frame, text="Conecta tu disco externo para ver y gestionar los trofeos (backups).",
                font=FONTS["body"], text_color=COLORS["text_secondary"]
            ).pack()
            return
            
        # SSD conectado, buscar carpetas
        dest_path = os.path.join(f"{ssd['letter']}:\\", "DarkPassenger_Backup")
        
        if not os.path.exists(dest_path):
            empty_frame = ctk.CTkFrame(self.trophies_container, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=50)
            
            ctk.CTkLabel(
                empty_frame, text="🩸", font=("Segoe UI Emoji", 48)
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                empty_frame, text="La colección está vacía.",
                font=FONTS["heading"], text_color=COLORS["text_primary"]
            ).pack()
            
            ctk.CTkLabel(
                empty_frame, text="No hay ningún backup guardado todavía.",
                font=FONTS["body"], text_color=COLORS["text_secondary"]
            ).pack()
            return
            
        ctk.CTkLabel(
            self.trophies_container, text=f"Ubicación: {dest_path}",
            font=FONTS["mono"], text_color=COLORS["text_dim"], anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        # Listar subdirectorios
        try:
            items = os.listdir(dest_path)
            folders = [f for f in items if os.path.isdir(os.path.join(dest_path, f))]
        except Exception as e:
            ctk.CTkLabel(self.trophies_container, text=f"Error leyendo el disco: {e}", text_color=COLORS["error"]).pack()
            return
            
        if not folders:
            empty_frame = ctk.CTkFrame(self.trophies_container, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=30)
            ctk.CTkLabel(empty_frame, text="No hay carpetas en el destino.", text_color=COLORS["text_dim"]).pack()
            return
            
        # Ordenar alfabéticamente
        folders.sort(key=str.lower)
        
        for folder in folders:
            full_path = os.path.join(dest_path, folder)
            
            row = ctk.CTkFrame(
                self.trophies_container, fg_color=COLORS["bg_card"],
                corner_radius=8, border_width=1, border_color=COLORS["border"]
            )
            row.pack(fill="x", pady=4)
            
            # Nombre de la carpeta
            ctk.CTkLabel(
                row, text=f"📁  {folder}",
                font=FONTS["body_bold"], text_color=COLORS["text_primary"],
                anchor="w"
            ).pack(side="left", padx=15, pady=12)
            
            # Botones de acción
            btn_delete = ctk.CTkButton(
                row, text="✕ Borrar",
                font=FONTS["small"],
                fg_color="transparent",
                hover_color=COLORS["blood_dim"],
                text_color=COLORS["error"],
                border_width=1, border_color=COLORS["error"],
                height=28, width=80, corner_radius=6,
                command=lambda p=full_path: self._delete_folder(p)
            )
            btn_delete.pack(side="right", padx=(5, 15), pady=12)
            
            btn_open = ctk.CTkButton(
                row, text="👁 Ver",
                font=FONTS["small"],
                fg_color="transparent",
                hover_color=COLORS["bg_card_hover"],
                text_color=COLORS["text_secondary"],
                border_width=1, border_color=COLORS["border"],
                height=28, width=80, corner_radius=6,
                command=lambda p=full_path: self._open_folder(p)
            )
            btn_open.pack(side="right", padx=5, pady=12)
            
    def _open_folder(self, path):
        """Abre la carpeta en el explorador de Windows."""
        try:
            import os
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{str(e)}")
            
    def _delete_folder(self, path):
        """Borra la carpeta de forma permanente."""
        folder_name = os.path.basename(path)
        if messagebox.askyesno(
            "Eliminar Trofeo",
            f"¿Estás seguro de que quieres eliminar la carpeta '{folder_name}' de tu SSD?\n\n¡Esta acción es irreversible y los datos se perderán para siempre!"
        ):
            # Iniciar UI de borrado
            self._create_delete_progress_ui()
            import threading
            threading.Thread(target=self._delete_folder_background, args=(path,), daemon=True).start()
            
    def _create_delete_progress_ui(self):
        """Crea la interfaz de la barra de progreso para borrar."""
        # Limpiamos la lista de trofeos para mostrar el progreso en su lugar
        if hasattr(self, 'trophies_container') and self.trophies_container.winfo_exists():
            for widget in self.trophies_container.winfo_children():
                widget.destroy()
            
        self.delete_progress_card = ctk.CTkFrame(
            self.trophies_container, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["blood_dim"]
        )
        self.delete_progress_card.pack(fill="x", padx=10, pady=20)
        
        progress_inner = ctk.CTkFrame(self.delete_progress_card, fg_color="transparent")
        progress_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            progress_inner, text="🔪 Destruyendo Trofeo...",
            font=FONTS["heading"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(anchor="w")
        
        self.del_progress_container = ctk.CTkFrame(progress_inner, fg_color="transparent", height=40)
        self.del_progress_container.pack(fill="x", pady=(10, 5))
        
        self.del_progress_bar = ctk.CTkProgressBar(
            self.del_progress_container,
            fg_color=COLORS["progress_bg"],
            progress_color=COLORS["blood_red"],
            height=12, corner_radius=6
        )
        self.del_progress_bar.place(relx=0, rely=0.5, relwidth=1.0, anchor="w")
        self.del_progress_bar.set(0)
        
        if hasattr(self, 'knife_image') and self.knife_image:
            self.del_knife_label = ctk.CTkLabel(self.del_progress_container, text="", image=self.knife_image)
            self.del_knife_label.place(relx=0, rely=0.5, anchor="center")
        else:
            self.del_knife_label = ctk.CTkLabel(self.del_progress_container, text="🔪", font=("Segoe UI Emoji", 24), text_color=COLORS["blood_bright"])
            self.del_knife_label.place(relx=0, rely=0.5, anchor="center")
            
        info_frame = ctk.CTkFrame(progress_inner, fg_color="transparent")
        info_frame.pack(fill="x", pady=(5, 0))
        
        self.del_progress_percentage = ctk.CTkLabel(
            info_frame, text="0%",
            font=FONTS["heading"],
            text_color=COLORS["blood_bright"]
        )
        self.del_progress_percentage.pack(side="right")
        
        self.del_progress_label = ctk.CTkLabel(
            info_frame, text="Escaneando para destruir...",
            font=FONTS["mono"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        self.del_progress_label.pack(side="left")
        
        self.del_files_count_label = ctk.CTkLabel(
            progress_inner, text="Archivos eliminados: 0 / 0",
            font=FONTS["small"],
            text_color=COLORS["text_dim"],
            anchor="w"
        )
        self.del_files_count_label.pack(anchor="w")
        
        btn_cancel_delete = ctk.CTkButton(
            progress_inner, text="✕  Detener",
            font=FONTS["small"],
            fg_color=COLORS["border"],
            hover_color=COLORS["blood_dim"],
            text_color=COLORS["text_secondary"],
            height=30, width=100, corner_radius=6,
            command=self._on_cancel_delete
        )
        btn_cancel_delete.pack(anchor="e", pady=(10, 0))
        
    def _on_cancel_delete(self):
        """Marca el flag para detener el borrado en curso."""
        self.cancel_delete_flag = True
        self.del_progress_label.configure(text="Deteniendo...", text_color=COLORS["warning"])

    def _do_update_delete_progress(self, percent, current_file, current_count, total_count):
        self.delete_stats["percent"] = percent
        self.delete_stats["current_file"] = current_file
        self.delete_stats["deleted"] = current_count
        self.delete_stats["total"] = total_count
        
        if hasattr(self, 'del_progress_bar') and self.del_progress_bar.winfo_exists():
            fraction = percent / 100.0
            self.del_progress_bar.set(fraction)
            safe_relx = max(0.02, min(0.98, fraction))
            self.del_knife_label.place(relx=safe_relx, rely=0.5, anchor="center")
            self.del_progress_percentage.configure(text=f"{percent}%")
            if len(current_file) > 60:
                current_file = "..." + current_file[-57:]
            self.del_progress_label.configure(text=current_file)
            self.del_files_count_label.configure(text=f"Archivos eliminados: {current_count} / {total_count}")
            
    def _finish_delete(self, error_msg=None):
        self.is_deleting = False
        if hasattr(self, 'delete_progress_card') and self.delete_progress_card.winfo_exists():
            self.delete_progress_card.destroy()
        if error_msg:
            messagebox.showerror("Error", f"Ocurrió un error al borrar:\n{error_msg}")
        self._refresh_destination_files()

    def _delete_folder_background(self, path):
        self.is_deleting = True
        self.cancel_delete_flag = False
        self.delete_stats = {"percent": 0, "current_file": "Escaneando...", "deleted": 0, "total": 0}
        
        import os, stat
        
        # 1. Contar archivos para la barra de progreso
        total_files = 1  # 1 para la carpeta raíz
        for root, dirs, files in os.walk(path):
            total_files += len(files) + len(dirs)
            
        deleted = 0
        
        def custom_rmtree(p):
            nonlocal deleted
            if self.cancel_delete_flag:
                return
            try:
                items = os.listdir(p)
            except Exception:
                return
            
            for item in items:
                if self.cancel_delete_flag:
                    return
                full_item_path = os.path.join(p, item)
                try:
                    if os.path.isdir(full_item_path):
                        custom_rmtree(full_item_path)
                    else:
                        # Fix WinError 5 for git objects or read-only files
                        os.chmod(full_item_path, stat.S_IWRITE)
                        os.remove(full_item_path)
                        deleted += 1
                        
                        if deleted % 50 == 0 or deleted >= total_files:
                            percent = int((deleted / total_files) * 100)
                            percent = min(100, max(0, percent))
                            self.after(0, lambda pct=percent, d=deleted, t=total_files, n=item: self._do_update_delete_progress(pct, n, d, t))
                except Exception:
                    pass
            
            if self.cancel_delete_flag:
                return
                
            try:
                os.chmod(p, stat.S_IWRITE)
                os.rmdir(p)
                deleted += 1
                
                if deleted % 50 == 0 or deleted >= total_files:
                    percent = int((deleted / total_files) * 100)
                    percent = min(100, max(0, percent))
                    self.after(0, lambda pct=percent, d=deleted, t=total_files, n=os.path.basename(p): self._do_update_delete_progress(pct, n, d, t))
            except Exception:
                pass
                
        try:
            custom_rmtree(path)
            if self.cancel_delete_flag:
                self.after(0, lambda: self._finish_delete("Operación cancelada por el usuario. El trofeo ha quedado a medio borrar."))
            else:
                self.after(0, self._finish_delete)
        except Exception as e:
            self.after(0, lambda err=str(e): self._finish_delete(err))

    # ═══════════════════════════════════════════════════════
    #  PÁGINA: AJUSTES
    # ═══════════════════════════════════════════════════════
    
    def _show_settings(self):
        """Muestra la página de configuración."""
        self._clear_content()
        self._set_active_nav("settings")
        self.current_page = "settings"
        
        scroll = ctk.CTkScrollableFrame(
            self.content_area, fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        if hasattr(self, 'img_settings') and self.img_settings:
            ctk.CTkLabel(header, text="", image=self.img_settings).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(
            header, text="El Código",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(side="left", pady=(0, 5))
        
        ctk.CTkLabel(
            scroll, text="Las reglas que gobiernan al pasajero oscuro.",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 20))
        
        # ── Programación de Backup ──
        schedule_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        schedule_card.pack(fill="x", pady=(0, 15))
        
        schedule_inner = ctk.CTkFrame(schedule_card, fg_color="transparent")
        schedule_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            schedule_inner, text="📅  Programación del Backup",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(0, 15))
        
        schedule = self.config.get("schedule", {})
        
        # Habilitado
        enable_frame = ctk.CTkFrame(schedule_inner, fg_color="transparent")
        enable_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            enable_frame, text="Activar programación:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.schedule_enabled_var = ctk.BooleanVar(value=schedule.get("enabled", True))
        ctk.CTkSwitch(
            enable_frame, text="",
            variable=self.schedule_enabled_var,
            progress_color=COLORS["blood_bright"],
            button_color=COLORS["text_secondary"],
            button_hover_color=COLORS["blood_glow"],
            command=self._save_settings
        ).pack(side="right")
        
        # Día de la semana
        day_frame = ctk.CTkFrame(schedule_inner, fg_color="transparent")
        day_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            day_frame, text="Día:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        days_en = list(DAY_MAP.keys())
        days_es = [DAY_NAMES_ES[d] for d in days_en]
        current_day = schedule.get("day", "Sunday")
        current_day_es = DAY_NAMES_ES.get(current_day, "Domingo")
        
        self.day_var = ctk.StringVar(value=current_day_es)
        day_menu = ctk.CTkOptionMenu(
            day_frame, values=days_es,
            variable=self.day_var,
            fg_color=COLORS["bg_input"],
            button_color=COLORS["blood_red"],
            button_hover_color=COLORS["blood_bright"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_hover_color=COLORS["sidebar_active"],
            font=FONTS["body"],
            width=150,
            command=lambda _: self._save_settings()
        )
        day_menu.pack(side="right")
        
        # Hora
        hour_frame = ctk.CTkFrame(schedule_inner, fg_color="transparent")
        hour_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            hour_frame, text="Hora:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        time_subframe = ctk.CTkFrame(hour_frame, fg_color="transparent")
        time_subframe.pack(side="right")
        
        hours = [f"{h:02d}" for h in range(24)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]
        
        self.hour_var = ctk.StringVar(value=f"{schedule.get('hour', 12):02d}")
        ctk.CTkOptionMenu(
            time_subframe, values=hours,
            variable=self.hour_var,
            fg_color=COLORS["bg_input"],
            button_color=COLORS["blood_red"],
            button_hover_color=COLORS["blood_bright"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_hover_color=COLORS["sidebar_active"],
            font=FONTS["mono"],
            width=80,
            command=lambda _: self._save_settings()
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            time_subframe, text=":",
            font=FONTS["mono_large"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.minute_var = ctk.StringVar(value=f"{schedule.get('minute', 0):02d}")
        ctk.CTkOptionMenu(
            time_subframe, values=minutes,
            variable=self.minute_var,
            fg_color=COLORS["bg_input"],
            button_color=COLORS["blood_red"],
            button_hover_color=COLORS["blood_bright"],
            dropdown_fg_color=COLORS["bg_card"],
            dropdown_hover_color=COLORS["sidebar_active"],
            font=FONTS["mono"],
            width=80,
            command=lambda _: self._save_settings()
        ).pack(side="left", padx=(5, 0))
        
        # ── Recordatorio ──
        reminder_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        reminder_card.pack(fill="x", pady=(0, 15))
        
        reminder_inner = ctk.CTkFrame(reminder_card, fg_color="transparent")
        reminder_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            reminder_inner, text="🔔  Recordatorios",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            reminder_inner,
            text="Si no has hecho backup, recibirás un recordatorio a la hora indicada.",
            font=FONTS["small"],
            text_color=COLORS["text_dim"]
        ).pack(anchor="w", pady=(0, 10))
        
        reminder = self.config.get("reminder", {})
        
        reminder_enable = ctk.CTkFrame(reminder_inner, fg_color="transparent")
        reminder_enable.pack(fill="x")
        
        ctk.CTkLabel(
            reminder_enable, text="Activar recordatorios:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.reminder_enabled_var = ctk.BooleanVar(value=reminder.get("enabled", True))
        ctk.CTkSwitch(
            reminder_enable, text="",
            variable=self.reminder_enabled_var,
            progress_color=COLORS["blood_bright"],
            button_color=COLORS["text_secondary"],
            button_hover_color=COLORS["blood_glow"],
            command=self._save_settings
        ).pack(side="right")
        
        # ── Popup al conectar SSD ──
        popup_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        popup_card.pack(fill="x", pady=(0, 15))
        
        popup_inner = ctk.CTkFrame(popup_card, fg_color="transparent")
        popup_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            popup_inner, text="🔌  Popup al Conectar SSD",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(0, 10))
        
        popup_toggle = ctk.CTkFrame(popup_inner, fg_color="transparent")
        popup_toggle.pack(fill="x")
        
        ctk.CTkLabel(
            popup_toggle,
            text="Mostrar popup cuando se detecta el SSD:",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.popup_enabled_var = ctk.BooleanVar(
            value=self.config.get("show_popup_on_ssd_connect", True)
        )
        ctk.CTkSwitch(
            popup_toggle, text="",
            variable=self.popup_enabled_var,
            progress_color=COLORS["blood_bright"],
            button_color=COLORS["text_secondary"],
            button_hover_color=COLORS["blood_glow"],
            command=self._save_settings
        ).pack(side="right")
        
        # ── Robocopy flags ──
        robo_card = ctk.CTkFrame(
            scroll, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"]
        )
        robo_card.pack(fill="x", pady=(0, 15))
        
        robo_inner = ctk.CTkFrame(robo_card, fg_color="transparent")
        robo_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            robo_inner, text="⚡  Robocopy (Avanzado)",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            robo_inner,
            text="Flags que se pasan a robocopy. Solo modifica si sabes lo que haces.",
            font=FONTS["small"],
            text_color=COLORS["text_dim"]
        ).pack(anchor="w", pady=(0, 10))
        
        self.robocopy_entry = ctk.CTkEntry(
            robo_inner,
            font=FONTS["mono"],
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            height=38
        )
        self.robocopy_entry.pack(fill="x")
        self.robocopy_entry.insert(0, self.config.get("robocopy_flags", "/MIR /FFT /Z /XA:H /W:5 /R:3"))
        self.robocopy_entry.bind("<FocusOut>", lambda e: self._save_settings())
    
    def _save_settings(self):
        """Guarda todos los ajustes en config.json."""
        # Mapear día de español a inglés
        day_es = self.day_var.get()
        day_en = "Sunday"
        for en, es in DAY_NAMES_ES.items():
            if es == day_es:
                day_en = en
                break
        
        self.config["schedule"]["enabled"] = self.schedule_enabled_var.get()
        self.config["schedule"]["day"] = day_en
        self.config["schedule"]["hour"] = int(self.hour_var.get())
        self.config["schedule"]["minute"] = int(self.minute_var.get())
        
        self.config["reminder"]["enabled"] = self.reminder_enabled_var.get()
        self.config["reminder"]["day"] = day_en
        self.config["reminder"]["hour"] = int(self.hour_var.get())
        self.config["reminder"]["minute"] = int(self.minute_var.get())
        
        self.config["show_popup_on_ssd_connect"] = self.popup_enabled_var.get()
        
        if hasattr(self, 'robocopy_entry'):
            self.config["robocopy_flags"] = self.robocopy_entry.get()
        
        config_manager.save_config(self.config)
    
    # ═══════════════════════════════════════════════════════
    #  ACCIONES DE BACKUP
    # ═══════════════════════════════════════════════════════
    
    def _on_backup_click(self):
        """Inicia un backup manual."""
        if self.backup_engine.is_running:
            messagebox.showinfo("En progreso", "Ya hay un backup en curso.")
            return
        
        if not self.config.get("source_folders"):
            messagebox.showwarning(
                "Sin carpetas",
                "No has configurado carpetas de origen.\nVe a la sección 'Carpetas' para añadirlas."
            )
            return
        
        if not self.config.get("destination_path"):
            messagebox.showwarning(
                "Sin destino",
                "No has configurado un destino.\nVe a 'Carpetas' y selecciona tu SSD."
            )
            return
        
        # Mostrar barra de progreso
        if hasattr(self, 'progress_card'):
            self.progress_card.pack(fill="x", pady=(0, 15))
        
        # Configurar callbacks
        self.backup_engine.set_callbacks(
            on_progress=self._update_progress,
            on_status=self._update_status,
            on_complete=self._on_backup_complete
        )
        
        self.btn_backup.configure(
            text="✕  DETENER BACKUP",
            fg_color=COLORS["border"],
            hover_color=COLORS["blood_dim"],
            state="normal",
            command=self._on_cancel_backup
        )
        self.progress_bar.set(0)
        self.backup_engine.start_backup()
    
    def _on_cancel_backup(self):
        """Cancela el backup en curso preguntando primero al usuario."""
        if not self.backup_engine.is_running:
            return
            
        popup = ctk.CTkToplevel(self)
        popup.title("Abortar Ritual")
        popup.geometry("400x260")
        popup.configure(fg_color=COLORS["bg_dark"])
        popup.transient(self)
        popup.grab_set()
        popup.attributes("-topmost", True)
        
        # Centrar
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 200
        y = (popup.winfo_screenheight() // 2) - 130
        popup.geometry(f"+{x}+{y}")
        
        # Borde superior decorativo
        top_bar = ctk.CTkFrame(popup, height=4, fg_color=COLORS["warning"], corner_radius=0)
        top_bar.pack(fill="x")
        
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            content, text="⚠ ¿Detener el Ritual?",
            font=("Consolas", 18, "bold"),
            text_color=COLORS["warning"]
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            content, 
            text="Si cancelas ahora, los archivos descargados durante esta sesión serán eliminados (Rollback) para asegurar que el backup quede intacto.\n\n¿Estás seguro?",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            wraplength=340,
            justify="center"
        ).pack(pady=(0, 25))
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", expand=True)
        
        def confirm():
            popup.destroy()
            if self.backup_engine.is_running:
                self.backup_engine.cancel_backup(rollback=True)
            
        def cancel():
            popup.destroy()
            
        ctk.CTkButton(
            btn_frame, text="No, continuar",
            font=FONTS["button"],
            fg_color="transparent",
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_secondary"],
            border_width=1, border_color=COLORS["border"],
            height=36, width=140, corner_radius=8,
            command=cancel
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame, text="Sí, abortar",
            font=FONTS["button"],
            fg_color=COLORS["error"],
            hover_color=COLORS["blood_dim"],
            text_color="white",
            height=36, width=140, corner_radius=8,
            command=confirm
        ).pack(side="right")
    
    def _update_progress(self, percent, current_file, current_count=None, total_count=None):
        """Callback: actualiza la barra de progreso (thread-safe)."""
        # Guardar el último estado (el hilo de backup puede llamar miles de veces)
        self._last_progress_state = (percent, current_file, current_count, total_count)
        
        # Solo encolar UN after() a la vez. Si ya hay uno pendiente, no encolar otro.
        # Esto evita saturar el event loop de tkinter con miles de callbacks.
        if not getattr(self, '_progress_update_pending', False):
            self._progress_update_pending = True
            self.after(50, self._process_pending_progress)

    def _process_pending_progress(self):
        """Aplica la última actualización de progreso a la UI."""
        self._progress_update_pending = False
        if hasattr(self, '_last_progress_state'):
            self._do_update_progress(*self._last_progress_state)
    
    def _do_update_progress(self, percent, current_file, current_count, total_count):
        """Actualiza la UI de progreso en el hilo principal."""
        fraction = percent / 100.0
        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(fraction)
        
        if hasattr(self, 'knife_label'):
            # Mover el cuchillo a lo largo de la barra (relx de 0 a 1)
            # Acotamos ligeramente para que no se salga de los bordes
            safe_relx = max(0.02, min(0.98, fraction))
            self.knife_label.place(relx=safe_relx, rely=0.5, anchor="center")
            
        if hasattr(self, 'progress_percentage'):
            self.progress_percentage.configure(text=f"{percent}%")
            
        if hasattr(self, 'progress_label'):
            # Truncar el nombre de archivo si es muy largo
            if len(current_file) > 60:
                current_file = "..." + current_file[-57:]
            self.progress_label.configure(text=current_file)
            
        if hasattr(self, 'files_count_label') and current_count is not None and total_count is not None:
            self.files_count_label.configure(text=f"Archivos guardados: {current_count} / {total_count}")
    
    def _update_status(self, message):
        """Callback: actualiza el mensaje de estado (thread-safe)."""
        self.after(0, lambda: self._do_update_status(message))
    
    def _do_update_status(self, message):
        """Actualiza el label de estado en el hilo principal."""
        if hasattr(self, 'progress_status'):
            self.progress_status.configure(text=message)
    
    def _on_backup_complete(self, success, entry):
        """Callback: cuando termina el backup (thread-safe)."""
        self.after(0, lambda: self._do_backup_complete(success, entry))
    
    def _do_backup_complete(self, success, entry):
        """Actualiza la UI al completar el backup."""
        # Ocultar la tarjeta de progreso
        if hasattr(self, 'progress_card') and self.progress_card.winfo_exists():
            self.progress_card.pack_forget()
        
        # Restaurar botón de backup
        if hasattr(self, 'btn_backup'):
            self.btn_backup.configure(
                text="▶  INICIAR BACKUP",
                fg_color=COLORS["blood_red"],
                hover_color=COLORS["blood_bright"],
                state="normal",
                command=self._on_backup_click
            )
        
        # Siempre mostrar popup de completado (éxito, error, al día)
        self._show_completion_popup(success, entry)
        
        # Refrescar dashboard para actualizar estadísticas e historial
        self.config = config_manager.load_config()
        if self.current_page == "dashboard":
            self._show_dashboard()
    
    def _show_completion_popup(self, success, entry):
        """Muestra un popup temático de éxito o fallo del backup."""
        popup = ctk.CTkToplevel(self)
        popup.title("Ritual Completado" if success else "Ritual Fallido")
        popup.geometry("420x380")
        popup.configure(fg_color=COLORS["bg_dark"])
        popup.transient(self)
        popup.grab_set()
        popup.attributes("-topmost", True)
        popup.overrideredirect(True)
        
        # Centrar
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 210
        y = (popup.winfo_screenheight() // 2) - 190
        popup.geometry(f"+{x}+{y}")
        
        # Borde decorativo superior rojo
        top_bar = ctk.CTkFrame(popup, height=4, fg_color=COLORS["blood_bright"] if success else COLORS["error"], corner_radius=0)
        top_bar.pack(fill="x")
        
        # Contenido
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        files_copied = entry.get('files_copied', 0)
        up_to_date = success and files_copied == 0
        
        # ── Tick rojo con círculo rojo (Canvas) ──
        import tkinter as tk
        icon_size = 80
        canvas = tk.Canvas(content, width=icon_size, height=icon_size, 
                          bg=COLORS["bg_dark"], highlightthickness=0)
        canvas.pack(pady=(10, 8))
        
        if success:
            circle_color = COLORS["blood_bright"]
            # Círculo rojo
            canvas.create_oval(4, 4, icon_size-4, icon_size-4, outline=circle_color, width=4)
            # Tick (✓) dentro del círculo
            cx, cy = icon_size // 2, icon_size // 2
            canvas.create_line(cx-18, cy+2, cx-6, cy+14, fill=circle_color, width=4, capstyle="round")
            canvas.create_line(cx-6, cy+14, cx+22, cy-14, fill=circle_color, width=4, capstyle="round")
        else:
            circle_color = COLORS["error"]
            # Círculo rojo error
            canvas.create_oval(4, 4, icon_size-4, icon_size-4, outline=circle_color, width=4)
            # X dentro del círculo
            cx, cy = icon_size // 2, icon_size // 2
            canvas.create_line(cx-14, cy-14, cx+14, cy+14, fill=circle_color, width=4, capstyle="round")
            canvas.create_line(cx+14, cy-14, cx-14, cy+14, fill=circle_color, width=4, capstyle="round")
        
        # Título
        if up_to_date:
            title = "Estás al día"
            subtitle = "No había archivos nuevos que copiar.\nTu SSD está completamente sincronizado."
        elif success:
            title = "Ritual Completado"
            subtitle = "Todos los archivos han sido guardados correctamente."
        else:
            title = "Error en el Ritual"
            subtitle = "Hubo un problema durante el backup."
        
        ctk.CTkLabel(
            content, text=title,
            font=("Consolas", 18, "bold"),
            text_color=COLORS["blood_bright"] if success else COLORS["error"]
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            content, text=subtitle,
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            justify="center"
        ).pack(pady=(0, 12))
        
        # Info de estadísticas
        files = entry.get('files_copied', 0)
        size = entry.get('size_display', '0 B')
        duration = entry.get('duration_display', '0s')
        
        if not up_to_date and files > 0:
            info_frame = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            info_frame.pack(fill="x", pady=(0, 10))
            
            info_text = f"📄 Archivos: {files}   💾 Tamaño: {size}   ⏱ {duration}"
            ctk.CTkLabel(
                info_frame, text=info_text,
                font=FONTS["small"],
                text_color=COLORS["text_secondary"],
                justify="center"
            ).pack(padx=15, pady=10)
        
        # Botón Aceptar
        ctk.CTkButton(
            content, text="Aceptar",
            font=FONTS["button"],
            fg_color=COLORS["blood_bright"] if success else COLORS["error"],
            hover_color=COLORS["blood_dim"],
            text_color="white",
            height=40, width=160, corner_radius=20,
            command=popup.destroy
        ).pack(pady=(5, 0))

    # ═══════════════════════════════════════════════════════
    #  SERVICIOS EN SEGUNDO PLANO
    # ═══════════════════════════════════════════════════════
    
    def _start_background_services(self):
        """Inicia los servicios en segundo plano (SSD Watcher + Scheduler)."""
        # SSD Watcher
        self.ssd_watcher = SSDWatcher(
            config=self.config,
            on_ssd_connected=self._on_ssd_connected,
            on_ssd_disconnected=self._on_ssd_disconnected,
            check_interval=3
        )
        self.ssd_watcher.start()
        
        # Scheduler
        self.scheduler = BackupScheduler(
            on_reminder=self._on_reminder,
            on_backup_due=self._on_backup_due,
            check_interval=60
        )
        self.scheduler.start()
    
    def _on_ssd_connected(self, ssd_info):
        """Callback: se llama cuando el SSD objetivo se conecta."""
        self.ssd_connected = True
        self.ssd_info = ssd_info
        
        self.after(0, lambda: self._update_ssd_indicator(True, ssd_info))
        
        # Mostrar popup si está habilitado
        if self.config.get("show_popup_on_ssd_connect", True):
            self.after(500, lambda: self._show_ssd_popup(ssd_info))
    
    def _on_ssd_disconnected(self):
        """Callback: se llama cuando el SSD se desconecta."""
        self.ssd_connected = False
        self.ssd_info = None
        self.after(0, lambda: self._update_ssd_indicator(False, None))
    
    def _update_ssd_indicator(self, connected, info):
        """Actualiza el indicador de SSD en la sidebar."""
        if connected and info:
            self.ssd_status_icon.configure(text_color=COLORS["success"])
            self.ssd_status_label.configure(
                text=f"{info['label']} ({info['letter']}:)\n{info['free_display']} libres",
                text_color=COLORS["success"],
                justify="left"
            )
        else:
            self.ssd_status_icon.configure(text_color=COLORS["blood_dim"])
            self.ssd_status_label.configure(
                text="SSD Desconectado",
                text_color=COLORS["text_dim"],
                justify="left"
            )
    
    def _show_ssd_popup(self, ssd_info):
        """Muestra el popup de confirmación cuando se conecta el SSD."""
        popup = ctk.CTkToplevel(self)
        popup.title("SSD Detectado")
        popup.geometry("520x360")
        popup.configure(fg_color=COLORS["bg_dark"])
        popup.transient(self)
        popup.grab_set()
        popup.attributes("-topmost", True)
        popup.overrideredirect(True)  # Eliminar bordes nativos (X, barra azul)
        
        # Centrar
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 260
        y = (popup.winfo_screenheight() // 2) - 180
        popup.geometry(f"+{x}+{y}")
        
        # Borde rojo superior decorativo (La línea de arriba roja)
        top_bar = ctk.CTkFrame(popup, height=4, fg_color=COLORS["blood_bright"], corner_radius=0)
        top_bar.pack(fill="x")
        
        # Contenido
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        if hasattr(self, 'img_knife_large') and self.img_knife_large:
            ctk.CTkLabel(content, text="", image=self.img_knife_large).pack(pady=(10, 10))
        else:
            ctk.CTkLabel(
                content, text="🔪",
                font=("Segoe UI Emoji", 48)
            ).pack(pady=(10, 10))
        
        ctk.CTkLabel(
            content, text="El pasajero oscuro ha despertado.",
            font=("Consolas", 18, "bold"),
            text_color=COLORS["blood_bright"]
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            content,
            text=f"SSD detectado: {ssd_info['label']} ({ssd_info['letter']}:)\n"
                 f"Espacio libre: {ssd_info['free_display']}",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            justify="center"
        ).pack(pady=(5, 20))
        
        # Botones con estilo Neón / Redondos
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(
            btn_frame, text="Sí, hazlo",
            font=FONTS["button"],
            fg_color=COLORS["blood_bright"],
            hover_color="#FF4C4C",
            text_color="white",
            height=45, width=160, corner_radius=22,
            border_width=2, border_color="#FF4C4C",
            command=lambda: self._popup_start_backup(popup)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            btn_frame, text="No, ahora no",
            font=FONTS["button"],
            fg_color="#2A2A2A",
            hover_color="#3A3A3A",
            text_color=COLORS["text_dim"],
            height=45, width=160, corner_radius=22,
            command=popup.destroy
        ).pack(side="left")
    
    def _popup_start_backup(self, popup):
        """Inicia backup desde el popup y lo cierra."""
        popup.destroy()
        self._show_dashboard()
        self.after(300, self._on_backup_click)
    
    def _on_reminder(self, message):
        """Callback: recordatorio de backup pendiente."""
        self.after(0, lambda: self._show_reminder(message))
    
    def _show_reminder(self, message):
        """Muestra una notificación de recordatorio."""
        messagebox.showinfo("⏰ Recordatorio - Dark Passenger", message)
    
    def _on_backup_due(self):
        """Callback: el backup está pendiente."""
        pass  # El popup del SSD ya se encarga
    
    def _check_startup_state(self):
        """Comprueba el estado al iniciar la app (backup pendiente, etc.)."""
        self.config = config_manager.load_config()
        
        # Comprobar si el SSD está conectado ahora mismo
        ssd = is_target_ssd_connected(self.config)
        if ssd:
            self._update_ssd_indicator(True, ssd)
            self.ssd_connected = True
            self.ssd_info = ssd
            
            # Mostrar el popup si el SSD está conectado y está activado en config
            # (El hilo vigilante ya no lo lanzará doble porque ya inicializa su estado)
            if self.config.get("show_popup_on_ssd_connect", True):
                self.after(500, lambda: self._show_ssd_popup(ssd))
    
    # ═══════════════════════════════════════════════════════
    #  CIERRE
    # ═══════════════════════════════════════════════════════
    
    def _on_close(self):
        """Maneja el cierre de la ventana."""
        if self.backup_engine.is_running:
            if not messagebox.askyesno(
                "Backup en curso",
                "Hay un backup en curso. ¿Seguro que quieres cerrar?\nEl backup se cancelará."
            ):
                return
            self.backup_engine.cancel_backup()
        
        # Detener servicios
        if self.ssd_watcher:
            self.ssd_watcher.stop()
        if self.scheduler:
            self.scheduler.stop()
        
        self._release_app_lock()
        self.destroy()
        
    def _acquire_app_lock(self):
        import os
        app_data = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "DarkPassengerBackup")
        os.makedirs(app_data, exist_ok=True)
        self._lock_file = os.path.join(app_data, "app.lock")
        try:
            with open(self._lock_file, "w") as f:
                f.write(str(os.getpid()))
        except Exception:
            pass
            
    def _release_app_lock(self):
        import os
        try:
            if hasattr(self, '_lock_file') and os.path.exists(self._lock_file):
                os.remove(self._lock_file)
        except Exception:
            pass


def main():
    """Punto de entrada principal."""
    # Aceptar argumento --ssd-popup (usado por startup_watcher.py)
    # No necesitamos procesarlo aquí porque _check_startup_state
    # ya detecta si el SSD está conectado y muestra el popup
    app = DarkPassengerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
