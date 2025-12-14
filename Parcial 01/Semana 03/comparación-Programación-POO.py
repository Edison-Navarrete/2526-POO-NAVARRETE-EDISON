""" clima semanal por ciudad con POO.

Para cada ciudad se registran sus temperaturas diarias, se calcula el promedio
 y se realizan comparaciones entre ciudades mostrando cuál tiene el promedio más alto.
 se organizó el código con clases y métodos para separar responsabilidades:
  - ClimaCiudad: clase base con datos y operaciones comunes.
  - CiudadCostera: especialización con un factor propio (herencia y polimorfismo).
  - comparar: función externa que simula “turnos” de reporte y decide el ganador.
"""
from typing import List

class ClimaCiudad:
    """
    Clase: ClimaCiudad
    Propósito: Representa la información diaria del clima para una ciudad.
        - Permite ingresar datos y calcular el promedio semanal.
    Encapsulamiento: Uso atributos internos (con guion bajo) y métodos para operar con ellos.
    """
    def __init__(self, nombre: str, temp_base: float, altitud: int, nubosidad: float, dias_por_semana: int = 7) -> None:
        # Atributos internos: se mantiene el orden evitando que se manipulen directo desde afuera.
        self._nombre: str = nombre
        self._temp_base: float = temp_base       # referencia de temperatura típica
        self._altitud: int = altitud             # altitud en msnm
        self._nubosidad: float = nubosidad       # 0.0 a 1.0
        self._dias_por_semana: int = dias_por_semana
        self._temperaturas: List[float] = []     # registro de temperaturas diarias
        self._activa: bool = True                # estado de la semana (para controlar turnos)

    def atributos(self) -> None:
        # atributos principales de la ciudad
        print(self._nombre, ":", sep="")
        print("·Temp. base:", self._temp_base, "°C")
        print("·Altitud:", self._altitud, "msnm")
        print("·Nubosidad:", self._nubosidad)
        print("·Días por semana:", self._dias_por_semana)

    def subir_nivel(self, temp_base: float, altitud: int, nubosidad: float) -> None:
        # establecer parámetros climáticos (similar a actualizar “stats”)
        self._temp_base = self._temp_base + temp_base
        self._altitud = self._altitud + altitud
        # mantengo la nubosidad en el rango correcto
        self._nubosidad = max(0.0, min(1.0, self._nubosidad + nubosidad))

    def esta_activa(self) -> bool:
        # Indica si la semana sigue activa (control del flujo)
        return self._activa

    def cerrar_semana(self) -> None:
        # Cierro la semana (cambio de estado)
        self._activa = False
        print(self._nombre, "ha cerrado su semana")

    def ingresar_datos(self) -> None:
        """
        Metodo: ingresar_datos
        Propósito:Capturar las temperaturas diarias de la semana para esta ciudad.
        Detalle: Valido entradas y guardo exactamente 'dias_por_semana' valores.
        """
        self._temperaturas = []
        print(f"\nIngreso de temperaturas para: {self._nombre}")
        for dia in range(1, self._dias_por_semana + 1):
            while True:
                try:
                    valor = float(input(f"  Día {dia} - temperatura (°C): "))
                    self._temperaturas.append(valor)
                    break
                except ValueError:
                    print("  Entrada inválida. Ingrese un número (ejemplo: 19.5).")

    def promedio_semana(self) -> float:
        """
        Metodo: promedio_semana
        Propósito: Calcular el promedio de la semana a partir de los datos ingresados.
        """
        if len(self._temperaturas) == 0:
            return float('nan')
        suma: float = 0.0
        for t in self._temperaturas:
            suma = suma + t
        promedio: float = suma / len(self._temperaturas)
        return promedio

    def impacto(self, otra: "ClimaCiudad") -> float:
        """
        Metodo: impacto.
        Propósito: Devolver la diferencia de promedios entre esta ciudad y otra.
        """
        return self.promedio_semana() - otra.promedio_semana()

    def comparar_con(self, otra: "ClimaCiudad") -> None:
        """
        Metodo: comparar_con.
        Propósito:
            - Mostrar el promedio propio y la diferencia respecto a otra ciudad.
        """
        propio = self.promedio_semana()
        diff = self.impacto(otra)
        print(self._nombre, "reporta promedio", f"{propio:.2f}", "°C frente a", otra._nombre, "(", f"{diff:+.2f}", ")")
        if otra.esta_activa():
            print("Promedio de", otra._nombre, "es", f"{otra.promedio_semana():.2f}", "°C")
        else:
            print("Semana de", otra._nombre, "ya está cerrada.")

