"""
Widget visor de logs en tiempo real para procesos externos
Muestra stdout/stderr de Andriller y ALEAPP
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QColor, QTextCursor
from PyQt6.QtCore import pyqtSignal, Qt


class LogViewer(QWidget):
    """Visor de logs en tiempo real con colores por tipo de mensaje"""
    
    def __init__(self, titulo: str = "Log de Ejecución", parent=None):
        super().__init__(parent)
        self.titulo = titulo
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        
        # Título
        lbl_titulo = QLabel(f"📋 {self.titulo}")
        lbl_titulo.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(lbl_titulo)
        
        # Área de texto para logs
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setFont(QFont("Courier", 9))
        self.txt_log.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 1px solid #4a5568;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        layout.addWidget(self.txt_log)
        
        # Botones de control
        layout_botones = QHBoxLayout()
        
        self.btn_limpiar = QPushButton("🗑️ Limpiar")
        self.btn_limpiar.setObjectName("btnSecondary")
        self.btn_limpiar.clicked.connect(self.limpiar)
        layout_botones.addWidget(self.btn_limpiar)
        
        self.btn_copiar = QPushButton("📋 Copiar")
        self.btn_copiar.setObjectName("btnSecondary")
        self.btn_copiar.clicked.connect(self.copiar_al_portapapeles)
        layout_botones.addWidget(self.btn_copiar)
        
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_guardar.setObjectName("btnSecondary")
        self.btn_guardar.clicked.connect(self.guardar_log)
        layout_botones.addWidget(self.btn_guardar)
        
        layout_botones.addStretch()
        layout.addLayout(layout_botones)
    
    def agregar_log(self, mensaje: str, tipo: str = 'info'):
        """
        Agregar línea al log con color según tipo
        
        Args:
            mensaje: Mensaje a mostrar
            tipo: 'info', 'error', 'success', 'warning'
        """
        colores = {
            'info': '#63b3ed',
            'error': '#fc8181',
            'success': '#68d391',
            'warning': '#f6ad55'
        }
        
        color = colores.get(tipo, '#e2e8f0')
        
        # Mover cursor al final
        cursor = self.txt_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Insertar texto con formato
        cursor.insertHtml(f'<span style="color: {color};">{mensaje}</span><br>')
        self.txt_log.setTextCursor(cursor)
        
        # Auto-scroll al final
        self.txt_log.verticalScrollBar().setValue(
            self.txt_log.verticalScrollBar().maximum()
        )
    
    def limpiar(self):
        """Limpiar todo el log"""
        self.txt_log.clear()
    
    def copiar_al_portapapeles(self):
        """Copiar contenido del log al portapapeles"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_log.toPlainText())
        self.agregar_log("✓ Log copiado al portapapeles", 'success')
    
    def guardar_log(self):
        """Guardar log en archivo"""
        from PyQt6.QtWidgets import QFileDialog
        from pathlib import Path
        
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Log",
            "",
            "Archivos de Texto (*.txt);;Todos los Archivos (*)"
        )
        
        if archivo:
            try:
                ruta = Path(archivo)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(self.txt_log.toPlainText())
                self.agregar_log(f"✓ Log guardado en: {archivo}", 'success')
            except Exception as e:
                self.agregar_log(f"✗ Error guardando log: {e}", 'error')
    
    def get_contenido(self) -> str:
        """Obtener contenido completo del log"""
        return self.txt_log.toPlainText()
    
    def set_contenido(self, texto: str):
        """Establecer contenido completo del log"""
        self.txt_log.setPlainText(texto)
