""".- Explicar a detalle el funcionamiento del codigo y la ejecución del ejemplo práctico en Python
que muestra cómo usar el módulo threading para aplicar el concepto de mutex en un
programa, en este caso se usa la biblioteca threading. Lock
El siguiente código simula un escenario en él creamos una variable global contador_global y
un objeto mutex utilizando threading. Lock().
El uso del mutex asegura que solo un hilo pueda ejecutar la sección crítica (incrementar el
contador) en un momento dado, evitando condiciones de carrera y garantizando que el
resultado final sea predecible y correcto."""
import threading
# Definimos una variable global compartida
contador_global = 0
# Creamos un objeto mutex
mutex = threading.Lock()
# Función que incrementa el contador global de forma segura utilizando un mutex
def incrementar():
 global contador_global
 # Adquirimos el mutex
 mutex.acquire()
try:
 # Sección crítica: Incrementamos el contador
 contador_global += 1
finally:
 # Liberamos el mutex
 mutex.release()
# Función que ejecuta la tarea de incrementar el contador un número determinado de veces
def tarea():
 for _ in range(100000):
  incrementar()
# Creamos dos hilos que ejecutarán la misma tarea
hilo1 = threading.Thread(target=tarea)
hilo2 = threading.Thread(target=tarea)
# Iniciamos los hilos
hilo1.start()
hilo2.start()
# Esperamos a que ambos hilos terminen
hilo1.join()
hilo2.join()
# Imprimimos el valor final del contador global
print("El valor final del contador global es:", contador_global)