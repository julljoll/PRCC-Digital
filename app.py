"""
PRCC Digital - Planilla de Registro de Cadena de Custodia
Aplicación de escritorio en Python con Flask para gestión de evidencia forense
Versión para Ubuntu 26.04+ con base de datos local SQLite
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import json
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sha256-forensic-lab-secret-key-2024'

# Configuración de directorios para aplicación de escritorio Linux
def get_data_dir():
    """Obtener directorio de datos del usuario en Linux"""
    xdg_data = os.getenv('XDG_DATA_HOME', '~/.local/share')
    return Path(xdg_data).expanduser() / 'prcc-digital'

def get_db_path():
    """Obtener ruta completa de la base de datos"""
    db_dir = get_data_dir()
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / 'prcc.db'

def get_db_connection():
    """Obtener conexión a la base de datos SQLite local"""
    try:
        conn = sqlite3.connect(str(get_db_path()))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_db():
    """Inicializar la tabla de registros si no existe"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id TEXT PRIMARY KEY,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                datos_generales TEXT,
                formas_obtencion TEXT,
                funcionario_obtiene TEXT,
                descripcion_evidencia TEXT,
                transferencia TEXT
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        return False

# Inicializar DB al arrancar
init_db()

@app.route('/')
def index():
    """Página principal con el formulario PRCC"""
    return render_template('index.html')

@app.route('/api/registro', methods=['POST'])
def crear_registro():
    """Crear un nuevo registro de cadena de custodia"""
    try:
        data = request.json
        registro_id = f"PRCC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        registro = {
            'id': registro_id,
            'fecha_creacion': datetime.now().isoformat(),
            'datos_generales': data.get('datos_generales', {}),
            'formas_obtencion': data.get('formas_obtencion', {}),
            'funcionario_obtiene': data.get('funcionario_obtiene', {}),
            'descripcion_evidencia': data.get('descripcion_evidencia', []),
            'transferencia': data.get('transferencia', {})
        }
        
        # Guardar en SQLite local
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO registros 
                    (id, datos_generales, formas_obtencion, funcionario_obtiene, descripcion_evidencia, transferencia)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    registro_id,
                    json.dumps(registro['datos_generales']),
                    json.dumps(registro['formas_obtencion']),
                    json.dumps(registro['funcionario_obtiene']),
                    json.dumps(registro['descripcion_evidencia']),
                    json.dumps(registro['transferencia'])
                ))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Error guardando en DB: {e}")
        
        return jsonify({
            'success': True,
            'mensaje': 'Registro creado exitosamente',
            'registro_id': registro_id,
            'registro': registro
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al crear registro: {str(e)}'
        }), 500

@app.route('/api/registro/<registro_id>', methods=['GET'])
def obtener_registro(registro_id):
    """Obtener un registro específico"""
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM registros WHERE id = ?', (registro_id,))
            row = cur.fetchone()
            
            if row:
                registro = dict(row)
                # Convertir strings JSON a objetos
                registro['datos_generales'] = json.loads(registro['datos_generales'])
                registro['formas_obtencion'] = json.loads(registro['formas_obtencion'])
                registro['funcionario_obtiene'] = json.loads(registro['funcionario_obtiene'])
                registro['descripcion_evidencia'] = json.loads(registro['descripcion_evidencia'])
                registro['transferencia'] = json.loads(registro['transferencia'])
                
                cur.close()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'registro': registro
                })
        except Exception as e:
            print(f"Error obteniendo registro: {e}")
    
    return jsonify({
        'success': False,
        'mensaje': 'Registro no encontrado'
    }), 404

@app.route('/api/registros', methods=['GET'])
def listar_registros():
    """Listar todos los registros"""
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM registros ORDER BY fecha_creacion DESC')
            rows = cur.fetchall()
            
            registros_list = []
            for row in rows:
                reg_dict = dict(row)
                reg_dict['datos_generales'] = json.loads(reg_dict['datos_generales'])
                reg_dict['formas_obtencion'] = json.loads(reg_dict['formas_obtencion'])
                reg_dict['funcionario_obtiene'] = json.loads(reg_dict['funcionario_obtiene'])
                reg_dict['descripcion_evidencia'] = json.loads(reg_dict['descripcion_evidencia'])
                reg_dict['transferencia'] = json.loads(reg_dict['transferencia'])
                registros_list.append(reg_dict)
            
            cur.close()
            conn.close()
            
            return jsonify({
                'success': True,
                'registros': registros_list,
                'total': len(registros_list)
            })
        except Exception as e:
            print(f"Error listando registros: {e}")
    
    return jsonify({
        'success': True,
        'registros': [],
        'total': 0
    })

@app.route('/api/exportar/<registro_id>', methods=['GET'])
def exportar_registro(registro_id):
    """Exportar registro como JSON"""
    from io import BytesIO
    
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM registros WHERE id = ?', (registro_id,))
            row = cur.fetchone()
            
            if row:
                output_data = dict(row)
                output_data['datos_generales'] = json.loads(output_data['datos_generales'])
                output_data['formas_obtencion'] = json.loads(output_data['formas_obtencion'])
                output_data['funcionario_obtiene'] = json.loads(output_data['funcionario_obtiene'])
                output_data['descripcion_evidencia'] = json.loads(output_data['descripcion_evidencia'])
                output_data['transferencia'] = json.loads(output_data['transferencia'])
                
                cur.close()
                conn.close()
                
                output = BytesIO()
                output.write(json.dumps(output_data, indent=2, ensure_ascii=False).encode('utf-8'))
                output.seek(0)
                
                return send_file(
                    output,
                    mimetype='application/json',
                    as_attachment=True,
                    download_name=f'{registro_id}.json'
                )
        except Exception as e:
            print(f"Error exportando registro: {e}")
    
    return jsonify({
        'success': False,
        'mensaje': 'Registro no encontrado'
    }), 404

@app.route('/api/imprimir')
def imprimir():
    """Vista optimizada para impresión"""
    return render_template('print.html')

@app.route('/api/health')
def health_check():
    """Endpoint para verificar el estado de la aplicación y DB"""
    db_status = "connected" if get_db_connection() else "disconnected"
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'version': '2.0.0-ubuntu',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("=" * 60)
    print("🔬 PRCC Digital - Laboratorio Informático Forense")
    print("=" * 60)
    print("📋 Sistema de Registro de Cadena de Custodia")
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("💾 Base de datos: SQLite (local)")
    print("🐧 Versión para Ubuntu 26.04+")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
