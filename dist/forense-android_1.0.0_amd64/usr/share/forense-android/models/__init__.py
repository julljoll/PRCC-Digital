"""
Modelos de datos para el Sistema Forense Android
Dataclasses que representan las entidades del dominio
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Caso:
    """Representa un caso forense"""
    id: Optional[int] = None
    numero_caso: str = ""
    fiscal: str = ""
    fecha_inicio: str = ""
    estado: str = "activo"
    paso_actual: int = 1
    
    def generar_numero_caso(self) -> str:
        """Generar número de caso único"""
        now = datetime.now()
        return f"CF-{now.year}-{now.strftime('%m%d%H%M%S')}"


@dataclass
class Dispositivo:
    """Representa un dispositivo móvil bajo análisis"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    marca: str = ""
    modelo: str = ""
    imei: str = ""
    sim_card: str = ""
    numero_tel: str = ""
    estado_fisico: str = ""
    modo_aislamiento: str = ""  # 'modo_avion' o 'bolsa_faraday'
    fotos: List[str] = field(default_factory=list)
    fecha_fijacion: str = ""
    
    @staticmethod
    def validar_imei(imei: str) -> bool:
        """Validar IMEI usando algoritmo de Luhn"""
        if not imei or len(imei) != 15 or not imei.isdigit():
            return False
        
        digits = [int(d) for d in imei]
        # Doblar cada segundo dígito desde la derecha
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        return sum(digits) % 10 == 0


@dataclass
class PRCC:
    """Planilla de Registro de Cadena de Custodia"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    numero_prcc: str = ""
    tipo: str = "principal"  # 'principal' o 'derivada'
    funcionario_colector: str = ""
    cargo: str = ""
    organo: str = ""
    tipo_embalaje: str = ""  # 'bolsa', 'caja', 'sobre'
    numero_precinto: str = ""
    hash_sha256: str = ""
    hash_md5: str = ""
    estado_embalaje: str = ""  # 'buenas', 'deterioradas', 'rotas'
    nombre_firmante: str = ""
    fecha_creacion: str = ""
    
    def generar_numero_prcc(self) -> str:
        """Generar número de PRCC único"""
        now = datetime.now()
        tipo_codigo = "P" if self.tipo == "principal" else "D"
        return f"CF-PRCC-{tipo_codigo}-{now.year}-{now.strftime('%m%d%H%M%S')}"


@dataclass
class Adquisicion:
    """Registro de adquisición forense"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    herramienta: str = ""  # 'andriller' o 'aleapp'
    version_herramienta: str = ""
    ruta_salida: str = ""
    hash_origen_sha256: str = ""
    hash_copia_sha256: str = ""
    hashes_coinciden: bool = False
    log_ejecucion: str = ""
    fecha_ejecucion: str = ""


@dataclass
class EvidenciaDerivada:
    """Evidencia derivada del análisis"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    prcc_id: Optional[int] = None
    nombre_nativo: str = ""
    ruta_origen: str = ""
    tamanio_bytes: int = 0
    hash_sha256: str = ""
    fecha_creacion_metadata: str = ""
    fecha_modificacion_metadata: str = ""
    fecha_acceso_metadata: str = ""
    relevancia: str = ""


@dataclass
class Dictamen:
    """Dictamen pericial"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    numero_dictamen: str = ""
    motivo: str = ""
    descripcion: str = ""
    examenes_practicados: str = ""
    resultados: Dict[str, Any] = field(default_factory=dict)
    conclusiones: str = ""
    consumo_evidencia: str = ""
    perito: str = ""
    credencial: str = ""
    fecha_emision: str = ""
    
    def generar_numero_dictamen(self) -> str:
        """Generar número de dictamen único"""
        now = datetime.now()
        return f"CF-DICT-{now.year}-{now.strftime('%m%d%H%M%S')}"


@dataclass
class AuditLog:
    """Registro de auditoría"""
    id: Optional[int] = None
    caso_id: Optional[int] = None
    fase: int = 0
    paso: int = 0
    accion: str = ""
    usuario: str = ""
    hash_anterior: str = ""
    hash_actual: str = ""
    fecha_registro: str = ""


@dataclass
class Configuracion:
    """Configuración de la aplicación"""
    andriller_path: str = "/usr/bin/andriller"
    aleapp_path: str = "/usr/bin/aleapp"
    directorio_casos: str = ""
    ultimo_caso_id: Optional[int] = None
