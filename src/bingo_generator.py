"""
Generador de Cartones de Bingo en PDF
======================================

Este módulo genera cartones de bingo personalizables en formato PDF.
Permite configurar el número de cartones, páginas, y texto central.

Autor: Proyecto Bingo
Fecha: 2025
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import random
import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

# ==================== CONSTANTES ====================

# Configuración de rangos de números para cada columna
COLUMN_RANGES = {
    "B": (1, 16),
    "I": (16, 31),
    "N": (31, 46),
    "G": (46, 61),
    "O": (61, 76)
}

# Configuración de colores para el encabezado BINGO
HEADER_COLORS = [
    colors.red,
    colors.orange,
    colors.HexColor("#FFD700"),  # Dorado
    colors.green,
    colors.blue
]

# Configuración de diseño
GRID_ROWS = 6
GRID_COLUMNS = 5
NUMBERS_PER_COLUMN = 5
CENTER_CELL_INDEX = 2

# Configuración de dimensiones de página
MARGIN_X = 30
MARGIN_Y = 50
SPACING_X = 20
SPACING_Y = 30

# Configuración de fuentes
HEADER_FONT = "Helvetica-Bold"
HEADER_FONT_SIZE = 14
NUMBER_FONT = "Helvetica"
NUMBER_FONT_SIZE = 12
FOOTER_FONT = "Helvetica"
FOOTER_FONT_SIZE = 10

# Configuración de líneas
BORDER_WIDTH = 2

# Texto por defecto para el centro
DEFAULT_FREE_TEXT = "FREE"

# Directorio de salida por defecto
DEFAULT_OUTPUT_DIR = "output"


# ==================== FUNCIONES ====================

def generate_bingo_numbers(free_text: str = DEFAULT_FREE_TEXT) -> Dict[str, List]:
    """
    Genera números aleatorios para un cartón de bingo.

    Args:
        free_text (str): Texto a colocar en la celda central (por defecto "FREE")

    Returns:
        Dict[str, List]: Diccionario con las columnas B, I, N, G, O y sus números

    Example:
        >>> numbers = generate_bingo_numbers("OH")
        >>> len(numbers["B"])
        5
        >>> numbers["N"][2]
        'OH'
    """
    columns = {}
    for letter, (start, end) in COLUMN_RANGES.items():
        columns[letter] = random.sample(range(start, end), NUMBERS_PER_COLUMN)

    # Colocar texto libre en el centro (columna N, posición 2)
    columns["N"][CENTER_CELL_INDEX] = free_text

    return columns


def create_bingo_card(c: canvas.Canvas, x: float, y: float,
                      width: float, height: float, card_number: int,
                      free_text: str = DEFAULT_FREE_TEXT) -> Dict[str, List]:
    """
    Crea un cartón individual de bingo en el PDF.

    Args:
        c (canvas.Canvas): Canvas de reportlab donde dibujar
        x (float): Posición X del cartón
        y (float): Posición Y del cartón
        width (float): Ancho del cartón
        height (float): Alto del cartón
        card_number (int): Número identificador del cartón
        free_text (str): Texto para la celda central

    Returns:
        Dict[str, List]: Los números generados para este cartón
    """
    # Dibujar el borde del cartón
    c.setStrokeColor(colors.black)
    c.setLineWidth(BORDER_WIDTH)
    c.rect(x, y, width, height, stroke=1, fill=0)

    # Calcular dimensiones de celdas
    cell_width = width / GRID_COLUMNS
    cell_height = height / GRID_ROWS

    # Dibujar encabezado (B-I-N-G-O) con colores
    c.setFont(HEADER_FONT, HEADER_FONT_SIZE)
    letters = list(COLUMN_RANGES.keys())

    for i, letter in enumerate(letters):
        # Dibujar celda de encabezado con color
        c.setFillColor(HEADER_COLORS[i])
        c.rect(x + i * cell_width, y + height - cell_height,
               cell_width, cell_height, stroke=1, fill=1)

        # Dibujar letra en blanco
        c.setFillColor(colors.white)
        c.drawCentredString(
            x + (i + 0.5) * cell_width,
            y + height - cell_height + 10,
            letter
        )

    # Generar y dibujar números del cartón
    numbers = generate_bingo_numbers(free_text)
    c.setFont(NUMBER_FONT, NUMBER_FONT_SIZE)

    for row in range(1, GRID_ROWS):
        for col, letter in enumerate(letters):
            value = numbers[letter][row - 1]

            # Dibujar celda
            c.setFillColor(colors.black)
            c.rect(
                x + col * cell_width,
                y + height - (row + 1) * cell_height,
                cell_width,
                cell_height,
                stroke=1,
                fill=0
            )

            # Dibujar número o texto libre
            if value == free_text:
                c.setFillColor(colors.orange)
            else:
                c.setFillColor(colors.black)

            c.drawCentredString(
                x + (col + 0.5) * cell_width,
                y + height - (row + 1) * cell_height + 10,
                str(value)
            )

    # Dibujar pie de cartón con número identificador
    c.setFont(FOOTER_FONT, FOOTER_FONT_SIZE)
    c.setFillColor(colors.black)
    c.drawCentredString(
        x + (width / 2),
        y - 15,
        f"Cartón #{card_number:03d}"
    )

    return numbers


def calculate_card_dimensions(page_width: float, page_height: float,
                              cards_per_row: int, cards_per_column: int) -> Tuple[float, float]:
    """
    Calcula las dimensiones óptimas para cada cartón.

    Args:
        page_width (float): Ancho de la página
        page_height (float): Alto de la página
        cards_per_row (int): Cartones por fila
        cards_per_column (int): Cartones por columna

    Returns:
        Tuple[float, float]: (ancho_cartón, alto_cartón)
    """
    card_width = (page_width - (2 * MARGIN_X) - ((cards_per_row - 1) * SPACING_X)) / cards_per_row
    card_height = (page_height - (2 * MARGIN_Y) - ((cards_per_column - 1) * SPACING_Y)) / cards_per_column

    return card_width, card_height


def calculate_card_positions(page_width: float, page_height: float,
                             cards_per_row: int, cards_per_column: int,
                             card_width: float, card_height: float) -> List[Tuple[float, float]]:
    """
    Calcula las posiciones de todos los cartones en la página.

    Args:
        page_width (float): Ancho de la página
        page_height (float): Alto de la página
        cards_per_row (int): Cartones por fila
        cards_per_column (int): Cartones por columna
        card_width (float): Ancho de cada cartón
        card_height (float): Alto de cada cartón

    Returns:
        List[Tuple[float, float]]: Lista de posiciones (x, y) para cada cartón
    """
    positions = []
    for row in range(cards_per_column):
        for col in range(cards_per_row):
            x = MARGIN_X + col * (card_width + SPACING_X)
            y = MARGIN_Y + row * (card_height + SPACING_Y)
            positions.append((x, y))

    return positions


def generate_pdf(output_file: str, num_pages: int = 1,
                cards_per_page: int = 6, free_text: str = DEFAULT_FREE_TEXT,
                cards_per_row: int = 3, cards_per_column: int = 2,
                export_numbers: bool = False) -> Dict:
    """
    Genera un PDF con cartones de bingo.

    Args:
        output_file (str): Nombre del archivo PDF de salida
        num_pages (int): Número de páginas a generar
        cards_per_page (int): Cartones por página
        free_text (str): Texto para la celda central
        cards_per_row (int): Cartones por fila
        cards_per_column (int): Cartones por columna
        export_numbers (bool): Si True, exporta los números a JSON

    Returns:
        Dict: Información sobre la generación (archivo, total de cartones, números)

    Raises:
        ValueError: Si los parámetros son inválidos
        IOError: Si hay problemas al guardar el archivo
    """
    # Validaciones
    if num_pages < 1:
        raise ValueError("El número de páginas debe ser al menos 1")

    if cards_per_page < 1:
        raise ValueError("Debe haber al menos 1 cartón por página")

    if cards_per_row < 1 or cards_per_column < 1:
        raise ValueError("Debe haber al menos 1 cartón por fila y columna")

    if cards_per_row * cards_per_column != cards_per_page:
        raise ValueError(f"cards_per_row ({cards_per_row}) × cards_per_column ({cards_per_column}) debe ser igual a cards_per_page ({cards_per_page})")

    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Crear el PDF
        c = canvas.Canvas(output_file, pagesize=landscape(A4))
        page_width, page_height = landscape(A4)

        # Calcular dimensiones y posiciones
        card_width, card_height = calculate_card_dimensions(
            page_width, page_height, cards_per_row, cards_per_column
        )

        positions = calculate_card_positions(
            page_width, page_height, cards_per_row, cards_per_column,
            card_width, card_height
        )

        # Almacenar información de todos los cartones
        all_cards_data = []
        card_number = 1

        # Generar páginas
        for page in range(num_pages):
            # Dibujar cartones en la página
            for x, y in positions:
                numbers = create_bingo_card(
                    c, x, y, card_width, card_height,
                    card_number, free_text
                )

                all_cards_data.append({
                    "card_number": card_number,
                    "page": page + 1,
                    "numbers": numbers
                })

                card_number += 1

            # Nueva página si no es la última
            if page < num_pages - 1:
                c.showPage()

        # Guardar el PDF
        c.save()

        # Exportar números a JSON si se solicita
        json_file = None
        if export_numbers:
            json_file = output_file.replace('.pdf', '_numbers.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "generated_at": datetime.now().isoformat(),
                    "total_cards": len(all_cards_data),
                    "total_pages": num_pages,
                    "cards_per_page": cards_per_page,
                    "free_text": free_text,
                    "cards": all_cards_data
                }, f, indent=2, ensure_ascii=False)

        result = {
            "success": True,
            "output_file": output_file,
            "total_cards": len(all_cards_data),
            "total_pages": num_pages,
            "json_file": json_file
        }

        return result

    except Exception as e:
        raise IOError(f"Error al generar el PDF: {str(e)}")


def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description='Generador de Cartones de Bingo en PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                                    # Genera 1 página con 6 cartones (configuración por defecto)
  %(prog)s -o mi_bingo.pdf                    # Especifica nombre de archivo
  %(prog)s -p 5                               # Genera 5 páginas (30 cartones)
  %(prog)s -c 4 -r 2 -l 2                     # 4 cartones por página en formato 2×2
  %(prog)s -f "GRATIS" -e                     # Usa "GRATIS" en el centro y exporta números
  %(prog)s -p 10 -o output/bingo.pdf -e       # 10 páginas en carpeta output, exportar números

Para más información: https://github.com/usuario/bingo
        """
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=f'{DEFAULT_OUTPUT_DIR}/cartones_bingo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        help='Nombre del archivo PDF de salida (default: output/cartones_bingo_YYYYMMDD_HHMMSS.pdf)'
    )

    parser.add_argument(
        '-p', '--pages',
        type=int,
        default=1,
        help='Número de páginas a generar (default: 1)'
    )

    parser.add_argument(
        '-c', '--cards-per-page',
        type=int,
        default=6,
        help='Número de cartones por página (default: 6)'
    )

    parser.add_argument(
        '-r', '--cards-per-row',
        type=int,
        default=3,
        help='Número de cartones por fila (default: 3)'
    )

    parser.add_argument(
        '-l', '--cards-per-column',
        type=int,
        default=2,
        help='Número de cartones por columna (default: 2)'
    )

    parser.add_argument(
        '-f', '--free-text',
        type=str,
        default=DEFAULT_FREE_TEXT,
        help=f'Texto para la celda central (default: {DEFAULT_FREE_TEXT})'
    )

    parser.add_argument(
        '-e', '--export-numbers',
        action='store_true',
        help='Exportar números generados a archivo JSON'
    )

    return parser.parse_args()


