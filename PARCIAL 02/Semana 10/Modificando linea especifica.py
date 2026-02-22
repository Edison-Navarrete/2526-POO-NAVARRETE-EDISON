# Modificando linea especifica.py
# -----------------------------------------------------------
# Este módulo modifica una línea específica del inventario por ID
# (cantidad y precio) y reescribe el archivo. Incluye run() para
# integrarse con el menú principal.
# -----------------------------------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "inventario.txt"

def run():
    objetivo = input("ID a actualizar: ").strip()
    try:
        nueva_cantidad = int(input("Nueva cantidad: ").strip())
        nuevo_precio = float(input("Nuevo precio: ").strip())
    except Exception:
        print("Entradas invalidas. La cantidad debe ser entero y el precio numerico.")
        return
    if nueva_cantidad < 0 or nuevo_precio < 0:
        print("No se admiten valores negativos.")
        return

    try:
        if not RUTA.exists():
            print("No existe inventario.txt.")
            return

        with open(RUTA, "r") as f:
            lineas = f.read().splitlines()
        if not lineas:
            print("Archivo vacio.")
            return

        cabecera = lineas[0]
        nuevas = [cabecera]
        hecho = False
        for linea in lineas[1:]:
            partes = linea.split(",")
            if len(partes) < 4:
                nuevas.append(linea)
                continue
            idp, nombre, cantidad, precio = partes[0], partes[1], partes[2], partes[3]
            if idp == objetivo:
                nuevas.append(f"{idp},{nombre},{nueva_cantidad},{nuevo_precio}")
                hecho = True
            else:
                nuevas.append(linea)

        with open(RUTA, "w") as f:
            f.write("\n".join(nuevas) + "\n")

        if hecho:
            print("OK: linea actualizada y archivo reescrito.")
        else:
            print("No se encontro el ID solicitado.")

    except PermissionError:
        print("ERROR: permiso denegado al modificar el archivo.")
    except OSError as e:
        print(f"ERROR: problema del sistema al reescribir: {e}")

if __name__ == "__main__":
    run()