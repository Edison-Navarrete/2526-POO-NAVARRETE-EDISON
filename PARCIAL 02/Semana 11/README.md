# Sistema Avanzado de Gestión de Inventario — Semana 11

Implementa un sistema de inventario con **POO**, uso de **colecciones** (listas, diccionarios, conjuntos, tuplas) y **persistencia en archivos** (JSON). Incluye un **menú de consola** para operaciones CRUD.

## 🎯 Objetivos
- Aplicar POO (clases `Producto` e `Inventario`).
- Usar colecciones adecuadas:
  - `dict[str, Producto]` para índice por ID (búsqueda O(1) promedio),
  - `list[Producto]` para listados/ordenamientos,
  - `set[str]` para unicidad/etiquetas (opcional),
  - `tuple[...]` para retornos inmutables (resúmenes).
- Persistir datos en **JSON** (lectura/escritura).#

# interactuar con el metodo main (main.py)
## 🗂️ Estructura