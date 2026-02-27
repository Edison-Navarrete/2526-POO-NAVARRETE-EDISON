# actividad_inventario/aplicacion/inventario.py
# Requisito: Clase Inventario que use una colección adecuada para almacenar productos,
#            con métodos para CRUD, búsqueda por nombre y listado.
# Integración de Colecciones (explícito):
#   - dict[str, Producto]: índice principal por ID para búsqueda/actualización O(1) promedio.
#   - set[str]: conjunto de IDs para reforzar unicidad (demuestra uso de conjuntos).
#   - list[Producto]: se devuelve en listados para recorrer/ordenar sin exponer el dict interno.
#   - tuple[int, float]: resumen inmutable (n_items_distintos, valor_total).
#
# Nota: El set de IDs es redundante con las claves del dict, pero se mantiene para
#       cumplir explícitamente el uso de CONJUNTOS según la consigna.

from __future__ import annotations
from typing import Dict, List, Tuple
from actividad_inventario.dominio.producto import Producto


class Inventario:
    def __init__(self) -> None:
        self._items: Dict[str, Producto] = {}   # dict para acceso por ID (clave-valor)
        self._ids: set[str] = set()            # set para demostrar unicidad/miembros

    # --- Requisito: Añadir nuevos productos ---
    def agregar_producto(self, p: Producto) -> None:
        # Se garantiza ID único con dict y set.
        if p.id in self._ids:
            raise ValueError(f"Ya existe un producto con ID '{p.id}'.")
        self._items[p.id] = p
        self._ids.add(p.id)

    # --- Requisito: Eliminar productos por ID ---
    def eliminar_por_id(self, id_prod: str) -> None:
        if id_prod not in self._ids:
            raise ValueError(f"No existe un producto con ID '{id_prod}'.")
        self._items.pop(id_prod, None)
        self._ids.discard(id_prod)

    # --- Requisito: Actualizar cantidad de un producto ---
    def actualizar_cantidad(self, id_prod: str, nueva_cantidad: int) -> None:
        if id_prod not in self._ids:
            raise ValueError(f"No existe un producto con ID '{id_prod}'.")
        self._items[id_prod].cantidad = nueva_cantidad

    # --- Requisito: Actualizar precio de un producto ---
    def actualizar_precio(self, id_prod: str, nuevo_precio: float) -> None:
        if id_prod not in self._ids:
            raise ValueError(f"No existe un producto con ID '{id_prod}'.")
        self._items[id_prod].precio = nuevo_precio

    # --- Requisito: Buscar y mostrar productos por nombre ---
    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        clave = (texto or "").strip().casefold()
        if not clave:
            return []
        # Se usa list para retornar una colección recorrible sin exponer el dict interno.
        return [p for p in self._items.values() if clave in p.nombre.casefold()]

    # --- Requisito: Mostrar todos los productos ---
    def listar_todos(self) -> List[Producto]:
        return list(self._items.values())

    # --- Integración de colecciones: resumen como tupla inmutable (tuple) ---
    def resumen(self) -> Tuple[int, float]:
        n_items = len(self._items)
        total = sum(p.cantidad * p.precio for p in self._items.values())
        return (n_items, round(total, 2))

    # --- Almacenamiento en Archivos: serialización/deserialización ---
    def a_dict(self) -> Dict[str, dict]:
        # Se serializa como { id: {...} } para JSON.
        return {pid: prod.to_dict() for pid, prod in self._items.items()}

    @classmethod
    def desde_dict(cls, data: Dict[str, dict]) -> "Inventario":
        inv = cls()
        if not isinstance(data, dict):
            return inv
        for pid, pdata in data.items():
            try:
                prod = Producto.from_dict(pdata)
                if not prod.id:
                    prod.id = str(pid)
                inv.agregar_producto(prod)
            except Exception:
                # Si algún registro está mal formado, se ignora y se continúa.
                continue
        return inv