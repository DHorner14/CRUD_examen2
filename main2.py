
from modelo.empleadoDAO import EmpleadoDAO

def main():
    empleadodao =EmpleadoDAO()
    empleadodao.empleado.Apellido="Hola"
    empleadodao.empleado.edad=45
    empleadodao.empleado.puesto="jefe"
    empleadodao.empleado.salario=89.99

    
    empleadodao.insertarEmpleado()
    empleadodao.actualizarEmpleado()
    empleadodao.listarEmpleados()

    
    
if __name__=='__main__':
    main()