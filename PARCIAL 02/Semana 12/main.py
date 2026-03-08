# main.py
# -------------------------------------------------------------
# Menú interactivo de consola para gestionar la Biblioteca Digital.
# Integra:
#   - Carga/creación de inventario.txt junto a main.py (robusto con pathlib).
#   - Menú de opciones para: usuarios, libros, préstamos, búsquedas e historial.
#   - Manejo de excepciones con mensajes claros.
#   - Opción para guardar el catálogo actual en inventario.txt.
# -------------------------------------------------------------

from biblioteca.biblioteca import (
    Biblioteca,
    UsuarioYaExisteError,
    UsuarioNoEncontradoError,
    UsuarioConPrestamosActivosError,
    LibroYaExisteError,
    LibroNoEncontradoError,
    LibroPrestadoError,
    PrestamoNoEncontradoError,
)
from biblioteca.modelos import Libro
from pathlib import Path
import os

# --------------------- Rutas robustas ------------------------
BASE_DIR = Path(__file__).resolve().parent
RUTA_INVENTARIO = BASE_DIR / "inventario.txt"


# --------------------- Utilidades E/S ------------------------
def limpiar_pantalla():
    # Limpia pantalla (funciona en Windows y en la mayoría de entornos)
    os.system("cls" if os.name == "nt" else "clear")


def pausar(msg: str = "Presiona Enter para continuar..."):
    input(msg)


def pedir_no_vacio(prompt: str) -> str:
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("Entrada vacía, intenta nuevamente.")


def pedir_opcion(opciones_validas: set[str]) -> str:
    while True:
        op = input("Elige una opción: ").strip()
        if op in opciones_validas:
            return op
        print(f"Opción inválida. Opciones válidas: {sorted(opciones_validas)}")


# ------------------- Inventario (TXT) ------------------------
def asegurar_inventario(ruta: Path):
    """
    Si inventario.txt no existe, lo crea con una cabecera y algunos ejemplos.
    """
    if ruta.exists():
        return
    CABECERA = "# Formato: ISBN;TITULO;AUTOR;CATEGORIA\n"
    EJEMPLO = (
        "1111;Python Básico;Guido V.;Programación\n"
        "2222;Cálculo I;James Stewart;Matemáticas\n"
        "3333;Algoritmos;S. Sedgewick;Informática\n"
        "4444;Fundamentos de Bases de Datos;Silberschatz;Informática\n"
        "5555;Estructuras de Datos;Mark A. Weiss;Informática\n"
    )
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(CABECERA)
            f.write(EJEMPLO)
        print("inventario.txt no existía; se creó con ejemplos.")
    except Exception as e:
        print(f"No fue posible crear inventario.txt: {e}")


def cargar_inventario_desde_txt(bib: Biblioteca, ruta: Path) -> int:
    """
    Carga libros desde inventario.txt (ignora líneas vacías/comentarios).
    Retorna cuántos libros se agregaron.
    """
    agregados = 0
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for i, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                partes = [p.strip() for p in linea.split(";")]
                if len(partes) != 4:
                    print(f"[AVISO] Línea {i} inválida: {linea}")
                    continue
                isbn, titulo, autor, categoria = partes
                try:
                    bib.añadir_libro(Libro(isbn, (titulo, autor), categoria))
                    agregados += 1
                except LibroYaExisteError:
                    # Evita detener la carga por duplicados en el archivo
                    print(f"[AVISO] ISBN duplicado en línea {i}: {isbn}")
                except Exception as e:
                    print(f"[AVISO] Línea {i}: no se agregó ISBN {isbn}: {e}")
    except FileNotFoundError:
        print("inventario.txt no encontrado (se creará si lo decides).")
    except UnicodeDecodeError:
        print("Codificación inválida. Guarde inventario.txt como UTF-8.")
    return agregados


