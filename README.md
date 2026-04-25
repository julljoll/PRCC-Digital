# PRCC Digital - Versión 2.0

**Planilla de Registro de Cadena de Custodia** - Aplicación web con interfaz Windows 95, optimizada para Vercel y Neon Database.

## 🔬 Descripción

Sistema digital para el registro y seguimiento de la cadena de custodia de evidencias forenses, desarrollado en Python con Flask, con diseño retro de Windows 95 y base de datos PostgreSQL serverless.

## 🚀 Características

- **Interfaz Retro Windows 95**: Diseño nostálgico con ventanas clásicas, botones 3D y fondo teal
- **PWA (Progressive Web App)**: Instalable en móviles y escritorio, funciona offline
  - Service Worker con estrategia Cache First
  - Manifiesto PWA configurado
  - Iconos generados automáticamente (192x192 y 512x512)
  - Soporte para iOS y Android
- **Backend Python/Flask**: API RESTful robusta y escalable
- **Base de Datos Neon**: PostgreSQL serverless con conexión SSL
- **Despliegue en Vercel**: Configuración lista para production
- **Formulario Completo**: Todas las secciones del PRCC oficial
- **Exportación JSON**: Descarga de registros en formato JSON
- **Optimizado para Impresión**: Vista específica para imprimir documentos legales

## 📋 Requisitos

