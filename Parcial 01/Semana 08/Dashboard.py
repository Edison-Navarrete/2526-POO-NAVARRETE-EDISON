"""
DASHBOARD POO – Versión adaptada
-----------------------------------------------------
Basado en Dashboard original (navega por UNIDAD 1/2, muestra y ejecuta scripts),
se integra un **Panel de Tareas** para organizar la materia de POO:

- Crear tarea (título, unidad, estado, fecha límite, nota)
- Listar tareas (todas / por estado / por unidad / pendientes próximas)
- Marcar como completada
- Eliminar tarea
- Persistencia en tareas.json (raíz del proyecto)

Se mantienen:
- Ver código de .py dentro de cada subcarpeta
- Ejecutar scripts desde el menú

Cambios marcados con:  # CAMBIO: ... / # NUEVO: ...
"""

import os
import subprocess
# NUEVO: imports para gestor de tareas
import json
from datetime import datetime

# ------------- BLOQUE ORIGINAL (con pequeños ajustes) -----------------

def mostrar_codigo(ruta_script):
    # Asegúramos de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:  # CAMBIO: encoding explícito
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':  # Windows
            # CAMBIO: usar 'python' por defecto en cmd
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            # CAMBIO: xterm puede no estar instalado; si falla, se imprime error
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def mostrar_menu():
    # Define la ruta base donde se encuentra el dashboard.py
    ruta_base = os.path.dirname(__file__)

    # CAMBIO: homogeneizamos a 'UNIDAD 1' / 'UNIDAD 2'
    unidades = {
        '1': 'UNIDAD 1',
        '2': 'UNIDAD 2'
    }

    while True:
        print("\nMenu Principal - Dashboard")
        # Imprime las opciones del menú principal
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        # NUEVO: opción para Panel de Tareas
        print("3 - Panel de Tareas (NUEVO)")
        print("0 - Salir")

        eleccion = input("Elige una opción: ").strip()

        if eleccion == '0':
            print("Saliendo del programa.")
            break
        elif eleccion in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion])
            if not os.path.isdir(ruta_unidad):
                print(f"No se encontró la carpeta: {ruta_unidad}")
            else:
                mostrar_sub_menu(ruta_unidad)
        elif eleccion == '3':
            gestionar_tareas()  # NUEVO: abre el panel de tareas
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_sub_menu(ruta_unidad):
    # Lista subcarpetas de la unidad seleccionada
    try:
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
    except FileNotFoundError:
        print("Ruta de unidad inválida.")
        return

    while True:
        print("\nSubmenú - Selecciona una subcarpeta")
        if not sub_carpetas:
            print("(No hay subcarpetas)")
        else:
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ").strip()
        if eleccion_carpeta == '0':
            break
        else:
            try:
                idx = int(eleccion_carpeta) - 1
                if 0 <= idx < len(sub_carpetas):
                    ruta_sub = os.path.join(ruta_unidad, sub_carpetas[idx])
                    mostrar_scripts(ruta_sub)
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_scripts(ruta_sub_carpeta):
    try:
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta)
                   if f.is_file() and f.name.endswith('.py')]
    except FileNotFoundError:
        print("Ruta de subcarpeta inválida.")
        return

    while True:
        print("\nScripts - Selecciona un script para ver y ejecutar")
        if not scripts:
            print("(No hay scripts .py en esta carpeta)")
        else:
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar o '9' para ir al menú principal: ").strip()
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                idx = int(eleccion_script) - 1
                if 0 <= idx < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[idx])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ").strip()
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

# ------------- BLOQUE NUEVO: GESTOR DE TAREAS -----------------

# NUEVO: Rutas y catálogos
RUTA_BASE = os.path.dirname(__file__)
RUTA_DB = os.path.join(RUTA_BASE, "tareas.json")
ESTADOS = ["pendiente", "en progreso", "completada"]
UNIDADES_LIST = ["UNIDAD 1", "UNIDAD 2", "UNIDAD 3", "UNIDAD 4"]  # ajustable