def guardar_catalogo_a_txt(bib: Biblioteca, ruta: Path):
    """
    Sobrescribe inventario.txt con el catálogo actual de la biblioteca.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("# Formato: ISBN;TITULO;AUTOR;CATEGORIA\n")
            for libro in bib.libros.values():
                f.write(f"{libro.isbn};{libro.titulo};{libro.autor};{libro.categoria}\n")
        print(f"Catálogo guardado en: {ruta.name}")
    except Exception as e:
        print(f"No fue posible guardar el catálogo: {e}")


# --------------------- Operaciones UI ------------------------
def ui_registrar_usuario(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Registrar usuario ===")
    nombre = pedir_no_vacio("Nombre: ")
    user_id = pedir_no_vacio("ID de usuario (único): ")
    try:
        bib.registrar_usuario(nombre, user_id)
        print(f"Usuario registrado: {nombre} ({user_id})")
    except UsuarioYaExisteError as e:
        print(e)
    pausar()


def ui_dar_baja_usuario(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Dar de baja usuario ===")
    user_id = pedir_no_vacio("ID de usuario: ")
    try:
        bib.dar_de_baja_usuario(user_id)
        print(f"Usuario dado de baja: {user_id}")
    except (UsuarioNoEncontradoError, UsuarioConPrestamosActivosError) as e:
        print(e)
    pausar()


def ui_añadir_libro(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Añadir libro ===")
    isbn = pedir_no_vacio("ISBN: ")
    titulo = pedir_no_vacio("Título: ")
    autor = pedir_no_vacio("Autor: ")
    categoria = pedir_no_vacio("Categoría: ")
    try:
        bib.añadir_libro(Libro(isbn, (titulo, autor), categoria))
        print(f"Libro añadido: {titulo} - {autor} (ISBN: {isbn})")
    except LibroYaExisteError as e:
        print(e)
    pausar()


def ui_quitar_libro(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Quitar libro ===")
    isbn = pedir_no_vacio("ISBN: ")
    try:
        bib.quitar_libro(isbn)
        print(f"Libro eliminado del catálogo: {isbn}")
    except (LibroNoEncontradoError, LibroPrestadoError) as e:
        print(e)
    pausar()


def ui_prestar_libro(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Prestar libro ===")
    isbn = pedir_no_vacio("ISBN: ")
    user_id = pedir_no_vacio("ID de usuario: ")
    try:
        bib.prestar_libro(isbn, user_id)
        print(f"Préstamo realizado: ISBN {isbn} → {user_id}")
    except (LibroNoEncontradoError, UsuarioNoEncontradoError, LibroPrestadoError) as e:
        print(e)
    pausar()


def ui_devolver_libro(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Devolver libro ===")
    isbn = pedir_no_vacio("ISBN: ")
    user_id = pedir_no_vacio("ID de usuario: ")
    try:
        bib.devolver_libro(isbn, user_id)
        print(f"Devolución registrada: ISBN {isbn} de {user_id}")
    except PrestamoNoEncontradoError as e:
        print(e)
    pausar()


def ui_busquedas(bib: Biblioteca):
    while True:
        limpiar_pantalla()
        print("=== Búsquedas ===")
        print("1) Por título")
        print("2) Por autor")
        print("3) Por categoría")
        print("0) Volver")
        op = pedir_opcion({"1", "2", "3", "0"})
        if op == "0":
            return
        texto = pedir_no_vacio("Texto a buscar: ")
        if op == "1":
            resultados = bib.buscar_por_titulo(texto)
        elif op == "2":
            resultados = bib.buscar_por_autor(texto)
        else:
            resultados = bib.buscar_por_categoria(texto)

        print("\n--- Resultados ---")
        if resultados:
            for l in resultados:
                print(f"- {l}")
        else:
            print("No se encontraron coincidencias.")
        pausar()


def ui_listar_prestamos_usuario(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Libros prestados por usuario ===")
    user_id = pedir_no_vacio("ID de usuario: ")
    try:
        libros = bib.listar_prestamos_usuario(user_id)
        if libros:
            print("\n--- Préstamos activos ---")
            for l in libros:
                print(f"- {l}")
        else:
            print("El usuario no tiene préstamos activos.")
    except UsuarioNoEncontradoError as e:
        print(e)
    pausar()


def ui_historial(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Historial de acciones ===")
    if not bib.historial:
        print("No hay eventos registrados.")
    else:
        for h in bib.historial:
            # (fecha, acción, isbn, user_id)
            print(h)
    pausar()


def ui_guardar_catalogo(bib: Biblioteca):
    limpiar_pantalla()
    print("=== Guardar catálogo en inventario.txt ===")
    guardar_catalogo_a_txt(bib, RUTA_INVENTARIO)
    pausar()


# ------------------------ Menú principal ---------------------
def menu_principal():
    bib = Biblioteca()

    # Carga de inventario
    asegurar_inventario(RUTA_INVENTARIO)
    cargados = cargar_inventario_desde_txt(bib, RUTA_INVENTARIO)

    while True:
        limpiar_pantalla()
        print("=== SISTEMA DE BIBLIOTECA DIGITAL ===\n")
        print(f"Libros en catálogo: {len(bib.libros)} (cargados: {cargados})")
        print(f"Usuarios registrados: {len(bib.usuarios)}")
        print(f"Préstamos activos: {len(bib.prestamos)}\n")

        print("1) Registrar usuario")
        print("2) Dar de baja usuario")
        print("3) Añadir libro")
        print("4) Quitar libro")
        print("5) Prestar libro")
        print("6) Devolver libro")
        print("7) Buscar libros")
        print("8) Listar préstamos por usuario")
        print("9) Ver historial")
        print("S) Guardar catálogo en inventario.txt")
        print("0) Salir")

        op = pedir_opcion({"1", "2", "3", "4", "5", "6", "7", "8", "9", "S", "s", "0"})

        if op == "1":
            ui_registrar_usuario(bib)
        elif op == "2":
            ui_dar_baja_usuario(bib)
        elif op == "3":
            ui_añadir_libro(bib)
        elif op == "4":
            ui_quitar_libro(bib)
        elif op == "5":
            ui_prestar_libro(bib)
        elif op == "6":
            ui_devolver_libro(bib)
        elif op == "7":
            ui_busquedas(bib)
        elif op == "8":
            ui_listar_prestamos_usuario(bib)
        elif op == "9":
            ui_historial(bib)
        elif op in {"S", "s"}:
            ui_guardar_catalogo(bib)
        elif op == "0":
            limpiar_pantalla()
            print("Gracias por usar la Biblioteca Digital.")
            break


if __name__ == "__main__":
    menu_principal()