- Python 3.11+
- Cuenta en [Neon](https://neon.tech) para base de datos
- Cuenta en [Vercel](https://vercel.com) para despliegue (opcional para local)

## 🛠️ Instalación Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd prcc-digital
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
SECRET_KEY=tu-clave-secreta-muy-segura-2024
DATABASE_URL=postgresql://usuario:password@ep-xxx.region.aws.neon.tech/prcc_db?sslmode=require
DEBUG=True
```

### 5. Obtener DATABASE_URL de Neon
1. Ve a [console.neon.tech](https://console.neon.tech)
2. Crea un nuevo proyecto
3. Copia la cadena de conexión (Connection String)
4. Pégala en `DATABASE_URL` en tu archivo `.env`

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## 🌐 Despliegue en Vercel

### Pre-requisitos importantes

⚠️ **Nota sobre el archivo `builds`**: Si usas la configuración con `builds` en `vercel.json`, algunas configuraciones automáticas de Vercel no se aplicarán. Esta configuración es necesaria para usar `vercel-flask`.

### Opción 1: Desde la CLI de Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel
```

Durante el despliegue, Vercel te preguntará por las variables de entorno. Asegúrate de configurar:
- `SECRET_KEY`
- `DATABASE_URL`

### Opción 2: Desde GitHub

1. Sube tu código a GitHub
2. Ve a [vercel.com/new](https://vercel.com/new)
3. Importa tu repositorio
4. **Configura las variables de entorno ANTES de desplegar**:
   - `SECRET_KEY`: Tu clave secreta (genera una única, ej: `openssl rand -hex 32`)
   - `DATABASE_URL`: Tu conexión a Neon (ej: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/db?sslmode=require`)
5. Haz clic en "Deploy"

### Configurar Variables de Entorno en Vercel

En el dashboard de Vercel:
1. Ve a tu proyecto
2. Settings → Environment Variables
3. Agrega las siguientes variables para **Production**, **Preview**, y **Development**:
   - `SECRET_KEY` (requerido)
   - `DATABASE_URL` (requerido)
4. Guarda los cambios

### Verificar el despliegue

Después del despliegue:
1. Revisa los logs: `vercel --logs`
2. Verifica el health check: `https://tu-app.vercel.app/api/health`
3. Confirma que la base de datos esté conectada

### Solución de problemas comunes

**Error: `vercel-wsgi-adapter no se encontró`**
- ✅ Solucionado: Ahora usamos `vercel-flask==0.0.4`

**Error de conexión a la base de datos**
- Verifica que `DATABASE_URL` incluya `?sslmode=require`
- Confirma que tu IP esté permitida en Neon (para local)
- En Vercel, las IPs son automáticas

**Build falla en Vercel**
- Revisa que `.python-version` esté presente (usamos Python 3.11)
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs con `vercel --logs`

## 🗄️ Estructura de la Base de Datos

La aplicación crea automáticamente la siguiente tabla en Neon:

```sql
CREATE TABLE registros (
    id VARCHAR(50) PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datos_generales JSONB,
    formas_obtencion JSONB,
    funcionario_obtiene JSONB,
    descripcion_evidencia JSONB,
    transferencia JSONB
);
```

## 📡 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| POST | `/api/registro` | Crear nuevo registro |
| GET | `/api/registro/<id>` | Obtener registro específico |
| GET | `/api/registros` | Listar todos los registros |
| GET | `/api/exportar/<id>` | Exportar registro como JSON |
| GET | `/api/health` | Verificar estado de la app y DB |
| GET | `/api/imprimir` | Vista para impresión |

## 🧪 Pruebas Locales

### Verificar salud de la aplicación
```bash
curl http://localhost:5000/api/health
```

### Crear un registro de prueba
```bash
curl -X POST http://localhost:5000/api/registro \
  -H "Content-Type: application/json" \
  -d '{
    "datos_generales": {
      "numero_expediente": "EXP-2024-001",
      "numero_prcc": "PRCC-001"
    }
  }'
```

## 📁 Estructura del Proyecto

```
prcc-digital/
├── app.py                 # Backend Flask + integración Neon
├── requirements.txt       # Dependencias Python
├── vercel.json           # Configuración para Vercel
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados por Git
├── README.md             # Este archivo
├── templates/
│   └── index.html        # Frontend HTML con estilo Windows 95
└── static/
    ├── css/
    │   └── styles.css    # Estilos Windows 95
    └── js/
        └── app.js        # Lógica frontend
```

## 📋 Funcionalidades del Formulario

### Sección I - Datos Generales
- Número de Expediente
- Número PRCC
- Despacho que instruye
- Organismo que investiga
- Despacho que inicia custodia
- Organismo que custodia
- Dirección de obtención
- Fecha y hora automática

### Sección II - Formas de Obtención
- ✅ Técnica
- ✅ Aseguramiento
- ✅ Consignación
- ✅ Derivación

### Sección III - Funcionario que Obtiene
Para cada rol (Protección, Observación Preliminar, Fijación, Colección):
- Nombres y apellidos
- Cédula de identidad
- Espacios para firma y huellas

### Sección VI - Descripción de la Evidencia
- 7 campos para descripción detallada
- Referencia a Anexo A

### Sección V - Transferencia de Evidencia
Motivos seleccionables:
- Traslado
- Peritaje
- Resguardo
- Disposición Judicial
- Disposición Final

## 🔒 Seguridad

- **SECRET_KEY**: Cambia la clave por defecto en producción
- **DATABASE_URL**: Usa siempre conexiones SSL (`sslmode=require`)
- **.env**: Nunca subas este archivo a Git
- **CORS**: Configura CORS si necesitas acceso desde otros dominios

## 🎨 Personalización

### Cambiar el tema
Edita `static/css/styles.css` para modificar colores y estilos.

### Modificar el formulario
Edita `templates/index.html` para agregar o quitar campos.

### Extender la API
Agrega nuevos endpoints en `app.py`.

## 🐛 Solución de Problemas

### Error de conexión a la base de datos
- Verifica que `DATABASE_URL` sea correcto
- Asegúrate de que tu IP esté permitida en Neon
- Confirma que `sslmode=require` esté incluido

### Error en Vercel
- Revisa los logs en el dashboard de Vercel
- Verifica que las variables de entorno estén configuradas
- Ejecuta `vercel --logs` para ver logs en tiempo real

### La aplicación no inicia localmente
- Ejecuta `pip install -r requirements.txt` nuevamente
- Verifica que Python 3.11+ esté instalado
- Revisa que el puerto 5000 no esté en uso

## 🛠️ Tecnologías

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Estilos**: CSS personalizado Windows 95
- **Base de Datos**: Neon PostgreSQL
- **Deploy**: Vercel Serverless Functions
- **PWA**: Service Worker + Web App Manifest
- **Iconos**: Generados con Pillow (PNG)

## 📱 Instalación como PWA

### En Android (Chrome):
1. Abre la aplicación en Chrome
2. Toca el menú (⋮) y selecciona "Instalar aplicación"
3. O espera a que aparezca el banner de instalación
4. La app se instalará como una app nativa

### En iOS (Safari):
1. Abre la aplicación en Safari
2. Toca el botón Compartir (📤)
3. Selecciona "Agregar a pantalla de inicio"
4. La app aparecerá en tu pantalla de inicio

### En Escritorio (Chrome/Edge):
1. Abre la aplicación
2. Verás un ícono de instalación en la barra de direcciones
3. Haz clic en "Instalar"
4. La app se abrirá en su propia ventana

### Funcionalidades Offline:
- ✅ La interfaz carga sin conexión
- ✅ Los formularios pueden llenarse offline
- ⚠️ El guardado requiere conexión (se sincroniza al reconectar)

## 📝 Notas

- La planilla debe permanecer siempre con la evidencia
- Solo el original es válido desde el llenado hasta la disposición final
- Optimizado para impresión en papel tamaño legal
- Interfaz Windows 95 para nostalgia y usabilidad retro

## 🔐 Consideraciones de Seguridad para Producción

1. Cambiar `SECRET_KEY` en variables de entorno
2. Usar Neon Database con SSL obligatorio
3. Implementar autenticación de usuarios
4. Habilitar HTTPS (automático en Vercel)
5. Configurar logs de auditoría
6. Rotar claves periódicamente

## 🔗 Enlaces Útiles

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Neon](https://neon.tech/docs/)
- [Documentación de Vercel](https://vercel.com/docs)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

**Desarrollado con ❤️ usando Python, Flask, Neon y Vercel**

**sha256.us** - Laboratorio Informático Forense
