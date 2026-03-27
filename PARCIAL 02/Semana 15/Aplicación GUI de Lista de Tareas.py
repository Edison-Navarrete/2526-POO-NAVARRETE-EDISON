import tkinter as tk
from tkinter import messagebox


class ListaTareasApp:
    """
    Clase principal que representa la aplicación de lista de tareas.
    Implementa Programación Orientada a Objetos encapsulando
    la interfaz gráfica, la lógica y el manejo de eventos.
    """

    def __init__(self, ventana):
        # Se inicializa la ventana principal de la aplicación
        self.root = ventana
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")

        # Se inicializan los atributos de la interfaz (buena práctica POO)
        self.entry_tarea = None
        self.lista_tareas = None

        # Se inicializa la estructura interna que almacena las tareas
        self.tareas = []

        # Se construye la interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        """
        Define y organiza todos los componentes gráficos
        requeridos por la aplicación.
        """

        # ===== REQUISITO: Campo de entrada para escribir nuevas tareas =====
        # Permite al usuario ingresar el texto de una nueva tarea
        self.entry_tarea = tk.Entry(self.root, width=35)
        self.entry_tarea.pack(pady=10)

        # ===== REQUISITO: Añadir tareas presionando la tecla Enter =====
        # Se asocia el evento Enter con el método de agregar tarea
        self.entry_tarea.bind("<Return>", self.agregar_tarea_evento)

        # ===== REQUISITO: Componente de lista para mostrar las tareas =====
        # Se utiliza un Listbox para visualizar las tareas registradas
        self.lista_tareas = tk.Listbox(self.root, width=50, height=12)
        self.lista_tareas.pack(pady=10)

        # ===== REQUISITO: Botón para añadir una nueva tarea =====
        # Inserta la tarea escrita en el campo de entrada
        btn_agregar = tk.Button(
            self.root,
            text="Añadir Tarea",
            command=self.agregar_tarea
        )
        btn_agregar.pack(pady=5)

        # ===== REQUISITO: Botón para marcar tarea como completada =====
        # Cambia el estado visual de la tarea seleccionada
        btn_completar = tk.Button(
            self.root,
            text="Marcar como Completada",
            command=self.marcar_completada
        )
        btn_completar.pack(pady=5)

        # ===== REQUISITO: Botón para eliminar tarea =====
        # Elimina la tarea seleccionada de la lista
        btn_eliminar = tk.Button(
            self.root,
            text="Eliminar Tarea",
            command=self.eliminar_tarea
        )
        btn_eliminar.pack(pady=5)

        # ===== EVENTO ADICIONAL: Doble clic para marcar tarea =====
        # Mejora la interacción permitiendo completar tareas con doble clic
        self.lista_tareas.bind("<Double-Button-1>", self.marcar_completada_evento)

    def agregar_tarea(self):
        """
        Agrega una nueva tarea a la lista si el campo no está vacío.
        """
        tarea_texto = self.entry_tarea.get().strip()

        if tarea_texto:
            self.tareas.append({
                "texto": tarea_texto,
                "completada": False
            })
            self.lista_tareas.insert(tk.END, tarea_texto)
            self.entry_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning(
                "Advertencia",
                "La tarea no puede estar vacía."
            )

    def agregar_tarea_evento(self, event):
        """
        Permite agregar tareas utilizando la tecla Enter.
        """
        _ = event  # El parámetro event es requerido por Tkinter
        self.agregar_tarea()

    def marcar_completada(self):
        """
        Marca una tarea seleccionada como completada
        cambiando su representación visual.
        """
        try:
            index = int(self.lista_tareas.curselection()[0])
            tarea = self.tareas[index]

            if not tarea["completada"]:
                tarea["completada"] = True
                texto_actualizado = "✔ " + tarea["texto"]
                self.lista_tareas.delete(index)
                self.lista_tareas.insert(index, texto_actualizado)
        except IndexError:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una tarea para marcarla."
            )

    def marcar_completada_evento(self, event):
        """
        Permite marcar una tarea como completada mediante doble clic.
        """
        _ = event
        self.marcar_completada()

    def eliminar_tarea(self):
        """
        Elimina la tarea seleccionada tanto de la interfaz
        como de la estructura interna de datos.
        """
        try:
            index = int(self.lista_tareas.curselection()[0])
            self.lista_tareas.delete(index)
            self.tareas.pop(index)
        except IndexError:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una tarea para eliminarla."
            )


# ===== PUNTO DE INICIO DE LA APLICACIÓN =====
# Se crea la ventana principal y se ejecuta el bucle de la interfaz gráfica
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = ListaTareasApp(ventana_principal)
    ventana_principal.mainloop()
