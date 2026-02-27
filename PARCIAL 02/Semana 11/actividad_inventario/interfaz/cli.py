# actividad_inventario/interfaz/cli.py
# Requisito: Interfaz de Usuario por consola (menú interactivo).
# Decisión: La CLI solo recoge/valida entradas y delega la lógica a Inventario.

from __future__ import annotations
from actividad_inventario.aplicacion.inventario import Inventario
from actividad_inventario.dominio.producto import Producto

# --- utilidades de entrada ---
def _leer_texto_no_vacio(msg: str) -> str:
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠ Este campo no puede estar vacío.")

def _leer_entero_no_negativo(msg: str) -> int:
    while True:
        try:
            v = int(input(msg).strip())
            if v < 0:
                print("⚠ Debe ser un entero ≥ 0.")
            else:
                return v
        except Exception:
            print("⚠ Ingresa un entero válido.")

def _leer_flotante_no_negativo(msg: str) -> float:
    while True:
        try:
            v = float(input(msg).strip())
            if v < 0:
                print("⚠ Debe ser un número ≥ 0.")
            else:
                return v
        except Exception:
            print("⚠ Ingresa un número válido (ej. 10.5).")

def _menu() -> None:
    print("\n===== SISTEMA AVANZADO DE INVENTARIO =====")
    print("1) Añadir producto")
    print("2) Eliminar producto por ID")
    print("3) Actualizar CANTIDAD por ID")
    print("4) Actualizar PRECIO por ID")
    print("5) Buscar producto(s) por NOMBRE")
    print("6) Mostrar TODOS los productos")
    print("7) Resumen (items, valor total)")
    print("0) Salir")

def ejecutar_menu(inv: Inventario) -> None:
    while True:
        _menu()
        op = input("Opción: ").strip()
        try:
            if op == "1":
                p = Producto(
                    id=_leer_texto_no_vacio("ID (único): "),
                    nombre=_leer_texto_no_vacio("Nombre: "),
                    cantidad=_leer_entero_no_negativo("Cantidad: "),
                    precio=_leer_flotante_no_negativo("Precio: "),
                )
                inv.agregar_producto(p)
                print("✅ Producto añadido.")

            elif op == "2":
                inv.eliminar_por_id(_leer_texto_no_vacio("ID a eliminar: "))
                print("✅ Producto eliminado.")

            elif op == "3":
                inv.actualizar_cantidad(
                    _leer_texto_no_vacio("ID: "),
                    _leer_entero_no_negativo("Nueva cantidad: ")
                )
                print("✅ Cantidad actualizada.")

            elif op == "4":
                inv.actualizar_precio(
                    _leer_texto_no_vacio("ID: "),
                    _leer_flotante_no_negativo("Nuevo precio: ")
                )
                print("✅ Precio actualizado.")

            elif op == "5":
                nombre = _leer_texto_no_vacio("Nombre a buscar: ")
                resultados = inv.buscar_por_nombre(nombre)
                if resultados:
                    print(f"🔎 {len(resultados)} coincidencia(s):")
                    for p in resultados:
                        print("   ", p)
                else:
                    print("ℹ No se encontraron coincidencias.")

            elif op == "6":
                productos = inv.listar_todos()
                if productos:
                    print(f"📋 Productos ({len(productos)}):")
                    for p in productos:
                        print("   ", p)
                else:
                    print("ℹ Inventario vacío.")

            elif op == "7":
                n, total = inv.resumen()
                print(f"📊 Resumen → Ítems distintos: {n} | Valor total: ${total:.2f}")

            elif op == "0":
                print("👋 Saliendo del sistema...")
                break

            else:
                print("⚠ Opción inválida. Elige entre 0 y 7.")
        except Exception as e:
            print("❌ Error:", e)