# Try y Except.py
# -----------------------------------------------------------
# Demuestra manejo basico de excepciones al intentar leer un archivo.
# Se define run() para integrarse con el menú principal.
# -----------------------------------------------------------

def leer_archivo(ruta):
    try:
        with open(ruta, "r") as f:
            print(f"Contenido de {ruta}:")
            print(f.read() or "(vacio)")
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except PermissionError:
        print("Permiso denegado para leer el archivo.")
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")

def run():
    ruta = input("Ruta de archivo a leer: ").strip()
    leer_archivo(ruta)

if __name__ == "__main__":
    run()