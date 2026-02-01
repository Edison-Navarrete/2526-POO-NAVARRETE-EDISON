"""
Dashboard POO – Versión compacta y robusta (PARCIAL 01 / PARCIAL 02)
--------------------------------------------------------------------
Menú:
  1) Navegar PARCIAL 01 (abrir carpetas y archivos; .py se ven/ejecutan)
  2) Navegar PARCIAL 02
  3) Gestor: crear carpeta/archivo + Panel de Tareas
  0) Salir

# CAMBIO: Ya no se usa UNIDAD 1/2. Se trabaja con PARCIAL 01/02.
# NUEVO: Detección de raíz del repo, navegador simple, gestor de tareas con JSON en la raíz.
"""

import os, sys, json, subprocess
from datetime import datetime

# ============= UTILIDADES BÁSICAS =============

def limpiar():
    """Limpia la consola (Windows/Linux/macOS)."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar(msg="Presiona Enter para continuar..."):
    """Pausa para leer resultados en consola."""
    try: input(msg)
    except EOFError: pass

# ============= RAÍZ DEL REPOSITORIO =============
# NUEVO: Detecta la raíz subiendo hasta encontrar carpetas 'PARCIAL 01' o 'PARCIAL 02'.

def contiene_parciales(path):
    try:
        d = {e.name.upper() for e in os.scandir(path) if e.is_dir()}
        return ("PARCIAL 01" in d) or ("PARCIAL 02" in d)
    except Exception:
        return False

def detectar_raiz():
    cur = os.path.abspath(os.path.dirname(__file__))
    while True:
        if contiene_parciales(cur): return cur
        padre = os.path.dirname(cur)
        if padre == cur:  # llegó al volumen raíz
            # Fallback: 2 niveles arriba (coincide con tu estructura)
            return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cur = padre

RAIZ = detectar_raiz()
PARCIAL_01 = os.path.join(RAIZ, "PARCIAL 01")
PARCIAL_02 = os.path.join(RAIZ, "PARCIAL 02")
TAREAS_JSON = os.path.join(RAIZ, "tareas.json")

def dentro_repo(path):
    """# NUEVO: Seguridad. Asegura que 'path' está dentro del repo para no salirnos."""
    try:
        return os.path.commonpath([os.path.realpath(path), os.path.realpath(RAIZ)]) == os.path.realpath(RAIZ)
    except Exception:
        return False

# ============= APERTURA / EJECUCIÓN =============

def mostrar_codigo(ruta):
    """Imprime el contenido de un archivo de texto (UTF-8)."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            print("\n--- Código ---\n")
            print(f.read())
    except UnicodeDecodeError:
        print("No parece texto legible (no UTF-8).")
    except Exception as e:
        print(f"Error al leer: {e}")

def ejecutar_py(ruta):
    """# CAMBIO: Ejecución inline (más seguro y portátil)."""
    try:
        print("\n--- Ejecución ---\n")
        res = subprocess.run([sys.executable, ruta], text=True, capture_output=True, cwd=os.path.dirname(ruta))
        print(res.stdout)
        if res.stderr: print("\n[stderr]:\n", res.stderr)
    except Exception as e:
        print(f"Error al ejecutar: {e}")

def abrir_sistema(ruta):
    """Abre con la app predeterminada del sistema (no obligatorio, pero útil)."""
    try:
        if os.name == "nt": os.startfile(ruta)                                      # type: ignore[attr-defined]
        elif sys.platform == "darwin": subprocess.Popen(["open", ruta])
        else: subprocess.Popen(["xdg-open", ruta])
    except Exception as e:
        print(f"No se pudo abrir: {e}")

# ============= NAVEGADOR SIMPLE =============
# NUEVO: Lista carpetas/archivos, entra a carpetas, abre/ejecuta archivos .py.

def listar_contenido(ruta):
    try:
        items = list(os.scandir(ruta))
    except FileNotFoundError:
        print("Ruta inexistente."); return [], []
    dirs = sorted([e.name for e in items if e.is_dir()])
    files = sorted([e.name for e in items if e.is_file()])
    return dirs, files

