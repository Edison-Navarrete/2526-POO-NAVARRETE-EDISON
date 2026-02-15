"""
Programa: registro_estudiantes_simple.py
Unidad Educativa "Antonio José de Sucre"
Descripción:
Gestión básica de estudiantes usando POO.
Campos: nombre, edad (12-19), curso, paralelo, promedio, estado (Aprobado/Reprobado).
Opciones: agregar, listar, actualizar promedio, salir.
"""

NOTA_APROBACION = 7.0  # Umbral para aprobar


class Estudiante:
    """Clase que representa a un estudiante."""

    def __init__(self, nombre: str, edad: int, curso: str, paralelo: str, promedio: float):
        if not (12 <= edad <= 19):
            raise ValueError("La edad debe estar entre 12 y 19 años.")
        if not (0.0 <= promedio <= 10.0):
            raise ValueError("El promedio debe estar entre 0.0 y 10.0.")
        self.nombre = nombre
        self.edad = edad
        self.curso = curso
        self.paralelo = paralelo
        self.promedio = promedio
        self.aprobado = self.promedio >= NOTA_APROBACION

    def actualizar_promedio(self, nuevo_promedio: float):
        if not (0.0 <= nuevo_promedio <= 10.0):
            raise ValueError("El promedio debe estar entre 0.0 y 10.0.")
        self.promedio = nuevo_promedio
        self.aprobado = self.promedio >= NOTA_APROBACION

    def __str__(self):
        estado = "Aprobado" if self.aprobado else "Reprobado"
        return f"{self.nombre} | Edad: {self.edad} | Curso: {self.curso}-{self.paralelo} | Promedio: {self.promedio:.2f} | Estado: {estado}"


class GestorEstudiantes:
    """Clase que gestiona la lista de estudiantes."""

    def __init__(self):
        self.estudiantes = []

    def agregar(self, estudiante: Estudiante):
        self.estudiantes.append(estudiante)

    def listar(self):
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
        else:
            print("\n--- Estudiantes ---")
            for e in self.estudiantes:
                print(e)

    def actualizar_promedio(self, nombre: str, nuevo_promedio: float):
        for e in self.estudiantes:
            if e.nombre.lower() == nombre.lower():
                e.actualizar_promedio(nuevo_promedio)
                print(f"Promedio actualizado para {e.nombre}.")
                return
        print("Estudiante no encontrado.")


def ejecutar_programa():
    gestor = GestorEstudiantes()
    while True:
        print("\n--- Menú ---")
        print("1) Agregar estudiante")
        print("2) Listar estudiantes")
        print("3) Actualizar promedio")
        print("0) Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            try:
                nombre = input("Nombre: ")
                edad = int(input("Edad (12-19): "))
                curso = input("Curso (ej. 1° BGU): ")
                paralelo = input("Paralelo (ej. A): ")
                promedio = float(input("Promedio (0-10): "))
                estudiante = Estudiante(nombre, edad, curso, paralelo, promedio)
                gestor.agregar(estudiante)
                print(" Estudiante agregado.")
            except ValueError as e:
                print(f" Error: {e}")

        elif opcion == "2":
            gestor.listar()

        elif opcion == "3":
            nombre = input("Nombre del estudiante: ")
            try:
                nuevo_promedio = float(input("Nuevo promedio (0-10): "))
                gestor.actualizar_promedio(nombre, nuevo_promedio)
            except ValueError as e:
                print(f" Error: {e}")

        elif opcion == "0":
            print("¡Hasta pronto!")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    ejecutar_programa()
