"""
PUNTO-CONTROL DE DATOS
Punto de entrada de la aplicación. Ensambla Modelo, Vista y Controlador.
"""

# --- Importaciones del paquete local que implementa el patrón MVC con Tkinter.
from punto_control_datos.modelo import ItemStore
from punto_control_datos.vista import AppView
from punto_control_datos.controlador import AppController


def main():
    # --- Inicialización del modelo que gestiona los datos en memoria.
    store = ItemStore()

    # --- Creación de la vista (ventana Tkinter) con componentes y layout.
    view = AppView()

    # --- Enlace entre la vista y el modelo mediante el controlador que gestiona eventos.
    controller = AppController(store=store, view=view)

    # --- Inicio del loop principal de la GUI para atender eventos de usuario.
    view.mainloop()


if __name__ == "__main__":
    main()