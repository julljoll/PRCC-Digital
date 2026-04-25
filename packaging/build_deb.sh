#!/bin/bash
# Script de construcción del paquete .deb para forense-android
# Requiere: dpkg-deb, pip3

set -e

PKG_NAME="forense-android"
VERSION="1.0.0"
ARCH="amd64"
DEST="dist/${PKG_NAME}_${VERSION}_${ARCH}"
APP_DIR="/usr/share/${PKG_NAME}"

echo "🔨 Construyendo paquete ${PKG_NAME} v${VERSION}..."

# Limpiar directorio de destino
rm -rf dist
mkdir -p "$DEST/DEBIAN"
mkdir -p "$DEST$APP_DIR"
mkdir -p "$DEST/usr/bin"
mkdir -p "$DEST/usr/share/applications"

# Copiar archivos de la aplicación
echo "📦 Copiando archivos de la aplicación..."
cp -r database "$DEST$APP_DIR/"
cp -r ui "$DEST$APP_DIR/"
cp -r services "$DEST$APP_DIR/"
cp -r models "$DEST$APP_DIR/"
cp -r assets "$DEST$APP_DIR/"
cp main.py "$DEST$APP_DIR/"
cp requirements.txt "$DEST$APP_DIR/"

# Instalar dependencias Python en el paquete
echo "📥 Instalando dependencias Python..."
pip3 install --target="$DEST$APP_DIR/vendor" \
    PyQt6>=6.6.0 \
    reportlab>=4.0.0 \
    Pillow>=10.0.0 \
    --quiet

# Crear script ejecutable wrapper
echo "🔧 Creando ejecutable..."
cat > "$DEST/usr/bin/forense-android" << 'EOF'
#!/bin/bash
cd /usr/share/forense-android
export PYTHONPATH=/usr/share/forense-android/vendor:$PYTHONPATH
python3 main.py "$@"
EOF
chmod +x "$DEST/usr/bin/forense-android"

# Crear entrada .desktop para el menú de aplicaciones
echo "🖥️  Creando entrada de menú..."
cat > "$DEST/usr/share/applications/forense-android.desktop" << 'EOF'
[Desktop Entry]
Name=Sistema Forense Android
Comment=Gestión del procedimiento forense informático de dispositivos Android
Exec=forense-android
Icon=/usr/share/forense-android/assets/logo.png
Terminal=false
Type=Application
Categories=Science;Utility;Legal;
Keywords=forense;android;custodia;evidencia;pericial;
EOF

# Copiar archivos DEBIAN (control, postinst, prerm)
echo "📋 Copiando metadatos del paquete..."
cp packaging/DEBIAN/control "$DEST/DEBIAN/"
cp packaging/DEBIAN/postinst "$DEST/DEBIAN/"
cp packaging/DEBIAN/prerm "$DEST/DEBIAN/"
chmod 755 "$DEST/DEBIAN/postinst" "$DEST/DEBIAN/prerm"

# Construir el paquete .deb
echo "🏗️  Construyendo paquete .deb..."
dpkg-deb --build --root-owner-group "$DEST"

# Verificar el paquete construido
if [ -f "${DEST}.deb" ]; then
    echo ""
    echo "✅ Paquete generado exitosamente: ${DEST}.deb"
    echo ""
    echo "Para instalar:"
    echo "  sudo apt install ./dist/${PKG_NAME}_${VERSION}_${ARCH}.deb"
    echo ""
    echo "Para verificar contenido:"
    echo "  dpkg -c dist/${PKG_NAME}_${VERSION}_${ARCH}.deb"
else
    echo "❌ Error: No se generó el paquete .deb"
    exit 1
fi
