#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.productodao import ProductoDAO 
#2.- Cargar archivo .ui
class Load_ui_productos(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        # Cargar archivo .ui
        uic.loadUi("ui/ui_productos.ui", self)
        self.show()    
        
        self.productodao=ProductoDAO()
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
        #Botones para guardar, buscar, actualizar, eliminar y salir
        self.accion_guardar.clicked.connect(self.guardar_producto)
        self.buscar_actualizar.clicked.connect(self.buscar_producto_actualizar)
        self.buscar_eliminar.clicked.connect(self.buscar_producto_eliminar)
        self.accion_actualizar.clicked.connect(self.actualizar_producto)
        self.accion_eliminar.clicked.connect(self.eliminar_producto)
        self.accion_limpiar.clicked.connect(self.limpiar_producto)
        self.buscar_buscar.clicked.connect(self.buscar_producto_buscar)
        self.boton_refresh.clicked.connect(self.actualizar_tabla)
        

#5.- Operaciones con el modelo de datos 

    def regresar_menu_principal(self):
        if self.parent:
            self.parent.mostrar_ventana_principal()
        self.close()


    def guardar_producto(self):
        self.productodao.producto.clave=self.sku_agregar.text()
        self.productodao.producto.descripcion=self.descripcion_agregar.text()
        self.productodao.producto.existencia=int(self.existencia_agregar.text())
        self.productodao.producto.precio=float(self.precio_agregar.text())
        
        self.productodao.insertarProducto()
    
    def actualizar_tabla(self):
        datos=self.productodao.listarProductos()
        self.tabla_consulta.setRowCount(len(datos))
        i=0
        for fila in datos:
            self.tabla_consulta.setItem(i,0,QtWidgets.QTableWidgetItem(str(fila[1])))
            self.tabla_consulta.setItem(i,1,QtWidgets.QTableWidgetItem(str(fila[2])))
            self.tabla_consulta.setItem(i,2,QtWidgets.QTableWidgetItem(str(fila[3])))
            self.tabla_consulta.setItem(i,3,QtWidgets.QTableWidgetItem(str(fila[4])))
            i+=1
    
    def actualizar_producto(self):
        self.productodao.producto.clave=self.sku_actualizar.text()
        self.productodao.producto.descripcion=self.descripcion_actualizar.text()
        self.productodao.producto.existencia=int(self.existencia_actualizar.text())
        self.productodao.producto.precio=float(self.precio_actualizar.text())
        self.productodao.actualizarProducto()    

    def eliminar_producto(self):
        self.productodao.producto.clave=self.sku_eliminar.text()
        self.productodao.eliminarProducto()
    
    def buscar_producto_buscar(self):
        self.productodao.producto.clave = self.sku_buscar.text()
        datos = self.productodao.buscarProducto()
        
        # Only proceed if we have valid data
        if datos and len(datos) > 0:
            # Get first row if it's a list of rows
            row = datos[0] if isinstance(datos, list) else datos
            
            # Set the text fields
            self.descripcion_buscar.setText(str(row[2]))
            self.existencia_buscar.setText(str(row[3]))
            self.precio_buscar.setText(str(row[4]))
        else:
            # Clear fields if no data found
            self.descripcion_buscar.setText("")
            self.existencia_buscar.setText("")
            self.precio_buscar.setText("")
    
    def buscar_producto_eliminar(self):
        self.productodao.producto.clave = self.sku_eliminar.text()
        datos = self.productodao.buscarProducto()
        
        # Only proceed if we have valid data
        if datos and len(datos) > 0:
            # Get first row if it's a list of rows
            row = datos[0] if isinstance(datos, list) else datos
            
            # Set the text fields
            self.descripcion_eliminar.setText(str(row[2]))
            self.existencia_eliminar.setText(str(row[3]))
            self.precio_eliminar.setText(str(row[4]))
        else:
            # Clear fields if no data found
            self.descripcion_eliminar.setText("")
            self.existencia_eliminar.setText("")
            self.precio_eliminar.setText("")
    
    def limpiar_producto(self):
        self.sku_buscar.setText("")
        self.descripcion_buscar.setText("")
        self.existencia_buscar.setText("")
        self.precio_buscar.setText("")
    
    def buscar_producto_actualizar(self):
        self.productodao.producto.clave=self.sku_buscar.text()
        datos=self.productodao.listarProductos()
        
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
            return

        # asignar campos de forma segura
        self.descripcion_actualizar.setText(str(row[2]))
        self.existencia_actualizar.setText(str(row[3]))
        self.precio_actualizar.setText(str(row[4]))
        
        
        
        
# 6.- mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()

    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
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