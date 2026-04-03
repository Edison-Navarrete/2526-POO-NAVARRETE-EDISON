"""
Módulo interfaces_gui.py

Implementa la vista completa de la aplicación.
"""

import tkinter as tk
from tkinter import ttk
from componentes_contenedores import (
    ContenedorEntrada,
    ContenedorLista,
    ContenedorBotones,
    ContenedorAtajos,
)


class InterfazGUI:
    """Clase que construye y gestiona toda la interfaz gráfica."""

    def __init__(self, root: tk.Tk, controlador):
        self.root = root
        self.controlador = controlador

        # Configuración profesional de la ventana
        self.root.title("Gestor de Tareas Pendientes")
        self.root.geometry("920x720")
        self.root.resizable(True, True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 11, "bold"))
        style.configure("TLabel", font=("Arial", 11))

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=25)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.cont_entrada = ContenedorEntrada(main_frame)
        self.cont_entrada.pack(fill=tk.X, pady=(0, 20))

        self.cont_lista = ContenedorLista(main_frame)
        self.cont_lista.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.cont_botones = ContenedorBotones(main_frame, self.controlador)
        self.cont_botones.pack(fill=tk.X, pady=(0, 20))

        self.cont_atajos = ContenedorAtajos(main_frame)
        self.cont_atajos.pack(fill=tk.X)

        self.entry = self.cont_entrada.entry
        self.tree = self.cont_lista.tree

    def actualizar_lista(self, tareas: list):
        """Actualiza el Treeview con las tareas actuales aplicando feedback visual."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, tarea in enumerate(tareas):
            prefix = "✅" if tarea.completada else "☐"
            tag = "completada" if tarea.completada else "pendiente"
            self.tree.insert(
                "", tk.END, iid=str(idx),
                values=(prefix, tarea.descripcion),
                tags=(tag,)
            )

    def obtener_seleccion(self) -> int | None:
        """Retorna el índice de la tarea seleccionada en la lista o None."""
        seleccion = self.tree.selection()
        if seleccion:
            return int(seleccion[0])
        return None