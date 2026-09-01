"""
Dark Passenger Backup - main.py
Punto de entrada principal de la aplicación.
"""

import sys
import os

# Asegurar que el directorio del script está en el path
if getattr(sys, 'frozen', False):
    # Ejecutando como .exe (PyInstaller)
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.app import main

if __name__ == "__main__":
    main()
