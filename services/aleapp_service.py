"""
Servicio de integración con ALEAPP para análisis forense
Utiliza QProcess para ejecución asíncrona sin bloquear la UI
"""

from PyQt6.QtCore import QProcess, pyqtSignal, QObject
from pathlib import Path
import json


class AleappService(QObject):
    """Servicio para ejecutar ALEAPP mediante QProcess"""
    
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
        
        self.ruta_imagen = ""
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
            mensaje = f"Análisis ALEAPP completado. Reporte en: {self.ruta_salida}"
        else:
            mensaje = f"Error en el análisis. Código: {exit_code}"
        
        self.proceso_finalizado.emit(exito, mensaje)
    
    def iniciar_analisis(self, ruta_imagen: str, ruta_salida: str,
                         aleapp_path: str = '/usr/bin/aleapp'):
        """
        Iniciar análisis con ALEAPP
        
        Args:
            ruta_imagen: Ruta de la imagen forense o backup
            ruta_salida: Directorio donde se guardarán los reportes
            aleapp_path: Ruta al ejecutable de ALEAPP
        """
        self.ruta_imagen = ruta_imagen
        self.ruta_salida = ruta_salida
        self.log_acumulado = []
        
        # Crear directorio de salida si no existe
        Path(ruta_salida).mkdir(parents=True, exist_ok=True)
        
        # Preparar argumentos de ALEAPP
        # ALEAPP usa: aleapp.py -i <input> -o <output> -t <tipo>
        args = [
            '-i', ruta_imagen,
            '-o', ruta_salida,
            '-t', 'fs'  # filesystem (para imágenes)
        ]
        
        self.proceso_iniciado.emit()
        self.process.start(aleapp_path, args)
    
    def detener_proceso(self):
        """Detener el proceso de análisis"""
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
    
    def obtener_ruta_reporte(self) -> str:
        """Obtener ruta del reporte HTML generado"""
        if self.ruta_salida:
            reporte_path = Path(self.ruta_salida) / 'index.html'
            if reporte_path.exists():
                return str(reporte_path)
        return ""


def create_aleapp_service(db_manager):
    """Factory function para crear instancia de AleappService"""
    return AleappService(db_manager)
