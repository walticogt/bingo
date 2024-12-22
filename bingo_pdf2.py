from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import random


# Crear el PDF en orientación horizontal
output_file = "cartones_bingo_3x2_variable_oh.pdf"

# Variable global para el texto FREE
OH = "OH"


# Función para generar números aleatorios para un cartón
def generar_numeros_bingo():
    columnas = {
        "B": random.sample(range(1, 16), 5),
        "I": random.sample(range(16, 31), 5),
        "N": random.sample(range(31, 46), 5),
        "G": random.sample(range(46, 61), 5),
        "O": random.sample(range(61, 76), 5)
    }
    # Colocar OH en el centro
    columnas["N"][2] = OH
    return columnas


# Función para crear un cartón individual con diseño mejorado
def crear_carton(c, x, y, ancho, alto, num_carton):
    # Dibujar el borde del cartón
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(x, y, ancho, alto, stroke=1, fill=0)
    
    # Dimensiones de celdas
    filas = 6
    columnas = 5
    celda_ancho = ancho / columnas
    celda_alto = alto / filas
    
    # Encabezado (BINGO) con colores específicos
    c.setFont("Helvetica-Bold", 14)
    colores_bingo = [colors.red, colors.orange, colors.HexColor("#FFD700"), colors.green, colors.blue]
    letras = ["B", "I", "N", "G", "O"]
    
    for i, letra in enumerate(letras):
        c.setFillColor(colores_bingo[i])
        c.rect(x + i * celda_ancho, y + alto - celda_alto, celda_ancho, celda_alto, stroke=1, fill=1)
        c.setFillColor(colors.white)
        c.drawCentredString(
            x + (i + 0.5) * celda_ancho,
            y + alto - celda_alto + 10,
            letra
        )
    
    # Números del cartón aleatorios
    numeros = generar_numeros_bingo()
    c.setFont("Helvetica", 12)
    
    for fila in range(1, filas):
        for col, letra in enumerate(letras):
            valor = numeros[letra][fila - 1]
            c.setFillColor(colors.black)
            c.rect(
                x + col * celda_ancho,
                y + alto - (fila + 1) * celda_alto,
                celda_ancho,
                celda_alto,
                stroke=1,
                fill=0
            )
            if valor == OH:
                c.setFillColor(colors.orange)
            else:
                c.setFillColor(colors.black)
            c.drawCentredString(
                x + (col + 0.5) * celda_ancho,
                y + alto - (fila + 1) * celda_alto + 10,
                str(valor)
            )
    
    # Pie de cada cartón
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(
        x + (ancho / 2),
        y - 15,
        f"01-{num_carton:02}"
    )


# Crear el PDF con 3x2 cartones
def generar_pdf():
    c = canvas.Canvas(output_file, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Ajuste de tamaño y posiciones
    margen_x = 30
    margen_y = 50
    espacio_x = 20
    espacio_y = 30
    
    ancho_carton = (width - (2 * margen_x) - (2 * espacio_x)) / 3
    alto_carton = (height - (2 * margen_y) - espacio_y) / 2
    
    posiciones = [
        (margen_x + (ancho_carton + espacio_x) * col, margen_y + (alto_carton + espacio_y) * fila)
        for fila in range(2)
        for col in range(3)
    ]
    
    # Dibujar los cartones
    num_carton = 1
    for x, y in posiciones:
        crear_carton(c, x, y, ancho_carton, alto_carton, num_carton)
        num_carton += 1
    
    # Guardar el PDF
    c.save()
    print(f"✅ PDF generado correctamente: {output_file}")


# Ejecutar la función
generar_pdf()
