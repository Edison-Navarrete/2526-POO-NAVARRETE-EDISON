# ======================================================
#  GESTOR DE INVENTARIO (versión copleta todos los requerimientos en un solo codigo)
#   - Producto con constructor, getters y setters (properties)
#   - Inventario con atributo "lista de productos"
#   - Estructura de datos personalizada para gestionar la colección
#   - CRUD + búsqueda + listado
#   - Menú interactivo en consola
#   - Comentarios en primera persona explicando mis decisiones
# ======================================================

# --- Clase Producto ---
# Aquí defino mi entidad base. Uso properties para validar toda asignación
# (incluida la que viene del constructor) y mantener los datos consistentes.
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        # Aplico setters para que todas las validaciones se ejecuten desde el inicio.
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        v = str(value).strip()
        if not v:
            raise ValueError("El ID no puede estar vacío.")
        self._id = v

    # nombre
    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        v = str(value).strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = v

    # cantidad
    @property
    def cantidad(self):
        return self._cantidad
    @cantidad.setter
    def cantidad(self, value):
        try:
            iv = int(value)
        except:
            raise ValueError("La cantidad debe ser un número entero.")
        if iv < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = iv

    # precio
    @property
    def precio(self):
        return self._precio
    @precio.setter
    def precio(self, value):
        try:
            fv = float(value)
        except:
            raise ValueError("El precio debe ser un número.")
        if fv < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = fv

    def __str__(self):
        return f"[{self.id}] {self.nombre} | Cant.: {self.cantidad} | Precio: ${self.precio:.2f}"


# --- Estructura de datos personalizada ---
# Aunque podría usar directamente una lista, yo prefiero encapsularla en una clase
# para controlar cómo se insertan, buscan, actualizan y eliminan los productos.
# Con esto evito que otra parte del programa manipule la colección sin reglas.
class EstructuraProductos:
    def __init__(self):
        self.__items = []  # mantengo la lista privada

    # Utilidad interna para encontrar índice por ID (evito duplicar lógica).
    def _index_por_id(self, id):
        for i, p in enumerate(self.__items):
            if p.id == id:
                return i
        return -1

    # Inserción con garantía de ID único.
    def insertar(self, producto: Producto):
        if self._index_por_id(producto.id) != -1:
            raise ValueError("Ya existe un producto con ese ID.")
        self.__items.append(producto)

    # Eliminación por ID.
    def eliminar(self, id: str):
        i = self._index_por_id(id)
        if i == -1:
            raise ValueError("No existe un producto con ese ID.")
        self.__items.pop(i)

    # Actualización de cantidad por ID.
    def actualizar_cantidad(self, id: str, nueva_cantidad):
        i = self._index_por_id(id)
        if i == -1:
            raise ValueError("No existe un producto con ese ID.")
        nc = int(nueva_cantidad)
        if nc < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__items[i].cantidad = nc

    # Actualización de precio por ID.
    def actualizar_precio(self, id: str, nuevo_precio):
        i = self._index_por_id(id)
        if i == -1:
            raise ValueError("No existe un producto con ese ID.")
        np = float(nuevo_precio)
        if np < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__items[i].precio = np

    # Búsqueda parcial por nombre (ignoro mayúsculas/minúsculas).
    def buscar_por_nombre(self, nombre_parcial: str):
        clave = (nombre_parcial or "").strip().lower()
        if not clave:
            return []
        return [p for p in self.__items if clave in p.nombre.lower()]

    # Entrego una copia para mostrar/recorrer (evito exponer la lista real).
    def todos(self):
        return self.__items[:]


