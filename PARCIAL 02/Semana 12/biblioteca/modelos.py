# modelos.py
# -------------------------------------------------------------
# Se definen las clases principales del dominio: Libro y Usuario.
# - Libro utiliza una tupla (titulo, autor) para cumplir la
#   inmutabilidad requerida en estos atributos.
# - Usuario mantiene una lista de ISBNs para gestionar sus préstamos.
# -------------------------------------------------------------

class Libro:
    # ---------------------------------------------------------
    # Se modela un Libro donde:
    # * 'metadata' es una tupla (titulo, autor) para garantizar
    #   inmutabilidad de estos datos una vez creados.
    # * 'categoria' permite búsquedas temáticas.
    # * 'isbn' será la clave del diccionario en Biblioteca.
    # ---------------------------------------------------------
    def __init__(self, isbn: str, metadata: tuple[str, str], categoria: str):
        self.isbn = isbn
        # Aunque internamente se guarda en atributos separados,
        # la fuente original es la tupla inmutable 'metadata'.
        self.titulo = metadata[0]
        self.autor = metadata[1]
        self.categoria = categoria

    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn}, Categoría: {self.categoria})"


class Usuario:
    # ---------------------------------------------------------
    # Se modela un Usuario donde:
    # * 'user_id' debe ser único (se asegura con un conjunto en Biblioteca).
    # * 'libros_prestados' es una lista de ISBNs para reflejar
    #   los préstamos activos del usuario (cumple el uso de listas).
    # ---------------------------------------------------------
    def __init__(self, nombre: str, user_id: str):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []  # lista de ISBNs

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.user_id})"

