#Taboada Ezequiel
from funciones import *
from modelo import Producto
from typing import Dict

menu = "1.Agregar Producto\n2.Mostrar Productos\n3.Actualizar cantidad de producto\n4.Eliminar producto\n5.Buscar producto\n6.Reporte de bajo stock\n7.Salir\n"

'''DB.insertar_productos_db(inventario)'''
seguir = True

while seguir:    
    inventario: Dict[int, Producto] = DB.leer_todos_los_productos()
    print("\t\t *** MENU PRINCIPAL ***")
    opcion = pedir_numero_en_rango(menu,"opcion incorecta",1,7)
    match opcion:
        case 1:
            print("\t\t *** Agregar Producto ***")
            producto = crear_producto()
            if agregar_producto(inventario,producto):            
                print(f"\n\t >>> El producto {producto["nombre"].capitalize()} ya existia en el inventario, se actualizo el stock y se modifico el precio a ${producto["precio"]} <<<\n")
            else:
                print(f"\n\t >>> El producto {producto["nombre"].capitalize()} se agrego correctamente <<<\n")            
        case 2:
            print("\t\t *** Mostrar Productos ***")
            mostrar_productos(inventario)
        case 3:
            print("\t\t *** Actualizar cantidad de producto ***")
            mensaje = " <<< Cantidad actualizada correctamente >>>" if actualizar_cantidad(inventario) else " XXX Error al intentar actualizar la cantidad XXX"
            print(mensaje)
                
        case 4:
            print("\t\t *** Eliminar producto ***")
            mensaje = " <<< Producto eliminado correctamente >>>" if eliminar_producto(inventario) else " XXX Eliminacion cancelada XXX"
            print(mensaje)
        case 5:
            print("\t\t *** Buscar producto ***")
            productos = buscar_productos(inventario)
            mostrar_productos(productos) if productos else print("No existen resultados con esos criterios") 
        case 6:
            print("\t\t *** Reporte de bajo stock ***")
            productos = reporte_bajo_stock(inventario)
            mostrar_productos(productos) if productos else print("No existen resultados con esos criterios") 
        case 7:
            print("\t\t *** Salir ***")
            seguir =  not confirmar("Desea salir: \"S\" para salir - cualquier otra para salir: ","s")