def navegar(carpeta, titulo):
    actual = os.path.abspath(carpeta)
    if not (os.path.isdir(actual) and dentro_repo(actual)):
        print("Carpeta inválida."); pausar(); return
    while True:
        limpiar()
        print(f"{titulo}\nRuta: {os.path.relpath(actual, RAIZ)}\n")
        dirs, files = listar_contenido(actual)
        idx = {}
        print("Carpetas:")
        if not dirs: print("  (ninguna)")
        for i, d in enumerate(dirs, 1):
            print(f"  {i:02d}) [D] {d}"); idx[i] = ("dir", d)
        base = len(idx)
        print("\nArchivos:")
        if not files: print("  (ninguno)")
        for j, f in enumerate(files, 1):
            print(f"  {base+j:02d}) [F] {f}"); idx[base+j] = ("file", f)
        print("\n0) Volver   U) Subir   A <n>) Abrir con app del sistema")
        op = input("Opción/índice: ").strip()
        if op == "0": break
        if op.upper() == "U":
            padre = os.path.dirname(actual)
            if dentro_repo(padre): actual = padre
            else: print("Estás en la raíz."); pausar()
            continue
        if op.upper().startswith("A"):
            try:
                _, n = op.split(); n = int(n)
                if n in idx and idx[n][0] == "file":
                    abrir_sistema(os.path.join(actual, idx[n][1]))
                else: print("Índice inválido."); pausar()
            except Exception: print("Usa: A <número>"); pausar()
            continue
        if op.isdigit():
            n = int(op)
            if n not in idx: print("Índice inválido."); pausar(); continue
            tipo, nombre = idx[n]; ruta = os.path.join(actual, nombre)
            if tipo == "dir": actual = ruta; continue
            ext = os.path.splitext(nombre)[1].lower()
            if ext == ".py":
                mostrar_codigo(ruta)
                if input("¿Ejecutar? (s/n): ").lower() == "s": ejecutar_py(ruta)
                pausar()
            else:
                # Ver texto rápido o abrir con la app del sistema
                ver = input("¿Ver en consola (v) o abrir con sistema (a)? [v/a]: ").lower()
                if ver == "a": abrir_sistema(ruta)
                else: mostrar_codigo(ruta); pausar()
            continue
        print("Opción no válida."); pausar()

# ============= GESTIÓN DE ARCHIVOS (CREAR) =============
# NUEVO: Crear carpetas/archivos en cualquier punto del repo con un selector simple.

def seleccionar_carpeta(base):
    cur = os.path.abspath(base)
    while True:
        limpiar()
        print("Selector de carpeta")
        print("Actual:", os.path.relpath(cur, RAIZ))
        dirs, _ = listar_contenido(cur)
        for i, d in enumerate(dirs, 1): print(f"  {i:02d}) {d}")
        print("\n0) Cancelar   U) Subir   E) Elegir esta")
        op = input("Opción/índice: ").strip().upper()
        if op == "0": return None
        if op == "U":
            padre = os.path.dirname(cur)
            if dentro_repo(padre): cur = padre
            else: print("Ya estás en la raíz."); pausar()
            continue
        if op == "E": return cur
        if op.isdigit():
            n = int(op)
            if 1 <= n <= len(dirs): cur = os.path.join(cur, dirs[n-1])
            else: print("Índice inválido."); pausar()
            continue
        print("Opción no válida."); pausar()

def crear_carpeta():
    print("\n== Crear carpeta ==")
    destino = seleccionar_carpeta(RAIZ)
    if not destino: print("Cancelado."); return
    nombre = input("Nombre de la nueva carpeta: ").strip()
    if not nombre: print("Nombre obligatorio."); return
    ruta = os.path.join(destino, nombre)
    if not dentro_repo(ruta): print("Ruta fuera del repo."); return
    try:
        os.makedirs(ruta, exist_ok=False); print("✔ Carpeta creada:", os.path.relpath(ruta, RAIZ))
    except FileExistsError: print("Ya existe.")
    except Exception as e: print("Error:", e)

def crear_archivo():
    print("\n== Crear archivo ==")
    destino = seleccionar_carpeta(RAIZ)
    if not destino: print("Cancelado."); return
    nombre = input("Nombre (con extensión): ").strip()
    if not nombre or any(c in nombre for c in "/\\"): print("Nombre inválido."); return
    ruta = os.path.join(destino, nombre)
    if not dentro_repo(ruta): print("Ruta fuera del repo."); return
    if os.path.exists(ruta): print("Ya existe."); return
    contenido = input("Contenido inicial (opcional): ")
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            if contenido: f.write(contenido)
        print("✔ Archivo creado:", os.path.relpath(ruta, RAIZ))
    except Exception as e: print("Error:", e)

# ============= PANEL DE TAREAS =============
# Requisitos:
# - Crear (título, unidad, estado, fecha límite YYYY-MM-DD, nota)
# - Listar (todas / por estado / por unidad / pendientes próximas)
# - Completar (por ID)
# - Eliminar (por ID)
# - Persistencia en tareas.json (RAÍZ del repo)

ESTADOS = ["pendiente", "en progreso", "completada"]
UNIDADES = ["PARCIAL 01", "PARCIAL 02"]  # CAMBIO: unidades = parciales

def cargar_tareas():
    if not os.path.exists(TAREAS_JSON): return []
    try:
        with open(TAREAS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        print("Aviso: tareas.json inválido. Se usará base vacía."); return []

def guardar_tareas(tareas):
    tmp = TAREAS_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)
    os.replace(tmp, TAREAS_JSON)

def gen_id(tareas): return (max([int(t.get("id", 0)) for t in tareas]) + 1) if tareas else 1

def fecha_valida(s):
    try: datetime.strptime(s, "%Y-%m-%d"); return True
    except: return False

