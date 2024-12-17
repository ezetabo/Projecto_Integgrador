from typing import TypedDict


class Producto(TypedDict):
    codigo: int   
    nombre: str
    descripcion: str
    cantidad: int
    precio: float
    categoria: str