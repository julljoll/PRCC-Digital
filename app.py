"""
PRCC Digital - Planilla de Registro de Cadena de Custodia
Aplicación web en Python con Flask para gestión de evidencia forense
Optimizado para Vercel y Neon Database
"""

from flask import Flask, render_template, request, jsonify, send_file, make_response
from datetime import datetime
import json
import os
from io import BytesIO
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sha256-forensic-lab-secret-key-2024')

# Configuración de base de datos Neon
def get_db_connection():
    """Obtener conexión a la base de datos Neon PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        return None
    
    try:
        conn = psycopg2.connect(database_url)
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
                id VARCHAR(50) PRIMARY KEY,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                datos_generales JSONB,
                formas_obtencion JSONB,
                funcionario_obtiene JSONB,
                descripcion_evidencia JSONB,
                transferencia JSONB
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
if os.getenv('VERCEL'):
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
        
        # Guardar en Neon Database
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO registros 
                    (id, datos_generales, formas_obtencion, funcionario_obtiene, descripcion_evidencia, transferencia)
                    VALUES (%s, %s, %s, %s, %s, %s)
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
                # Fallback a memoria si falla DB
        
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
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM registros WHERE id = %s', (registro_id,))
            registro = cur.fetchone()
            cur.close()
            conn.close()
            
            if registro:
                # Convertir tipos JSONB
                registro['datos_generales'] = json.loads(registro['datos_generales']) if isinstance(registro['datos_generales'], str) else registro['datos_generales']
                registro['formas_obtencion'] = json.loads(registro['formas_obtencion']) if isinstance(registro['formas_obtencion'], str) else registro['formas_obtencion']
                registro['funcionario_obtiene'] = json.loads(registro['funcionario_obtiene']) if isinstance(registro['funcionario_obtiene'], str) else registro['funcionario_obtiene']
                registro['descripcion_evidencia'] = json.loads(registro['descripcion_evidencia']) if isinstance(registro['descripcion_evidencia'], str) else registro['descripcion_evidencia']
                registro['transferencia'] = json.loads(registro['transferencia']) if isinstance(registro['transferencia'], str) else registro['transferencia']
                
                return jsonify({
                    'success': True,
                    'registro': dict(registro)
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
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM registros ORDER BY fecha_creacion DESC')
            registros = cur.fetchall()
            cur.close()
            conn.close()
            
            # Convertir tipos JSONB
            registros_list = []
            for reg in registros:
                reg_dict = dict(reg)
                reg_dict['datos_generales'] = json.loads(reg_dict['datos_generales']) if isinstance(reg_dict['datos_generales'], str) else reg_dict['datos_generales']
                reg_dict['formas_obtencion'] = json.loads(reg_dict['formas_obtencion']) if isinstance(reg_dict['formas_obtencion'], str) else reg_dict['formas_obtencion']
                reg_dict['funcionario_obtiene'] = json.loads(reg_dict['funcionario_obtiene']) if isinstance(reg_dict['funcionario_obtiene'], str) else reg_dict['funcionario_obtiene']
                reg_dict['descripcion_evidencia'] = json.loads(reg_dict['descripcion_evidencia']) if isinstance(reg_dict['descripcion_evidencia'], str) else reg_dict['descripcion_evidencia']
                reg_dict['transferencia'] = json.loads(reg_dict['transferencia']) if isinstance(reg_dict['transferencia'], str) else reg_dict['transferencia']
                registros_list.append(reg_dict)
            
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
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT * FROM registros WHERE id = %s', (registro_id,))
            registro = cur.fetchone()
            cur.close()
            conn.close()
            
            if registro:
                # Convertir tipos JSONB
                output_data = dict(registro)
                output_data['datos_generales'] = json.loads(output_data['datos_generales']) if isinstance(output_data['datos_generales'], str) else output_data['datos_generales']
                output_data['formas_obtencion'] = json.loads(output_data['formas_obtencion']) if isinstance(output_data['formas_obtencion'], str) else output_data['formas_obtencion']
                output_data['funcionario_obtiene'] = json.loads(output_data['funcionario_obtiene']) if isinstance(output_data['funcionario_obtiene'], str) else output_data['funcionario_obtiene']
                output_data['descripcion_evidencia'] = json.loads(output_data['descripcion_evidencia']) if isinstance(output_data['descripcion_evidencia'], str) else output_data['descripcion_evidencia']
                output_data['transferencia'] = json.loads(output_data['transferencia']) if isinstance(output_data['transferencia'], str) else output_data['transferencia']
                
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
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })

# Handler para Vercel
def handler(request):
    """Handler para Vercel Serverless Functions"""
    from vercel_flask import serve_wsgi_app
    return serve_wsgi_app(app, request.environ)

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Inicializar DB en modo local
    if not os.getenv('VERCEL'):
        init_db()
    
    print("=" * 60)
    print("🔬 PRCC Digital - Laboratorio Informático Forense")
    print("=" * 60)
    print("📋 Sistema de Registro de Cadena de Custodia")
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("💾 Base de datos: Neon PostgreSQL")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
