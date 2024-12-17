from modelo import Producto
import DB
'''
Se encarga de pedir, validar y retornar un entero dentro del rango minimo y maximo establecido.

# mensaje: parametro str para ingresar la peticion de un dato.
# msj_error: parametro str para informar que el dato no es correcto.
# minimo: valor minimo esperado.
# maximo: valor maximo esperado
#RETURN: un numero entero dentro del rango.
'''
def pedir_numero_en_rango(mensaje,msj_error, minimo, maximo):
    numero = input(mensaje)
    while numero.isdigit() == False or int(numero) <minimo or int(numero) >maximo :
        print(f"{msj_error}, debe estar entre {minimo} y {maximo}.")
        numero = input(mensaje)
    return int(numero)

'''
Se encarga de pedir el ingreso de un str y retorna un booleano para informar la coincidencia del ingreso.

# mensaje: parametro str para ingresar la peticion de un dato.
# esperado: dato que se espera recibir por consola.
# RETURN: true en caso de coincidencia, false en caso contrario.
'''
def confirmar(mensaje,esperado):
    resp = input(mensaje)
    if resp.lower() == esperado.lower():
        return True
    else:
        return False
    
'''
Se encarga de pedir, validar y retornar un entero superior al minimo establecido.

# mensaje: parametro str para ingresar la peticion de un dato.
# msj_error: parametro str para informar que el dato no es correcto.
# minimo: valor minimo esperado.
#RETURN: un numero entero superior al minimo establecido.
'''   
def pedir_entero_rango_minimo(mensaje, msj_error, minimo,):
    numero = input(mensaje)
    while numero.isdigit() == False or int(numero) <= minimo:
        print(f"{msj_error}, debe ser superior a {minimo}")
        numero = input(mensaje)
    return int(numero)