# --- Clase Inventario ---
# Aquí agrupo las operaciones de negocio del inventario.txt. Internamente me apoyo
# en mi estructura personalizada. Para cumplir literalmente la consigna
# “Atributos: Una lista de productos”, expongo una propiedad que devuelve
# SIEMPRE una lista (copia) de los productos.
class Inventario:
    def __init__(self):
        self._estructura = EstructuraProductos()

    # Atributo: Una lista de productos (lo expongo como propiedad de solo lectura).
    @property
    def productos(self):
        # Devuelvo una lista (copia) para cumplir la consigna y mantener encapsulación.
        return self._estructura.todos()[:]

    # Métodos solicitados (CRUD + búsqueda + mostrar)
    def anadir_producto(self, producto: Producto):
        self._estructura.insertar(producto)

    def eliminar_por_id(self, id: str):
        self._estructura.eliminar(id)

    def actualizar_cantidad(self, id: str, cantidad):
        self._estructura.actualizar_cantidad(id, cantidad)

    def actualizar_precio(self, id: str, precio):
        self._estructura.actualizar_precio(id, precio)

    def buscar_por_nombre(self, nombre: str):
        return self._estructura.buscar_por_nombre(nombre)

    def mostrar_todos(self):
        return self._estructura.todos()


# --- Utilidades de entrada ---
# Centralizo validaciones básicas para que el programa no falle por entradas erróneas.
def leer_entero_no_negativo(msg):
    while True:
        try:
            v = int(input(msg).strip())
            if v < 0:
                print("⚠ Debe ser un entero >= 0.")
            else:
                return v
        except:
            print("⚠ Ingresa un entero válido.")

def leer_flotante_no_negativo(msg):
    while True:
        try:
            v = float(input(msg).strip())
            if v < 0:
                print("⚠ Debe ser un número >= 0.")
            else:
                return v
        except:
            print("⚠ Ingresa un número válido (ej. 10.5).")

def leer_texto_no_vacio(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠ Este campo no puede estar vacío.")


# --- Interfaz de Usuario (Consola) ---
# Mantengo el menú simple y claro: cada opción pide datos, valida y delega en Inventario.
def mostrar_menu():
    print("\n===== GESTOR DE INVENTARIO =====")
    print("1) Añadir producto")
    print("2) Eliminar producto por ID")
    print("3) Actualizar cantidad por ID")
    print("4) Actualizar precio por ID")
    print("5) Buscar producto(s) por nombre")
    print("6) Mostrar todos los productos")
    print("0) Salir")

def main():
    inv = Inventario()

    while True:
        mostrar_menu()
        op = input("Opción: ").strip()

        try:
            if op == "1":
                p = Producto(
                    leer_texto_no_vacio("ID (único): "),
                    leer_texto_no_vacio("Nombre: "),
                    leer_entero_no_negativo("Cantidad: "),
                    leer_flotante_no_negativo("Precio: ")
                )
                inv.anadir_producto(p)
                print("✅ Producto añadido.")

            elif op == "2":
                inv.eliminar_por_id(leer_texto_no_vacio("ID a eliminar: "))
                print("✅ Producto eliminado.")

            elif op == "3":
                inv.actualizar_cantidad(
                    leer_texto_no_vacio("ID: "),
                    leer_entero_no_negativo("Nueva cantidad: ")
                )
                print("✅ Cantidad actualizada.")

            elif op == "4":
                inv.actualizar_precio(
                    leer_texto_no_vacio("ID: "),
                    leer_flotante_no_negativo("Nuevo precio: ")
                )
                print("✅ Precio actualizado.")

            elif op == "5":
                resultados = inv.buscar_por_nombre(leer_texto_no_vacio("Nombre a buscar: "))
                if resultados:
                    for p in resultados:
                        print("   ", p)
                else:
                    print("ℹ No se encontraron coincidencias.")

            elif op == "6":
                productos = inv.mostrar_todos()
                if productos:
                    for p in productos:
                        print("   ", p)
                else:
                    print("ℹ Inventario vacío.")

            elif op == "0":
                print("👋 Saliendo del gestor...")
                break

            else:
                print("⚠ Opción inválida. Elige entre 0 y 6.")

        except Exception as e:
            print("❌ Error:", e)


# Punto de entrada
if __name__ == "__main__":
    main()