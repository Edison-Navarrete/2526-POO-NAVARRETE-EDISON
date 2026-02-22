# Abrir y cerrar archivo (Metodo with).py
# -----------------------------------------------------------
# Este módulo implementa:
# 1) El menú principal que orquesta la ejecución de los otros cinco módulos
#    cuyos nombres contienen espacios/paréntesis (se usan importlib por ruta).
# 2) Un CRUD mínimo del inventario usando with open(...) sobre inventario.txt.
# -----------------------------------------------------------

import importlib.util
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "inventario.txt"
CABECERA = "id,nombre,cantidad,precio\n"

# Nombres de los otros scripts (exactos)
MOD_TRAD = BASE_DIR / "Abrir y cerrar archivo (Metodo tradicional).py"
MOD_MOD_LINEA = BASE_DIR / "Modificando linea especifica.py"
MOD_TRY_EXCEPT = BASE_DIR / "Try y Except.py"
MOD_ELSE_FNFE = BASE_DIR / "Else y Finally (FileNotFound).py"
MOD_ELSE_ZDIV = BASE_DIR / "Else y Finally (ZeroDivision).py"

def cargar_modulo_por_ruta(nombre_modulo, ruta_archivo: Path):
    # Carga un módulo por ruta de archivo, permitiendo nombres con espacios/paréntesis.
    spec = importlib.util.spec_from_file_location(nombre_modulo, str(ruta_archivo))
    if spec is None or spec.loader is None:
        raise ImportError(f"No fue posible generar el spec para {ruta_archivo.name}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# -------------------- CRUD con with --------------------

def asegurar_archivo():
    # Garantiza que exista inventario.txt con cabecera.
    if not RUTA.exists():
        try:
            with open(RUTA, "w") as f:
                f.write(CABECERA)
            print("INFO: inventario.txt no existia; se creo con cabecera.")
        except PermissionError:
            print("ERROR: permiso denegado para crear inventario.txt.")
        except OSError as e:
            print(f"ERROR: no fue posible crear inventario.txt: {e}")

def listar():
    try:
        with open(RUTA, "r") as f:
            lineas = f.read().strip().splitlines()
        if len(lineas) <= 1:
            print("Inventario vacio.")
            return
        print("Listado de productos:")
        for linea in lineas[1:]:
            print("  ", linea)
    except FileNotFoundError:
        print("ADVERTENCIA: el archivo no existe.")
    except PermissionError:
        print("ERROR: permiso denegado al leer.")
    except OSError as e:
        print(f"ERROR: problema del sistema al leer: {e}")

def anadir():
    idp = input("ID: ").strip()
    nombre = input("Nombre: ").strip()
    try:
        cantidad = int(input("Cantidad: ").strip())
        precio = float(input("Precio: ").strip())
    except Exception:
        print("Datos invalidos. La cantidad debe ser entero y el precio numerico.")
        return
    if not idp or not nombre or cantidad < 0 or precio < 0:
        print("Datos invalidos. No se admiten vacios ni valores negativos.")
        return

    try:
        asegurar_archivo()
        con_duplicado = False
        with open(RUTA, "r") as f:
            for i, linea in enumerate(f):
                if i == 0:
                    continue
                partes = linea.strip().split(",")
                if partes and partes[0] == idp:
                    con_duplicado = True
                    break
        if con_duplicado:
            print("El ID ya existe. No se puede duplicar.")
            return

        with open(RUTA, "a") as f:
            f.write(f"{idp},{nombre},{cantidad},{precio}\n")
        print("OK: producto anadido y guardado en archivo.")
    except PermissionError:
        print("ERROR: permiso denegado al escribir.")
    except OSError as e:
        print(f"ERROR: problema del sistema al escribir: {e}")

def eliminar():
    objetivo = input("ID a eliminar: ").strip()
    try:
        if not RUTA.exists():
            print("No existe inventario.txt.")
            return
        with open(RUTA, "r") as f:
            lineas = f.read().splitlines()
        if not lineas:
            print("Archivo vacio.")
            return

        nuevas = [lineas[0]]
        borrado = False
        for linea in lineas[1:]:
            partes = linea.split(",")
            if partes and partes[0] == objetivo:
                borrado = True
                continue
            nuevas.append(linea)

        with open(RUTA, "w") as f:
            f.write("\n".join(nuevas) + ("\n" if nuevas else ""))

        if borrado:
            print("OK: producto eliminado y cambios guardados.")
        else:
            print("No se encontro el ID indicado.")
    except PermissionError:
        print("ERROR: permiso denegado al modificar el archivo.")
    except OSError as e:
        print(f"ERROR: problema del sistema al reescribir: {e}")

# -------------------- Menús --------------------

def menu_principal():
    print("\n===== MENU PRINCIPAL (with) =====")
    print("1) Inventario: Listar")
    print("2) Inventario: Anadir")
    print("3) Inventario: Eliminar")
    print("4) Ejecutar: Metodo tradicional (crear y leer)")
    print("5) Ejecutar: Modificar linea especifica")
    print("6) Ejecutar: Try y Except")
    print("7) Ejecutar: Else y Finally (FileNotFound)")
    print("8) Ejecutar: Else y Finally (ZeroDivision)")
    print("0) Salir")

def main():
    asegurar_archivo()
    while True:
        menu_principal()
        op = input("Opcion: ").strip()
        if op == "1":
            listar()
        elif op == "2":
            anadir()
        elif op == "3":
            eliminar()
        elif op == "4":
            try:
                mod = cargar_modulo_por_ruta("trad", MOD_TRAD)
                mod.run()
            except Exception as e:
                print(f"No fue posible ejecutar el modulo tradicional: {e}")
        elif op == "5":
            try:
                mod = cargar_modulo_por_ruta("mod_linea", MOD_MOD_LINEA)
                mod.run()
            except Exception as e:
                print(f"No fue posible ejecutar Modificando linea especifica: {e}")
        elif op == "6":
            try:
                mod = cargar_modulo_por_ruta("try_except", MOD_TRY_EXCEPT)
                mod.run()
            except Exception as e:
                print(f"No fue posible ejecutar Try y Except: {e}")
        elif op == "7":
            try:
                mod = cargar_modulo_por_ruta("else_fnf", MOD_ELSE_FNFE)
                mod.run()
            except Exception as e:
                print(f"No fue posible ejecutar Else y Finally (FileNotFound): {e}")
        elif op == "8":
            try:
                mod = cargar_modulo_por_ruta("else_zdiv", MOD_ELSE_ZDIV)
                mod.run()
            except Exception as e:
                print(f"No fue posible ejecutar Else y Finally (ZeroDivision): {e}")
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()