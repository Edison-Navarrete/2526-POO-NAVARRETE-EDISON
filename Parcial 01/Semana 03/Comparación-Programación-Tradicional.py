# Calcular el promedio de temperaturas por ciudad.
""" Se presenta una matriz donde cada fila representa una ciudad y cada columna es una medición diaria,
dónde el código recorrá cada fila, sumará las temperaturas y calculará el promedio semanal por ciudad. Al final,se
imprime el nombre de la ciudad junto con su promedio para interpretar fácilmente cada resultado."""

# Defino funciones para separar responsabilidades y mantener el código ordenado:
# Con esto evito repetir lógica, hago más legible el programa y facilito su mantenimiento.
from typing import List

# - ingresar_temperaturas: se encarga de capturar desde teclado las temperaturas diarias por ciudad.
def ingresar_temperaturas(ciudades: List[str], dias_por_semana: int = 7) -> List[List[float]]:
    """
    Función: ingresar_temperaturas
    Propósito:
        - Pedir las temperaturas diarias por cada ciudad, una a una, controlando las entradas.
        - Devolver una matriz (lista de listas) donde cada fila corresponde a una ciudad
          y cada columna a un día de la semana.
    Parámetros:
        - ciudades: lista con los nombres de las ciudades.
        - dias_por_semana: cantidad de días a registrar (por defecto, 7).
    Retorna:
        - Lista de listas de floats con las temperaturas registradas.
    Buenas prácticas aplicadas:
        - Validación de entrada (try/except) para asegurar que el usuario ingrese números válidos.
        - Uso de tipos (type hints) para claridad.
    """
    temperaturas: List[List[float]] = []

    for ciudad in ciudades:
        print(f"\nIngreso de temperaturas para: {ciudad}")
        datos_ciudad: List[float] = []

        # Capturo exactamente 'dias_por_semana' valores por ciudad
        for dia in range(1, dias_por_semana + 1):
            while True:
                try:
                    valor = float(input(f"  Día {dia} - temperatura (°C): "))
                    datos_ciudad.append(valor)
                    break
                except ValueError:
                    # Mensaje claro para corregir la entrada
                    print("  Entrada inválida. Ingrese un número (ejemplo: 19.5).")

        temperaturas.append(datos_ciudad)

    return temperaturas

# - calcular_promedio_semana: recibe una lista de temperaturas (una semana) y devuelve el promedio.
def calcular_promedio_semana(temps_ciudad: List[float]) -> float:
    """
    Función: calcular_promedio_semana
    Propósito:
        - Recibir una lista de temperaturas diarias de una ciudad y devolver el promedio semanal.
    Parámetros:
        - temps_ciudad: lista de temperaturas (floats) correspondientes a una semana para una ciudad.
    Retorna:
        - El promedio aritmético como float. Si la lista está vacía, devuelve NaN para no romper el flujo.
    Buenas prácticas aplicadas:
        - Manejo de caso borde (lista vacía).
        - Cálculo usando bucle tradicional para ser claro y controlado.
    """
    if len(temps_ciudad) == 0:
        return float('nan')

    suma: float = 0.0
    for t in temps_ciudad:
        suma = suma + t  # Suma acumulada de las temperaturas

    promedio: float = suma / len(temps_ciudad)
    return promedio

# - calcularClima: recorre todas las ciudades, calcula el promedio semanal y presenta los resultados.
def calcularClima(temperatura: List[List[float]], nombreCiudades: List[str]) -> None:
    """
    Función: calcularClima
    Propósito:
        - Recorrer todas las ciudades, calcular el promedio semanal de sus temperaturas
          e imprimir el resultado junto con el nombre de la ciudad.
    Parámetros:
        - temperatura: matriz (lista de listas) con las temperaturas por ciudad.
        - nombreCiudades: lista con los nombres de las ciudades en el mismo orden que la matriz.
    Buenas prácticas aplicadas:
        - Validación simple de tamaños para evitar desalineaciones entre ciudades y datos.
        - Formateo de salida con dos decimales para presentación uniforme.
    """
    if len(temperatura) != len(nombreCiudades):
        print("Advertencia: la cantidad de ciudades no coincide con la cantidad de filas de la matriz de temperaturas.")
        # Continúo, pero el mensaje ayuda a detectar problemas de entrada.

    for i in range(len(temperatura)):
        promedio = calcular_promedio_semana(temperatura[i])
        # Muestro la ciudad y su promedio semanal con dos decimales
        print("Ciudad:", nombreCiudades[i], "-> Promedio semanal:", f"{promedio:.2f}", "°C")

# Bloque principal: aquí preparo la lista de ciudades, obtengo las temperaturas y llamo a la función principal.
if __name__ == "__main__":
    # Lista de ciudades (puedo ampliarla o cambiarla según el caso)
    ciudades: List[str] = ["Cuenca", "Quito", "Ambato"]

    # Opción A: entrada por teclado (activa para capturar datos reales de la semana)
    temperatura: List[List[float]] = ingresar_temperaturas(ciudades, dias_por_semana=7)

    # Opción B (comentada): datos fijos para pruebas rápidas sin entrada por teclado
    # temperatura = [
    #     [18.5, 21.5, 17.5, 20.0, 19.0, 20.5, 18.5],  # Cuenca
    #     [18.0, 17.0, 19.5, 16.5, 17.8, 18.1, 16.9],  # Quito
    #     [19.0, 16.0, 15.5, 21.0, 20.1, 19.3, 18.7],  # Ambato
    # ]

    # Cálculo e impresión de resultados
    calcularClima(temperatura, ciudades)
