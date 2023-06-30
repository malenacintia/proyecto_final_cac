import sqlite3
from flask import Flask, jsonify, request

# Configurar la conexión a la base de datos SQLite
DATABASE = 'Cronograma.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'cursos' si no existe
def create_table():
    print("Creando tabla cursos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cupo INTEGER NOT NULL,
            horario TEXT NOT NULL,
            precio REAL NOT NULL
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()


# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()


# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()



class Curso:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cupo, horario ,precio):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cupo = cupo
        self.horario = horario       # Cantidad disponible (stock)
        self.precio = precio           # Precio 


    # Este método permite modificar un curso.
    def modificar(self, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cupo = nuevo_cupo
        self.horario = nuevo_horario        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

class Cronograma:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()


    # Este método permite crear objetos de la clase "curso" y agregarlos al Cronograma.
    def agregar_curso(self, codigo, descripcion, cupo, horario, precio):
        curso_existente = self.consultar_curso(codigo)
        if curso_existente:
            return jsonify({'message': 'Ya existe un curso con ese código.'}), 400
        nuevo_curso = Curso (codigo, descripcion, cupo, horario, precio)
        sql = f'INSERT INTO productos VALUES ({codigo}, "{descripcion}", {cupo}, "{horario}", {precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Curso agregado correctamente.'}), 200

    '''
    def agregar_curso(self, codigo, descripcion, cupo, horario, precio):
        curso_existente = self.consultar_curso(codigo)
        if curso_existente:
            print("Ya existe un curso con ese código.")
            return False
        nuevo_curso = Curso (codigo, descripcion, cupo, horario, precio)
        sql = f'INSERT INTO cursos VALUES ({codigo}, "{descripcion}", {cupo},"{horario}", {precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
    '''


    # Este método permite consultar datos de cursos que están en el Cronograma
    # Devuelve el curso correspondiente al código proporcionado o False si no existe.
    def consultar_curso(self, codigo):
        sql = f'SELECT * FROM cursos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cupo, horario, precio = row
            return Curso(codigo, descripcion, cupo, horario, precio)
        return None
        #return False


    # Este método permite modificar datos de cursos que están en el Cronograma
    # Utiliza el método consultar_curso del Cronograma y modificar del curso.
    def modificar_curso(self, codigo, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio):
        curso = self.consultar_curso(codigo)
        if curso:
            curso.modificar(nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio)
            sql = f'UPDATE cursos SET descripcion = "{nueva_descripcion}", cupo = {nuevo_cupo}, horario = "{nuevo_horario}" precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Curso modificado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404
    '''
    def modificar_curso(self, codigo, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio):
        curso = self.consultar_curso(codigo)
        if curso:
            curso.modificar(nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio)
            sql = f'UPDATE cursos SET descripcion = "{nueva_descripcion}", cupo = {nuevo_cupo}, horario = "{nuevo_horario}", precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()
    '''
    # Este método elimina el curso indicado por codigo de la lista mantenida en el Cronograma.
    def eliminar_curso(self, codigo):
        sql = f'DELETE FROM cursos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Curso eliminado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404
    '''
    def eliminar_curso(self, codigo):
        sql = f'DELETE FROM cursos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'curso {codigo} eliminado.')
            self.conexion.commit()
        else:
            print(f'curso {codigo} no encontrado.')
    '''
    # Este método imprime en la terminal una lista con los datos de los cursos que figuran en el Cronograma.
    def listar_cursos(self):
        self.cursor.execute("SELECT * FROM cursos")
        rows = self.cursor.fetchall()
        cursos = []
        for row in rows:
            codigo, descripcion, cupo, horario, precio = row
            curso = {'codigo': codigo, 'descripcion': descripcion, 'cupo': cupo, 'horario': horario, 'precio': precio}
            cursos.append(curso)
        return jsonify(cursos), 200
    '''
    def listar_cursos(self):
        print("-"*50)
        print("Lista de cursos en el Cronograma:")
        print("Código\tDescripción\tCupo\tHorario\tPrecio")
        self.cursor.execute("SELECT * FROM cursos")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, descripcion, cupo, horario, precio = row
            print(f'{codigo}\t{descripcion}\t{cupo}\t{horario}\t{precio}')
        print("-"*50)
    '''

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = get_db_connection()
        #self.conexion = sqlite3.connect('Cronograma.db')  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []  # Lista de items en el carrito (variable de clase)

    # Este método permite agregar cursos del Cronograma al carrito.
    def agregar(self, codigo, cupo, Cronograma):
        curso = cronograma.consultar_curso(codigo)
        if curso is None:
            return jsonify({'message': 'El curso no existe.'}), 404
        if curso.cupo < cupo:
            return jsonify({'message': 'No hay vacantes en este curso.'}), 400


        for item in self.items:
            if item.codigo == codigo:
                item.cupo += cupo
                sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Curso agregado al carrito correctamente.'}), 200


        nuevo_item = Curso(codigo, curso.descripcion, cupo, curso.horario, curso.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Curso agregado al carrito correctamente.'}), 200
    '''
    def agregar(self, codigo, cupo, Cronograma):
        curso = Cronograma.consultar_curso(codigo)
        if curso is False:
            print("El curso no existe.")
            return False
        if curso.cupo < cupo:
            print("No hay vacantes en este curso.")
            return False


        for item in self.items:
            if item.codigo == codigo:
                item.cupo += cupo
                sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True


        nuevo_item = Curso(codigo, curso.descripcion, cupo, curso.horario, curso.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
        '''

    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cupo, Cronograma):
        for item in self.items:
            if item.codigo == codigo:
                if cupo > item.cupo:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cupo -= cupo
                if item.cupo == 0:
                    self.items.remove(item)
                #actualizamos la cantidad en el Cronograma
                sql = f'UPDATE cursos SET cupo = cupo + {cupo} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Curso quitado del carrito correctamente.'}), 200
        return jsonify({'message': 'El curso no se encuentra en el carrito.'}), 404
                #return True

    def mostrar(self):
        cursos_carrito = []
        for item in self.items:
            curso = {'codigo': item.codigo, 'descripcion': item.descripcion, 'cupo': item.cupo, 'horario': item.horario, 'precio': item.precio}
            cursos_carrito.append(curso)
        return jsonify(cursos_carrito), 200

    '''
    def mostrar(self):
        print("-"*50)
        print("Lista de cursos en el carrito:")
        print("Código\tDescripción\tCupo\tHorario\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cupo}\t{item.horario}\t{item.precio}')
        print("-"*50)
    '''
