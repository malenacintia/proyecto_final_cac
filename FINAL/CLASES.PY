class Producto:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad disponible (stock)
        self.precio = precio           # Precio 


    # Este método permite modificar un producto.
    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.productos = []  # Lista de productos en el inventario (variable de clase)


    # Este método permite crear objetos de la clase "Producto" y agregarlos al inventario.
    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        self.productos.append(nuevo_producto)  # Agrega un nuevo producto a la lista


    # Este método permite consultar datos de productos que están en el inventario
    # Devuelve el producto correspondiente al código proporcionado o False si no existe.
    def consultar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto # Retorna un objeto
        return False

    # Este método permite modificar datos de productos que están en el inventario
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            sql = f'UPDATE productos SET descripcion = "{nueva_descripcion}", cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()


    # Este método elimina el producto indicado por codigo de la lista mantenida en el inventario.
    def eliminar_producto(self, codigo):
        sql = f'DELETE FROM productos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Producto {codigo} eliminado.')
            self.conexion.commit()
        else:
            print(f'Producto {codigo} no encontrado.')

    def listar_productos(self):
        print("-"*50)
        print("Lista de productos en el inventario:")
        print("Código\tDescripción\tCant\tPrecio")
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            print(f'{codigo}\t{descripcion}\t{cantidad}\t{precio}')
            print("-"*50)


class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []


    # Este método permite agregar productos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)
        if producto is False:
            print("El producto no existe.")
            return False
        if producto.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True

        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    print("Cantidad a quitar mayor a la cantidad en el carrito.")
                    return False
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                sql = f'UPDATE productos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True


        # Si el bucle finaliza sin novedad, es que ese producto NO ESTA en el carrito.
        print("El producto no se encuentra en el carrito.")
        return False

    def mostrar(self):
        print("-"*50)
        print("Lista de productos en el carrito:")
        print("Código\tDescripción\tCant\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}')
        print("-"*50)


# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()


# Agregar productos al inventario
mi_inventario.agregar_producto(1, "Producto 1", 10, 19.99)
mi_inventario.agregar_producto(2, "Producto 2", 5, 9.99)
mi_inventario.agregar_producto(3, "Producto 3", 15, 29.99)


# Consultar algún producto del inventario
print(mi_inventario.consultar_producto(3)) #Existe, se muestra la dirección de memoria
print(mi_inventario.consultar_producto(4)) #No existe, se muestra False


# Listar los productos del inventario
mi_inventario.listar_productos()

# Modificar un producto del inventario
mi_inventario.modificar_producto(2, "Mouse Rojo", 10, 19.99)


# Listar nuevamente los productos del inventario para ver la modificación
mi_inventario.listar_productos()


# Eliminar un producto
mi_inventario.eliminar_producto(3)


# Listar nuevamente los productos del inventario para ver la eliminación
mi_inventario.listar_productos()


# Crear una instancia de la clase Carrito
mi_carrito = Carrito()
# Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(1, 2, mi_inventario)  
# Agregar 1 unidad del producto con código 2 al carrito
mi_carrito.agregar(2, 1, mi_inventario)  


# Mostrar el contenido del carrito y del inventario
mi_carrito.mostrar()
mi_inventario.listar_productos()


'''
# Programa principal
producto = Producto(1, 'Teclado USB 101 teclas', 10, 4500)
# Accedemos a los atributos del objeto
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')
# Modificar los datos del producto
producto.modificar('Teclado Mecánico USB', 20, 4800) 
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')

# Programa principal
# Crear una instancia de la clase Inventario
mi_inventario = Inventario() 

# Agregar productos 
mi_inventario.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500)
mi_inventario.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500)
mi_inventario.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500)
mi_inventario.agregar_producto(4, 'Monitor LCD 27 pulgadas', 25, 78500)
mi_inventario.agregar_producto(5, 'Mouse Pad color azul', 5, 500)



# Consultar un producto 
producto = mi_inventario.consultar_producto(3)
if producto != False:
    print(f'Producto encontrado:\nCódigo: {producto.codigo}\nDescripción: {producto.descripcion}\nCantidad: {producto.cantidad}\nPrecio: {producto.precio}')  
else:
    print("Producto no encontrado.")


# Modificar un producto 
mi_inventario.modificar_producto(3, 'Monitor LCD 24 pulgadas', 5, 62000)


# Listar todos los productos
mi_inventario.listar_productos()


# Eliminar un producto 
mi_inventario.eliminar_producto(2)


# Confirmamos que haya sido eliminado
mi_inventario.listar_productos()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()


# Crear 3 productos y agregarlos al inventario
mi_inventario.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500)
mi_inventario.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500)
mi_inventario.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500)


# Listar todos los productos del inventario
mi_inventario.listar_productos()

# Agregar 2 productos al carrito
mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del producto con código 1 al carrito

mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del producto con código 3 al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Quitar 1 producto al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Mostramos el inventario
mi_inventario.listar_productos()
'''


