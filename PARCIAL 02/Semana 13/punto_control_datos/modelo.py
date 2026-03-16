"""
Módulo: modelo
Responsabilidad: gestionar los datos (lista de ítems) y exponer operaciones de negocio.
"""

from typing import List


class ItemStore:
    """
    Clase de dominio que representa un almacén sencillo de ítems en memoria.
    Proporciona operaciones para agregar, eliminar y consultar la colección.
    """

    def __init__(self) -> None:
        # --- Colección interna donde se mantendrán los datos mostrados en la GUI.
        self._items: List[str] = []

    # --- Operación de negocio para incorporar un nuevo elemento validando entrada.
    def agregar(self, texto: str) -> str:
        """
        Agrega un ítem no vacío al almacén.

        :param texto: Cadena con el contenido a guardar.
        :return: El texto almacenado (normalizado).
        :raises ValueError: Si el texto está vacío o contiene solo espacios.
        """
        normalizado = (texto or "").strip()
        if not normalizado:
            raise ValueError("El texto no puede estar vacío.")
        self._items.append(normalizado)
        return normalizado

    # --- Operación de negocio para eliminar por posición sincronizada con la vista.
    def eliminar_por_indice(self, idx: int) -> str:
        """
        Elimina el elemento en la posición indicada.

        :param idx: Índice del elemento a eliminar.
        :return: El texto eliminado.
        :raises IndexError: Si el índice no existe.
        """
        eliminado = self._items.pop(idx)
        return eliminado

    # --- Provee una copia de la lista para mostrar en la interfaz sin exponer el estado interno.
    def listar(self) -> List[str]:
        """
        Devuelve una copia de los ítems actuales.

        :return: Lista de cadenas almacenadas.
        """
        return list(self._items)
