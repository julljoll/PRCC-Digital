#!/usr/bin/env python3
"""
Sistema Forense Android - Punto de entrada principal
Aplicación de escritorio PyQt6 para gestión del proceso forense
informático de dispositivos Android según marco legal venezolano
"""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QStackedWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importar módulos del proyecto
from database.db_manager import db_manager
from models import Caso
from ui.sidebar import Sidebar
from services import create_audit_service


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar base de datos
        db_manager.init_db()
        
        # Crear servicio de auditoría
        self.audit_service = create_audit_service(db_manager)
        
        # Configurar ventana principal
        self.setWindowTitle("🔬 Sistema Forense Android - Laboratorio Informático Forense")
        self.setMinimumSize(1200, 800)
        
        # Aplicar estilos
        self._aplicar_estilos()
        
        # Configurar UI
        self._inicializar_ui()
        
        # Estado inicial
        self.caso_activo = None
        self.paso_actual = 0
    
    def _aplicar_estilos(self):
        """Aplicar hoja de estilos global (tema oscuro profesional)"""
        style_qss = Path(__file__).parent / 'assets' / 'style.qss'
        
        if style_qss.exists():
            with open(style_qss, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        else:
            # Estilos por defecto si no existe el archivo QSS
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a1d23;
                }
                QWidget#sidebar {
                    background-color: #13161b;
                    border-right: 2px solid #2d3748;
                    min-width: 220px;
                    max-width: 260px;
                }
                QListWidget {
                    background: transparent;
                    border: none;
                    color: #a0aec0;
                    font-size: 13px;
                }
                QListWidget::item:selected {
                    background-color: #2b6cb0;
                    color: #ffffff;
                    border-radius: 6px;
                }
                QListWidget::item:hover {
                    background-color: #2d3748;
                    border-radius: 6px;
                }
                QPushButton#btnPrimary {
                    background-color: #2b6cb0;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton#btnPrimary:hover {
                    background-color: #3182ce;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #2d3748;
                    border: 1px solid #4a5568;
                    border-radius: 4px;
                    color: #e2e8f0;
                    padding: 6px;
                }
                QLabel#sectionTitle {
                    color: #90cdf4;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
    
    def _inicializar_ui(self):
        """Inicializar componentes de la interfaz"""
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        
        # Splitter horizontal (sidebar + panel central)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar (panel lateral izquierdo)
        self.sidebar = Sidebar()
        self.sidebar.paso_seleccionado.connect(self._on_paso_seleccionado)
        splitter.addWidget(self.sidebar)
        
        # Panel central (QStackedWidget para las páginas)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #1a1d23;")
        
        # Página de bienvenida (placeholder hasta que se seleccione/cree un caso)
        pagina_bienvenida = self._crear_pagina_bienvenida()
        self.stacked_widget.addWidget(pagina_bienvenida)
        
        splitter.addWidget(self.stacked_widget)
        
        # Configurar proporciones del splitter
        splitter.setStretchFactor(0, 0)  # Sidebar no estirable
        splitter.setStretchFactor(1, 1)  # Panel central estirable
        splitter.setSizes([260, 940])
        
        layout_principal.addWidget(splitter)
    
    def _crear_pagina_bienvenida(self) -> QWidget:
        """Crear página de bienvenida/dashboard"""
        from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout
        from PyQt6.QtGui import QFont
        
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("🔬 SISTEMA FORENSE ANDROID")
        lbl_titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet("color: #ffffff;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)
        
        # Subtítulo
        lbl_subtitulo = QLabel("Gestión del Procedimiento Forense Informático\nDispositivos Android - Marco Legal Venezolano")
        lbl_subtitulo.setFont(QFont("Arial", 12))
        lbl_subtitulo.setStyleSheet("color: #a0aec0;")
        lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_subtitulo)
        
        # Separador
        from PyQt6.QtWidgets import QFrame
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("background-color: #4a5568; min-height: 2px; max-width: 600px;")
        layout.addWidget(separador)
        
        # Botones de acción
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(20)
        
        btn_nuevo_caso = QPushButton("📁 Nuevo Caso")
        btn_nuevo_caso.setObjectName("btnPrimary")
        btn_nuevo_caso.setFixedSize(200, 50)
        btn_nuevo_caso.clicked.connect(self._nuevo_caso)
        layout_botones.addWidget(btn_nuevo_caso)
        
        btn_abrir_caso = QPushButton("📂 Abrir Caso Existente")
        btn_abrir_caso.setObjectName("btnPrimary")
        btn_abrir_caso.setFixedSize(200, 50)
        btn_abrir_caso.clicked.connect(self._abrir_caso)
        layout_botones.addWidget(btn_abrir_caso)
        
        layout.addLayout(layout_botones)
        
        # Información de fases
        lbl_fases = QLabel(
            "Proceso Forense en 3 Fases:\n"
            "FASE I → Obtención y Adquisición en Sitio\n"
            "FASE II → Peritaje y Análisis en Laboratorio\n"
            "FASE III → Emisión del Dictamen Pericial"
        )
        lbl_fases.setFont(QFont("Arial", 10))
        lbl_fases.setStyleSheet("color: #68d391;")
        lbl_fases.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_fases)
        
        return pagina
    
    def _nuevo_caso(self):
        """Crear nuevo caso"""
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit
        from datetime import datetime
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Caso")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        
        input_numero = QLineEdit()
        input_numero.setPlaceholderText("Ej: CF-2024-001")
        layout.addRow("Número de Caso:", input_numero)
        
        input_fiscal = QLineEdit()
        input_fiscal.setPlaceholderText("Nombre del fiscal asignado")
        layout.addRow("Fiscal Asignado:", input_fiscal)
        
        # Botones
        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(dialog.accept)
        botones.rejected.connect(dialog.reject)
        layout.addRow(botones)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            numero_caso = input_numero.text().strip()
            fiscal = input_fiscal.text().strip()
            
            if not numero_caso:
                # Generar número automático
                now = datetime.now()
                numero_caso = f"CF-{now.year}-{now.strftime('%m%d%H%M%S')}"
            
            caso_id = db_manager.crear_caso(numero_caso, fiscal if fiscal else None)
            
            if caso_id:
                self.caso_activo = db_manager.obtener_caso(caso_id)
                self.sidebar.set_caso_activo(numero_caso)
                self.audit_service.registrar_accion(caso_id, 0, 0, "Caso abierto", "usuario")
                
                # Mostrar mensaje de éxito
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Caso Creado",
                    f"Caso {numero_caso} creado exitosamente.\n\n"
                    f"Comience con el Paso 1: Aislamiento y Fijación"
                )
                
                # Seleccionar primer paso
                self.sidebar.seleccionar_paso(0)
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo crear el caso. El número ya existe."
                )
    
    def _abrir_caso(self):
        """Abrir caso existente"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
        
        casos = db_manager.listar_casos()
        
        if not casos:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Sin Casos", "No hay casos registrados.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Abrir Caso Existente")
        dialog.setModal(True)
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        lista = QListWidget()
        for caso in casos:
            estado_icon = "✅" if caso['estado'] == 'activo' else "🔒"
            lista.addItem(f"{estado_icon} {caso['numero_caso']} - {caso['fecha_inicio']}")
        
        layout.addWidget(lista)
        
        btn_abrir = QPushButton("Abrir Caso Seleccionado")
        btn_abrir.setObjectName("btnPrimary")
        btn_abrir.clicked.connect(dialog.accept)
        layout.addWidget(btn_abrir)
        
        if dialog.exec() == QDialog.DialogCode.Accepted and lista.currentRow() >= 0:
            caso_seleccionado = casos[lista.currentRow()]
            self.caso_activo = caso_seleccionado
            self.sidebar.set_caso_activo(caso_seleccionado['numero_caso'])
            self.audit_service.registrar_accion(
                caso_seleccionado['id'], 0, 0, "Caso abierto", "usuario"
            )
            
            # Ir al paso actual del caso
            paso_actual = caso_seleccionado.get('paso_actual', 1)
            self.sidebar.seleccionar_paso(max(0, paso_actual - 1))
    
    def _on_paso_seleccionado(self, paso_numero: int):
        """Manejar selección de un paso del proceso"""
        if not self.caso_activo:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Seleccione un Caso",
                "Primero debe crear o abrir un caso para acceder a las etapas del proceso forense."
            )
            return
        
        self.paso_actual = paso_numero
        # TODO: Cargar la página correspondiente al paso seleccionado


def main():
    """Función principal de entrada"""
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
