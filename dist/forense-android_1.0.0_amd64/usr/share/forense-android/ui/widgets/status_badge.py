"""
Widget indicador de estado (semáforo) para pasos del proceso forense
Muestra visualmente el estado: pendiente, en progreso, completado, error
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont


class StatusBadge(QWidget):
    """Indicador visual de estado tipo semáforo"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Icono de estado (emoji o círculo)
        self.lbl_icono = QLabel("🔘")
        self.lbl_icono.setFont(QFont("Segoe UI Emoji", 14))
        layout.addWidget(self.lbl_icono)
        
        # Texto de estado
        self.lbl_texto = QLabel("Pendiente")
        self.lbl_texto.setFont(QFont("Arial", 10))
        layout.addWidget(self.lbl_texto)
        
        layout.addStretch()
    
    def set_estado_pendiente(self):
        """Marcar como pendiente (gris)"""
        self.lbl_icono.setText("🔘")
        self.lbl_texto.setText("Pendiente")
        self.lbl_texto.setStyleSheet("color: #a0aec0;")
    
    def set_estado_progreso(self):
        """Marcar como en progreso (amarillo)"""
        self.lbl_icono.setText("⏳")
        self.lbl_texto.setText("En Progreso")
        self.lbl_texto.setStyleSheet("color: #f6ad55;")
    
    def set_estado_completado(self):
        """Marcar como completado (verde)"""
        self.lbl_icono.setText("✅")
        self.lbl_texto.setText("Completado")
        self.lbl_texto.setStyleSheet("color: #68d391;")
    
    def set_estado_error(self, mensaje_error: str = ""):
        """Marcar como error (rojo)"""
        self.lbl_icono.setText("❌")
        self.lbl_texto.setText(f"Error{': ' + mensaje_error if mensaje_error else ''}")
        self.lbl_texto.setStyleSheet("color: #fc8181;")
    
    def set_estado(self, estado: str, mensaje: str = ""):
        """
        Establecer estado por nombre
        
        Args:
            estado: 'pendiente', 'progreso', 'completado', 'error'
            mensaje: Mensaje adicional para errores
        """
        estados = {
            'pendiente': self.set_estado_pendiente,
            'progreso': self.set_estado_progreso,
            'completado': self.set_estado_completado,
            'error': lambda: self.set_estado_error(mensaje)
        }
        
        metodo = estados.get(estado.lower(), self.set_estado_pendiente)
        metodo()
    
    def get_estado(self) -> str:
        """Obtener estado actual como texto"""
        icono = self.lbl_icono.text()
        
        if icono == "🔘":
            return "pendiente"
        elif icono == "⏳":
            return "progreso"
        elif icono == "✅":
            return "completado"
        elif icono == "❌":
            return "error"
        
        return "desconocido"
