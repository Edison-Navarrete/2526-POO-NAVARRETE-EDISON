"""
Módulo tareas_datos.py

Contiene el modelo de datos de la aplicación.
"""

class Tarea:
    """Clase que representa una tarea individual con su estado."""

    def __init__(self, descripcion: str, completada: bool = False):
        self.descripcion = descripcion.strip()
        self.completada = completada


class TareaManager:
    """Clase responsable de gestionar la lista de tareas en memoria."""

    def __init__(self):
        self.tareas: list[Tarea] = []

    def agregar_tarea(self, descripcion: str) -> bool:
        """Añade una nueva tarea si la descripción no está vacía."""
        if not descripcion or not descripcion.strip():
            return False
        self.tareas.append(Tarea(descripcion))
        return True

    def marcar_completada(self, indice: int) -> bool:
        """Marca como completada (o desmarca) la tarea en el índice indicado."""
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completada = not self.tareas[indice].completada
            return True
        return False

    def eliminar_tarea(self, indice: int) -> bool:
        """Elimina la tarea en el índice indicado."""
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
            return True
        return False

    def obtener_tareas(self) -> list[Tarea]:
        """Retorna la lista completa de tareas para la vista."""
        return self.tareas