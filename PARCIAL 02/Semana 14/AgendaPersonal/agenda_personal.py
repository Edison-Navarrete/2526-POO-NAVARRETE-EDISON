import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar
import itertools

# ============================================================
# Selector de fecha (DatePicker) sin dependencias externas
# ============================================================
class DatePicker(tk.Toplevel):
    """
    Este componente proporciona un selector de fecha modal con navegación mensual.
    Se diseña para integrarse con entradas que usan el formato DD/MM/AAAA.
    """

    def __init__(self, master=None, initial_date=None, locale_es=True):
        super().__init__(master)
        self.title("Seleccionar fecha")
        self.resizable(False, False)
        self.transient(master)   # Se muestra como ventana hija
        self.grab_set()          # Modal: bloquea interacción con la ventana principal
        self.selected = None

        # Se establece el mes y año iniciales a partir de la fecha indicada o la actual.
        today = date.today()
        base = initial_date or today
        self.current_year = base.year
        self.current_month = base.month
        self.locale_es = locale_es

        # Encabezado de navegación
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        btn_prev = ttk.Button(top, text="<<", width=3, command=self._prev_month)
        btn_prev.pack(side="left")

        self.lbl_month = ttk.Label(top, text="", anchor="center", font=("Segoe UI", 10, "bold"))
        self.lbl_month.pack(side="left", expand=True, fill="x")

        btn_next = ttk.Button(top, text=">>", width=3, command=self._next_month)
        btn_next.pack(side="right")

        # Contenedor de encabezado de días y grilla de días
        grid = ttk.Frame(self, padding=(8, 0, 8, 8))
        grid.pack()

        self.weekday_header = ttk.Frame(grid)
        self.weekday_header.pack(fill="x", pady=(0, 4))

        self.days_frame = ttk.Frame(grid)
        self.days_frame.pack()

        # Botón de cancelación
        bottom = ttk.Frame(self, padding=8)
        bottom.pack(fill="x")
        btn_cancel = ttk.Button(bottom, text="Cancelar", command=self._cancel)
        btn_cancel.pack(side="right")

        # Construcciones iniciales
        self._build_header()
        self._build_days()

        # Centrado respecto a la ventana padre
        self.update_idletasks()
        if master is not None:
            self._center_to_parent(master)

    def _center_to_parent(self, parent):
        """Centra la ventana emergente con respecto a su ventana padre."""
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        sw = self.winfo_width()
        sh = self.winfo_height()
        x = px + (pw - sw) // 2
        y = py + (ph - sh) // 2
        self.geometry(f"+{x}+{y}")

    def _month_year_label(self):
        """Devuelve la etiqueta de mes y año localizados."""
        if self.locale_es:
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            return f"{meses[self.current_month - 1]} {self.current_year}"
        return f"{calendar.month_name[self.current_month]} {self.current_year}"

    def _build_header(self):
        """Construye los nombres de los días de la semana, comenzando en lunes."""
        for w in self.weekday_header.winfo_children():
            w.destroy()
        nombres = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, name in enumerate(nombres):
            lbl = ttk.Label(self.weekday_header, text=name, width=4, anchor="center")
            lbl.grid(row=0, column=i, padx=2)

    def _build_days(self):
        """Construye la grilla de días del mes vigente."""
        self.lbl_month.config(text=self._month_year_label())

        for w in self.days_frame.winfo_children():
            w.destroy()

        cal = calendar.Calendar(firstweekday=calendar.MONDAY)
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)

        for r, week in enumerate(month_days):
            for c, day_num in enumerate(week):
                if day_num == 0:
                    # Celda fuera del mes: se muestra vacía
                    lbl = ttk.Label(self.days_frame, text="", width=4, anchor="center")
                    lbl.grid(row=r, column=c, padx=2, pady=2)
                else:
                    # Cada día es un botón que fija la fecha seleccionada
                    btn = ttk.Button(self.days_frame, text=str(day_num), width=4,
                                     command=lambda d=day_num: self._select_day(d))
                    btn.grid(row=r, column=c, padx=2, pady=2)

    def _select_day(self, day):
        """Fija la fecha seleccionada y cierra la ventana."""
        try:
            self.selected = date(self.current_year, self.current_month, day)
        except ValueError:
            messagebox.showerror("Fecha inválida", "La fecha seleccionada no es válida.")
            self.selected = None
        self.destroy()

    def _prev_month(self):
        """Navega al mes anterior."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._build_days()

    def _next_month(self):
        """Navega al mes siguiente."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._build_days()

    def _cancel(self):
        """Cancela la selección de fecha."""
        self.selected = None
        self.destroy()

    def show(self):
        """Muestra la ventana de forma modal y devuelve la fecha seleccionada o None."""
        self.wait_window(self)
        return self.selected


