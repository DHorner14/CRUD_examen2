import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from load.load_ui_productos import Load_ui_productos

# Importar empleados solo si existe
try:
    from load.load_ui_empleados import Load_ui_empleado
    EMPLEADOS_DISPONIBLE = True
except ImportError as e:
    print(f"Advertencia: Módulo de empleados no disponible - {e}")
    EMPLEADOS_DISPONIBLE = False
    class Load_ui_empleado(QtWidgets.QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Empleados - No disponible")
            label = QtWidgets.QLabel("Módulo de empleados no disponible")
            label.setAlignment(Qt.AlignCenter)
            self.setCentralWidget(label)

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.btnLogin.clicked.connect(self.verificar_login)
        self.btnCancel.clicked.connect(self.reject)
        self.editPass.returnPressed.connect(self.verificar_login)
        self.setWindowTitle("Acceso al Sistema")
        self.editUser.setFocus()
        
    def verificar_login(self):
        usuario = self.editUser.text().strip()
        contraseña = self.editPass.text().strip()
        
        if not usuario or not contraseña:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            self.editUser.setFocus()
            return

        # VERIFICACIÓN CON BASE DE DATOS - SOLO ESTO CAMBIA
        if self.verificar_en_bd(usuario, contraseña):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            self.editPass.clear()
            self.editUser.selectAll()
            self.editUser.setFocus()
    
    def verificar_en_bd(self, usuario, contraseña):
        """Verifica las credenciales en la base de datos"""
        try:
            # Importa tu conexión existente
            from modelo.conexionbd import ConexionBD  # Ajusta el import
            
            conn = ConexionBD()  # Usa tu función existente
            cursor = conn.cursor()
            
            # Llamar al procedimiento almacenado
            cursor.execute("EXEC sp_ValidarUsuario ?, ?", usuario, contraseña)
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return bool(result[0]) if result else False
            
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            # Fallback a verificación local si hay error de BD
            return usuario == "admin" and contraseña == "1234"
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/chooser.ui", self)
        self.boton_salir.clicked.connect(self.salir_aplicacion)
        self.btnMenuA.clicked.connect(self.menu_a_seleccionado)
        self.btnMenuB.clicked.connect(self.menu_b_seleccionado)
        self.setWindowTitle("Selector de Menú - Sistema Principal")
        
        if not EMPLEADOS_DISPONIBLE:
            self.btnMenuA.setEnabled(False)
            self.btnMenuA.setText("Empleados (No disponible)")
        
    def menu_a_seleccionado(self):
        """Abrir ventana de empleados"""
        try:
            self.hide()  # Ocultar en lugar de cerrar
            self.empleados_window = Load_ui_empleado(self)  # Pasar self como parent
            self.empleados_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar Empleados:\n{str(e)}")
            
    def menu_b_seleccionado(self):
        """Abrir ventana de productos"""
        try:
            self.hide()  # Ocultar en lugar de cerrar
            self.productos_window = Load_ui_productos(self)  # Pasar self como parent
            self.productos_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar Productos:\n{str(e)}")
    
    def mostrar_ventana_principal(self):
        """Mostrar esta ventana principal nuevamente"""
        self.show()
    
    def salir_aplicacion(self):
        """Salir completamente de la aplicación"""
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Sistema con Login")
    
    login_dialog = LoginDialog()
    
    if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()