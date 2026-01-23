
# tarea_constructores_destructores.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable
import logging
import socket
import gc

# -----------------------------------------------------------
# Configuración de logging para ver a detalle el desarrollo
# -----------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


class GestorArchivo:
    """
    Clase que DEMUESTRA el uso de:
      - __init__ (constructor): adquiere un recurso (archivo) e inicializa atributos.
      - __del__ (destructor): como RED DE SEGURIDAD para cerrar si el usuario olvidó.
      - Protocolo de contexto (__enter__/__exit__): garantiza cierre (mejor práctica).

    NOTAS CLAVE:
    - __init__ se ejecuta AL CREAR la instancia (p.ej., a = GestorArchivo(...)).
    - __del__ lo invoca el recolector de basura cuando el objeto queda sin referencias.
      *No es determinístico ni está garantizado en un momento exacto.*
    - __exit__ se ejecuta al SALIR del bloque 'with', con o sin excepciones.
    """

    def __init__(self, path: str | Path, mode: str = "a", encoding: str = "utf-8", buffering: int = 1):
        """
        Constructor: prepara el objeto y abre el archivo (recurso a gestionar).
        """
        self.path: Path = Path(path)
        self._fh = open(self.path, mode=mode, encoding=encoding, buffering=buffering)
        self._cerrado: bool = False
        log.info(f"[GestorArchivo.__init__] Abrí: {self.path} (mode={mode}, encoding={encoding})")

    def write_line(self, text: str) -> None:
        """
        Escribe una línea de texto asegurando un único salto de línea final.
        """
        if self._cerrado:
            raise RuntimeError("Archivo cerrado.")
        self._fh.write(text.rstrip("\n") + "\n")

    def write_lines(self, lines: Iterable[str]) -> None:
        """
        Escribe múltiples líneas, reutilizando write_line.
        """
        for line in lines:
            self.write_line(line)

    def close(self) -> None:
        """
        Cierre EXPLÍCITO (recomendado). Idempotente: seguro si se llama más de una vez.
        """
        if not self._cerrado:
            try:
                self._fh.close()
                log.info(f"[GestorArchivo.close] Cerré: {self.path}")
            finally:
                self._cerrado = True

    # ---- Context manager (mejor práctica) ----
    def __enter__(self) -> "GestorArchivo":
        """
        Permite: with GestorArchivo(...) as f: ...
        """
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        """
        Se ejecuta SIEMPRE al salir del 'with': garantiza el cierre determinístico.
        Retorna False para no suprimir excepciones del bloque 'with'.
        """
        self.close()
        return False

    # ---- Destructor (último recurso) ----
    def __del__(self):
        """
        Destructor llamado por el GC cuando ya no hay referencias.
        Debe ser SILENCIOSO ante errores y actuar solo como respaldo.
        """
        if hasattr(self, "_cerrado") and not self._cerrado:
            try:
                self._fh.close()
                log.warning(f"[GestorArchivo.__del__] Cerré automáticamente (olvido) -> {self.path}")
            except Exception:
                # Nunca propagar excepciones desde __del__
                pass
            finally:
                self._cerrado = True


class ConexionSimulada:
    """
    Segunda clase para demostrar otro recurso (socket) y el patrón de limpieza.

    - __init__: crea el socket y configura timeout (recurso del sistema).
    - close: cierre explícito del socket (buena práctica).
    - __del__: red de seguridad si se olvidó cerrar.
    - (Opcional) __enter__/__exit__ para usarlo con 'with'.
    """

    def __init__(self, host: str = "localhost", port: int = 80, timeout: float = 1.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self.timeout)
        self._cerrado = False
        log.info(f"[ConexionSimulada.__init__] Socket creado para {self.host}:{self.port} (timeout={self.timeout})")
        # Para la demo NO conectamos a ningún sitio real (evita dependencias de red).

    def enviar_ping(self, data: bytes = b"ping") -> None:
        """
        Método ilustrativo (no conecta).
        """
        if self._cerrado:
            raise RuntimeError("Conexión cerrada.")
        log.info(f"[ConexionSimulada.enviar_ping] Simulando envío de {data!r} a {self.host}:{self.port}")

    def close(self) -> None:
        """
        Cierre explícito del socket (idempotente).
        """
        if not self._cerrado:
            try:
                self._sock.close()
                log.info("[ConexionSimulada.close] Socket cerrado.")
            finally:
                self._cerrado = True

    def __enter__(self) -> "ConexionSimulada":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False

    def __del__(self):
        if hasattr(self, "_cerrado") and not self._cerrado:
            try:
                self._sock.close()
                log.warning("[ConexionSimulada.__del__] Cerré socket automáticamente (olvido).")
            except Exception:
                pass
            finally:
                self._cerrado = True


# -----------------------------------------------------------
# ejemplo aplicacion(para ejecutar y observar constructores/destructores)
# -----------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Ejemplo 1: Uso recomendado con 'with' (cierre garantizado) ===")
    salida1 = Path("salida_con_with.txt")
    with GestorArchivo(salida1, mode="w") as f:
        f.write_lines(["Línea A", "Línea B", "Línea C"])
    # __exit__ ya cerró el archivo:
    print("Contenido (con with):")
    print(salida1.read_text(encoding="utf-8"))

    print("\n=== Ejemplo 2: Olvidar close() (ver __del__ como respaldo) ===")
    salida2 = Path("salida_olvido.txt")
    f2 = GestorArchivo(salida2, mode="w")
    f2.write_line("Este archivo se cerrará en __del__ si olvido close()")
    # Intencionalmente NO llamamos close()
    del f2
    # Forzamos recolección de basura para favorecer la ejecución de __del__ en la demo:
    gc.collect()
    print("Contenido (olvido):")
    print(salida2.read_text(encoding="utf-8"))

    print("\n=== Ejemplo 3: Recurso de sistema (socket) con 'with' ===")
    with ConexionSimulada(host="example.com", port=443, timeout=0.5) as conn:
        conn.enviar_ping()

    print("\n=== Ejemplo 4: Socket sin cerrar explícitamente (ver __del__) ===")
    conn2 = ConexionSimulada(host="example.org", port=80, timeout=0.5)
    conn2.enviar_ping(b"hola")
    # Olvidamos cerrar para que __del__ actúe
    del conn2
    gc.collect()

    print("\n=== Fin de la demostración ===")



