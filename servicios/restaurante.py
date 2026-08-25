from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class Restaurante:
    RUTA_PRODUCTOS = "datos/productos.json"
    RUTA_USUARIOS = "datos/usuarios.json"
    RUTA_VENTAS = "datos/ventas.json"

    def __init__(self):
        self._productos = []
        self._usuarios = []
        self._ventas = []
        self.cargar_todo()

    def cargar_todo(self):
        datos_prod = ArchivoServicio.cargar_datos(self.RUTA_PRODUCTOS)
        self._productos = [Producto.desde_diccionario(p) for p in datos_prod]

        datos_usr = ArchivoServicio.cargar_datos(self.RUTA_USUARIOS)
        self._usuarios = [Usuario.desde_diccionario(u) for u in datos_usr]

        datos_vta = ArchivoServicio.cargar_datos(self.RUTA_VENTAS)
        self._ventas = [Venta.desde_diccionario(v) for v in datos_vta]

    def guardar_todo(self):
        ArchivoServicio.guardar_datos(self.RUTA_PRODUCTOS, [p.a_diccionario() for p in self._productos])
        ArchivoServicio.guardar_datos(self.RUTA_USUARIOS, [u.a_diccionario() for u in self._usuarios])
        ArchivoServicio.guardar_datos(self.RUTA_VENTAS, [v.a_diccionario() for v in self._ventas])

    def buscar_usuario(self, identificacion: str):
        for usr in self._usuarios:
            if usr.identificacion == identificacion:
                return usr
        return None

    def buscar_producto(self, codigo: str):
        for prod in self._productos:
            if prod.codigo == codigo:
                return prod
        return None

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        
        self.guardar_todo()
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list:
        ventas_usuario = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)
        return ventas_usuario