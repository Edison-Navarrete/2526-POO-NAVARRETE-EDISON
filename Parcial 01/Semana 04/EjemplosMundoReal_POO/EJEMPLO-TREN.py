
class Tren:
    def __init__(self, fabricante, modelo, capacidad, color, tipo_motor, tonelaje):
        # Atributos del tren
        self.fabricante = fabricante           # "ALSTOM"
        self.modelo = modelo                   # "TGV DUPLEX"
        self.capacidad = capacidad             # 634 pasajeros
        self.color = color                     # "naranja"
        self.tipo_motor = tipo_motor           # "eléctrico"
        self.tonelaje = tonelaje               # "424 toneladas"

        # Atributos operativos
        self.velocidad = 0
        self.ruta = None
        self.maquinista = None  # inicialmente sin maquinista

    # Métodos de acción
    def asignar_maquinista(self, persona):
        """Asigna un maquinista al tren si es instancia de Maquinista."""
        if isinstance(persona, Maquinista):
            self.maquinista = persona

    def establecer_ruta(self, ruta):
        """Establece la ruta actual del tren."""
        self.ruta = ruta
        # (Opcional)

    def acelerar(self, incremento):
        """Aumenta la velocidad del tren."""
        self.velocidad += incremento
        # print(f"El tren {self.modelo} aceleró a {self.velocidad} km/h")

    def frenar(self, decremento):
        """Disminuye la velocidad del tren (no baja de 0)."""
        self.velocidad = max(0, self.velocidad - decremento)
        # (Opcional)
        # print(f"El tren {self.modelo} frenó a {self.velocidad} km/h")

    def __str__(self):
        """
        Impresión EXACTA
        - Modelo del tren
        - Color
        - Capacidad
        - Nombre del maquinista y su cargo (Operador)
        """
        if self.maquinista:
            datos_maquinista = f"{self.maquinista.nombre} ({self.maquinista.cargo})"
        else:
            datos_maquinista = "Sin maquinista asignado"

        return (
            "Impresión solicitada:\n"
            f"        - Modelo del tren: {self.modelo}\n"
            f"        - Color: {self.color}\n"
            f"        - Capacidad: {self.capacidad} pasajeros\n"
            f"        - Nombre del maquinista y su cargo: {datos_maquinista}"
        )


class Maquinista:
    def __init__(self, nombre, identificacion, edad, cargo="Operador"):
        self.nombre = nombre
        self.identificacion = identificacion
        self.edad = edad
        self.cargo = cargo

    def __str__(self):
        """Descripción del maquinista (usada si se imprime directamente)."""
        return f"Maquinista: {self.nombre} (ID: {self.identificacion}, Edad: {self.edad}, Cargo: {self.cargo})"


# -----------------------------
# Demostración
# -----------------------------
if __name__ == "__main__":
    # Datos del tren
    tren = Tren(
        fabricante="ALSTOM",
        modelo="TGV DUPLEX",
        capacidad=634,
        color="naranja",
        tipo_motor="eléctrico",
        tonelaje="424 toneladas"
    )

    # Datos del maquinista
    operador = Maquinista(
        nombre="Marcos Kennedy",
        identificacion="0534527730",
        edad=28,
        cargo="Operador"
    )

    # Asignar maquinista y  operar
    tren.asignar_maquinista(operador)
    # tren.establecer_ruta("Quevedo - Guayaquil")
    # tren.acelerar(80)
    # tren.frenar(20)

    # Impresión final
    print(tren)