# NUEVO: utilidades de persistencia
def cargar_tareas():
    """Carga la lista de tareas desde tareas.json (si no existe, devuelve [])."""
    if not os.path.exists(RUTA_DB):
        return []
    try:
        with open(RUTA_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Aviso: 'tareas.json' no es válido. Se iniciará una base vacía.")
        return []

def guardar_tareas(tareas):
    """Guarda la lista de tareas en tareas.json, con indentación legible."""
    with open(RUTA_DB, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

def generar_id(tareas):
    """Genera un ID incremental sencillo basado en los existentes."""
    return (max([t["id"] for t in tareas]) + 1) if tareas else 1

def validar_fecha(fecha):
    """Valida formato YYYY-MM-DD (devuelve True/False)."""
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# NUEVO: operaciones sobre tareas
#solicitael (título, unidad, estado, fecha límite, nota) y la guardaen tarjetas.Json
def crear_tarea():
    """Crea y persiste una nueva tarea."""
    tareas = cargar_tareas()
    print("\n== Nueva tarea ==")
    titulo = input("Título: ").strip()
    if not titulo:
        print("El título es obligatorio.")
        return

    print("Unidades disponibles:", ", ".join(UNIDADES_LIST))
    unidad = input("Unidad (e.g., UNIDAD 1): ").strip().upper()
    if unidad not in UNIDADES_LIST:
        print("Unidad no reconocida. Se asignará 'UNIDAD 1'.")
        unidad = "UNIDAD 1"

    print("Estados:", ", ".join(ESTADOS))
    estado = input("Estado [pendiente/en progreso/completada]: ").strip().lower()
    if estado not in ESTADOS:
        print("Estado no válido. Se asignará 'pendiente'.")
        estado = "pendiente"

    fecha_limite = input("Fecha límite (YYYY-MM-DD, opcional): ").strip()
    if fecha_limite and not validar_fecha(fecha_limite):
        print("Fecha inválida. Se dejará vacía.")
        fecha_limite = ""

    nota = input("Nota (opcional): ").strip()

    nueva = {
        "id": generar_id(tareas),
        "titulo": titulo,
        "unidad": unidad,
        "estado": estado,
        "fecha_limite": fecha_limite,
        "nota": nota
    }
    tareas.append(nueva)
    guardar_tareas(tareas)
    print(f"✔ Tarea creada con id={nueva['id']}")

def listar_tareas(filtro_estado=None, filtro_unidad=None, solo_pendientes_proximas=False):
    """Lista tareas, permitiendo filtrar por estado/unidad y ver próximas (ordenadas) por fechas."""
    tareas = cargar_tareas()
    filtradas = tareas

    if filtro_estado:
        filtradas = [t for t in filtradas if t["estado"] == filtro_estado]
    if filtro_unidad:
        filtradas = [t for t in filtradas if t["unidad"] == filtro_unidad]

    if solo_pendientes_proximas:
        hoy = datetime.now().date()
        proximas = []
        for t in filtradas:
            if t["estado"] != "completada" and t.get("fecha_limite"):
                try:
                    f = datetime.strptime(t["fecha_limite"], "%Y-%m-%d").date()
                    if f >= hoy:
                        proximas.append(t)
                except ValueError:
                    pass
        filtradas = sorted(proximas, key=lambda t: t["fecha_limite"])

    if not filtradas:
        print("\n(No hay tareas para los filtros indicados)")
        return

    print("\n== Lista de tareas ==")
    for t in filtradas:
        print(f"[{t['id']:03}] {t['titulo']} | {t['unidad']} | {t['estado']} | "
              f"vence: {t['fecha_limite'] or '—'} | nota: {t['nota'] or '—'}")

def completar_tarea():
    """Marca una tarea como 'completada' por ID."""
    tareas = cargar_tareas()
    try:
        idt = int(input("ID de la tarea a completar: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    for t in tareas:
        if t["id"] == idt:
            t["estado"] = "completada"
            guardar_tareas(tareas)
            print("✔ Tarea marcada como completada.")
            return
    print("No se encontró una tarea con ese ID.")

def eliminar_tarea():
    """Elimina una tarea por ID."""
    tareas = cargar_tareas()
    try:
        idt = int(input("ID de la tarea a eliminar: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    nuevas = [t for t in tareas if t["id"] != idt]
    if len(nuevas) == len(tareas):
        print("No se encontró una tarea con ese ID.")
        return
    guardar_tareas(nuevas)
    print("🗑 Tarea eliminada.")

# NUEVO: menú del gestor de tareas
def gestionar_tareas():
    """Panel de Tareas: menú interactivo para CRUD y filtros."""
    while True:
        print("\n===== PANEL DE TAREAS =====")
        print("1) Crear tarea")
        print("2) Listar todas")
        print("3) Listar por estado")
        print("4) Listar por unidad")
        print("5) Ver pendientes con fecha próxima (ordenadas)")
        print("6) Marcar como completada")
        print("7) Eliminar tarea")
        print("0) Volver al menú principal")
        op = input("Elige una opción: ").strip()

        if op == "1":
            crear_tarea()
        elif op == "2":
            listar_tareas()
        elif op == "3":
            print("Estados:", ", ".join(ESTADOS))
            est = input("Estado: ").strip().lower()
            if est not in ESTADOS:
                print("Estado no válido.")
            else:
                listar_tareas(filtro_estado=est)
        elif op == "4":
            print("Unidades:", ", ".join(UNIDADES_LIST))
            un = input("Unidad: ").strip().upper()
            if un not in UNIDADES_LIST:
                print("Unidad no válida.")
            else:
                listar_tareas(filtro_unidad=un)
        elif op == "5":
            listar_tareas(solo_pendientes_proximas=True)
        elif op == "6":
            completar_tarea()
        elif op == "7":
            eliminar_tarea()
        elif op == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# ------------- PUNTO DE ENTRADA -----------------

if __name__ == "__main__":
    # CAMBIO: el original tenía "mostrar_menu()." (con punto) -> SyntaxError.
    mostrar_menu()