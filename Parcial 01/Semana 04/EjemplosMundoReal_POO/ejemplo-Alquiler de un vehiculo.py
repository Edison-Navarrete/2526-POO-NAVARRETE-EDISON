
class Vehiculo:
    """Representa un vehículo disponible para alquiler en la agencia."""

    def __init__(self, placa, marca, modelo, anio, color):
        """Inicializa un nuevo vehículo con placa, marca, modelo, año y color."""
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.esta_alquilado = False  # análogo a 'is_borrowed' del ejemplo

    def alquilar(self):
        """Alquila el vehículo si no está actualmente alquilado."""
        if not self.esta_alquilado:
            self.esta_alquilado = True
            return True
        return False

    def devolver(self):
        """Devuelve el vehículo a la agencia (marca como no alquilado)."""
        self.esta_alquilado = False

    def __str__(self):
        """Devuelve una representación en cadena del vehículo."""
        estado = "Alquilado" if self.esta_alquilado else "Disponible"
        return f"{self.marca} {self.modelo} ({self.anio}) | Placa: {self.placa} | Color: {self.color} | Estado: {estado}"


class Persona:
    """Representa una persona en el sistema: cliente (usuario) o agente (de la agencia)."""

    def __init__(self, nombre, rol):
        """Inicializa una nueva persona con un nombre y un rol ('cliente' o 'agente')."""
        self.nombre = nombre
        self.rol = rol  # 'cliente' o 'agente'
        if self.rol == 'cliente':
            self.vehiculos_alquilados = []  # análogo a borrowed_books

    def alquilar_vehiculo(self, vehiculo):
        """Permite a la persona alquilar un vehículo (si es 'cliente' y el vehículo está disponible)."""
        if self.rol == 'cliente':
            if not vehiculo.esta_alquilado:
                ok = vehiculo.alquilar()
                if ok:
                    self.vehiculos_alquilados.append(vehiculo)
                    print(f"{self.nombre} ha alquilado el vehículo: {vehiculo.marca} {vehiculo.modelo}")
                else:
                    print(f"El vehículo con placa {vehiculo.placa} no está disponible.")
            else:
                print(f"El vehículo con placa {vehiculo.placa} no está disponible.")
        else:
            print(f"{self.nombre} no puede alquilar (rol '{self.rol}').")

    def devolver_vehiculo(self, vehiculo):
        """Permite a la persona devolver un vehículo (si es 'cliente' y lo tiene alquilado)."""
        if self.rol == 'cliente':
            if vehiculo in self.vehiculos_alquilados:
                vehiculo.devolver()
                self.vehiculos_alquilados.remove(vehiculo)
                print(f"{self.nombre} ha devuelto el vehículo: {vehiculo.marca} {vehiculo.modelo}")
            else:
                print(f"{self.nombre} no tiene alquilado el vehículo: {vehiculo.marca} {vehiculo.modelo}")
        else:
            print(f"{self.nombre} no puede devolver (rol '{self.rol}').")

    def gestionar_vehiculo(self, vehiculo, accion):
        """Gestiona acciones de alquiler o devolución (si es 'agente')."""
        if self.rol == 'agente':
            if accion == 'alquilar':
                return vehiculo.alquilar()
            elif accion == 'devolver':
                vehiculo.devolver()
        else:
            print(f"{self.nombre} no puede gestionar (rol '{self.rol}').")


# -----------------------------
# Ejemplo de uso con datos cargados
# -----------------------------
if __name__ == "__main__":
    # Vehículo: año: 2024 - marca: Toyota - modelo: Fortuner - color: negro
    vehiculo1 = Vehiculo(
        placa="ABC-2024",
        marca="Toyota",
        modelo="Fortuner",
        anio=2024,
        color="negro"
    )

    # Usuario (cliente) y agente
    cliente = Persona("María Fernández", "cliente")
    agente = Persona("Samantha Galarza", "agente")

    # Flujo: el cliente alquila el vehículo
    cliente.alquilar_vehiculo(vehiculo1)

    # Impresión final debe mostrar estado "Alquilado"
    print(vehiculo1)
