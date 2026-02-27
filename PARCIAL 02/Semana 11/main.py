# Semana 11/main.py — Punto de entrada
from pathlib import Path
from actividad_inventario.aplicacion.inventario import Inventario
from actividad_inventario.infraestructura.almacenamiento import cargar_json, guardar_json
from actividad_inventario.interfaz.cli import ejecutar_menu

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "inventario.json"

def main():
    # Almacenamiento en archivos: lectura (deserialización)
    estado_dict = cargar_json(DATA_FILE)
    inv = Inventario.desde_dict(estado_dict)

    try:
        # Interfaz de usuario: menú interactivo por consola
        ejecutar_menu(inv)
    finally:
        # Almacenamiento en archivos: escritura (serialización)
        guardar_json(DATA_FILE, inv.a_dict())

if __name__ == "__main__":
    main()
    #