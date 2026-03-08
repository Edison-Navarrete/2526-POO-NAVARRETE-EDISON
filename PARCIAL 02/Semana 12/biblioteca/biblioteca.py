# biblioteca.py
# -------------------------------------------------------------
# Se implementa la clase orquestadora 'Biblioteca' y las
# excepciones personalizadas para un control de flujo claro.
#
# Estructuras clave que cumplen los requerimientos:
# * Diccionario 'libros':   ISBN -> Libro        (acceso O(1)).
# * Diccionario 'usuarios': ID   -> Usuario      (acceso O(1)).
# * Conjunto 'ids_usuario': asegura unicidad de IDs de usuario.
# * Diccionario 'prestamos': ISBN -> user_id     (quién tiene qué).
# * Lista 'historial': registra (fecha, acción, isbn, user_id).
#
# Funcionalidades cubiertas:
# - Añadir/Quitar libros
# - Registrar/Dar de baja usuarios
# - Prestar/Devolver libros (con historial)
# - Buscar por título/autor/categoría (tolerante a acentos y mayúsculas)
# - Listar libros prestados por usuario
# -------------------------------------------------------------

from .modelos import Libro, Usuario
from datetime import datetime
import unicodedata


# -------------------------------------------------------------
# Excepciones personalizadas
# Se definen para comunicar errores de negocio de forma precisa.
# -------------------------------------------------------------
class UsuarioYaExisteError(Exception):
    pass

class UsuarioNoEncontradoError(Exception):
    pass

class UsuarioConPrestamosActivosError(Exception):
    pass

class LibroYaExisteError(Exception):
    pass

class LibroNoEncontradoError(Exception):
    pass

class LibroPrestadoError(Exception):
    pass

class PrestamoNoEncontradoError(Exception):
    pass


# -------------------------------------------------------------
# Utilidad de normalización
# Permite búsquedas case-insensitive y tolerantes a acentos.
# -------------------------------------------------------------
def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto if not unicodedata.combining(c))


