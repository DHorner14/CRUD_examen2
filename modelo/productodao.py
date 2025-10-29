from modelo.producto import Producto
from modelo.conexionbd import ConexionBD

class ProductoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.producto = Producto()
    
    def listarProductos(self):
        self.bd.establecerConexionBD()
        cursor=self.bd.conexion.cursor()
        sp="exec [dbo].[sp_listar_productos]"
        cursor.execute(sp)
        filas=cursor.fetchall()
        self.bd.CerrarConexion()
        return filas

    
    def insertarProducto(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_insertar_producto] @Clave=?,@Descripcion=?,@Existencia=?,@Precio=?"
        params = (self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.CerrarConexion()
    
    def actualizarProducto(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_actualizar_producto] @Clave=?,@Descripcion=?,@Existencia=?,@Precio=?"
        params = (self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.CerrarConexion()
    
    def eliminarProducto(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_eliminar_producto] @Clave=?"
        params = (self.producto.clave,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        self.bd.conexion.commit()
        self.bd.CerrarConexion()
    
    def buscarProducto(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_buscar_producto] @clave=?"
        params = (self.producto.clave,)
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, params)
        fila = cursor.fetchone()
        self.bd.CerrarConexion()
        return fila