"""
Servicio de cálculo de hashes (SHA-256 y MD5)
Calcula hashes de archivos con soporte para progreso
"""

import hashlib
from pathlib import Path
from typing import Callable, Optional, Tuple


class HashService:
    """Servicio para cálculo de hashes criptográficos"""
    
    @staticmethod
    def calcular_hash_archivo(
        ruta_archivo: str,
        algoritmo: str = 'sha256',
        callback_progreso: Optional[Callable[[int], None]] = None
    ) -> str:
        """
        Calcular hash de un archivo
        
        Args:
            ruta_archivo: Ruta completa del archivo
            algoritmo: 'sha256' o 'md5'
            callback_progreso: Función que recibe porcentaje (0-100)
        
        Returns:
            Hash hexadecimal del archivo
        """
        if algoritmo == 'sha256':
            hasher = hashlib.sha256()
        elif algoritmo == 'md5':
            hasher = hashlib.md5()
        else:
            raise ValueError(f"Algoritmo no soportado: {algoritmo}")
        
        ruta = Path(ruta_archivo)
        if not ruta.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
        
        tamano_archivo = ruta.stat().st_size
        bytes_leidos = 0
        
        with open(ruta, 'rb') as f:
            while True:
                chunk = f.read(8192)  # Leer de 8KB en 8KB
                if not chunk:
                    break
                
                hasher.update(chunk)
                bytes_leidos += len(chunk)
                
                if callback_progreso and tamano_archivo > 0:
                    progreso = int((bytes_leidos / tamano_archivo) * 100)
                    callback_progreso(progreso)
        
        return hasher.hexdigest()
    
    @staticmethod
    def calcular_hashes_duales(
        ruta_archivo: str,
        callback_progreso: Optional[Callable[[int], None]] = None
    ) -> Tuple[str, str]:
        """
        Calcular SHA-256 y MD5 simultáneamente en una sola pasada
        
        Args:
            ruta_archivo: Ruta completa del archivo
            callback_progreso: Función que recibe porcentaje (0-100)
        
        Returns:
            Tupla (hash_sha256, hash_md5)
        """
        hasher_sha256 = hashlib.sha256()
        hasher_md5 = hashlib.md5()
        
        ruta = Path(ruta_archivo)
        if not ruta.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
        
        tamano_archivo = ruta.stat().st_size
        bytes_leidos = 0
        
        with open(ruta, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                
                hasher_sha256.update(chunk)
                hasher_md5.update(chunk)
                bytes_leidos += len(chunk)
                
                if callback_progreso and tamano_archivo > 0:
                    progreso = int((bytes_leidos / tamano_archivo) * 100)
                    callback_progreso(progreso)
        
        return hasher_sha256.hexdigest(), hasher_md5.hexdigest()
    
    @staticmethod
    def comparar_hashes(hash1: str, hash2: str) -> bool:
        """
        Comparar dos hashes de forma segura
        
        Args:
            hash1: Primer hash
            hash2: Segundo hash
        
        Returns:
            True si los hashes coinciden, False en caso contrario
        """
        # Normalizar a minúsculas y eliminar espacios
        h1 = hash1.lower().strip()
        h2 = hash2.lower().strip()
        
        # Comparación constante para evitar timing attacks
        if len(h1) != len(h2):
            return False
        
        resultado = 0
        for x, y in zip(h1, h2):
            resultado |= ord(x) ^ ord(y)
        
        return resultado == 0
    
    @staticmethod
    def validar_formato_hash(hash_value: str, algoritmo: str = 'sha256') -> bool:
        """
        Validar que un hash tenga el formato correcto
        
        Args:
            hash_value: Valor del hash a validar
            algoritmo: 'sha256' o 'md5'
        
        Returns:
            True si el formato es válido
        """
        longitudes_esperadas = {
            'sha256': 64,
            'md5': 32
        }
        
        longitud_esperada = longitudes_esperadas.get(algoritmo.lower())
        if not longitud_esperada:
            return False
        
        if len(hash_value) != longitud_esperada:
            return False
        
        try:
            int(hash_value, 16)
            return True
        except ValueError:
            return False


# Instancia global
hash_service = HashService()
