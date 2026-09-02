import json
import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

# Adaptador para garantizar que las ventas tengan los atributos que busca main.py
class VentaAdapter:
    def __init__(self, data):
        if isinstance(data, dict):
            self.usuario_id = data.get("usuario_id") or data.get("identificacion_usuario", "")
            self.producto_codigo = data.get("producto_codigo") or data.get("codigo_producto", "")
            self.cantidad = data.get("cantidad", 0)
            self._raw = data
        else:
            self.usuario_id = getattr(data, "usuario_id", None) or getattr(data, "identificacion_usuario", "")
            self.producto_codigo = getattr(data, "producto_codigo", None) or getattr(data, "codigo_producto", "")
            self.cantidad = getattr(data, "cantidad", 0)
            self._raw = data

# Adaptador para garantizar que los productos expongan la propiedad .nombre y .codigo
class ProductoAdapter:
    def __init__(self, data):
        if isinstance(data, dict):
            self.codigo = str(data.get("codigo", ""))
            self.nombre = data.get("nombre", "Producto sin nombre")
            self.precio = data.get("precio", 0.0)
            self.stock = data.get("stock", 0)
            self._raw = data
        else:
            self.codigo = str(getattr(data, "codigo", ""))
            self.nombre = getattr(data, "nombre", "Producto sin nombre")
            self.precio = getattr(data, "precio", 0.0)
            self.stock = getattr(data, "stock", 0)
            self._raw = data

class Restaurante:
    def __init__(self):
        # Listas principales
        self._productos = []
        self._usuarios = []
        self._ventas = []

        # Estructuras auxiliares (Índices)
        self._productos_por_codigo = {}          # dict: codigo -> ProductoAdapter
        self._usuarios_por_identificacion = {}   # dict: identificacion -> Usuario
        self._ventas_por_usuario = {}           # dict: usuario_id -> list[VentaAdapter]

        # Cargar datos e inicializar índices
        self.cargar_datos()

    def _reconstruir_indices(self):
        """Construye los diccionarios auxiliares para búsquedas O(1)."""
        # 1. Índice de productos
        self._productos_por_codigo = {}
        for prod in self._productos:
            adapter = ProductoAdapter(prod)
            if adapter.codigo:
                self._productos_por_codigo[adapter.codigo] = adapter

        # Respaldo directo para productos.json si no venían instanciados
        if not self._productos_por_codigo and os.path.exists("datos/productos.json"):
            try:
                with open("datos/productos.json", "r", encoding="utf-8") as f:
                    prods_raw = json.load(f)
                    for p_dict in prods_raw:
                        adapter = ProductoAdapter(p_dict)
                        if adapter.codigo:
                            self._productos_por_codigo[adapter.codigo] = adapter
            except Exception:
                pass
        
        # 2. Índice de usuarios
        self._usuarios_por_identificacion = {
            str(getattr(u, 'identificacion', '')): u for u in self._usuarios if hasattr(u, 'identificacion')
        }

        # 3. Índice de ventas
        self._ventas_por_usuario = {}
        for venta in self._ventas:
            adapter = VentaAdapter(venta)
            u_id = str(adapter.usuario_id)
            if u_id:
                if u_id not in self._ventas_por_usuario:
                    self._ventas_por_usuario[u_id] = []
                self._ventas_por_usuario[u_id].append(adapter)

        # Respaldo directo para ventas.json
        if not self._ventas_por_usuario and os.path.exists("datos/ventas.json"):
            try:
                with open("datos/ventas.json", "r", encoding="utf-8") as f:
                    ventas_raw = json.load(f)
                    for v_dict in ventas_raw:
                        adapter = VentaAdapter(v_dict)
                        u_id = str(adapter.usuario_id)
                        if u_id:
                            if u_id not in self._ventas_por_usuario:
                                self._ventas_por_usuario[u_id] = []
                            self._ventas_por_usuario[u_id].append(adapter)
            except Exception:
                pass

    def cargar_datos(self):
        try:
            self._productos = ArchivoServicio.cargar_json("datos/productos.json", Producto)
        except Exception:
            self._productos = []

        try:
            self._usuarios = ArchivoServicio.cargar_json("datos/usuarios.json", Usuario)
        except Exception:
            self._usuarios = []

        try:
            self._ventas = ArchivoServicio.cargar_json("datos/ventas.json", Venta)
        except Exception:
            self._ventas = []

        self._reconstruir_indices()

    def guardar_datos(self):
        productos_a_guardar = [getattr(p, '_raw', p) for p in self._productos] if self._productos else []
        ArchivoServicio.guardar_json("datos/productos.json", productos_a_guardar)
        ArchivoServicio.guardar_json("datos/usuarios.json", self._usuarios)
        ventas_a_guardar = [getattr(v, '_raw', v) for v in self._ventas] if self._ventas else []
        ArchivoServicio.guardar_json("datos/ventas.json", ventas_a_guardar)

    # --- Búsquedas optimizadas en O(1) ---
    def buscar_producto_por_codigo(self, codigo):
        return self._productos_por_codigo.get(str(codigo))

    def buscar_producto(self, codigo):
        """Requerido directamente por main.py (línea 37)"""
        return self.buscar_producto_por_codigo(codigo)

    def buscar_usuario_por_identificacion(self, identificacion):
        return self._usuarios_por_identificacion.get(str(identificacion))

    def consultar_ventas_usuario(self, identificacion):
        """Requerido directamente por main.py (línea 31)"""
        return self._ventas_por_usuario.get(str(identificacion), [])

    def consultar_ventas_por_usuario(self, identificacion):
        return self.consultar_ventas_usuario(identificacion)

    # --- Métodos de registro ---
    def registrar_producto(self, producto):
        adapter = ProductoAdapter(producto)
        if adapter.codigo in self._productos_por_codigo:
            raise ValueError("Ya existe un producto registrado con ese código.")

        self._productos.append(producto)
        self._productos_por_codigo[adapter.codigo] = adapter
        self.guardar_datos()

    def registrar_usuario(self, usuario):
        id_str = str(usuario.identificacion)
        if id_str in self._usuarios_por_identificacion:
            raise ValueError("Ya existe un usuario registrado con esa identificación.")

        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[id_str] = usuario
        self.guardar_datos()

    def registrar_venta(self, venta):
        v_adapter = VentaAdapter(venta)
        producto = self.buscar_producto(v_adapter.producto_codigo)
        
        if not producto:
            raise ValueError("El producto solicitado no existe.")

        if producto.stock < v_adapter.cantidad:
            raise ValueError("Stock insuficiente.")

        producto.stock -= v_adapter.cantidad
        self._ventas.append(venta)

        u_id_str = str(v_adapter.usuario_id)
        if u_id_str not in self._ventas_por_usuario:
            self._ventas_por_usuario[u_id_str] = []
        self._ventas_por_usuario[u_id_str].append(v_adapter)

        self.guardar_datos()

    def obtener_productos(self):
        return self._productos

    def obtener_usuarios(self):
        return self._usuarios

    def obtener_ventas(self):
        return self._ventas