# -------------------------------------------------------------
# Clase principal: Biblioteca
# Encapsula colecciones, préstamos e historial.
# -------------------------------------------------------------
class Biblioteca:
    def __init__(self):
        # -----------------------------------------------------
        # Diccionario de catálogo: ISBN -> Libro (requerimiento).
        # -----------------------------------------------------
        self.libros = {}

        # -----------------------------------------------------
        # Diccionario de usuarios: ID -> Usuario para accesos O(1).
        # -----------------------------------------------------
        self.usuarios = {}

        # -----------------------------------------------------
        # Conjunto de IDs para garantizar unicidad (requerimiento).
        # -----------------------------------------------------
        self.ids_usuario = set()

        # -----------------------------------------------------
        # Estado de préstamos: ISBN -> user_id (un libro por usuario a la vez).
        # -----------------------------------------------------
        self.prestamos = {}

        # -----------------------------------------------------
        # Historial de auditoría: (timestamp, acción, isbn, user_id).
        # -----------------------------------------------------
        self.historial = []

    # =========================================================
    # GESTIÓN DE USUARIOS
    # =========================================================
    def registrar_usuario(self, nombre: str, user_id: str):
        # -----------------------------------------------------
        # Registra un usuario nuevo:
        # * Verifica unicidad con 'ids_usuario' (conjunto).
        # * Añade entrada en 'usuarios' (diccionario).
        # -----------------------------------------------------
        if user_id in self.ids_usuario:
            raise UsuarioYaExisteError("El ID ya está registrado.")
        usuario = Usuario(nombre, user_id)
        self.usuarios[user_id] = usuario
        self.ids_usuario.add(user_id)
        return usuario

    def dar_de_baja_usuario(self, user_id: str):
        # -----------------------------------------------------
        # Da de baja un usuario:
        # * Debe existir.
        # * No debe tener libros prestados activos.
        # * Se elimina de 'usuarios' y 'ids_usuario'.
        # -----------------------------------------------------
        if user_id not in self.usuarios:
            raise UsuarioNoEncontradoError("El usuario no existe.")

        usuario = self.usuarios[user_id]
        if usuario.libros_prestados:
            raise UsuarioConPrestamosActivosError("El usuario tiene libros prestados.")

        del self.usuarios[user_id]
        self.ids_usuario.remove(user_id)

    # =========================================================
    # GESTIÓN DE LIBROS
    # =========================================================
    def añadir_libro(self, libro: Libro):
        # -----------------------------------------------------
        # Añade un libro al catálogo:
        # * La clave es el ISBN en el diccionario 'libros'.
        # * Impide duplicados por ISBN.
        # -----------------------------------------------------
        if libro.isbn in self.libros:
            raise LibroYaExisteError("Ya existe un libro con ese ISBN.")
        self.libros[libro.isbn] = libro

    def quitar_libro(self, isbn: str):
        # -----------------------------------------------------
        # Quita un libro del catálogo:
        # * Debe existir.
        # * No puede estar prestado en ese momento.
        # -----------------------------------------------------
        if isbn not in self.libros:
            raise LibroNoEncontradoError("El libro no existe.")

        if isbn in self.prestamos:
            raise LibroPrestadoError("No se puede quitar un libro que está prestado.")

        del self.libros[isbn]

    # =========================================================
    # PRÉSTAMOS
    # =========================================================
    def prestar_libro(self, isbn: str, user_id: str):
        # -----------------------------------------------------
        # Realiza un préstamo:
        # * Verifica existencia de libro y usuario.
        # * Confirma disponibilidad (no prestado).
        # * Actualiza 'prestamos' y la lista del usuario.
        # * Registra evento en 'historial' con timestamp.
        # -----------------------------------------------------
        if isbn not in self.libros:
            raise LibroNoEncontradoError("No existe ese libro.")
        if user_id not in self.usuarios:
            raise UsuarioNoEncontradoError("El usuario no existe.")
        if isbn in self.prestamos:
            raise LibroPrestadoError("El libro ya está prestado.")

        self.prestamos[isbn] = user_id
        self.usuarios[user_id].libros_prestados.append(isbn)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historial.append((fecha, "PRESTAMO", isbn, user_id))

    def devolver_libro(self, isbn: str, user_id: str):
        # -----------------------------------------------------
        # Registra una devolución:
        # * Verifica que el préstamo exista y pertenezca al usuario.
        # * Quita de 'prestamos' y de la lista del usuario.
        # * Loguea el evento en el 'historial'.
        # -----------------------------------------------------
        if isbn not in self.prestamos:
            raise PrestamoNoEncontradoError("Ese libro no está prestado.")

        if self.prestamos[isbn] != user_id:
            raise PrestamoNoEncontradoError("Ese libro no lo tiene ese usuario.")

        del self.prestamos[isbn]
        self.usuarios[user_id].libros_prestados.remove(isbn)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historial.append((fecha, "DEVOLUCION", isbn, user_id))

    # =========================================================
    # BÚSQUEDAS
    # =========================================================
    def buscar_por_titulo(self, texto: str):
        # -----------------------------------------------------
        # Búsqueda por título:
        # * Case-insensitive y tolerante a acentos con 'normalizar'.
        # * Devuelve coincidencias parciales.
        # -----------------------------------------------------
        texto = normalizar(texto)
        return [l for l in self.libros.values() if texto in normalizar(l.titulo)]

    def buscar_por_autor(self, texto: str):
        # -----------------------------------------------------
        # Búsqueda por autor (mismas reglas de normalización).
        # -----------------------------------------------------
        texto = normalizar(texto)
        return [l for l in self.libros.values() if texto in normalizar(l.autor)]

    def buscar_por_categoria(self, texto: str):
        # -----------------------------------------------------
        # Búsqueda por categoría (mismas reglas de normalización).
        # -----------------------------------------------------
        texto = normalizar(texto)
        return [l for l in self.libros.values() if texto in normalizar(l.categoria)]

    # =========================================================
    # LISTAR PRÉSTAMOS DE UN USUARIO
    # =========================================================
    def listar_prestamos_usuario(self, user_id: str):
        # -----------------------------------------------------
        # Retorna los libros actualmente prestados a un usuario:
        # * Usa la lista de ISBNs del usuario para armar objetos Libro.
        # -----------------------------------------------------
        if user_id not in self.usuarios:
            raise UsuarioNoEncontradoError("El usuario no existe.")
        return [self.libros[isbn] for isbn in self.usuarios[user_id].libros_prestados]