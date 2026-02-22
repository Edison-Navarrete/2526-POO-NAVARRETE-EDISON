# Else y Finally (ZeroDivision).py
# -----------------------------------------------------------
# Demuestra try/except/else/finally con una division que puede
# generar ZeroDivisionError. Incluye run() para integrarse
# con el menú principal.
# -----------------------------------------------------------

def dividir(a, b):
    try:
        resultado = a / b
    except ZeroDivisionError:
        print("Division por cero no permitida.")
    except TypeError:
        print("Los operandos deben ser numericos.")
    else:
        print("Division correcta. Resultado:", resultado)
    finally:
        print("Finally ejecutado (limpieza).")

def run():
    try:
        a = float(input("Ingrese a: ").strip())
        b = float(input("Ingrese b: ").strip())
    except Exception:
        print("Entradas invalidas.")
        return
    dividir(a, b)

if __name__ == "__main__":
    run()