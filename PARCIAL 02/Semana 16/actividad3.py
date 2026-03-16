"""3.- Explicar a detalle el funcionamiento del codigo del siguiente ejemplo básico en Python que
muestra cómo usar el módulo threading para aplicar el concepto de eventos en un programa,
análizar el resultado:"""

import threading
import time
# Creamos un objeto evento
evento = threading.Event()
# Función que espera a que se active el evento
def esperar_evento():
 print("Esperando al evento...")
 # Esperamos a que el evento se active
 evento.wait()
 print("El evento ha sido activado!")
# Función que activa el evento después de un cierto tiempo

def activar_evento():
 print("Esperando 5 segundos antes de activar el evento...")
 time.sleep(5)
 # Activamos el evento
 evento.set()
 print("El evento ha sido activado después de 5 segundos")
# Creamos dos hilos que ejecutarán las funciones
hilo1 = threading.Thread(target=esperar_evento)
hilo2 = threading.Thread(target=activar_evento)
# Iniciamos los hilos
hilo1.start()
hilo2.start()
# Esperamos a que ambos hilos terminen
hilo1.join()
hilo2.join()
print("Programa terminado")