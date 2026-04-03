"""
Módulo main.py

Punto de entrada de la aplicación completa.
"""

import sys
import os
# ====================== SOLUCIÓN AL ERROR ModuleNotFoundError ======================
# Esta línea fuerza a Python a encontrar todos los archivos .py de la carpeta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# =================================================================================

import tkinter as tk
from controlador_app import ControladorApp

if __name__ == "__main__":
    root = tk.Tk()
    # La aplicación completa se inicia aquí cumpliendo todos los requisitos:
    # interfaz gráfica, botones, lista con feedback visual, eventos de clic
    # y atajos de teclado (Enter, C, Delete/D y Escape).
    app = ControladorApp(root)
    root.mainloop()
