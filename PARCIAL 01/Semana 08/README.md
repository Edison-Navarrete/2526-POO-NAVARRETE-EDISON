# PROGRAMACION-ORIENTADA-A-OBJETOS
Este repositorio contiene el código fuente desarrollado durante la asignatura **Programación Orientada a Objetos**, impartida en la **Universidad Estatal Amazónica**. Está diseñado como un recurso de apoyo para estudiantes y profesionales interesados en conceptos y prácticas de programación orientada a objetos.

## Información de la asignatura

- **Institución**: Universidad Estatal Amazónica (UEA)  
- **Carrera**: Ingeniería en Tecnologías de la Información  
- **Asignatura**: Programación Orientada a Objetos  

## Contenido del repositorio

Este repositorio incluye:
1. Ejercicios prácticos de programación orientada a objetos.
2. Ejemplos de implementación en Python.
3. Proyectos desarrollados como parte de las actividades de la asignatura.
4. Documentación y apuntes adicionales para reforzar el aprendizaje.

## Objetivos

- Aplicar los principios fundamentales de la programación orientada a objetos.
- Desarrollar soluciones eficientes y estructuradas utilizando Python.
- Familiarizarse con conceptos como clases, objetos, herencia, polimorfismo y encapsulamiento.

## Instrucciones para el uso

1. Clona el repositorio:  
   ```bash
   git clone https://github.com/snogales-uea/2525-PROGRAMACION-ORIENTADA-A-OBJETOS.git
   cd 2525-PROGRAMACION-ORIENTADA-A-OBJETOS 

2. Crear un nuevo repositorio en tu cuenta de GitHub Ve a GitHub: https://github.com/new

3. Cambiar el repositorio remoto del proyecto clonado
   ```bash
   git remote remove origin
   git remote add origin https://github.com/tu-usuario/proyecto-clonado.git

4. Subir el proyecto a tu repositorio personal
   ```bash
   git push -u origin main
# Nuevo proyecto:
# Dashboard POO – Adaptación personal (Edison Navarrete)

Este proyecto parte del dashboard original del curso (UNIDAD 1/2: ver/ejecutar scripts) y **añade un Panel de Tareas** para organizar la materia de Programación Orientada a Objetos.

## ¿Qué hace?
- **Menú por unidades:** navegar por subcarpetas, **ver el código** de cada `.py` y **ejecutarlo** desde el menú.
- **Panel de Tareas (nuevo):**
  - Crear tarea (título, unidad, estado: `pendiente|en progreso|completada`, fecha `YYYY-MM-DD`, nota)
  - Listar todas
  - Filtrar por **estado** y por **unidad**
  - Ver **pendientes próximas** (ordenadas por fecha)
  - **Marcar como completada** (por ID)
  - **Eliminar** (por ID)
  - **Persistencia:** se guarda en `tareas.json` en la raíz del proyecto

## Cómo ejecutar
```bash
python Dashboard.py
## Adaptación realizada (Entrega)

Para esta tarea se adaptó el archivo `Dashboard.py` agregando un
**Panel de Tareas**, que permite:

- Crear tareas por unidad
- Listar tareas
- Filtrar por estado y unidad
- Ver pendientes próximas ordenadas por fecha
- Marcar tareas como completadas
- Eliminar tareas

Las tareas se guardan en el archivo `tareas.json`, lo que permite
persistencia de datos entre ejecuciones del programa.
 