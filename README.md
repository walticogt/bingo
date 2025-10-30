# 🎲 Generador de Cartones de Bingo en PDF

Generador profesional de cartones de bingo completamente configurables en formato PDF. Perfecto para eventos, fiestas, y actividades recreativas.

## ✨ Características

- 📄 **Generación de PDFs**: Crea cartones de bingo en formato A4 horizontal
- 🎨 **Diseño colorido**: Encabezados con colores vibrantes (BINGO)
- ⚙️ **Altamente configurable**: Control total sobre páginas, cartones y distribución
- 📊 **Exportación de datos**: Guarda los números generados en formato JSON
- 🔢 **Números aleatorios**: Generación única por cada cartón
- 📝 **Texto personalizable**: Cambia el texto del centro (FREE, GRATIS, OH, etc.)
- 🧪 **Bien testeado**: Suite completa de tests unitarios e integración
- 📖 **Documentación completa**: Código completamente documentado con docstrings

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/bingo.git
cd bingo
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📖 Uso

### Uso básico

Genera 1 página con 6 cartones (configuración por defecto):

```bash
python src/bingo_generator.py
```

### Especificar nombre de archivo

```bash
python src/bingo_generator.py -o mi_bingo.pdf
```

### Generar múltiples páginas

Genera 5 páginas (30 cartones total):

```bash
python src/bingo_generator.py -p 5
```

### Personalizar distribución

4 cartones por página en formato 2×2:

```bash
python src/bingo_generator.py -c 4 -r 2 -l 2
```

### Cambiar texto del centro

Usar "GRATIS" en lugar de "FREE":

```bash
python src/bingo_generator.py -f "GRATIS"
```

### Exportar números a JSON

Genera el PDF y un archivo JSON con todos los números:

```bash
python src/bingo_generator.py -e
```

### Ejemplo completo

10 páginas en carpeta personalizada con exportación:

```bash
python src/bingo_generator.py -p 10 -o output/mi_evento.pdf -f "OH" -e
```

## 🎮 Opciones de línea de comandos

| Opción | Forma larga | Descripción | Por defecto |
|--------|------------|-------------|-------------|
| `-o` | `--output` | Archivo PDF de salida | `output/cartones_bingo_TIMESTAMP.pdf` |
| `-p` | `--pages` | Número de páginas | `1` |
| `-c` | `--cards-per-page` | Cartones por página | `6` |
| `-r` | `--cards-per-row` | Cartones por fila | `3` |
| `-l` | `--cards-per-column` | Cartones por columna | `2` |
| `-f` | `--free-text` | Texto de celda central | `FREE` |
| `-e` | `--export-numbers` | Exportar números a JSON | `False` |

### Ver ayuda completa

```bash
python src/bingo_generator.py --help
```

## 📁 Estructura del Proyecto

```
bingo/
├── src/
│   └── bingo_generator.py      # Código principal del generador
├── tests/
│   └── test_bingo_generator.py # Suite de tests
├── output/                      # Directorio para PDFs generados
│   └── .gitkeep
├── venv/                        # Entorno virtual (no en git)
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
├── .gitignore                   # Archivos ignorados por git
└── bingo_pdf2.py               # Versión legacy (deprecated)
```

## 🎯 Especificaciones de Cartones

### Rangos de números por columna

| Columna | Rango | Cantidad |
|---------|-------|----------|
| B | 1-15 | 5 números |
| I | 16-30 | 5 números |
| N | 31-45 | 5 números (centro = texto) |
| G | 46-60 | 5 números |
| O | 61-75 | 5 números |

### Diseño

- **Formato**: A4 horizontal (landscape)
- **Distribución por defecto**: 3×2 (6 cartones por página)
- **Colores del encabezado**:
  - B: Rojo
  - I: Naranja
  - N: Dorado
  - G: Verde
  - O: Azul
- **Celda central**: Texto personalizable (por defecto "FREE") en naranja

## 🧪 Ejecutar Tests

### Todos los tests

```bash
python -m pytest tests/ -v
```

### Tests específicos

