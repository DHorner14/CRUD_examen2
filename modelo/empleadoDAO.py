from modelo.empleado import Empleado
from modelo.conexionbd import ConexionBD

class EmpleadoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.empleado = Empleado()
    
    def listarEmpleados(self):
        self.bd.establecerConexionBD()
        cursor=self.bd.conexion.cursor()
        sp="exec [dbo].[sp_listar_empleados]"
        cursor.execute(sp)
        filas=cursor.fetchall()
        for fila in filas:
            print (fila)
        
        self.bd.CerrarConexion()
    
    def insertarEmpleado(self):
        self.bd.establecerConexionBD()
        sp="exec [dbo].[sp_insertar_empleado] @Apellido=?,@puesto=?,@edad=?,@salario=?"
        param=(self.empleado.Apellido,self.empleado.puesto,self.empleado.edad,self.empleado.salario)
        cursor=self.bd.conexion.cursor()
        cursor.execute(sp,param)
        cursor.commit()
        self.bd.CerrarConexion()
    
    def actualizarEmpleado(self):
        self.bd.establecerConexionBD()
        sp="exec [dbo].[sp_actualizar_empleado] @id_empleado=?,@Apellido=?,@puesto=?,@edad=?,@salario=?"
        param=(self.empleado.id_empleado,self.empleado.Apellido,self.empleado.puesto,self.empleado.edad,self.empleado.salario)
        cursor=self.bd.conexion.cursor()
        cursor.execute(sp,param)
        cursor.commit()
        self.bd.CerrarConexion()
    
    def eliminarEmpleado(self):
        self.bd.establecerConexionBD()
        sp="exec [dbo].[sp_eliminar_empleado] @id_empleado"
        param=(self.empleado.id_empleado)
        cursor=self.bd.conexion.cursor()
        cursor.execute(sp,param)
        cursor.commit()
        self.bd.CerrarConexion()
        
        