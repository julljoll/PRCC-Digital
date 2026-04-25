# Iconos para PWA

Para que la aplicación sea instalable como PWA, necesitas generar los iconos en las siguientes rutas:

## Rutas requeridas:
- `/workspace/static/icons/icon-192.png` (192x192 píxeles)
- `/workspace/static/icons/icon-512.png` (512x512 píxeles)

## Cómo generar los iconos:

### Opción 1: Usando Python con PIL/Pillow
```bash
pip install Pillow
```

```python
from PIL import Image, ImageDraw, ImageFont

# Crear icono estilo Windows 95
def create_win95_icon(size, filename):
    img = Image.new('RGB', (size, size), color='#008080')
    draw = ImageDraw.Draw(img)
    
    # Borde blanco estilo Windows 95
    margin = size // 10
    draw.rectangle([margin, margin, size-margin, size-margin], fill='#C0C0C0', outline='white', width=max(2, size//50))
    
    # Texto PRCC
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size//3)
    except:
        font = ImageFont.load_default()
    
    text = "PRCC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='#000080', font=font)
    
    img.save(filename)
    print(f"Icono creado: {filename}")

create_win95_icon(192, 'static/icons/icon-192.png')
create_win95_icon(512, 'static/icons/icon-512.png')
```

### Opción 2: Usando herramientas online
1. Visita https://realfavicongenerator.net/
2. Sube una imagen base (puede ser un screenshot de la app)
3. Descarga los iconos generados
4. Colócalos en `/workspace/static/icons/`

### Opción 3: Usando Canva o similar
1. Crea un diseño de 512x512 con el logo de tu aplicación
2. Exporta como PNG
3. Redimensiona a 192x192 para el segundo icono
4. Guarda en la carpeta `static/icons/`

## Verificación

Una vez creados los iconos, verifica que existan:
```bash
ls -la static/icons/
```

Deberías ver:
```
icon-192.png
icon-512.png
```

## Notas importantes:
- Los iconos deben ser PNG con fondo transparente o sólido
- El tamaño exacto es importante para la instalación en dispositivos móviles
- Para iOS, también se usa el icon-192.png como apple-touch-icon
- Los iconos deben ser visibles y reconocibles incluso en tamaños pequeños