```bash
# Solo tests de generación de números
python -m pytest tests/test_bingo_generator.py::TestBingoNumberGeneration -v

# Solo tests de PDF
python -m pytest tests/test_bingo_generator.py::TestPDFGeneration -v
```

### Con cobertura

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 📊 Formato del archivo JSON exportado

Cuando usas la opción `-e`, se genera un archivo JSON con la siguiente estructura:

```json
{
  "generated_at": "2025-10-30T10:30:45.123456",
  "total_cards": 6,
  "total_pages": 1,
  "free_text": "FREE",
  "cards": [
    {
      "card_number": 1,
      "page": 1,
      "numbers": {
        "B": [3, 12, 5, 14, 1],
        "I": [18, 25, 20, 16, 29],
        "N": [35, 42, "FREE", 31, 44],
        "G": [50, 58, 46, 55, 60],
        "O": [65, 72, 61, 70, 75]
      }
    }
    // ... más cartones
  ]
}
```

## 🎲 Generador de Números para Jugar

Para generar números aleatorios durante el juego, utiliza:

**[Bingo Caller - BingoMaker](https://app.bingomaker.com/free/caller)**

Esta herramienta online genera números aleatorios de forma visual y audible para dirigir tu juego de bingo.

## 🛠️ Desarrollo

### Configurar entorno de desarrollo

```bash
# Clonar repositorio
git clone https://github.com/usuario/bingo.git
cd bingo

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install pytest pytest-cov black flake8
```

### Ejecutar linter

```bash
flake8 src/ tests/
```

### Formatear código

```bash
black src/ tests/
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Evento pequeño

6 cartones para una reunión familiar:

```bash
python src/bingo_generator.py -o output/familia.pdf -f "GRATIS"
```

### Ejemplo 2: Evento grande

100 cartones (17 páginas aprox) con registro:

```bash
python src/bingo_generator.py -p 17 -o output/evento_grande.pdf -e
```

### Ejemplo 3: Formato compacto

9 cartones por página (3×3):

```bash
python src/bingo_generator.py -c 9 -r 3 -l 3 -o output/compacto.pdf
```

### Ejemplo 4: Formato espaciado

2 cartones por página (2×1):

```bash
python src/bingo_generator.py -c 2 -r 2 -l 1 -o output/espaciado.pdf
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'reportlab'"

Asegúrate de haber instalado las dependencias:

```bash
pip install -r requirements.txt
```

### Error: "Permission denied" al guardar PDF

Verifica que tienes permisos de escritura en el directorio de salida:

```bash
mkdir -p output
chmod 755 output
```

### Los números no son únicos entre cartones

Esto es normal. Cada cartón genera sus propios números aleatorios. Si necesitas garantizar que no haya cartones duplicados, considera implementar una validación adicional.

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de contribución

- Sigue PEP 8 para el estilo de código
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Usa mensajes de commit descriptivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- **Tu Nombre** - *Trabajo inicial* - [usuario](https://github.com/usuario)

## 🙏 Agradecimientos

- ReportLab por la excelente biblioteca de generación de PDFs
- Comunidad Python por las herramientas y documentación
- BingoMaker por su generador de números online

## 📞 Contacto

- GitHub: [@usuario](https://github.com/usuario)
- Email: tu-email@ejemplo.com

## 🔄 Changelog

### v2.0.0 (2025-10-30)

- ✨ Refactorización completa del código
- ✨ Agregado sistema de argumentos CLI
- ✨ Exportación a JSON
- ✨ Múltiples páginas
- ✨ Diseño completamente configurable
- 🧪 Suite completa de tests
- 📖 Documentación mejorada
- 🎨 Código limpio y bien organizado

### v1.0.0 (2025-10-29)

- 🎉 Versión inicial
- Generación básica de cartones 3×2

## 🗺️ Roadmap

- [ ] Interfaz gráfica (GUI)
- [ ] Temas de colores personalizables
- [ ] Generación de cartones con imágenes
- [ ] Soporte para diferentes idiomas
- [ ] Exportación a otros formatos (PNG, SVG)
- [ ] Validación de cartones únicos
- [ ] API REST
- [ ] Aplicación web

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
