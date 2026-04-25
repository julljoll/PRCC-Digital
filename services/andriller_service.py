"""
Servicio de integración con Andriller para extracción forense
Utiliza QProcess para ejecución asíncrona sin bloquear la UI
"""

from PyQt6.QtCore import QProcess, pyqtSignal, QObject
from pathlib import Path
import json


class AndrillerService(QObject):
    """Servicio para ejecutar Andriller mediante QProcess"""
    
    # Señales para comunicación con la UI
    proceso_iniciado = pyqtSignal()
    proceso_finalizado = pyqtSignal(bool, str)  # exito, mensaje
    log_actualizado = pyqtSignal(str)  # línea de log
    progreso_actualizado = pyqtSignal(int)  # porcentaje 0-100
    
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self._leer_salida)
        self.process.readyReadStandardError.connect(self._leer_error)
        self.process.finished.connect(self._proceso_finalizado)
        
        self.ruta_salida = ""
        self.log_acumulado = []
    
    def _leer_salida(self):
        """Leer salida estándar del proceso"""
        salida = bytes(self.process.readAllStandardOutput()).decode('utf-8', errors='replace')
        lineas = salida.strip().split('\n')
        
        for linea in lineas:
            if linea.strip():
                self.log_acumulado.append(linea)
                self.log_actualizado.emit(linea)
                
                # Intentar detectar progreso desde el log
                if 'progress' in linea.lower() or '%' in linea:
                    try:
                        # Buscar patrón de porcentaje
                        import re
                        match = re.search(r'(\d+)%', linea)
                        if match:
                            self.progreso_actualizado.emit(int(match.group(1)))
                    except:
                        pass
    
    def _leer_error(self):
        """Leer error estándar del proceso"""
        error = bytes(self.process.readAllStandardError()).decode('utf-8', errors='replace')
        lineas = error.strip().split('\n')
        
        for linea in lineas:
            if linea.strip():
                self.log_acumulado.append(f"ERROR: {linea}")
                self.log_actualizado.emit(f"ERROR: {linea}")
    
    def _proceso_finalizado(self, exit_code, exit_status):
        """Manejar finalización del proceso"""
        exito = exit_code == 0 and exit_status == QProcess.ExitStatus.NormalExit
        
        if exito:
            mensaje = f"Extracción completada exitosamente. Salida: {self.ruta_salida}"
        else:
            mensaje = f"Error en la extracción. Código: {exit_code}"
        
        self.proceso_finalizado.emit(exito, mensaje)
    
    def iniciar_extraccion(self, ruta_imagen: str, tipo_extraccion: str = 'logica',
                           andriller_path: str = '/usr/bin/andriller'):
        """
        Iniciar extracción con Andriller
        
        Args:
            ruta_imagen: Ruta donde se guardará la imagen forense
            tipo_extraccion: 'logica' o 'fisica'
            andriller_path: Ruta al ejecutable de Andriller
        """
        self.ruta_salida = ruta_imagen
        self.log_acumulado = []
        
        # Crear directorio de salida si no existe
        Path(ruta_imagen).parent.mkdir(parents=True, exist_ok=True)
        
        # Preparar argumentos de Andriller
        # Nota: Los argumentos reales dependen de la CLI de Andriller
        args = [
            '--output', ruta_imagen,
            '--type', tipo_extraccion,
            '--no-gui'  # Modo sin interfaz gráfica
        ]
        
        self.proceso_iniciado.emit()
        self.process.start(andriller_path, args)
    
    def detener_proceso(self):
        """Detener el proceso de extracción"""
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
    
    def obtener_log_completo(self) -> str:
        """Obtener todo el log acumulado"""
        return '\n'.join(self.log_acumulado)
    
    def estado_proceso(self) -> str:
        """Obtener estado actual del proceso"""
        estados = {
            QProcess.ProcessState.NotRunning: "No ejecutándose",
            QProcess.ProcessState.Starting: "Iniciando",
            QProcess.ProcessState.Running: "Ejecutándose"
        }
        return estados.get(self.process.state(), "Desconocido")


def create_andriller_service(db_manager):
    """Factory function para crear instancia de AndrillerService"""
    return AndrillerService(db_manager)