def main():
    """
    Función principal del programa.
    """
    try:
        # Parsear argumentos
        args = parse_arguments()

        print("=" * 60)
        print("GENERADOR DE CARTONES DE BINGO")
        print("=" * 60)
        print(f"Configuración:")
        print(f"  - Páginas: {args.pages}")
        print(f"  - Cartones por página: {args.cards_per_page}")
        print(f"  - Distribución: {args.cards_per_row}×{args.cards_per_column}")
        print(f"  - Texto central: {args.free_text}")
        print(f"  - Archivo salida: {args.output}")
        print(f"  - Exportar números: {'Sí' if args.export_numbers else 'No'}")
        print("-" * 60)

        # Generar PDF
        result = generate_pdf(
            output_file=args.output,
            num_pages=args.pages,
            cards_per_page=args.cards_per_page,
            free_text=args.free_text,
            cards_per_row=args.cards_per_row,
            cards_per_column=args.cards_per_column,
            export_numbers=args.export_numbers
        )

        # Mostrar resultado
        print(f"✅ PDF generado exitosamente!")
        print(f"   📄 Archivo: {result['output_file']}")
        print(f"   📊 Total de cartones: {result['total_cards']}")
        print(f"   📑 Total de páginas: {result['total_pages']}")

        if result['json_file']:
            print(f"   📋 Números exportados a: {result['json_file']}")

        print("=" * 60)

    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        return 1
    except IOError as e:
        print(f"❌ Error de entrada/salida: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