# ============================================================
# Aplicación principal de Agenda Personal
# ============================================================
class AgendaApp(tk.Tk):
    """
    Esta aplicación implementa una agenda personal con:
    - Listado de eventos en un Treeview (Fecha, Hora, Descripción).
    - Formulario para registrar nuevos eventos.
    - Selector de fecha propio y validación estricta de hora (24 h).
    - Eliminación con confirmación.
    - Organización visual mediante Frames.
    - Inserción ordenada (cronológica) por fecha y hora.
    """

    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("860x540")
        self.minsize(760, 480)

        # Contenedor en memoria: cada evento es un dict con id, fecha, hora, descripcion y datetime combinado
        self._id_counter = itertools.count(1)
        self.events = []

        # Construcción de interfaz y atajos
        self._build_ui()
        self._bind_shortcuts()

    # ---------------------- Construcción UI ----------------------
    def _build_ui(self):
        """Construye la interfaz en tres áreas mediante Frames: lista, formulario y acciones."""
        # Área superior: Treeview con scroll
        frame_tree = ttk.Frame(self, padding=8)
        frame_tree.pack(fill="both", expand=True)

        columnas = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", selectmode="browse")
        self.tree.heading("fecha", text="Fecha (DD/MM/AAAA)")
        self.tree.heading("hora", text="Hora (HH:MM)")
        self.tree.heading("descripcion", text="Descripción")

        self.tree.column("fecha", width=160, anchor="center")
        self.tree.column("hora", width=120, anchor="center")
        self.tree.column("descripcion", width=520, anchor="w")

        vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        # Parámetros correctos de asociación de scrollbars
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_tree.rowconfigure(0, weight=1)
        frame_tree.columnconfigure(0, weight=1)

        # Área media: formulario
        frame_form = ttk.LabelFrame(self, text="Nuevo evento", padding=8)
        frame_form.pack(fill="x", padx=8, pady=(0, 8))

        # Campo Fecha
        lbl_fecha = ttk.Label(frame_form, text="Fecha:")
        lbl_fecha.grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)

        self.var_fecha = tk.StringVar()
        self.ent_fecha = ttk.Entry(frame_form, textvariable=self.var_fecha, width=16)
        self.ent_fecha.grid(row=0, column=1, sticky="w", pady=4)

        self.btn_cal = ttk.Button(frame_form, text="Calendario", width=10, command=self._open_datepicker)
        self.btn_cal.grid(row=0, column=2, sticky="w", padx=(6, 12), pady=4)

        lbl_fmt_fecha = ttk.Label(frame_form, text="Formato: DD/MM/AAAA")
        lbl_fmt_fecha.grid(row=0, column=3, sticky="w", pady=4)

        # Campo Hora
        lbl_hora = ttk.Label(frame_form, text="Hora:")
        lbl_hora.grid(row=1, column=0, sticky="w", padx=(0, 6), pady=4)

        self.var_hora = tk.StringVar()
        self.ent_hora = ttk.Entry(frame_form, textvariable=self.var_hora, width=16)
        self.ent_hora.grid(row=1, column=1, sticky="w", pady=4)

        lbl_fmt_hora = ttk.Label(frame_form, text="Formato: 24 h (HH:MM)")
        lbl_fmt_hora.grid(row=1, column=3, sticky="w", pady=4)

        # Campo Descripción
        lbl_desc = ttk.Label(frame_form, text="Descripción:")
        lbl_desc.grid(row=2, column=0, sticky="w", padx=(0, 6), pady=4)

        self.var_desc = tk.StringVar()
        self.ent_desc = ttk.Entry(frame_form, textvariable=self.var_desc, width=70)
        self.ent_desc.grid(row=2, column=1, columnspan=3, sticky="we", pady=4)

        frame_form.columnconfigure(1, weight=0)
        frame_form.columnconfigure(3, weight=1)

        # Doble clic en el Entry de fecha abre el calendario
        self.ent_fecha.bind("<Double-1>", lambda e: self._open_datepicker())

        # Área inferior: acciones
        frame_actions = ttk.Frame(self, padding=8)
        frame_actions.pack(fill="x")

        self.btn_add = ttk.Button(frame_actions, text="Agregar Evento", command=self._on_add)
        self.btn_add.pack(side="left")

        self.btn_del = ttk.Button(frame_actions, text="Eliminar Evento Seleccionado", command=self._on_delete)
        self.btn_del.pack(side="left", padx=6)

        btn_exit = ttk.Button(frame_actions, text="Salir", command=self.destroy)
        btn_exit.pack(side="right")

        # Foco inicial sobre la descripción para agilizar captura
        self.ent_desc.focus_set()

    def _bind_shortcuts(self):
        """Asigna atajos de teclado para mejorar la usabilidad."""
        self.bind("<Return>", lambda e: self._on_add())
        self.bind("<Delete>", lambda e: self._on_delete())

    # ---------------------- Lógica de acciones ----------------------
    def _open_datepicker(self):
        """Abre el DatePicker con la fecha actual o la escrita si es válida."""
        init_date = date.today()
        texto = self.var_fecha.get().strip()
        if texto:
            try:
                init_date = datetime.strptime(texto, "%d/%m/%Y").date()
            except ValueError:
                # Si la fecha no es válida, se ignora y se usa hoy.
                pass

        dp = DatePicker(self, initial_date=init_date, locale_es=True)
        selected = dp.show()
        if selected:
            self.var_fecha.set(selected.strftime("%d/%m/%Y"))

    def _on_add(self):
        """Valida campos y agrega un evento ordenándolo cronológicamente."""
        fecha_str = self.var_fecha.get().strip()
        hora_str = self.var_hora.get().strip()
        desc_str = self.var_desc.get().strip()

        # Validación de campos vacíos
        if not fecha_str or not hora_str or not desc_str:
            messagebox.showwarning("Campos incompletos", "Completar Fecha, Hora y Descripción.")
            return

        # Validación de fecha
        try:
            fecha_dt = datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usar formato DD/MM/AAAA y una fecha existente.")
            return

        # Validación de hora (24 h)
        try:
            hora_dt = datetime.strptime(hora_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Hora inválida", "Usar formato 24 h HH:MM (ej.: 09:30, 14:05).")
            return

        combinado = datetime(
            year=fecha_dt.year, month=fecha_dt.month, day=fecha_dt.day,
            hour=hora_dt.hour, minute=hora_dt.minute
        )

        # Alta del evento
        ev = {
            "id": next(self._id_counter),
            "fecha": fecha_str,
            "hora": hora_str,
            "descripcion": desc_str,
            "dt": combinado
        }
        self.events.append(ev)

        # Refresco de la vista
        self._refresh_tree()

        # Limpieza parcial para agilizar nuevas capturas
        self.var_desc.set("")
        self.ent_desc.focus_set()

    def _on_delete(self):
        """Solicita confirmación y elimina el evento seleccionado."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Sin selección", "Seleccionar un evento de la lista para eliminarlo.")
            return

        if not messagebox.askyesno("Confirmar eliminación", "¿Eliminar el evento seleccionado?"):
            return

        iid = sel[0]
        # Se mapea el iid del Treeview al id interno del evento para eliminar en el modelo
        try:
            ev_id = int(iid)
            self.events = [e for e in self.events if e["id"] != ev_id]
            self.tree.delete(iid)
        except ValueError:
            # Respaldo: eliminación por valores (no debería ser necesario)
            vals = self.tree.item(iid, "values")
            f, h, d = vals
            self.events = [e for e in self.events if not (e["fecha"] == f and e["hora"] == h and e["descripcion"] == d)]
            self.tree.delete(iid)

    def _refresh_tree(self):
        """Ordena y repuebla el Treeview con los datos consistentes."""
        # Orden cronológico
        self.events.sort(key=lambda e: e["dt"])

        # Limpieza
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Inserción (iid = id interno)
        for ev in self.events:
            self.tree.insert("", "end", iid=str(ev["id"]), values=(ev["fecha"], ev["hora"], ev["descripcion"]))


# ---------------------- Punto de entrada ----------------------
if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