class CiudadCostera(ClimaCiudad):
    """
    Clase: CiudadCostera
    Herencia: Especializa ClimaCiudad con un factor de brisa.
    Polimorfismo: Redefino 'promedio_semana' para aplicar el factor costero.
    """
    def __init__(self, nombre: str, temp_base: float, altitud: int, nubosidad: float,
                 dias_por_semana: int = 7, brisa: float = 1.00) -> None:
        super().__init__(nombre, temp_base, altitud, nubosidad, dias_por_semana)
        self._brisa: float = brisa  # factor multiplicador leve

    def cambiar_brisa(self) -> None:
        # Selección del factor de brisa (similar a cambiar arma)
        print("Elige brisa: (1) Suave (x1.00), (2) Fuerte (x1.05), (3) Marina (x1.10)")
        try:
            opcion = int(input("Opción: "))
            if opcion == 1:
                self._brisa = 1.00
            elif opcion == 2:
                self._brisa = 1.05
            elif opcion == 3:
                self._brisa = 1.10
            else:
                print("Número de opción incorrecta")
        except ValueError:
            print("Entrada inválida, se mantiene el factor actual.")

    def atributos(self) -> None:
        # Muestra atributos base y agrega el factor de brisa
        super().atributos()
        print("·Brisa (factor):", self._brisa)

    def promedio_semana(self) -> float:
        # Aplico leve modificación por efecto costero (polimorfismo)
        base = super().promedio_semana()
        return base * self._brisa


def comparar(ciudad_1: ClimaCiudad, ciudad_2: ClimaCiudad) -> None:
    """
    Función: comparar (similar a 'combate' del ejemplo de juego).
    Propósito: Mostrar “turnos” donde cada ciudad reporta su promedio semanal
          y luego decidir cuál tiene el promedio más alto.
    """
    turno = 1
    while ciudad_1.esta_activa() and ciudad_2.esta_activa():
        print("\n========================= Turno", turno, "=========================")
        print(">>> Acción de", ciudad_1._nombre, ":", sep=" ")
        ciudad_1.comparar_con(ciudad_2)

        print(">>> Acción de", ciudad_2._nombre, ":", sep=" ")
        ciudad_2.comparar_con(ciudad_1)

        turno = turno + 1
        # Cierro la semana al terminar el turno para ambas ciudades
        ciudad_1.cerrar_semana()
        ciudad_2.cerrar_semana()

    print("\n=========================== Fin ===========================")
    p1 = ciudad_1.promedio_semana()
    p2 = ciudad_2.promedio_semana()
    if p1 > p2:
        print("Mayor promedio:", ciudad_1._nombre)
    elif p2 > p1:
        print("Mayor promedio:", ciudad_2._nombre)
    else:
        print("Empate")


# Bloque principal: instancio tres ciudades (Salitre, Daule y Milagro), ingreso datos y comparo
if __name__ == "__main__":
    # Ciudades
    salitre = CiudadCostera("Salitre", temp_base=27.5, altitud=10, nubosidad=0.60, dias_por_semana=7, brisa=1.02)
    daule = CiudadCostera("Daule",   temp_base=27.0, altitud=6,  nubosidad=0.55, dias_por_semana=7, brisa=1.00)
    milagro = CiudadCostera("Milagro", temp_base=27.8, altitud=13, nubosidad=0.58, dias_por_semana=7, brisa=1.03)

    # Muestro atributos iniciales
    salitre.atributos()
    daule.atributos()
    milagro.atributos()

    # Permito ajustar el factor de brisa si quiero
    salitre.cambiar_brisa()
    daule.cambiar_brisa()
    milagro.cambiar_brisa()

    # Ingreso de datos diarios por ciudad
    salitre.ingresar_datos()
    daule.ingresar_datos()
    milagro.ingresar_datos()

    # Comparaciones por pares (cada una cierra su semana al final de la función)
    comparar(salitre, daule)
    comparar(milagro, salitre)   # segunda comparación usando los datos ya capturados
    comparar(daule, milagro)

    # Resumen final simple: muestro los promedios (aunque ya se imprimen en las comparaciones)
    print("\n--- Promedios finales ---")
    print("Salitre:", f"{salitre.promedio_semana():.2f}", "°C")
    print("Daule:",   f"{daule.promedio_semana():.2f}",   "°C")
    print("Milagro:", f"{milagro.promedio_semana():.2f}", "°C")
