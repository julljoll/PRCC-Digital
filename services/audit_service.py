"""
Servicio de auditoría para trazabilidad del proceso forense
Registra todas las acciones en el log inmutable
"""

from datetime import datetime
from typing import Optional, List, Dict, Any


class AuditService:
    """Servicio para gestión del log de auditoría"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def registrar_accion(
        self,
        caso_id: Optional[int],
        fase: int,
        paso: int,
        accion: str,
        usuario: str = "system"
    ) -> str:
        """
        Registrar una acción en el log de auditoría
        
        Args:
            caso_id: ID del caso (None para acciones globales)
            fase: Número de fase (1, 2, 3)
            paso: Número de paso dentro de la fase
            accion: Descripción de la acción realizada
            usuario: Usuario que realizó la acción
        
        Returns:
            Hash actual del registro (para encadenamiento)
        """
        hash_anterior = self.db.get_last_audit_hash(caso_id)
        return self.db.audit_action(caso_id, fase, paso, accion, usuario, hash_anterior)
    
    def obtener_log_caso(self, caso_id: int, limite: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener log de auditoría de un caso específico
        
        Args:
            caso_id: ID del caso
            limite: Máximo número de registros a devolver
        
        Returns:
            Lista de registros de auditoría
        """
        return self.db.obtener_audit_log(caso_id, limite)
    
    def obtener_log_completo(self, limite: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener log de auditoría completo
        
        Args:
            limite: Máximo número de registros a devolver
        
        Returns:
            Lista de registros de auditoría
        """
        return self.db.obtener_audit_log(None, limite)
    
    def verificar_integridad_log(self, caso_id: Optional[int] = None) -> bool:
        """
        Verificar la integridad del log de auditoría (cadena de hashes)
        
        Args:
            caso_id: ID del caso a verificar (None para todo el log)
        
        Returns:
            True si la cadena de hashes es válida
        """
        logs = self.obtener_log_caso(caso_id) if caso_id else self.obtener_log_completo()
        
        if not logs:
            return True
        
        # Verificar desde el más antiguo al más reciente
        logs_reversed = list(reversed(logs))
        hash_esperado = None
        
        for i, log in enumerate(logs_reversed):
            if i == 0:
                # El primer registro puede no tener hash_anterior
                continue
            
            # Recalcular hash actual basado en los datos
            timestamp = log['fecha_registro']
            hash_anterior_real = logs_reversed[i-1]['hash_actual'] if i > 0 else None
            
            if log.get('hash_anterior') != hash_anterior_real:
                return False
        
        return True
    
    def generar_reporte_auditoria(self, caso_id: int) -> str:
        """
        Generar reporte textual de auditoría para un caso
        
        Args:
            caso_id: ID del caso
        
        Returns:
            Reporte formateado como texto
        """
        logs = self.obtener_log_caso(caso_id)
        
        lineas = [
            "=" * 80,
            "REPORTE DE AUDITORÍA - TRAZABILIDAD DEL PROCESO FORENSE",
            "=" * 80,
            f"Caso ID: {caso_id}",
            f"Fecha generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total registros: {len(logs)}",
            "-" * 80,
            ""
        ]
        
        for log in reversed(logs):  # Mostrar del más antiguo al más reciente
            linea = (
                f"[{log['fecha_registro']}] "
                f"Fase {log['fase']} - Paso {log['paso']} | "
                f"{log['accion']} | "
                f"Usuario: {log['usuario']}"
            )
            lineas.append(linea)
        
        lineas.extend([
            "",
            "-" * 80,
            "FIN DEL REPORTE",
            "=" * 80
        ])
        
        return "\n".join(lineas)


# Factory function para crear instancia con db_manager
def create_audit_service(db_manager):
    """Crear instancia de AuditService con el database manager"""
    return AuditService(db_manager)
