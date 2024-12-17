from typing import Dict
from modelo import Producto
import sqlite3

data_base = "Deposito.db"
tabla = "Productos"


def crear_tabla():
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()
    db.execute(f'''
    CREATE TABLE IF NOT EXISTS {tabla}
            (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,           
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
            )
            ''')
    conexion.commit()
    conexion.close()

    """
    Obtiene el siguiente id auto incrementado.    
    return: El siguiente id auto incrementado o -1 en caso de error.
    """
def Obtener_id_disponible() -> int:
    try:        
        conn = sqlite3.connect(data_base)
        db = conn.cursor()
        db.execute(f"SELECT seq FROM sqlite_sequence WHERE name = ?", (tabla,))
        result = db.fetchone()
        if result is None:
            siguiente_id = 1
        else:
            siguiente_id = result[0]       
        conn.close()
        return siguiente_id
    except:       
        return -1 

import sqlite3

def obtener_id_por_nombre(nombre_producto: str) -> int:   
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()   
    db.execute("SELECT codigo FROM Productos WHERE nombre = ?", (nombre_producto,))  
    resultado = db.fetchone()    
    conexion.close()  
    if resultado:
        return resultado[0]  
    else:
        return -1
    

def insertar_producto_db(p:Producto):
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()   
    db.execute('''INSERT INTO Productos (nombre, descripcion, cantidad, precio, categoria)
                  VALUES ( ?, ?, ?, ?, ?)''', (p['nombre'], p['descripcion'], p['cantidad'],p['precio'], p['categoria']))
    conexion.commit()
    conexion.close()

def insertar_productos_db(inventario: Dict[int, Producto]):
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()   
    for producto in inventario.values():
        db.execute('''INSERT INTO Productos (nombre, descripcion, cantidad, precio, categoria)
                      VALUES ( ?, ?, ?, ?, ?)''', (producto['nombre'], producto['descripcion'], 
                                                   producto['cantidad'], producto['precio'], producto['categoria']))
    conexion.commit()
    conexion.close()

def leer_todos_los_productos()->Dict[int, Producto] :
    dicc: Dict[int, Producto] = {}
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()
    db.execute("SELECT * FROM Productos")
    productos = db.fetchall()   
    conexion.close()
    for p in productos:
        dicc[p[0]] = {
            "codigo": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "cantidad": p[3],
            "precio": p[4],
            "categoria": p[5]
        }
    return dicc

def actualizar_producto(producto: Producto) -> bool:   
    conexion = sqlite3.connect(data_base)
    db = conexion.cursor()       
    db.execute('''UPDATE Productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE codigo = ?''', 
                (producto["nombre"], producto["descripcion"], producto["cantidad"], producto["precio"], producto["categoria"]
                    ,producto["codigo"]))
    conexion.commit()
    filas_afectadas = db.rowcount
    conexion.close()       
    return filas_afectadas > 0

def eliminar_producto(p:Producto):
    codigo = p["codigo"]
    conn = sqlite3.connect(data_base)
    db = conn.cursor()       
    db.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))        
    conn.commit() 
    conn.close()
