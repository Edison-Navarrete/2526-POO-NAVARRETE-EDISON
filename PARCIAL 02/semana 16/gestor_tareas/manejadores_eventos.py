"""
Módulo manejedores_eventos.py

Contiene los manejadores de eventos de clic y atajos de teclado.
"""

import tkinter as tk
from tkinter import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controlador_app import ControladorApp


class ManejadoresEventos:
    """Agrupa todos los manejadores de eventos."""

    def __init__(self, controlador: 'ControladorApp'):
        self.controlador = controlador

    def manejar_agregar(self, event: Event):
        """Manejador del atajo Enter para añadir tarea."""
        self.controlador.agregar_tarea()

    def manejar_marcar(self, event: Event):
        """Manejador del atajo C para marcar como completada."""
        self.controlador.marcar_completada()

    def manejar_eliminar(self, event: Event):
        """Manejador de los atajos Delete / D para eliminar tarea."""
        self.controlador.eliminar_tarea()

    def manejar_cerrar(self, event: Event):
        """Manejador del atajo Escape para cerrar la aplicación."""
        self.controlador.cerrar_aplicacion()