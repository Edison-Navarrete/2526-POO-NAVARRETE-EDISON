"""
Módulo: vista
Responsabilidad: construir la interfaz gráfica (Tkinter/ttk), sus componentes y layout.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from pathlib import Path


class AppView(tk.Tk):
    """
    Ventana principal con título, entrada, botones, lista con scroll y barra de estado.
    Expone métodos para que el controlador actualice la UI y proxies para invocar handlers.
    """

    def __init__(self) -> None:
        super().__init__()

        # --- Estilo visual: tema ttk y colores base sobrios para una apariencia consistente.
        style = ttk.Style(self)
        try:
            style.theme_use("clam")  # 'clam' es un tema consistente y personalizable
        except Exception:
            pass  # Si no existe, se mantiene el tema por defecto

        # Colores base (ajustables)
        BG = "#F5F6FA"         # Fondo ventana
        FG = "#1c1f23"         # Texto principal

        # --- Fondo de la ventana principal y estilos generales.
        self.configure(bg=BG)
        style.configure("TLabel", background=BG, foreground=FG)
        style.configure("TButton", padding=6)
        style.configure("TEntry", fieldbackground="white")

        # --- Ventana principal con título descriptivo para identificar la aplicación en el sistema operativo.
        #     Título: "PUNTO-CONTROL DE DATOS".
        self.title("PUNTO-CONTROL DE DATOS")

        # --- Establece el icono de la aplicación, usando un archivo .ico o .png desde la carpeta assets.
        self._icon_img_ref = None  # Referencia para evitar GC si se usa PNG
        try:
            self.iconbitmap(default=str(self._resolver_ruta_asset("app_icon.ico")))
        except Exception:
            try:
                icon_img = tk.PhotoImage(file=str(self._resolver_ruta_asset("app_icon.png")))
                self.iconphoto(True, icon_img)
                self._icon_img_ref = icon_img
            except Exception:
                pass  # Si no hay icono disponible, continuar sin interrumpir la app

        # --- Ajuste visual general: tamaño mínimo y padding consistente.
        self.minsize(520, 360)
        self._pad = {"padx": 12, "pady": 10}

        # --- Variables y handlers (inyectados por el controlador).
        self.var_entrada = tk.StringVar()
        self.var_estado = tk.StringVar(value="Listo")
        self.handlers = None  # type: ignore
        self._estado_after_id: Optional[str] = None  # Timer para auto-reset de estado

        # --- Construcción UI + layout + atajos
        self._build()
        self._layout()
        self._bind()

    # ------------------------
    #  Construcción de widgets
    # ------------------------
    def _build(self) -> None:
        # --- Etiqueta de instrucción para guiar el ingreso de datos.
        self.lbl_instruccion = ttk.Label(self, text="Ingrese un ítem:")

        # --- Campo de texto (Entry) para capturar la información a agregar.
        self.txt_entrada = ttk.Entry(self, textvariable=self.var_entrada, width=48)

        # --- Botón "Agregar": incorpora el contenido del Entry a la lista mostrada.
        self.btn_agregar = ttk.Button(self, text="Agregar", command=self._proxy_on_agregar)

        # --- Listbox con scrollbar para presentar los ítems ingresados.
        self.lst_items = tk.Listbox(self, height=12, activestyle="dotbox")
        self.lst_items.configure(bg="white", fg="#1c1f23", highlightthickness=1,
                                 highlightcolor="#d0d4dc", relief="flat")
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.lst_items.yview)
        self.lst_items.configure(yscrollcommand=self.scroll.set)

        # --- Botón "Limpiar": borra el Entry y deselecciona la lista (Opción B).
        self.btn_limpiar = ttk.Button(self, text="Limpiar", command=self._proxy_on_limpiar)

        # --- Botón "Eliminar seleccionado": remueve el elemento activo (inicia deshabilitado).
        self.btn_eliminar = ttk.Button(self, text="Eliminar seleccionado",
                                       command=self._proxy_on_eliminar, state="disabled")

        # --- Botón "Salir": cierra la aplicación de forma segura.
        self.btn_salir = ttk.Button(self, text="Salir", command=self._proxy_on_cerrar)

        # --- Etiqueta de estado para mensajes informativos y de validación.
        self.lbl_estado = ttk.Label(self, textvariable=self.var_estado, foreground="#1f6f1f")

    # -----------------
    #  Distribución UI
    # -----------------
    def _layout(self) -> None:
        # --- Expansión: Entry/Listbox crecen con la ventana.
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        self.lbl_instruccion.grid(row=0, column=0, sticky="w", **self._pad)
        self.txt_entrada.grid(row=0, column=1, sticky="we", **self._pad)
        self.btn_agregar.grid(row=0, column=2, sticky="e", **self._pad)

        self.lst_items.grid(row=1, column=0, columnspan=2, rowspan=3, sticky="nsew", **self._pad)
        self.scroll.grid(row=1, column=2, rowspan=3, sticky="ns", **self._pad)

        self.btn_limpiar.grid(row=4, column=0, sticky="w", **self._pad)
        self.btn_eliminar.grid(row=4, column=1, sticky="e", **self._pad)
        self.btn_salir.grid(row=4, column=2, sticky="e", **self._pad)

        self.lbl_estado.grid(row=5, column=0, columnspan=3, sticky="we", **self._pad)

        # --- Foco inicial en el Entry para agilizar la interacción.
        self.txt_entrada.focus_set()

    # ---------------------
    #  Atajos de teclado
    # ---------------------
    def _bind(self) -> None:
        # --- Asociación de Enter para agregar.
        self.txt_entrada.bind("<Return>", lambda e: self._proxy_on_agregar())
        # --- Asociación de Supr para eliminar seleccionado.
        self.lst_items.bind("<Delete>", lambda e: self._proxy_on_eliminar())
        # --- Habilita o deshabilita el botón Eliminar según la selección actual.
        self.lst_items.bind("<<ListboxSelect>>", lambda e: self._actualizar_estado_eliminar())
        # --- Gestión del cierre por botón de ventana.
        self.protocol("WM_DELETE_WINDOW", self._proxy_on_cerrar)

    # ============== API de UI ==============

    def mostrar_item(self, texto: str) -> None:
        """Inserta un nuevo ítem en la Listbox."""
        self.lst_items.insert(tk.END, texto)

    def cargar_lista(self, items: list) -> None:
        """Carga una colección completa en la lista."""
        self.lst_items.delete(0, tk.END)
        for it in items:
            self.lst_items.insert(tk.END, it)

    def limpiar_entrada(self) -> None:
        """Limpia el campo de entrada y mantiene el foco para nueva captura."""
        self.var_entrada.set("")
        self.txt_entrada.focus_set()

    def deseleccionar_lista(self) -> None:
        """Opción B: deselecciona cualquier elemento activo de la lista."""
        self.lst_items.selection_clear(0, tk.END)
        self.lst_items.activate(-1)

    def indice_seleccionado(self) -> Optional[int]:
        """Devuelve el índice seleccionado o None si no hay selección."""
        sel = self.lst_items.curselection()
        return sel[0] if sel else None

    def eliminar_en_lista(self, idx: int) -> None:
        """Elimina el elemento en el índice indicado de la vista."""
        self.lst_items.delete(idx)

    def set_estado(self, mensaje: str, *, color: Optional[str] = None) -> None:
        """
        Actualiza el mensaje de estado; restaura automáticamente a “Listo” tras 2 segundos.
        Evita solapamientos de timers si se muestra otro estado antes de completar el anterior.
        """
        self.var_estado.set(mensaje)
        if color:
            self.lbl_estado.configure(foreground=color)

        if self._estado_after_id:
            try:
                self.after_cancel(self._estado_after_id)
            except Exception:
                pass
            self._estado_after_id = None

        def _reset():
            self.var_estado.set("Listo")
            self.lbl_estado.configure(foreground="#1f6f1f")
            self._estado_after_id = None

        self._estado_after_id = str(self.after(2000, _reset))

    def _actualizar_estado_eliminar(self) -> None:
        """Habilita o deshabilita el botón Eliminar dependiendo de la selección."""
        sel = self.lst_items.curselection()
        if sel:
            self.btn_eliminar.configure(state="normal")
        else:
            self.btn_eliminar.configure(state="disabled")

    def _resolver_ruta_asset(self, nombre: str) -> Path:
        """
        Resuelve la ruta absoluta de un archivo dentro de la carpeta 'assets' de Semana 13,
        independientemente de si el script se ejecuta desde PyCharm o terminal.
        """
        base = Path(__file__).resolve().parent.parent  # .../Semana 13/punto_control_datos
        semana_13_dir = base.parent                     # .../Semana 13
        assets = semana_13_dir / "assets"
        return assets / nombre

    # ============== Proxies a handlers ==============

    def _proxy_on_agregar(self) -> None:
        if self.handlers and hasattr(self.handlers, "on_agregar"):
            self.handlers.on_agregar()

    def _proxy_on_limpiar(self) -> None:
        if self.handlers and hasattr(self.handlers, "on_limpiar"):
            self.handlers.on_limpiar()

    def _proxy_on_eliminar(self) -> None:
        if self.handlers and hasattr(self.handlers, "on_eliminar"):
            self.handlers.on_eliminar()

    def _proxy_on_cerrar(self) -> None:
        if self.handlers and hasattr(self.handlers, "on_cerrar"):
            self.handlers.on_cerrar()
        else:
            # Cierre seguro por defecto en caso de no existir controlador.
            self.destroy()