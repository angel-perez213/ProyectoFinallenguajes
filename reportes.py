import os
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def _escribir_lineas(canvas_obj, lineas, x, y_inicio, salto):
    texto = canvas_obj.beginText(x, y_inicio)
    for linea in lineas:
        texto.textLine(linea)
    canvas_obj.drawText(texto)
    return texto.getY()


def generar_reporte_pdf(
    ruta_pdf: str,
    titulo: str,
    texto_entrada: str,
    es_gramatica: bool,
    resultado,
    rutas_imagenes,
):
    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    ancho, alto = letter

    c.setTitle(titulo)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, titulo)

    c.setFont("Helvetica", 10)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, alto - 70, "Fecha: " + fecha)

    c.setFont("Helvetica-Bold", 12)
    etiqueta_tipo = "Tipo detectado: " + str(resultado.etiqueta)
    c.drawString(50, alto - 90, etiqueta_tipo)

    c.setFont("Helvetica", 11)
    y = alto - 120
    encabezado = "Gramatica analizada:" if es_gramatica else "Automata analizado (texto):"
    c.drawString(50, y, encabezado)
    y -= 15

    lineas_entrada = texto_entrada.splitlines()
    y = _escribir_lineas(c, lineas_entrada, 60, y, 14)
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Explicacion:")
    y -= 15
    c.setFont("Helvetica", 11)
    y = _escribir_lineas(c, resultado.explicacion, 60, y, 14)
    y -= 20

    for ruta_img in rutas_imagenes:
        if not os.path.exists(ruta_img):
            continue
        try:
            img = ImageReader(ruta_img)
            iw, ih = img.getSize()
            escala = min((ancho - 100) / iw, 300 / ih)
            w = iw * escala
            h = ih * escala

            if y - h < 80:
                c.showPage()
                y = alto - 80

            c.drawImage(img, 50, y - h, width=w, height=h)
            y -= h + 20
        except Exception:
            continue

    c.showPage()
    c.save()