'''
Se encarga de pedir, validar y retornar un float superior al minimo establecido.

# mensaje: parametro str para ingresar la peticion de un dato.
# msj_error: parametro str para informar que el dato no es correcto.
# minimo: valor minimo esperado.
#RETURN: un numero float superior al minimo establecido.
'''   
def pedir_float_rango_minimo(mensaje, msj_error, minimo):
    while True:
        try:
            numero = float(input(mensaje))
            if numero > minimo:
                return numero
            else:
                print(f"{msj_error}, debe ser superior a {minimo}.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

'''
Se encarga de pedir y validar el ingreso de datos para crear un producto.

#RETURN: una lista que representa un producto.
'''     
def crear_producto()->Producto:
    nombre = input("ingrese el nombre del producto: ")
    valor = DB.obtener_id_por_nombre(nombre)
    codigo =  valor  if valor != -1 else DB.obtener_id_disponible()
    cantidad = pedir_entero_rango_minimo(f"ingrese la cantidad de [{nombre}]: ","cantidad incorrecta",0)
    precio =  pedir_float_rango_minimo(f"Ingrese el precio de [{nombre}]: ","precio incorrecto",0)
    descripcion = input(f"ingrese la descripcion para [{nombre}]: ")
    categoria = input(f"ingrese la categoria para [{nombre}]: ")
    return { "codigo":codigo,"nombre":nombre, "descripcion":descripcion,"cantidad":cantidad,"precio":precio,"categoria":categoria}

"""
Agrega un producto al dicc inventario y actualiza la DB. 
Si el producto ya existe (comparando por el código), actualiza la cantidad y el precio.

# dicc: dicc de productos en el inventario.
# producto: Producto a agregar o actualizar.
#return: True si el producto ya existia y fue actualizado, False si se agregó como nuevo.
"""
def agregar_producto(dicc :dict[int, Producto], producto:Producto):
    encontrado = False    
    for p in dicc.values():
        if p["codigo"] == producto["codigo"]:            
            p["cantidad"] += producto["cantidad"]
            p["precio"] = producto["precio"]
            p["categoria"] = producto["categoria"]
            p["descripcion"] = producto["descripcion"]
            encontrado = True
            DB.actualizar_producto(p)
            break
    if encontrado == False:
        dicc[producto["codigo"]] = producto
        DB.insertar_producto_db(producto)
    return encontrado

'''
Recibe un producto e imprime todos sus valores.
'''        
def mostrar_producto(p:Producto,show = True,simbolo = "-",cantidad=132):
    if show:
        print(simbolo * cantidad)
    print(f"| Codigo: {p["codigo"]:<3} | Nombre: {p["nombre"].capitalize():<10} | Stock: {p["cantidad"]:<5} | Precio: ${p["precio"]:<8.2f} | Categoria: {p["categoria"].capitalize():<12} | Descripcion: {p["descripcion"]:<19} |")
    if show:
        print(simbolo * cantidad)
'''
Recibe un diccionario de productos e imprime todos sus valores.
'''          
def mostrar_productos(dicc :dict[int, Producto],simbolo = "-",cantidad=132):    
    print(simbolo * cantidad)
    for producto in dicc.values():
        mostrar_producto(producto,False)
        print(simbolo * cantidad)

"""
Actualiza la cantidad de un producto en el diccionario y actualiza la DB.

# dicc: Diccionario de productos.
# return: True si la cantidad fue actualizada correctamente, False si ocurrio un error.
"""
def actualizar_cantidad(dicc: dict[int, Producto])->bool:
    try:
        producto = elegir_producto(dicc)
        mostrar_producto(producto)
        nueva_cantidad = pedir_entero_rango_minimo(f"Ingrese la nueva cantidad de [{producto['nombre']}]: ","Valor incorrecto",0)
        producto["cantidad"] = nueva_cantidad
        DB.actualizar_producto(producto)
        return True
    except:
        return False

"""
Muestra los productos disponibles y permite al usuario seleccionar uno por su codigo.

# dicc: Diccionario de productos.
# return: El producto correspondiente al codigo seleccionado por el usuario.
"""
def elegir_producto(dicc: dict[int, Producto])->Producto:
    mostrar_productos(dicc)
    while True:
        codigo = pedir_entero_rango_minimo("Seleccione el codigo del producto: ","Codigo incorrecto", 0)
        producto = dicc.get(codigo)
        if producto:
            break
        print("\t\t>>> Codigo no valido <<<")
    return producto

def eliminar_producto(dicc: dict[int, Producto])->bool:
    producto = elegir_producto(dicc)
    print("\t\t ¡¡¡ ESTA ACCION ES IRREVERSIBLE !!!")
    mostrar_producto(producto)
    if confirmar(f"Seguro que desea eliminar [{producto['nombre']}]??  S-SI / cualquier otra tecla para cancelar: ","s"):
        DB.eliminar_producto(producto)
        return True
    return False

"""
Busca un producto en el diccionario por un campo específico y valor.

# dicc: Diccionario de productos.
# campo: El campo por el que se busca (por ejemplo, 'nombre', 'codigo', etc.).
# valor: El valor que debe tener el campo especificado.
#return: El producto encontrado o None si no se encuentra.
"""
def buscar_producto_por_campo(dicc: dict[int, Producto], campo: str, valor: str | int) -> Producto | None:

    valor = str(valor).lower().strip()
    for producto in dicc.values():
        if str(producto[campo]).lower().strip() == valor:
            return producto
    return None

def obtener_nombre_campo()->str:
    campos = {
        1:"codigo",
        2:"nombre",
        3:"descripcion",
        4:"cantidad",
        5:"precio",
        6:"categoria"
        }
    for k,v in campos.items():
        print(f"{k}.{v}")
    sel = pedir_numero_en_rango("Elija un criterio de busqueda: ","Numero incorrecto",1,6)
    return campos[sel]

"""
Busca productos en el diccionario por un campo específico y valor.

# dicc: Diccionario de productos.
# campo: El campo por el que se busca (por ejemplo, 'nombre', 'codigo', etc.).
# valor: El valor que debe tener el campo especificado.
#return: Un subdiccionario con todas las coincidencias o None si no se encuentra ningún producto.
"""
def buscar_productos_por_campo(dicc: dict[int, Producto], campo: str, valor: str|int|float):
    valor = str(valor).lower().strip()
    coincidencias = {}
    for codigo, producto in dicc.items():
        if str(producto[campo]).lower().strip() == valor:
            coincidencias[codigo] = producto
    return coincidencias if coincidencias else None


def buscar_productos(dicc: dict[int, Producto]):
    campo = obtener_nombre_campo()
    valor = input(f"Por cual valor de \"{campo}\" quiere buscar: ")
    return buscar_productos_por_campo(dicc,campo,valor)

def reporte_bajo_stock(dicc: dict[int, Producto]):
    valor = pedir_entero_rango_minimo("Indique el valor de busqueda: ","Valor incorrecto",0)   
    coincidencias = {}
    for codigo, producto in dicc.items():
        if producto["cantidad"] <= valor:
            coincidencias[codigo] = producto
    return coincidencias if coincidencias else None
