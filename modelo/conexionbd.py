import pyodbc

class ConexionBD:
    def __init__(self):
        self.conexion = None

    def establecerConexionBD(self):
        try:
            self.conexion = pyodbc.connect(
                r'DRIVER={SQL Server};'
                r'SERVER=DESKTOP-SSUO5NK\SQLEXPRESS04;'
                r'DATABASE=bdsistema;'
                r'Trusted_Connection=yes;'
            )
            print("Conexión establecida correctamente.")
        except Exception as ex:
            print("No se pudo establecer la conexión.")
            print("Error:", ex)

    def CerrarConexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión finalizada.")
        else:
            print("No hay conexión abierta para cerrar.")

def main():
    conexion = ConexionBD()
    conexion.establecerConexionBD()
    # Aquí puedes agregar consultas o llamadas a procedimientos
    conexion.cerrarConexion()

if __name__ == "__main__":
    main()
