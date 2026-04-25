"""
Widget reutilizable para cálculo y visualización de hashes
Muestra SHA-256 y MD5 con indicador visual de coincidencia
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QProgressBar, QFrame)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont


class HashWidget(QWidget):
    """Widget para cálculo y comparación de hashes"""
    
    hash_calculado = pyqtSignal(str, str)  # sha256, md5
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Título
        titulo = QLabel("🔐 HASHES DE INTEGRIDAD")
        titulo.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(titulo)
        
        # Campo SHA-256
        layout_sha = QHBoxLayout()
        lbl_sha = QLabel("SHA-256:")
        lbl_sha.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        lbl_sha.setFixedWidth(70)
        
        self.input_sha256 = QLineEdit()
        self.input_sha256.setPlaceholderText("Ingrese o calcule hash SHA-256...")
        self.input_sha256.setFont(QFont("Courier", 9))
        self.input_sha256.setReadOnly(True)
        
        layout_sha.addWidget(lbl_sha)
        layout_sha.addWidget(self.input_sha256)
        layout.addLayout(layout_sha)
        
        # Campo MD5
        layout_md5 = QHBoxLayout()
        lbl_md5 = QLabel("MD5:")
        lbl_md5.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        lbl_md5.setFixedWidth(70)
        
        self.input_md5 = QLineEdit()
        self.input_md5.setPlaceholderText("Ingrese o calcule hash MD5...")
        self.input_md5.setFont(QFont("Courier", 9))
        self.input_md5.setReadOnly(True)
        
        layout_md5.addWidget(lbl_md5)
        layout_md5.addWidget(self.input_md5)
        layout.addLayout(layout_md5)
        
        # Botón calcular
        self.btn_calcular = QPushButton("📂 Calcular Hashes")
        self.btn_calcular.setObjectName("btnPrimary")
        self.btn_calcular.clicked.connect(self._on_calcular_clicked)
        layout.addWidget(self.btn_calcular)
        
        # Barra de progreso
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setVisible(False)
        layout.addWidget(self.barra_progreso)
        
        # Indicador de estado
        self.lbl_estado = QLabel("")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_estado.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(self.lbl_estado)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("background-color: #4a5568;")
        layout.addWidget(separador)
    
    def _on_calcular_clicked(self):
        """Manejar click en botón calcular"""
        # Este método será sobrescrito por el padre que conecte el servicio
        pass
    
    def set_hash_values(self, sha256: str, md5: str):
        """Establecer valores de hash"""
        self.input_sha256.setText(sha256)
        self.input_md5.setText(md5)
    
    def clear(self):
        """Limpiar todos los campos"""
        self.input_sha256.clear()
        self.input_md5.clear()
        self.lbl_estado.clear()
        self.lbl_estado.setStyleSheet("")
        self.barra_progreso.setValue(0)
    
    def set_estado(self, coinciden: bool, mensaje: str = ""):
        """
        Establecer estado visual de comparación
        
        Args:
            coinciden: True si los hashes coinciden
            mensaje: Mensaje adicional opcional
        """
        if coinciden:
            self.lbl_estado.setText(f"✅ {mensaje or 'Hashes coinciden'}")
            self.lbl_estado.setStyleSheet("color: #68d391; background-color: #22543d; padding: 8px; border-radius: 4px;")
        else:
            self.lbl_estado.setText(f"❌ {mensaje or 'Hashes NO coinciden'}")
            self.lbl_estado.setStyleSheet("color: #fc8181; background-color: #742a2a; padding: 8px; border-radius: 4px;")
    
    def set_progreso(self, valor: int):
        """Actualizar barra de progreso"""
        self.barra_progreso.setValue(valor)
        self.barra_progreso.setVisible(valor > 0 and valor < 100)
    
    def habilitar_botones(self, habilitado: bool):
        """Habilitar o deshabilitar botones"""
        self.btn_calcular.setEnabled(habilitado)


# Import necesario para Qt.AlignmentFlag
from PyQt6.QtCore import Qt
