#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.empleadoDAO import EmpleadoDAO  # Cambio a EmpleadoDAO

#2.- Cargar archivo .ui
class Load_ui_empleado(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        # Cargar archivo .ui
        uic.loadUi("ui/ui_empleados.ui", self)  # Cambiar a la UI de empleados
        self.show()    
        
        self.empleadodao = EmpleadoDAO()  # Cambio a EmpleadoDAO
        
#3.- Configurar contenedores
        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Cerrar ventana
        self.boton_salir.clicked.connect(self.regresar_menu_principal)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_menu.clicked.connect(self.mover_menu)
        #Fijar ancho columnas
        self.tabla_consulta.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        #4.- Conectar botones a funciones

        #Botones para cambiar de página
        self.boton_agregar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_consultar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar))

        #Botones para guardar, buscar, actualizar, eliminar y salir
        self.accion_guardar.clicked.connect(self.guardar_empleado)
        self.buscar_actualizar.clicked.connect(self.buscar_empleado_actualizar)
        self.buscar_eliminar.clicked.connect(self.buscar_empleado_eliminar)
        self.accion_actualizar.clicked.connect(self.actualizar_empleado)
        self.accion_eliminar.clicked.connect(self.eliminar_empleado)
        self.accion_limpiar.clicked.connect(self.limpiar_empleado)
        self.buscar_buscar.clicked.connect(self.buscar_empleado_buscar)
        self.boton_refresh.clicked.connect(self.actualizar_tabla)

#5.- Operaciones con el modelo de datos 
    def regresar_menu_principal(self):
        if self.parent:
            self.parent.mostrar_ventana_principal()
        self.close()

    def guardar_empleado(self):
        self.empleadodao.empleado.id_empleado = self.sku_agregar.text()
        self.empleadodao.empleado.apellido = self.descripcion_agregar.text()
        self.empleadodao.empleado.puesto = self.existencia_agregar.text()
        self.empleadodao.empleado.edad = self.precio_agregar.text()
        self.empleadodao.empleado.salario = self.lineEdit.text()  # Campo adicional para salario
        
        self.empleadodao.insertarEmpleado()
    
    def actualizar_tabla(self):
        datos = self.empleadodao.listarEmpleados()
        self.tabla_consulta.setRowCount(len(datos))
        i = 0
        for fila in datos:
            self.tabla_consulta.setItem(i, 0, QtWidgets.QTableWidgetItem(str(fila[0])))  # id_empleado
            self.tabla_consulta.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fila[1])))  # apellido
            self.tabla_consulta.setItem(i, 2, QtWidgets.QTableWidgetItem(str(fila[2])))  # puesto
            self.tabla_consulta.setItem(i, 3, QtWidgets.QTableWidgetItem(str(fila[3])))  # edad
            self.tabla_consulta.setItem(i, 4, QtWidgets.QTableWidgetItem(str(fila[4])))  # salario
            i += 1
    
    def actualizar_empleado(self):
        self.empleadodao.empleado.id_empleado = self.sku_actualizar.text()
        self.empleadodao.empleado.apellido = self.descripcion_actualizar.text()
        self.empleadodao.empleado.puesto = self.existencia_actualizar.text()
        self.empleadodao.empleado.edad = self.precio_actualizar.text()
        self.empleadodao.empleado.salario = self.precio_actualizar_2.text()
        self.empleadodao.actualizarEmpleado()    

    def eliminar_empleado(self):
        self.empleadodao.empleado.id_empleado = self.sku_eliminar.text()
        self.empleadodao.eliminarEmpleado()
    
    def buscar_empleado_buscar(self):
        self.empleadodao.empleado.id_empleado = self.sku_buscar.text()
        datos = self.empleadodao.buscarEmpleado()

        # normalizar a una sola fila
        if isinstance(datos, list) and datos:
            row = datos[0]
        elif isinstance(datos, tuple):
            row = datos
        else:
            row = None

        # limpiar si no hay resultado
        if not row:
            self.descripcion_buscar.setText("")
            self.existencia_buscar.setText("")
            self.precio_buscar.setText("")
            self.precio_buscar_2.setText("")
            return

        # asignar campos de forma segura
        self.descripcion_buscar.setText(str(row[1]))  # apellido
        self.existencia_buscar.setText(str(row[2]))   # puesto
        self.precio_buscar.setText(str(row[3]))       # edad
        self.precio_buscar_2.setText(str(row[4]))     # salario
    
    def buscar_empleado_eliminar(self):
        self.empleadodao.empleado.id_empleado = self.sku_eliminar.text()
        datos = self.empleadodao.buscarEmpleado()
        
        # normalizar a una sola fila
        if isinstance(datos, list) and datos:
            row = datos[0]
        elif isinstance(datos, tuple):
            row = datos
        else:
            row = None

        # limpiar si no hay resultado
        if not row:
            self.descripcion_eliminar.setText("")
            self.existencia_eliminar.setText("")
            self.precio_eliminar.setText("")
            self.precio_eliminar2.setText("")
            return

        # asignar campos de forma segura
        self.descripcion_eliminar.setText(str(row[1]))  # apellido
        self.existencia_eliminar.setText(str(row[2]))   # puesto
        self.precio_eliminar.setText(str(row[3]))       # edad
        self.precio_eliminar2.setText(str(row[4]))      # salario
    
    def limpiar_empleado(self):
        self.sku_buscar.setText("")
        self.descripcion_buscar.setText("")
        self.existencia_buscar.setText("")
        self.precio_buscar.setText("")
        self.precio_buscar_2.setText("")
    
    def buscar_empleado_actualizar(self):
        self.empleadodao.empleado.id_empleado = self.sku_actualizar.text()
        datos = self.empleadodao.buscarEmpleado()
        
        # normalizar a una sola fila
        if isinstance(datos, list) and datos:
            row = datos[0]
        elif isinstance(datos, tuple):
            row = datos
        else:
            row = None

        # limpiar si no hay resultado
        if not row:
            self.descripcion_actualizar.setText("")
            self.existencia_actualizar.setText("")
            self.precio_actualizar.setText("")
            self.precio_actualizar_2.setText("")
            return

        # asignar campos de forma segura
        self.descripcion_actualizar.setText(str(row[1]))  # apellido
        self.existencia_actualizar.setText(str(row[2]))   # puesto
        self.precio_actualizar.setText(str(row[3]))       # edad
        self.precio_actualizar_2.setText(str(row[4]))     # salario
        
# 6.- mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

#7.- Mover menú
    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width == 0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
            self.animacionb.setStartValue(widthb)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()