"""
Panel lateral de navegación para el Sistema Forense Android
Muestra las 3 fases y 9 pasos del proceso forense con indicadores de estado
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QLabel, QScrollArea, QFrame, QPushButton)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class Sidebar(QWidget):
    """Panel lateral con navegación por etapas del proceso forense"""
    
    paso_seleccionado = pyqtSignal(int)  # índice del paso seleccionado (0-8)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Encabezado
        lbl_titulo = QLabel("🔒 SISTEMA FORENSE ANDROID")
        lbl_titulo.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet("color: #ffffff; padding: 15px; background-color: #1a202c;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)
        
        # Área scrollable para la lista
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Lista de navegación
        self.lista_pasos = QListWidget()
        self.lista_pasos.setFixedWidth(260)
        self.lista_pasos.setStyleSheet("""
            QListWidget {
                background-color: #13161b;
                border: none;
                color: #a0aec0;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #2d3748;
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
            QListWidget::item:disabled {
                color: #4a5568;
            }
        """)
        self.lista_pasos.currentRowChanged.connect(self._on_paso_seleccionado)
        container_layout.addWidget(self.lista_pasos)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("background-color: #4a5568; min-height: 2px;")
        layout.addWidget(separador)
        
        # Botones inferiores
        lbl_trazabilidad = QLabel("📊 Trazabilidad")
        lbl_trazabilidad.setStyleSheet("color: #a0aec0; padding: 10px;")
        layout.addWidget(lbl_trazabilidad)
        
        lbl_config = QLabel("⚙️ Configuración")
        lbl_config.setStyleSheet("color: #a0aec0; padding: 10px;")
        layout.addWidget(lbl_config)
        
        # Información del caso activo
        self.lbl_caso_activo = QLabel("")
        self.lbl_caso_activo.setStyleSheet("color: #68d391; padding: 10px; font-weight: bold;")
        self.lbl_caso_activo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_caso_activo)
        
        # Inicializar items de la lista
        self._inicializar_lista()
    
    def _inicializar_lista(self):
        """Inicializar la lista con las fases y pasos del proceso"""
        self.lista_pasos.clear()
        
        # Estructura del proceso forense
        self.pasos = [
            # Header Caso Activo
            ("📁 CASO ACTIVO", True),
            
            # FASE I
            ("── FASE I ──", False),
            ("1. Aislamiento y Fijación", True),
            ("2. Adquisición (Andriller)", True),
            ("3. Cadena de Custodia (PRCC)", True),
            
            # FASE II
            ("── FASE II ──", False),
            ("4. Recepción en Laboratorio", True),
            ("5. Análisis (ALEAPP)", True),
            ("6. Evidencia Derivada", True),
            
            # FASE III
            ("── FASE III ──", False),
            ("7. Fundamentación Jurídica", True),
            ("8. Dictamen Pericial", True),
            ("9. Cierre y Disposición", True),
        ]
        
        for i, (texto, seleccionable) in enumerate(self.pasos):
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, seleccionable)
            
            if not seleccionable:
                # Headers de fase - no seleccionables
                item.setForeground(Qt.GlobalColor.gray)
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled & ~Qt.ItemFlag.ItemIsSelectable)
            
            self.lista_pasos.addItem(item)
    
    def _on_paso_seleccionado(self, index: int):
        """Manejar selección de un paso"""
        item = self.lista_pasos.item(index)
        if item and item.data(Qt.ItemDataRole.UserRole):
            # Convertir índice de lista a índice de paso (0-8)
            # Saltando headers
            pasos_reales = [i for i, (_, sel) in enumerate(self.pasos) if sel]
            if index in pasos_reales:
                paso_numero = pasos_reales.index(index)
                self.paso_seleccionado.emit(paso_numero)
    
    def set_estado_paso(self, paso_numero: int, estado: str):
        """
        Establecer estado visual de un paso
        
        Args:
            paso_numero: Número del paso (0-8)
            estado: 'pendiente', 'progreso', 'completado', 'error'
        """
        # Mapear número de paso a índice en la lista
        pasos_reales = [i for i, (_, sel) in enumerate(self.pasos) if sel]
        
        if 0 <= paso_numero < len(pasos_reales):
            indice_lista = pasos_reales[paso_numero]
            item = self.lista_pasos.item(indice_lista)
            
            if item:
                iconos = {
                    'pendiente': '🔘',
                    'progreso': '⏳',
                    'completado': '✅',
                    'error': '❌'
                }
                
                texto_original = self.pasos[indice_lista][0]
                # Extraer solo el nombre sin el número inicial
                partes = texto_original.split('. ', 1)
                if len(partes) > 1:
                    nombre = partes[1]
                else:
                    nombre = texto_original
                
                icono = iconos.get(estado, '🔘')
                item.setText(f"{icono} {nombre}")
    
    def habilitar_paso(self, paso_numero: int, habilitado: bool):
        """Habilitar o deshabilitar un paso"""
        pasos_reales = [i for i, (_, sel) in enumerate(self.pasos) if sel]
        
        if 0 <= paso_numero < len(pasos_reales):
            indice_lista = pasos_reales[paso_numero]
            item = self.lista_pasos.item(indice_lista)
            
            if item:
                if habilitado:
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled & ~Qt.ItemFlag.ItemIsSelectable)
    
    def set_caso_activo(self, numero_caso: str):
        """Mostrar número de caso activo"""
        self.lbl_caso_activo.setText(f"Caso: {numero_caso}")
    
    def seleccionar_paso(self, paso_numero: int):
        """Seleccionar programáticamente un paso"""
        pasos_reales = [i for i, (_, sel) in enumerate(self.pasos) if sel]
        
        if 0 <= paso_numero < len(pasos_reales):
            indice_lista = pasos_reales[paso_numero]
            self.lista_pasos.setCurrentRow(indice_lista)
