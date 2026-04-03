"""
Módulo componentes_contenedores.py

Contiene los contenedores (frames) que organizan visualmente la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk


class ContenedorEntrada(ttk.LabelFrame):
    """Contenedor para el campo de entrada de nuevas tareas."""

    def __init__(self, parent):
        super().__init__(parent, text="Nueva Tarea", padding=10)
        self.entry = ttk.Entry(self, font=("Arial", 12), width=60)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))


class ContenedorLista(ttk.LabelFrame):
    """Contenedor para la lista de tareas con feedback visual."""

    def __init__(self, parent):
        super().__init__(parent, text="Lista de Tareas", padding=10)
        self.tree = ttk.Treeview(
            self,
            columns=("estado", "descripcion"),
            show="headings",
            height=18
        )
        self.tree.heading("estado", text="Estado")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("estado", width=70, anchor="center")
        self.tree.column("descripcion", width=680)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configuración de tags para diferenciar visualmente tareas pendientes y completadas
        self.tree.tag_configure("pendiente", foreground="#2c3e50")
        self.tree.tag_configure(
            "completada",
            foreground="#28a745",
            font=("Arial", 11, "overstrike")
        )


class ContenedorBotones(ttk.Frame):
    """Contenedor para los botones de acción (añadir, marcar, eliminar)."""

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.btn_agregar = ttk.Button(
            self, text="Añadir Tarea", command=controlador.agregar_tarea
        )
        self.btn_agregar.pack(side=tk.LEFT, padx=8)

        self.btn_marcar = ttk.Button(
            self, text="Marcar como Completada", command=controlador.marcar_completada
        )
        self.btn_marcar.pack(side=tk.LEFT, padx=8)

        self.btn_eliminar = ttk.Button(
            self, text="Eliminar Tarea", command=controlador.eliminar_tarea
        )
        self.btn_eliminar.pack(side=tk.LEFT, padx=8)


class ContenedorAtajos(ttk.LabelFrame):
    """Contenedor que muestra permanentemente los comandos de teclado."""

    def __init__(self, parent):
        super().__init__(parent, text="Atajos de Teclado Disponibles", padding=12)
        texto = (
            "Enter          →  Añadir nueva tarea\n"
            "C o Mayús+C    →  Marcar como completada\n"
            "Delete o D     →  Eliminar tarea seleccionada\n"
            "Escape         →  Cerrar la aplicación"
        )
        self.label = ttk.Label(self, text=texto, justify=tk.LEFT, font=("Consolas", 10))
        self.label.pack(anchor=tk.W)