# actividad_inventario/dominio/producto.py
# Requisito: Clase Producto con atributos (ID, nombre, cantidad, precio) y
#            métodos para obtener/establecer (validando en properties).
# Decisión: Validación centralizada en setters para mantener consistencia de datos.

from __future__ import annotations

class Producto:
    def __init__(self, id: str, nombre: str, cantidad: int, precio: float) -> None:
        # Se usan los setters para aplicar validaciones desde el constructor.
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # --- ID ---
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        v = str(value).strip()
        if not v:
            raise ValueError("El ID no puede estar vacío.")
        self._id = v

    # --- Nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        v = str(value).strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = v

    # --- Cantidad ---
    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int) -> None:
        try:
            iv = int(value)
        except Exception:
            raise ValueError("La cantidad debe ser un entero.")
        if iv < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = iv

    # --- Precio ---
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float) -> None:
        try:
            fv = float(value)
        except Exception:
            raise ValueError("El precio debe ser un número.")
        if fv < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = fv

    def __str__(self) -> str:
        # Soporta el requisito de "mostrar productos" de forma legible.
        return f"[{self.id}] {self.nombre} | Cant.: {self.cantidad} | Precio: ${self.precio:.2f}"

    # --- Serialización para archivos (Almacenamiento en Archivos) ---
    def to_dict(self) -> dict:
        # Se serializa a un dict simple para guardarlo en JSON.
        return {"id": self.id, "nombre": self.nombre, "cantidad": self.cantidad, "precio": self.precio}

    @classmethod
    def from_dict(cls, data: dict) -> "Producto":
        # Se deserializa desde un dict cargado desde JSON.
        return cls(
            id=data.get("id", ""),
            nombre=data.get("nombre", ""),
            cantidad=data.get("cantidad", 0),
            precio=data.get("precio", 0.0),
        )
    #