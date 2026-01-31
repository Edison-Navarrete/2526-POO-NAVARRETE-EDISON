
class Bitacora:
    """Constructor abre/crea CSV; destructor cierra como respaldo; with garantiza cierre."""
    HEAD = ["fecha", "hora", "nombre", "tipo"]  # tipo: ENTRADA | SALIDA

    def __init__(self, ruta="bitacora.csv", encoding="utf-8"):
        self.ruta = Path(ruta)
        self._cerrado = False
        self._fh = open(self.ruta, "a", encoding=encoding, newline="")
        self._w = csv.writer(self._fh)
        if self.ruta.stat().st_size == 0:
            self._w.writerow(self.HEAD); self._fh.flush()
        log.info(f"Bitácora lista: {self.ruta.resolve()}")

    def entrada(self, nombre: str):
        self._reg(nombre, "ENTRADA")

    def salida(self, nombre: str):
        self._reg(nombre, "SALIDA")

    def _reg(self, nombre: str, tipo: str):
        nombre = nombre.strip()
        if not nombre or any(c in nombre for c in "\r\n"):
            raise ValueError("Nombre inválido.")
        ahora = datetime.now()
        self._w.writerow([ahora.strftime("%Y-%m-%d"),
                          ahora.strftime("%H:%M:%S"),
                          nombre, tipo])
        self._fh.flush()
        log.info(f"{tipo}: {nombre}")

    def close(self):
        if not self._cerrado:
            try: self._fh.close(); log.info("CSV cerrado.")
            finally: self._cerrado = True

    def __enter__(self): return self
    def __exit__(self, *_): self.close(); return False

    def __del__(self):
        if hasattr(self, "_cerrado") and not self._cerrado:
            try: self._fh.close(); log.warning("Cierre automático en __del__.")
            except Exception: pass
            finally: self._cerrado = True


# --------- DEMOSTRACION -EJEMPLO ---------
if __name__ == "__main__":
    print("== with (cierre garantizado) ==")
    with Bitacora("bitacora_demo.csv") as b:
        b.entrada("Ana Pérez"); b.entrada("Carlos Ramírez")
        b.salida("Ana Pérez");  b.salida("Carlos Ramírez")
    print(Path("bitacora_demo.csv").read_text(encoding="utf-8"))

    print("\n== olvido de close() (actúa __del__) ==")
    b2 = Bitacora("bitacora_demo.csv"); b2.entrada("María López")
    del b2; gc.collect()
    print(Path("bitacora_demo.csv").read_text(encoding="utf-8"))
