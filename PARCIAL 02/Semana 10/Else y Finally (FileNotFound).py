# Else y Finally (FileNotFound).py
# -----------------------------------------------------------
# Demuestra try/except/else/finally con lectura de archivo.
# Se define run() para integrarse con el menú principal.
# -----------------------------------------------------------

def leer_con_else_finally(ruta):
    f = None
    try:
        f = open(ruta, "r")
        contenido = f.read()
    except FileNotFoundError:
        print("El archivo no existe.")
    except PermissionError:
        print("Permiso denegado.")
    else:
        print("Lectura correcta. Contenido:")
        print(contenido if contenido else "(vacio)")
    finally:
        if f:
            f.close()
        print("Finally ejecutado (cierre de recursos).")

def run():
    ruta = input("Ruta de archivo: ").strip()
    leer_con_else_finally(ruta)

if __name__ == "__main__":
    run()