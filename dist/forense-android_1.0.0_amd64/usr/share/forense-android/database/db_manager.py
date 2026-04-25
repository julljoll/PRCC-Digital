"""
Gestor de base de datos SQLite para el Sistema Forense Android
Maneja conexiones, migraciones y operaciones CRUD
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib
import json


def get_data_dir():
    """Obtener directorio de datos del usuario en Linux"""
    xdg_data = Path.home() / '.local' / 'share' / 'forense-android'
    xdg_data.mkdir(parents=True, exist_ok=True)
    return xdg_data


def get_db_path():
    """Obtener ruta completa de la base de datos"""
    return get_data_dir() / 'forense.db'


def get_config_path():
    """Obtener ruta del archivo de configuración"""
    config_dir = Path.home() / '.config' / 'forense-android'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.ini'


class DatabaseManager:
    """Clase singleton para gestión de la base de datos"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Obtener conexión a la base de datos SQLite"""
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(str(get_db_path()))
                self._connection.row_factory = sqlite3.Row
                # Habilitar foreign keys
                self._connection.execute("PRAGMA foreign_keys = ON")
            except Exception as e:
                print(f"Error conectando a la base de datos: {e}")
                raise
        return self._connection
    
    def init_db(self):
        """Inicializar la base de datos con el esquema"""
        conn = self.get_connection()
        schema_path = Path(__file__).parent.parent / 'database' / 'schema.sql'
        
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            
            try:
                conn.executescript(schema)
                conn.commit()
                self.audit_action(None, 0, 0, "Base de datos inicializada", "system")
                return True
            except Exception as e:
                print(f"Error inicializando base de datos: {e}")
                return False
        else:
            print(f"Esquema no encontrado en {schema_path}")
            return False
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def audit_action(self, caso_id, fase, paso, accion, usuario, hash_anterior=None):
        """Registrar acción en el log de auditoría (inmutable)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Calcular hash actual encadenado
        timestamp = datetime.now().isoformat()
        data = f"{caso_id}:{fase}:{paso}:{accion}:{usuario}:{timestamp}:{hash_anterior or ''}"
        hash_actual = hashlib.sha256(data.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO audit_log (caso_id, fase, paso, accion, usuario, hash_anterior, hash_actual)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (caso_id, fase, paso, accion, usuario, hash_anterior, hash_actual))
            conn.commit()
            return hash_actual
        except Exception as e:
            print(f"Error registrando en audit_log: {e}")
            conn.rollback()
            raise
    
    def get_last_audit_hash(self, caso_id=None):
        """Obtener el último hash del log de auditoría para encadenamiento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if caso_id:
            cursor.execute('''
                SELECT hash_actual FROM audit_log 
                WHERE caso_id = ? 
                ORDER BY fecha_registro DESC LIMIT 1
            ''', (caso_id,))
        else:
            cursor.execute('''
                SELECT hash_actual FROM audit_log 
                ORDER BY fecha_registro DESC LIMIT 1
            ''')
        
        row = cursor.fetchone()
        return row['hash_actual'] if row else None
    
    # Operaciones CRUD para Casos
    def crear_caso(self, numero_caso, fiscal=None):
        """Crear un nuevo caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO casos (numero_caso, fiscal)
                VALUES (?, ?)
            ''', (numero_caso, fiscal))
            conn.commit()
            caso_id = cursor.lastrowid
            
            self.audit_action(caso_id, 0, 0, f"Caso creado: {numero_caso}", "system")
            return caso_id
        except sqlite3.IntegrityError as e:
            print(f"Error: El número de caso ya existe: {numero_caso}")
            return None
    
    def obtener_caso(self, caso_id):
        """Obtener un caso por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM casos WHERE id = ?', (caso_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def obtener_caso_por_numero(self, numero_caso):
        """Obtener un caso por número"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM casos WHERE numero_caso = ?', (numero_caso,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def listar_casos(self, estado=None):
        """Listar todos los casos o filtrar por estado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if estado:
            cursor.execute('SELECT * FROM casos WHERE estado = ? ORDER BY fecha_inicio DESC', (estado,))
        else:
            cursor.execute('SELECT * FROM casos ORDER BY fecha_inicio DESC')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def actualizar_paso_caso(self, caso_id, paso_actual):
        """Actualizar el paso actual de un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE casos SET paso_actual = ? WHERE id = ?
        ''', (paso_actual, caso_id))
        conn.commit()
        
        self.audit_action(caso_id, 0, paso_actual, f"Paso actualizado a {paso_actual}", "system")
    
    def cerrar_caso(self, caso_id):
        """Cerrar un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE casos SET estado = 'cerrado' WHERE id = ?
        ''', (caso_id,))
        conn.commit()
        
        self.audit_action(caso_id, 3, 9, "Caso cerrado", "system")
    
    # Operaciones CRUD para Dispositivos
    def guardar_dispositivo(self, caso_id, datos):
        """Guardar información del dispositivo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dispositivos 
            (caso_id, marca, modelo, imei, sim_card, numero_tel, 
             estado_fisico, modo_aislamiento, fotos_path, fecha_fijacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_id,
            datos.get('marca'),
            datos.get('modelo'),
            datos.get('imei'),
            datos.get('sim_card'),
            datos.get('numero_tel'),
            datos.get('estado_fisico'),
            datos.get('modo_aislamiento'),
            json.dumps(datos.get('fotos', [])),
            datos.get('fecha_fijacion', datetime.now().isoformat())
        ))
        conn.commit()
        
        dispositivo_id = cursor.lastrowid
        self.audit_action(caso_id, 1, 1, "Dispositivo registrado", "system")
        return dispositivo_id
    
    def obtener_dispositivo(self, caso_id):
        """Obtener dispositivo asociado a un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM dispositivos WHERE caso_id = ?', (caso_id,))
        row = cursor.fetchone()
        if row:
            data = dict(row)
            data['fotos'] = json.loads(data.get('fotos_path') or '[]')
            return data
        return None
    
    # Operaciones CRUD para PRCC
    def guardar_prcc(self, caso_id, datos, tipo='principal'):
        """Guardar Planilla de Registro de Cadena de Custodia"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO prcc 
            (caso_id, numero_prcc, tipo, funcionario_colector, cargo, organo,
             tipo_embalaje, numero_precinto, hash_sha256, hash_md5, 
             estado_embalaje, nombre_firmante)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_id,
            datos.get('numero_prcc'),
            tipo,
            datos.get('funcionario_colector'),
            datos.get('cargo'),
            datos.get('organo'),
            datos.get('tipo_embalaje'),
            datos.get('numero_precinto'),
            datos.get('hash_sha256'),
            datos.get('hash_md5'),
            datos.get('estado_embalaje'),
            datos.get('nombre_firmante')
        ))
        conn.commit()
        
        prcc_id = cursor.lastrowid
        self.audit_action(caso_id, 1, 3, f"PRCC registrada: {datos.get('numero_prcc')}", "system")
        return prcc_id
    
    def obtener_prcc(self, caso_id, tipo='principal'):
        """Obtener PRCC de un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM prcc WHERE caso_id = ? AND tipo = ?
        ''', (caso_id, tipo))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Operaciones CRUD para Adquisiciones
    def guardar_adquisicion(self, caso_id, datos):
        """Guardar registro de adquisición forense"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO adquisiciones 
            (caso_id, herramienta, version_herramienta, ruta_salida,
             hash_origen_sha256, hash_copia_sha256, hashes_coinciden,
             log_ejecucion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_id,
            datos.get('herramienta'),
            datos.get('version_herramienta'),
            datos.get('ruta_salida'),
            datos.get('hash_origen_sha256'),
            datos.get('hash_copia_sha256'),
            1 if datos.get('hashes_coinciden') else 0,
            datos.get('log_ejecucion', '')
        ))
        conn.commit()
        
        adquisicion_id = cursor.lastrowid
        self.audit_action(caso_id, 1, 2, f"Adquisición realizada con {datos.get('herramienta')}", "system")
        return adquisicion_id
    
    def obtener_adquisicion(self, caso_id, herramienta=None):
        """Obtener adquisición de un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if herramienta:
            cursor.execute('''
                SELECT * FROM adquisiciones WHERE caso_id = ? AND herramienta = ?
            ''', (caso_id, herramienta))
        else:
            cursor.execute('''
                SELECT * FROM adquisiciones WHERE caso_id = ?
            ''', (caso_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Operaciones CRUD para Evidencias Derivadas
    def guardar_evidencia_derivada(self, caso_id, prcc_id, datos):
        """Guardar evidencia derivada"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO evidencias_derivadas 
            (caso_id, prcc_id, nombre_nativo, ruta_origen, tamanio_bytes,
             hash_sha256, fecha_creacion_metadata, fecha_modificacion_metadata,
             fecha_acceso_metadata, relevancia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_id,
            prcc_id,
            datos.get('nombre_nativo'),
            datos.get('ruta_origen'),
            datos.get('tamanio_bytes'),
            datos.get('hash_sha256'),
            datos.get('fecha_creacion_metadata'),
            datos.get('fecha_modificacion_metadata'),
            datos.get('fecha_acceso_metadata'),
            datos.get('relevancia')
        ))
        conn.commit()
        
        evidencia_id = cursor.lastrowid
        self.audit_action(caso_id, 2, 6, f"Evidencia derivada registrada: {datos.get('nombre_nativo')}", "system")
        return evidencia_id
    
    def obtener_evidencias_derivadas(self, caso_id):
        """Obtener todas las evidencias derivadas de un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM evidencias_derivadas WHERE caso_id = ?
        ''', (caso_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # Operaciones CRUD para Dictámenes
    def guardar_dictamen(self, caso_id, datos):
        """Guardar dictamen pericial"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dictamenes 
            (caso_id, numero_dictamen, motivo, descripcion, examenes_practicados,
             resultados_json, conclusiones, consumo_evidencia, perito, credencial)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso_id,
            datos.get('numero_dictamen'),
            datos.get('motivo'),
            datos.get('descripcion'),
            datos.get('examenes_practicados'),
            json.dumps(datos.get('resultados', {})),
            datos.get('conclusiones'),
            datos.get('consumo_evidencia'),
            datos.get('perito'),
            datos.get('credencial')
        ))
        conn.commit()
        
        dictamen_id = cursor.lastrowid
        self.audit_action(caso_id, 3, 8, f"Dictamen registrado: {datos.get('numero_dictamen')}", "system")
        return dictamen_id
    
    def obtener_dictamen(self, caso_id):
        """Obtener dictamen de un caso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM dictamenes WHERE caso_id = ?', (caso_id,))
        row = cursor.fetchone()
        if row:
            data = dict(row)
            data['resultados'] = json.loads(data.get('resultados_json') or '{}')
            return data
        return None
    
    # Operaciones de Configuración
    def guardar_configuracion(self, clave, valor):
        """Guardar parámetro de configuración"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO configuracion (clave, valor)
            VALUES (?, ?)
        ''', (clave, valor))
        conn.commit()
    
    def obtener_configuracion(self, clave, default=None):
        """Obtener parámetro de configuración"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT valor FROM configuracion WHERE clave = ?', (clave,))
        row = cursor.fetchone()
        return row['valor'] if row else default
    
    def obtener_toda_la_configuracion(self):
        """Obtener toda la configuración"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT clave, valor FROM configuracion')
        return {row['clave']: row['valor'] for row in cursor.fetchall()}
    
    # Utilidades de auditoría
    def obtener_audit_log(self, caso_id=None, limite=100):
        """Obtener log de auditoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if caso_id:
            cursor.execute('''
                SELECT * FROM audit_log WHERE caso_id = ?
                ORDER BY fecha_registro DESC LIMIT ?
            ''', (caso_id, limite))
        else:
            cursor.execute('''
                SELECT * FROM audit_log
                ORDER BY fecha_registro DESC LIMIT ?
            ''', (limite,))
        
        return [dict(row) for row in cursor.fetchall()]


# Instancia global
db_manager = DatabaseManager()