app = Flask(__name__)

carrito = Carrito()         # Instanciamos un carrito
cronograma = Cronograma()   # Instanciamos un cronograma

# Ruta para obtener los datos de un curso según su código
@app.route('/curso/<int:codigo>', methods=['GET'])
def obtener_curso(codigo):
    curso = cronograma.consultar_curso(codigo)
    if curso:
        return jsonify({
            'codigo': curso.codigo,
            'descripcion': curso.descripcion,
            'cupo': curso.cupo,
            'horario': curso.horario,
            'precio': curso.precio
        }), 200
    return jsonify({'message': 'Producto no encontrado.'}), 404

# Ruta para obtener el index
@app.route('/')
def index():
    return 'API de Cronograma'

# Ruta para obtener la lista de cursos del cronograma
@app.route('/cursos', methods=['GET'])
def obtener_cursos():
    return cronograma.listar_cursos()

# Ruta para agregar un curso al cronograma
@app.route('/cursos', methods=['POST'])
def agregar_curso():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cupo = request.json.get('cupo')
    horario = request.json.get('horario')
    precio = request.json.get('precio')
    return cronograma.agregar_curso(codigo, descripcion, cupo, horario, precio)

# Ruta para modificar un producto del cronograma
@app.route('/cursos/<int:codigo>', methods=['PUT'])
def modificar_curso(codigo):
    nueva_descripcion = request.json.get('descripcion')
    nuevo_cupo = request.json.get('cupo')
    nuevo_horario = request.json.get('horario')
    nuevo_precio = request.json.get('precio')
    return cronograma.modificar_curso(codigo, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio)

# Ruta para eliminar un curso del inventario
@app.route('/cursos/<int:codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    return cronograma.eliminar_curso(codigo)

# Ruta para agregar un curso al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cupo = request.json.get('cupo')
    horario = request.json.get('horario')
    cronograma = Cronograma()
    return carrito.agregar(codigo, cupo, horario, cronograma)

# Ruta para quitar un curso del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cupo = request.json.get('cupo')
    horario = request.json.get('horario')
    cronograma = Cronograma()
    return carrito.quitar(codigo, cupo, horario, cronograma)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()







'''
# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()


# Crear una instancia de la clase Cronograma
mi_Cronograma = Cronograma()


# Agregar cursos al Cronograma
mi_Cronograma.agregar_curso(1, "curso 1", 10, "08:30",19.99)
mi_Cronograma.agregar_curso(2, "curso 2", 5, "08:30",9.99)
mi_Cronograma.agregar_curso(3, "curso 3", 15, "08:30",29.99)

# Consultar algún curso del Cronograma
print(mi_Cronograma.consultar_curso(3)) #Existe, se muestra la dirección de memoria
print(mi_Cronograma.consultar_curso(4)) #No existe, se muestra False

# Listar los cursos del Cronograma
mi_Cronograma.listar_cursos()


# Modificar un curso del Cronograma
mi_Cronograma.modificar_curso(2, "Pilates", 10, "08:30",19.99)
# Listar nuevamente los cursos del Cronograma para ver la modificación
mi_Cronograma.listar_cursos()
# Eliminar un curso
mi_Cronograma.eliminar_curso(3)
# Listar nuevamente los cursos del Cronograma para ver la eliminación
mi_Cronograma.listar_cursos()


# Crear una instancia de la clase Carrito
mi_carrito = Carrito()
# Agregar 2 unidades del curso con código 1 al carrito
mi_carrito.agregar(1, 2, mi_Cronograma)
# Agregar 1 unidad del curso con código 2 al carrito
mi_carrito.agregar(2, 1, mi_Cronograma)
# Mostrar el contenido del carrito y del Cronograma
mi_carrito.mostrar()
mi_Cronograma.listar_cursos()

# Quitar 1 unidad del curso con código 1 al carrito y 1 unidad del curso con código 2 al carrito
mi_carrito.quitar(1, 1, mi_Cronograma)
mi_carrito.quitar(2, 1, mi_Cronograma)
# Mostrar el contenido del carrito y del Cronograma
mi_carrito.mostrar()
mi_Cronograma.listar_cursos()
'''