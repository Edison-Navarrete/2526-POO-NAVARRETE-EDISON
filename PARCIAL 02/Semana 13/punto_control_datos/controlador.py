"""
Módulo: controlador
Responsabilidad: enlazar la vista con el modelo y gestionar los eventos de usuario.
"""

from tkinter import messagebox
from .modelo import ItemStore
from .vista import AppView


class AppController:
    """
    Orquestador de la aplicación. Recibe eventos de la vista, aplica reglas del modelo
    y actualiza la interfaz conforme a los resultados.
    """

    def __init__(self, store: ItemStore, view: AppView) -> None:
        # --- Inyección de dependencias: modelo (datos) y vista (interfaz gráfica).
        self.store = store
        self.view = view

        # --- Registro de handlers en la vista para que los botones y atajos llamen a estas funciones.
        self.view.handlers = self

        # --- Carga inicial de datos (si existiera persistencia futura). Por ahora inicia vacío.
        self._refrescar_lista_inicial()

    # --- Refresca la vista con el contenido del modelo al iniciar o en recargas completas.
    def _refrescar_lista_inicial(self) -> None:
        self.view.cargar_lista(self.store.listar())
        self.view.set_estado("Listo", color="#1f6f1f")
        # --- Asegura que el botón Eliminar quede coherente con la selección (deshabilitado al inicio).
        self.view._actualizar_estado_eliminar()

    # =================
    #  MANEJADORES UI
    # =================

    # --- Botón "Agregar" y tecla Enter: obtiene texto del Entry, valida y persiste en el modelo.
    #     Luego inserta en la lista, limpia el Entry y actualiza el estado.
    def on_agregar(self) -> None:
        try:
            texto = self.view.var_entrada.get()
            agregado = self.store.agregar(texto)
            self.view.mostrar_item(agregado)
            self.view.limpiar_entrada()
            self.view.set_estado("Ítem agregado correctamente.", color="#1f6f1f")
            # --- Tras agregar no hay selección nueva, mantener coherencia del botón Eliminar.
            self.view._actualizar_estado_eliminar()
        except ValueError as ex:
            # --- Mensaje de validación no intrusivo para entradas vacías o inválidas.
            self.view.set_estado(str(ex), color="#9c2626")

    # --- Botón "Limpiar": borra el Entry y deselecciona la lista (Opción B).
    #     Mejora el flujo de trabajo cuando se está ingresando una serie de elementos.
    def on_limpiar(self) -> None:
        self.view.limpiar_entrada()
        self.view.deseleccionar_lista()
        self.view._actualizar_estado_eliminar()
        self.view.set_estado("Entrada y selección limpiadas.", color="#1f6f1f")

    # --- Botón "Eliminar seleccionado" y tecla Supr: remueve el elemento activo de la vista y del modelo.
    #     Si no hay selección, se informa al usuario sin interrumpir el flujo con errores.
    def on_eliminar(self) -> None:
        idx = self.view.indice_seleccionado()
        if idx is None:
            self.view.set_estado("No hay selección para eliminar.", color="#9c2626")
            return
        try:
            self.store.eliminar_por_indice(idx)
            self.view.eliminar_en_lista(idx)
            self.view._actualizar_estado_eliminar()
            self.view.set_estado("Ítem eliminado correctamente.", color="#1f6f1f")
        except IndexError:
            # --- Contención defensiva en caso de desincronización improbable.
            self.view.set_estado("No fue posible eliminar el elemento seleccionado.", color="#9c2626")

    # --- Botón "Salir" o cierre de ventana: finaliza la aplicación con confirmación amigable.
    def on_cerrar(self) -> None:
        salir = messagebox.askyesno(
            title="Confirmar salida",
            message="¿Desea cerrar la aplicación?"
        )
        if salir:
            self.view.destroy()