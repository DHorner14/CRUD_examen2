import pyodbc 
class ConexionBD:
    def __init__(self):
        self.conexion=''

    def establecerConexionBD(self):
        try:
            self.conexion=pyodbc.connect('DRIVER={SQL Server};SERVER=SALAF008-07\SQLEXPRESS;DATABASE=bdsistema;UID=sa;PWD=Password01')
            print("Conexion establecida")
        except Exception as ex:
            print("No se pudo estabñecer conexion")
            print("Error=",ex)
            
    def CerrarConexion(self):
        self.conexion.close()
        print("Conexion finalizada")
