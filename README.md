# Sistema Forense Android - Panel de Control

Aplicación de escritorio en Python/PyQt6 para gestionar el proceso forense informático de dispositivos Android según el marco legal venezolano.

## 📋 Descripción

Este sistema permite gestionar las **3 fases del procedimiento forense** de dispositivos Android:

- **FASE I**: Obtención y Adquisición en Sitio
- **FASE II**: Peritaje y Análisis en Laboratorio  
- **FASE III**: Emisión del Dictamen Pericial

## 🔧 Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| GUI | PyQt6 |
| Base de Datos | SQLite |
| PDF/Impresión | reportlab |
| Hash | hashlib (SHA-256/MD5) |
| Herramientas externas | subprocess/QProcess (Andriller, ALEAPP) |
| Empaquetado | dpkg-deb (.deb para Ubuntu) |

## 📦 Instalación

### Desde código fuente

```bash
cd /workspace
pip install -r requirements.txt
python main.py
```

### Desde paquete .deb (Ubuntu 24.04+)

```bash
./packaging/build_deb.sh
sudo apt install ./dist/forense-android_1.0.0_amd64.deb
```

## 🚀 Uso

1. Iniciar la aplicación: `python main.py`
2. Crear nuevo caso haciendo clic en "📁 Nuevo Caso"
3. Seguir los 9 pasos del proceso forense en orden secuencial

## 📁 Estructura del Proyecto

```
forense-android/
├── main.py                    # Punto de entrada
├── database/                  # Base de datos SQLite
├── models/                    # Modelos de datos
├── services/                  # Servicios (hash, audit, print)
├── ui/                        # Interfaz de usuario PyQt6
├── assets/                    # Recursos y estilos
└── packaging/                 # Empaquetado .deb
```

## ⚖️ Marco Legal Venezolano

El sistema sigue protocolos de:
- Ley sobre Mensajes de Datos y Firmas Electrónicas
- Código Orgánico Procesal Penal (COPP)
- Ley Especial contra Delitos Informáticos
- ISO/IEC 27037:2012, ISO/IEC 27042:2015
- NIST SP 800-101r1

## 🛠️ Requisitos

- Python 3.11+
- PyQt6 >= 6.6.0
- reportlab >= 4.0.0
- Pillow >= 10.0.0
- Ubuntu 24.04+ (recomendado)

---
**Versión**: 1.0.0 | **Laboratorio Forense** | 2024
