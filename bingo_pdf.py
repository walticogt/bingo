import random
from fpdf import FPDF
from datetime import datetime

# Función para generar un cartón de bingo
def generar_carton():
    carton = {
        'B': random.sample(range(1, 16), 5),
        'I': random.sample(range(16, 31), 5),
        'N': random.sample(range(31, 46), 4),
        'G': random.sample(range(46, 61), 5),
        'O': random.sample(range(61, 76), 5)
    }
    return carton

# Función para agregar un cartón al PDF con borde externo
def agregar_carton(pdf, carton, x, y):
    margen = 2
    ancho_celda = 14
    alto_celda = 6
    ancho_total = 5 * ancho_celda + (margen * 2)
    alto_total = 6 * alto_celda + (margen * 2) + 6
    
    # Dibujar borde exterior
    pdf.set_xy(x, y)
    pdf.set_line_width(0.5)
    pdf.rect(x, y, ancho_total, alto_total)
    
    # Dibujar título
    pdf.set_xy(x + margen, y + margen)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(255, 0, 0)
    pdf.cell(ancho_celda, alto_celda, 'B', border=1, align='C', fill=True)
    pdf.set_fill_color(255, 255, 0)
    pdf.cell(ancho_celda, alto_celda, 'I', border=1, align='C', fill=True)
    pdf.set_fill_color(0, 255, 0)
    pdf.cell(ancho_celda, alto_celda, 'N', border=1, align='C', fill=True)
    pdf.set_fill_color(0, 0, 255)
    pdf.cell(ancho_celda, alto_celda, 'G', border=1, align='C', fill=True)
    pdf.set_fill_color(255, 0, 255)
    pdf.cell(ancho_celda, alto_celda, 'O', border=1, align='C', fill=True)
    pdf.ln()
    
    # Dibujar números
    for i in range(5):
        pdf.set_font('Helvetica', '', 7)
        pdf.cell(ancho_celda, alto_celda, str(carton['B'][i]), border=1, align='C')
        pdf.cell(ancho_celda, alto_celda, str(carton['I'][i]), border=1, align='C')
        if i == 2:
            pdf.cell(ancho_celda, alto_celda, '*', border=1, align='C')
        else:
            pdf.cell(ancho_celda, alto_celda, str(carton['N'][i] if i < 2 else carton['N'][i-1]), border=1, align='C')
        pdf.cell(ancho_celda, alto_celda, str(carton['G'][i]), border=1, align='C')
        pdf.cell(ancho_celda, alto_celda, str(carton['O'][i]), border=1, align='C')
        pdf.ln()
    
    # Dibujar pie de cartón
    pdf.set_font('Helvetica', 'I', 6)
    pdf.cell(ancho_total - (margen * 2), alto_celda, f'001 {str(datetime.now().strftime("%H%M%S"))}    littlebanditgames.com', align='C')

# Función principal para generar el PDF
def generar_cartones_pdf():
    try:
        cantidad = input("Ingrese la cantidad de cartones a generar (presione Enter para generar 6 por defecto): ")
        cantidad = int(cantidad) if cantidad.strip() else 6
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print("¡Entrada no válida! Se generarán 6 cartones por defecto.")
        cantidad = 6
    
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(10, 10, 10)
    
    filas = 3
    columnas = 2
    margen_general = 10
    espacio_horizontal = 5
    espacio_vertical = 5
    ancho_carton = 90
    alto_carton = 60
    
    carton_actual = 1
    total_paginas = (cantidad + (filas * columnas) - 1) // (filas * columnas)
    
    for pagina in range(1, total_paginas + 1):
        pdf.add_page()
        for fila in range(filas):
            for columna in range(columnas):
                if carton_actual > cantidad:
                    break
                x = margen_general + columna * (ancho_carton + espacio_horizontal)
                y = margen_general + fila * (alto_carton + espacio_vertical)
                carton = generar_carton()
                agregar_carton(pdf, carton, x, y)
                carton_actual += 1
    
    nombre_archivo = datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdf.output(nombre_archivo)
    print(f"Archivo PDF generado: {nombre_archivo}")

generar_cartones_pdf()
