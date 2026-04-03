"""
Módulo controlador_app.py

Controla la comunicación entre modelo, vista y eventos.
"""

import tkinter as tk
from tareas_datos import TareaManager
from interfaces_gui import InterfazGUI
from manejadores_eventos import ManejadoresEventos
from conceptos_eventos import SHORTCUTS


class ControladorApp:
    """Controlador principal de la aplicación."""

    def __init__(self, root: tk.Tk):
        self.model = TareaManager()
        self.view = InterfazGUI(root, self)
        self.manejadores = ManejadoresEventos(self)
        self.bindear_eventos()
        self.actualizar_vista()

    def bindear_eventos(self):
        """Asigna todos los atajos de teclado requeridos."""
        self.view.entry.bind(SHORTCUTS["agregar"], self.manejadores.manejar_agregar)

        self.view.root.bind(SHORTCUTS["completar"], self.manejadores.manejar_marcar)
        self.view.root.bind(SHORTCUTS["completar_mayus"], self.manejadores.manejar_marcar)
        self.view.root.bind(SHORTCUTS["eliminar"], self.manejadores.manejar_eliminar)
        self.view.root.bind(SHORTCUTS["eliminar_alt"], self.manejadores.manejar_eliminar)
        self.view.root.bind(SHORTCUTS["eliminar_alt_mayus"], self.manejadores.manejar_eliminar)
        self.view.root.bind(SHORTCUTS["cerrar"], self.manejadores.manejar_cerrar)

    def agregar_tarea(self):
        """Añade tarea y actualiza la vista."""
        descripcion = self.view.entry.get().strip()
        if self.model.agregar_tarea(descripcion):
            self.view.entry.delete(0, tk.END)
            self.actualizar_vista()

    def marcar_completada(self):
        """Marca la tarea seleccionada y actualiza la vista."""
        indice = self.view.obtener_seleccion()
        if indice is not None:
            if self.model.marcar_completada(indice):
                self.actualizar_vista()

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada y actualiza la vista."""
        indice = self.view.obtener_seleccion()
        if indice is not None:
            if self.model.eliminar_tarea(indice):
                self.actualizar_vista()

    def cerrar_aplicacion(self):
        """Cierra la ventana."""
        self.view.root.destroy()

    def actualizar_vista(self):
        """Solicita las tareas al modelo y las envía a la vista."""
        tareas = self.model.obtener_tareas()
        self.view.actualizar_lista(tareas)