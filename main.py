#!/usr/bin/env python3
"""
Sistema Forense Android - Formulario Simplificado
Versión reducida para integración en la suite forense SHA256
"""

import sys
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QFormLayout, QLineEdit, QPushButton, QLabel, 
                             QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importar módulos del proyecto
from database.db_manager import db_manager
from models import Caso


class FormularioCaso(QMainWindow):
    """Ventana principal con formulario de caso simplificado"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar base de datos
        db_manager.init_db()
        
        # Configurar ventana principal
        self.setWindowTitle("🔬 Sistema Forense Android - Formulario")
        self.setMinimumSize(600, 400)
        self.setMaximumSize(800, 600)
        
        # Aplicar estilos
        self._aplicar_estilos()
        
        # Configurar UI
        self._inicializar_ui()
    
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
                QWidget {
                    background-color: #1a1d23;
                    color: #e2e8f0;
                }
                QFrame#formulario_container {
                    background-color: #2d3748;
                    border-radius: 10px;
                    padding: 20px;
                }
                QLabel#titulo {
                    color: #90cdf4;
                    font-size: 20px;
                    font-weight: bold;
                }
                QLabel#subtitulo {
                    color: #a0aec0;
                    font-size: 12px;
                }
                QLineEdit {
                    background-color: #1a202c;
                    border: 1px solid #4a5568;
                    border-radius: 4px;
                    color: #e2e8f0;
                    padding: 8px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 1px solid #4299e1;
                }
                QPushButton#btnPrimary {
                    background-color: #2b6cb0;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton#btnPrimary:hover {
                    background-color: #3182ce;
                }
                QPushButton#btnSecondary {
                    background-color: #4a5568;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 24px;
                    font-size: 14px;
                }
                QPushButton#btnSecondary:hover {
                    background-color: #718096;
                }
            """)
    
    def _inicializar_ui(self):
        """Inicializar componentes de la interfaz"""
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)
        
        # Título
        lbl_titulo = QLabel("🔬 SISTEMA FORENSE ANDROID")
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_titulo)
        
        # Subtítulo
        lbl_subtitulo = QLabel("Registro de Caso - Suite Forense SHA256")
        lbl_subtitulo.setObjectName("subtitulo")
        lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_subtitulo)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("background-color: #4a5568; min-height: 2px;")
        layout_principal.addWidget(separador)
        
        # Contenedor del formulario
        contenedor = QFrame()
        contenedor.setObjectName("formulario_container")
        layout_contenedor = QVBoxLayout(contenedor)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Campo Número de Caso
        self.input_numero_caso = QLineEdit()
        self.input_numero_caso.setPlaceholderText("Ej: CF-2024-001 o dejar vacío para autogenerar")
        form_layout.addRow("Número de Caso:", self.input_numero_caso)
        
        # Campo Fiscal Asignado
        self.input_fiscal = QLineEdit()
        self.input_fiscal.setPlaceholderText("Nombre del fiscal asignado")
        form_layout.addRow("Fiscal Asignado:", self.input_fiscal)
        
        layout_contenedor.addLayout(form_layout)
        layout_principal.addWidget(contenedor)
        
        # Botones
        layout_botones = QVBoxLayout()
        layout_botones.setSpacing(10)
        
        btn_guardar = QPushButton("💾 Guardar Caso")
        btn_guardar.setObjectName("btnPrimary")
        btn_guardar.setFixedHeight(45)
        btn_guardar.clicked.connect(self._guardar_caso)
        layout_botones.addWidget(btn_guardar)
        
        btn_limpiar = QPushButton("🗑️ Limpiar Formulario")
        btn_limpiar.setObjectName("btnSecondary")
        btn_limpiar.setFixedHeight(45)
        btn_limpiar.clicked.connect(self._limpiar_formulario)
        layout_botones.addWidget(btn_limpiar)
        
        layout_principal.addLayout(layout_botones)
        
        # Espacio flexible
        layout_principal.addStretch()
    
    def _guardar_caso(self):
        """Guardar caso en la base de datos"""
        numero_caso = self.input_numero_caso.text().strip()
        fiscal = self.input_fiscal.text().strip()
        
        # Generar número automático si está vacío
        if not numero_caso:
            now = datetime.now()
            numero_caso = f"CF-{now.year}-{now.strftime('%m%d%H%M%S')}"
        
        # Validar que no exista
        caso_existente = db_manager.obtener_caso_por_numero(numero_caso)
        if caso_existente:
            QMessageBox.warning(
                self,
                "Caso Existente",
                f"El número de caso '{numero_caso}' ya existe.\nPor favor use un número diferente."
            )
            return
        
        # Guardar en base de datos
        caso_id = db_manager.crear_caso(numero_caso, fiscal if fiscal else None)
        
        if caso_id:
            QMessageBox.information(
                self,
                "✅ Caso Creado Exitosamente",
                f"Número de Caso: {numero_caso}\n"
                f"ID Interno: {caso_id}\n"
                f"Fiscal: {fiscal or 'No asignado'}\n\n"
                "El caso ha sido registrado en la base de datos."
            )
            self._limpiar_formulario()
        else:
            QMessageBox.critical(
                self,
                "❌ Error",
                "No se pudo crear el caso.\nPor favor intente nuevamente."
            )
    
    def _limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.input_numero_caso.clear()
        self.input_fiscal.clear()
        self.input_numero_caso.setFocus()


def main():
    """Función principal de entrada"""
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Crear y mostrar ventana principal
    window = FormularioCaso()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
