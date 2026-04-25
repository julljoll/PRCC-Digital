-- Esquema de base de datos para Sistema Forense Android
-- Base de datos SQLite para trazabilidad de casos

-- Tabla principal de casos
CREATE TABLE IF NOT EXISTS casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_caso TEXT UNIQUE NOT NULL,
    fiscal TEXT,
    fecha_inicio TEXT DEFAULT (datetime('now', 'localtime')),
    estado TEXT DEFAULT 'activo',
    paso_actual INTEGER DEFAULT 1
);

-- Dispositivos
CREATE TABLE IF NOT EXISTS dispositivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER REFERENCES casos(id) ON DELETE CASCADE,
    marca TEXT,
    modelo TEXT,
    imei TEXT,
    sim_card TEXT,
    numero_tel TEXT,
    estado_fisico TEXT,
    modo_aislamiento TEXT,
    fotos_path TEXT,  -- JSON array de rutas
    fecha_fijacion TEXT
);

-- PRCC (Planilla de Cadena de Custodia)
CREATE TABLE IF NOT EXISTS prcc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER REFERENCES casos(id) ON DELETE CASCADE,
    numero_prcc TEXT UNIQUE,
    tipo TEXT DEFAULT 'principal',  -- 'principal' | 'derivada'
    funcionario_colector TEXT,
    cargo TEXT,
    organo TEXT,
    tipo_embalaje TEXT,
    numero_precinto TEXT,
    hash_sha256 TEXT,
    hash_md5 TEXT,
    estado_embalaje TEXT,
    nombre_firmante TEXT,
    fecha_creacion TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Adquisiciones
CREATE TABLE IF NOT EXISTS adquisiciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER REFERENCES casos(id) ON DELETE CASCADE,
    herramienta TEXT,  -- 'andriller' | 'aleapp'
    version_herramienta TEXT,
    ruta_salida TEXT,
    hash_origen_sha256 TEXT,
    hash_copia_sha256 TEXT,
    hashes_coinciden INTEGER,
    log_ejecucion TEXT,
    fecha_ejecucion TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Evidencias derivadas
CREATE TABLE IF NOT EXISTS evidencias_derivadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER REFERENCES casos(id) ON DELETE CASCADE,
    prcc_id INTEGER REFERENCES prcc(id) ON DELETE SET NULL,
    nombre_nativo TEXT,
    ruta_origen TEXT,
    tamanio_bytes INTEGER,
    hash_sha256 TEXT,
    fecha_creacion_metadata TEXT,
    fecha_modificacion_metadata TEXT,
    fecha_acceso_metadata TEXT,
    relevancia TEXT
);

-- Dictámenes
CREATE TABLE IF NOT EXISTS dictamenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER REFERENCES casos(id) ON DELETE CASCADE,
    numero_dictamen TEXT,
    motivo TEXT,
    descripcion TEXT,
    examenes_practicados TEXT,
    resultados_json TEXT,
    conclusiones TEXT,
    consumo_evidencia TEXT,
    perito TEXT,
    credencial TEXT,
    fecha_emision TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Log de trazabilidad (inmutable — solo INSERT)
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER,
    fase INTEGER,
    paso INTEGER,
    accion TEXT,
    usuario TEXT,
    hash_anterior TEXT,
    hash_actual TEXT,
    fecha_registro TEXT DEFAULT (datetime('now', 'localtime'))
);

-- Configuración de la aplicación
CREATE TABLE IF NOT EXISTS configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_casos_numero ON casos(numero_caso);
CREATE INDEX IF NOT EXISTS idx_dispositivos_caso ON dispositivos(caso_id);
CREATE INDEX IF NOT EXISTS idx_prcc_caso ON prcc(caso_id);
CREATE INDEX IF NOT EXISTS idx_adquisiciones_caso ON adquisiciones(caso_id);
CREATE INDEX IF NOT EXISTS idx_evidencias_caso ON evidencias_derivadas(caso_id);
CREATE INDEX IF NOT EXISTS idx_dictamenes_caso ON dictamenes(caso_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_caso ON audit_log(caso_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_fecha ON audit_log(fecha_registro);
