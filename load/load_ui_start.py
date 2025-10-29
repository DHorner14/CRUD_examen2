import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from load.load_ui_productos import Load_ui_productos
from load.load_ui_empleados import Load_ui_empleado

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        # Cargar la interfaz de login
        uic.loadUi("ui/login.ui", self)
        
        # Conectar señales
        self.btnLogin.clicked.connect(self.verificar_login)
        self.btnCancel.clicked.connect(self.reject)
        self.editPass.returnPressed.connect(self.verificar_login)
        
        # Configuración inicial
        self.setWindowTitle("Acceso al Sistema")
        self.editUser.setFocus()
        
    def verificar_login(self):
        usuario = self.editUser.text().strip()
        contraseña = self.editPass.text().strip()
        
        # Verificar que no estén vacíos
        if not usuario or not contraseña:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            self.editUser.setFocus()
            return

        # Credenciales válidas
        usuario_valido = "admin"
        contraseña_valida = "1234"
        
        if usuario == usuario_valido and contraseña == contraseña_valida:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            self.editPass.clear()
            self.editUser.selectAll()
            self.editUser.setFocus()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar la interfaz principal
        uic.loadUi("ui/chooser.ui", self)
        
        # Conectar señales
        self.boton_salir.clicked.connect(self.close)
        self.btnMenuA.clicked.connect(self.menu_a_seleccionado)
        self.btnMenuB.clicked.connect(self.menu_b_seleccionado)
        
        # Configuración inicial
        self.setWindowTitle("Selector de Menú - Sistema Principal")
        
    def menu_a_seleccionado(self):
        """Abrir la interfaz del Menú A (Empleados)"""
        try:
            # Cerrar ventana principal
            self.close()
            # Abrir ventana de empleados
            self.abrir_ventana_empleados()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el Menú A:\n{str(e)}")
            
    def menu_b_seleccionado(self):
        """Abrir la interfaz del Menú B (Productos)"""
        try:
            # Cerrar ventana principal
            self.close()
            # Abrir ventana de productos
            self.abrir_ventana_productos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el Menú B:\n{str(e)}")
    
    def abrir_ventana_empleados(self):
        """Abrir ventana de empleados en la misma aplicación"""
        self.empleados_window = Load_ui_empleado()
        self.empleados_window.show()
    
    def abrir_ventana_productos(self):
        """Abrir ventana de productos en la misma aplicación"""
        self.productos_window = Load_ui_productos()
        self.productos_window.show()