def crear_tarea():
    tareas = cargar_tareas()
    print("\n== Nueva tarea ==")
    titulo = input("Título: ").strip()
    if not titulo: print("El título es obligatorio."); return
    print("Unidades:", ", ".join(UNIDADES))
    unidad = input("Unidad: ").strip().upper()
    if unidad not in UNIDADES: print("Unidad no válida. Se usará PARCIAL 01."); unidad = "PARCIAL 01"
    print("Estados:", ", ".join(ESTADOS))
    estado = input("Estado: ").strip().lower()
    if estado not in ESTADOS: print("Estado no válido. Se usará 'pendiente'."); estado = "pendiente"
    fecha = input("Fecha límite (YYYY-MM-DD, opcional): ").strip()
    if fecha and not fecha_valida(fecha): print("Fecha inválida. Se deja vacía."); fecha = ""
    nota = input("Nota (opcional): ").strip()
    nueva = {"id": gen_id(tareas), "titulo": titulo, "unidad": unidad, "estado": estado, "fecha_limite": fecha, "nota": nota}
    tareas.append(nueva); guardar_tareas(tareas); print(f"✔ Tarea creada (id={nueva['id']})")

def _parse_fecha(s):
    try: return datetime.strptime(s, "%Y-%m-%d")
    except: return None

def listar_tareas(f_estado=None, f_unidad=None, proximas=False):
    tareas = cargar_tareas(); data = tareas
    if f_estado: data = [t for t in data if t.get("estado") == f_estado]
    if f_unidad: data = [t for t in data if t.get("unidad") == f_unidad]
    if proximas:
        hoy = datetime.now().date()
        data = [t for t in data if t.get("estado") != "completada" and _parse_fecha(t.get("fecha_limite") or "") and _parse_fecha(t["fecha_limite"]).date() >= hoy]
        data.sort(key=lambda t: _parse_fecha(t["fecha_limite"]))
    if not data: print("(Sin tareas)"); return
    print("\n== Tareas ==")
    for t in data:
        print(f"[{int(t['id']):03}] {t['titulo']} | {t['unidad']} | {t['estado']} | vence: {t.get('fecha_limite') or '—'} | nota: {t.get('nota') or '—'}")

def completar_tarea():
    tareas = cargar_tareas()
    try:
        i = int(input("ID a completar: ").strip())
    except: print("ID inválido."); return
    for t in tareas:
        if int(t.get("id", -1)) == i:
            t["estado"] = "completada"; guardar_tareas(tareas); print("✔ Marcada como completada."); return
    print("No existe ese ID.")

def eliminar_tarea():
    tareas = cargar_tareas()
    try:
        i = int(input("ID a eliminar: ").strip())
    except: print("ID inválido."); return
    nuevo = [t for t in tareas if int(t.get("id", -1)) != i]
    if len(nuevo) == len(tareas): print("No existe ese ID."); return
    guardar_tareas(nuevo); print("🗑 Eliminada.")

def panel_tareas():
    while True:
        limpiar()
        print("PANEL DE TAREAS")
        print("1) Crear")
        print("2) Listar todas")
        print("3) Listar por estado")
        print("4) Listar por unidad")
        print("5) Pendientes próximas (ordenadas)")
        print("6) Completar por ID")
        print("7) Eliminar por ID")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1": crear_tarea(); pausar()
        elif op == "2": listar_tareas(); pausar()
        elif op == "3":
            print("Estados:", ", ".join(ESTADOS)); e = input("Estado: ").strip().lower()
            if e in ESTADOS: listar_tareas(f_estado=e)
            else: print("Estado inválido.")
            pausar()
        elif op == "4":
            print("Unidades:", ", ".join(UNIDADES)); u = input("Unidad: ").strip().upper()
            if u in UNIDADES: listar_tareas(f_unidad=u)
            else: print("Unidad inválida.")
            pausar()
        elif op == "5": listar_tareas(proximas=True); pausar()
        elif op == "6": completar_tarea(); pausar()
        elif op == "7": eliminar_tarea(); pausar()
        elif op == "0": break
        else: print("Opción no válida."); pausar()

# ============= GESTOR (OPCIÓN 3) =============

def gestor():
    while True:
        limpiar()
        print("GESTOR (Repositorio)")
        print("1) Crear carpeta")
        print("2) Crear archivo")
        print("3) Panel de Tareas")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1": crear_carpeta(); pausar()
        elif op == "2": crear_archivo(); pausar()
        elif op == "3": panel_tareas()
        elif op == "0": break
        else: print("Opción no válida."); pausar()

# ============= MENÚ PRINCIPAL =============

def menu():
    while True:
        limpiar()
        print("DASHBOARD POO – Repositorio")
        print("Raíz:", RAIZ)
        print("1) Navegar PARCIAL 01")
        print("2) Navegar PARCIAL 02")
        print("3) Gestor (crear + tareas)")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "0": break
        if op == "1":
            if os.path.isdir(PARCIAL_01): navegar(PARCIAL_01, "Explorador PARCIAL 01")
            else: print("No existe PARCIAL 01."); pausar()
        elif op == "2":
            if os.path.isdir(PARCIAL_02): navegar(PARCIAL_02, "Explorador PARCIAL 02")
            else: print("No existe PARCIAL 02."); pausar()
        elif op == "3": gestor()
        else: print("Opción no válida."); pausar()

if __name__ == "__main__":
    menu()