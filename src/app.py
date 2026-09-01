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
                
            icon_path = os.path.join(base_dir, "app_hd.ico")
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
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        self.ssd_status_frame = ctk.CTkFrame(
            self.sidebar, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1,
            border_color=COLORS["border"]
        )
        self.ssd_status_frame.pack(fill="x", padx=12, pady=(5, 15))
        
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
            self.content_area, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ── Header ──
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header, text="Tonight's the night.",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(side="left")
        
        # Botón principal de Backup
        self.btn_backup = ctk.CTkButton(
            header, text="▶  INICIAR BACKUP",
            font=FONTS["button"],
            fg_color=COLORS["blood_red"],
            hover_color=COLORS["blood_bright"],
            text_color="white",
            height=42, width=200,
            corner_radius=8,
            command=self._on_backup_click
        )
        self.btn_backup.pack(side="right")
        
        # ── Tarjetas de estado ──
        stats = history_manager.get_stats()
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="card")
        
        self._create_stat_card(cards_frame, 0, "Total Backups", str(stats["total_backups"]), "📊")
        self._create_stat_card(cards_frame, 1, "Exitosos", str(stats["successful"]), "✅")
        self._create_stat_card(cards_frame, 2, "Datos Copiados", stats.get("total_bytes_display", "0 B"), "💾")
        self._create_stat_card(cards_frame, 3, "Archivos", str(stats["total_files"]), "📄")
        
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
        if BackupScheduler.is_backup_overdue(self.config):
            overdue_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
            overdue_frame.pack(fill="x", pady=(5, 0))
            ctk.CTkLabel(
                overdue_frame, text="⚠  ¡Backup pendiente! Conecta tu SSD.",
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
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_inner,
            fg_color=COLORS["progress_bg"],
            progress_color=COLORS["blood_red"],
            height=12, corner_radius=6
        )
        self.progress_bar.pack(fill="x", pady=(15, 5))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_inner, text="Preparando...",
            font=FONTS["mono"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        self.progress_label.pack(anchor="w", pady=(5, 0))
        
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
        
        ctk.CTkLabel(
            top, text=icon,
            font=("Segoe UI Emoji", 18)
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
            self.content_area, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        ctk.CTkLabel(
            scroll, text="La Mesa de Trabajo",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            scroll, text="Selecciona las carpetas que el pasajero oscuro debe proteger.",
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
            self.content_area, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
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
    #  PÁGINA: AJUSTES
    # ═══════════════════════════════════════════════════════
    
    def _show_settings(self):
        """Muestra la página de configuración."""
        self._clear_content()
        self._set_active_nav("settings")
        self.current_page = "settings"
        
        scroll = ctk.CTkScrollableFrame(
            self.content_area, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["blood_dim"]
        )
        scroll.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        ctk.CTkLabel(
            scroll, text="El Código",
            font=FONTS["title"],
            text_color=COLORS["blood_bright"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
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
            text="⏸  EN CURSO...",
            fg_color=COLORS["blood_dim"],
            state="disabled"
        )
        
        self.backup_engine.start_backup()
    
    def _on_cancel_backup(self):
        """Cancela el backup en curso."""
        if self.backup_engine.is_running:
            self.backup_engine.cancel_backup()
    
    def _update_progress(self, percent, current_file):
        """Callback: actualiza la barra de progreso (thread-safe)."""
        self.after(0, lambda: self._do_update_progress(percent, current_file))
    
    def _do_update_progress(self, percent, current_file):
        """Actualiza la UI de progreso en el hilo principal."""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(percent / 100)
        if hasattr(self, 'progress_label'):
            self.progress_label.configure(text=f"{percent}% - {current_file}")
    
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
        if hasattr(self, 'btn_backup'):
            self.btn_backup.configure(
                text="▶  INICIAR BACKUP",
                fg_color=COLORS["blood_red"],
                state="normal"
            )
        
        if success:
            messagebox.showinfo(
                "Ritual completado",
                f"✅ Backup completado exitosamente.\n\n"
                f"Archivos copiados: {entry.get('files_copied', 0)}\n"
                f"Tamaño: {entry.get('size_display', '0 B')}\n"
                f"Duración: {entry.get('duration_display', '0s')}"
            )
        
        # Refrescar dashboard
        if self.current_page == "dashboard":
            self._show_dashboard()
    
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
                text=f"{info['label']} ({info['letter']}:)",
                text_color=COLORS["success"]
            )
        else:
            self.ssd_status_icon.configure(text_color=COLORS["blood_dim"])
            self.ssd_status_label.configure(
                text="SSD Desconectado",
                text_color=COLORS["text_dim"]
            )
    
    def _show_ssd_popup(self, ssd_info):
        """Muestra el popup de confirmación cuando se conecta el SSD."""
        popup = ctk.CTkToplevel(self)
        popup.title("SSD Detectado")
        popup.geometry("480x320")
        popup.configure(fg_color=COLORS["bg_dark"])
        popup.transient(self)
        popup.grab_set()
        popup.attributes("-topmost", True)
        
        # Centrar
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 240
        y = (popup.winfo_screenheight() // 2) - 160
        popup.geometry(f"+{x}+{y}")
        
        # Borde rojo superior decorativo
        top_bar = ctk.CTkFrame(popup, height=4, fg_color=COLORS["blood_bright"], corner_radius=0)
        top_bar.pack(fill="x")
        
        # Contenido
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            content, text="🔪",
            font=("Segoe UI Emoji", 48)
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            content, text="El pasajero oscuro ha despertado.",
            font=("Consolas", 16, "bold"),
            text_color=COLORS["blood_bright"]
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            content,
            text=f"SSD detectado: {ssd_info['label']} ({ssd_info['letter']}:)\n"
                 f"Espacio libre: {ssd_info['free_display']}",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            justify="center"
        ).pack(pady=(5, 5))
        
        ctk.CTkLabel(
            content, text="¿Iniciamos el backup ahora?",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"]
        ).pack(pady=(5, 15))
        
        # Botones
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(
            btn_frame, text="🔪  Sí, hazlo",
            font=FONTS["button"],
            fg_color=COLORS["blood_red"],
            hover_color=COLORS["blood_bright"],
            text_color="white",
            height=42, width=160, corner_radius=8,
            command=lambda: self._popup_start_backup(popup)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame, text="No, ahora no",
            font=FONTS["button"],
            fg_color=COLORS["border_light"],
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_secondary"],
            height=42, width=160, corner_radius=8,
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
