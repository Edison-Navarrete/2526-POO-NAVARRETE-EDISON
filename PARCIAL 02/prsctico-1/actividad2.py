"""2.- Explicar a detalle el funcionamiento del codigo del siguiente ejemplo básico en Python que
muestra cómo usar el módulo threading para aplicar el concepto de barreras en un programa,
análizar el resultado:"""

import threading
# Creamos una barrera para sincronizar dos hilos
barrera = threading.Barrier(2)
# Función que ejecuta la tarea de imprimir un mensaje y esperar en la barrera
def tarea():
 print("Hilo iniciado")
 # Esperamos en la barrera
 barrera.wait()
 print("Hilo continuando")
# Creamos dos hilos que ejecutarán la misma tarea
hilo1 = threading.Thread(target=tarea)
hilo2 = threading.Thread(target=tarea)
# Iniciamos los hilos
hilo1.start()
hilo2.start()
# Esperamos a que ambos hilos terminen
hilo1.join()
hilo2.join()
print("Programa terminado")