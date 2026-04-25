# PRCC Digital - Versión 2.0 (Ubuntu .deb)

**Planilla de Registro de Cadena de Custodia** - Aplicación de escritorio para Ubuntu, con interfaz Windows 95 y base de datos local SQLite.

## 🔬 Descripción

Sistema digital para el registro y seguimiento de la cadena de custodia de evidencias forenses, desarrollado en Python con Flask. Esta versión está diseñada para distribuirse como paquete `.deb` para Ubuntu 26.04+, funcionando completamente offline sin dependencias de servicios en la nube.

## 🚀 Características

- **Aplicación de Escritorio Nativa**: Diseñada para Ubuntu 26.04+ como paquete `.deb`
- **Interfaz Retro Windows 95**: Diseño nostálgico con ventanas clásicas, botones 3D y fondo teal
- **Base de Datos Local SQLite**: No requiere conexión a internet ni servicios externos
- **Funcionamiento Offline Completo**: Todos los datos se almacenan localmente
- **Formulario Completo**: Todas las secciones del PRCC oficial
- **Exportación JSON**: Descarga de registros en formato JSON
- **Optimizado para Impresión**: Vista específica para imprimir documentos legales
- **Fácil Instalación**: Paquete `.deb` listo para instalar con `dpkg` o `apt`

## 📋 Requisitos

- Ubuntu 26.04 LTS o superior (también compatible con 24.04, 22.04)
- Python 3.11+
- Permisos de administrador para instalación (sudo)

## 🛠️ Instalación desde Paquete .deb

### Método 1: Usando dpkg

```bash
# Descargar el paquete .deb
wget https://github.com/tu-usuario/prcc-digital/releases/download/v2.0.0/prcc-digital_2.0.0_amd64.deb

# Instalar el paquete
sudo dpkg -i prcc-digital_2.0.0_amd64.deb

# Si hay dependencias faltantes
sudo apt-get install -f
```

### Método 2: Usando apt

```bash
# Instalar directamente (maneja dependencias automáticamente)
sudo apt install ./prcc-digital_2.0.0_amd64.deb
```

### Método 3: Compilar desde código fuente

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd prcc-digital

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

## 🎯 Uso de la Aplicación

### Iniciar la aplicación

Una vez instalada, puedes iniciar PRCC Digital de varias formas:

**Desde la terminal:**
```bash
prcc-digital
```

**Desde el menú de aplicaciones:**
1. Abre el menú de aplicaciones de Ubuntu
2. Busca "PRCC Digital"
3. Haz clic en el ícono

**Acceso directo:**
La aplicación estará disponible en:
- Menú de aplicaciones → Categoría: Oficina/Utilidades
- Lanzador de Ubuntu (Dash)

### Primer uso

1. Al iniciar, la aplicación creará automáticamente la base de datos local en `~/.local/share/prcc-digital/prcc.db`
2. La interfaz se abrirá en tu navegador predeterminado en `http://localhost:5000`
3. ¡Listo! Puedes comenzar a crear registros

## 📁 Ubicación de Datos

Los datos se almacenan localmente en:

- **Base de datos**: `~/.local/share/prcc-digital/prcc.db`
- **Configuración**: `~/.config/prcc-digital/config.json`
- **Registros exportados**: `~/Documentos/PRCC-Exports/`

## 🗄️ Estructura de la Base de Datos

La aplicación crea automáticamente una base de datos SQLite local:

```sql
CREATE TABLE IF NOT EXISTS registros (
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
| GET | `/api/health` | Verificar estado de la app |
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

## 📦 Crear Paquete .deb

Para desarrolladores que quieran compilar su propio paquete:

```bash
# Estructura requerida
prcc-digital/
├── debian/
│   ├── control
│   ├── rules
│   ├── compat
│   └── prcc-digital.desktop
├── usr/
│   ├── bin/
│   │   └── prcc-digital
│   └── share/
│       ├── prcc-digital/
│       │   ├── app.py
│       │   ├── templates/
│       │   └── static/
│       └── applications/
│           └── prcc-digital.desktop
└── README.md

# Compilar el paquete
dpkg-deb --build prcc-digital
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

## 🔒 Seguridad y Privacidad

- **Datos 100% Locales**: Toda la información se almacena en tu computadora
- **Sin Conexión Requerida**: No envía datos a servidores externos
- **Control Total**: Tú eres el único dueño de tus datos
- **Copia de Seguridad**: Recomendamos hacer backups periódicos de `~/.local/share/prcc-digital/`

### Realizar Copia de Seguridad

```bash
# Crear backup de la base de datos
cp ~/.local/share/prcc-digital/prcc.db ~/Documentos/prcc-backup-$(date +%Y%m%d).db

# O comprimir todo el directorio
tar -czvf prcc-backup-$(date +%Y%m%d).tar.gz ~/.local/share/prcc-digital/
```

## 🎨 Personalización

### Cambiar el tema
Edita `static/css/styles.css` para modificar colores y estilos.

### Modificar el formulario
Edita `templates/index.html` para agregar o quitar campos.

### Extender la API
Agrega nuevos endpoints en `app.py`.

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Verificar si el puerto está en uso
sudo lsof -i :5000

# Reinstalar la aplicación
sudo apt reinstall prcc-digital
```

### Error en la base de datos
```bash
# Eliminar base de datos corrupta y reiniciar
rm ~/.local/share/prcc-digital/prcc.db
prcc-digital
```

### Desinstalar completamente
```bash
sudo apt remove prcc-digital
sudo rm -rf ~/.local/share/prcc-digital
sudo rm -rf ~/.config/prcc-digital
```

## 🛠️ Tecnologías

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Estilos**: CSS personalizado Windows 95
- **Base de Datos**: SQLite (local, sin servidor)
- **Empaquetado**: Debian package (.deb)
- **PWA**: Service Worker + Web App Manifest
- **Iconos**: PNG optimizados para escritorio Linux

## 📝 Notas Importantes

- La planilla debe permanecer siempre con la evidencia
- Solo el original es válido desde el llenado hasta la disposición final
- Optimizado para impresión en papel tamaño legal
- Interfaz Windows 95 para nostalgia y usabilidad retro
- **No requiere conexión a internet para funcionar**

## 📋 Licencia

Este software está licenciado bajo la **Licencia de Construcción Comunitaria - No Comercial**.

✅ **PUEDES**:
- Usar libremente para trabajo, estudios e investigación
- Modificar el código para uso personal
- Distribuir copias gratuitas
- Empaquetar y redistribuir en formatos .deb

❌ **NO PUEDES**:
- Vender este software o sus derivados
- Cobrar por licencias de uso
- Incluir en productos comerciales sin autorización

Ver archivo `LICENSE` para detalles completos.

## 🔗 Enlaces Útiles

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Ubuntu Packaging Guide](https://packaging.ubuntu.com/html/)
- [Debian Developer's Reference](https://www.debian.org/doc/manuals/developers-reference/)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Envía un Pull Request

## 📞 Soporte

Para reportar errores o solicitar características:
- GitHub Issues: [tu-repositorio]/issues
- Email: soporte@sha256.us

---

**Desarrollado con ❤️ para Ubuntu y la comunidad forense**

**sha256.us** - Laboratorio Informático Forense

*Versión 2.0 - Paquete nativo para Ubuntu 26.04+*
