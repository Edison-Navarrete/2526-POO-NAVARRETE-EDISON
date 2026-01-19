
# -*- coding: utf-8 -*-
"""
Gestor simple de nómina con POO:
- Herencia: Empleado -> EmpleadoAsalariado / EmpleadoPorHoras
- Encapsulación: atributos privados con @property (validación)
- Polimorfismo: calcular_pago() implementado distinto en cada derivada
"""

class Empleado:
    """Clase base: define interfaz común para los empleados."""
    def __init__(self, nombre: str):
        self.nombre = nombre  # público por simplicidad

    def calcular_pago(self) -> float:
        """Método polimórfico (se implementa en clases hijas)."""
        raise NotImplementedError("Debes implementar calcular_pago() en la subclase.")

    def resumen(self) -> str:
        """Describe el tipo de empleado y su pago calculado."""
        return f"{self.__class__.__name__} - {self.nombre}: ${self.calcular_pago():.2f}"


class EmpleadoAsalariado(Empleado):
    """Empleado con salario fijo mensual."""
    def __init__(self, nombre: str, salario_mensual: float):
        super().__init__(nombre)
        self.__salario_mensual = 0.0
        self.salario_mensual = salario_mensual  # usa property para validar

    @property
    def salario_mensual(self) -> float:
        return self.__salario_mensual

    @salario_mensual.setter
    def salario_mensual(self, valor: float):
        if valor < 0:
            raise ValueError("El salario mensual no puede ser negativo.")
        self.__salario_mensual = float(valor)

    def calcular_pago(self) -> float:
        # Polimorfismo: para asalariado, el pago es el salario mensual fijo.
        return self.__salario_mensual


class EmpleadoPorHoras(Empleado):
    """Empleado pagado por horas trabajadas."""
    def __init__(self, nombre: str, tarifa_hora: float, horas_trabajadas: float):
        super().__init__(nombre)
        self.__tarifa_hora = 0.0
        self.__horas_trabajadas = 0.0
        self.tarifa_hora = tarifa_hora         # usa property para validar
        self.horas_trabajadas = horas_trabajadas

    @property
    def tarifa_hora(self) -> float:
        return self.__tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor: float):
        if valor < 0:
            raise ValueError("La tarifa por hora no puede ser negativa.")
        self.__tarifa_hora = float(valor)

    @property
    def horas_trabajadas(self) -> float:
        return self.__horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor: float):
        if valor < 0:
            raise ValueError("Las horas trabajadas no pueden ser negativas.")
        self.__horas_trabajadas = float(valor)

    def calcular_pago(self) -> float:
        """
        Polimorfismo: pago por horas, con regla simple de horas extra:
        - Hasta 40h se paga tarifa normal.
        - Horas > 40 se pagan a 1.5x (tiempo extra).
        """
        horas = self.__horas_trabajadas
        tarifa = self.__tarifa_hora
        if horas <= 40:
            return horas * tarifa
        normales = 40 * tarifa
        extras = (horas - 40) * tarifa * 1.5
        return normales + extras


def calcular_nomina(empleados: list) -> float:
    """Suma el pago de todos los empleados (polimorfismo en acción)."""
    return sum(emp.calcular_pago() for emp in empleados)


if __name__ == "__main__":
    # --- Demostración simple ---
    # 1) Crear empleados (uno asalariado y dos por horas)
    ana = EmpleadoAsalariado("Ana", salario_mensual=1200)
    luis = EmpleadoPorHoras("Luis", tarifa_hora=6.0, horas_trabajadas=38)
    maria = EmpleadoPorHoras("María", tarifa_hora=5.5, horas_trabajadas=45)  # con extras

    # 2) Mostrar resumen individual (usa el mismo método en tipos distintos = polimorfismo)
    empleados = [ana, luis, maria]
    for emp in empleados:
        print(emp.resumen())

    # 3) Calcular nómina total
    total = calcular_nomina(empleados)
    print(f"\nNómina total a pagar: ${total:.2f}")
