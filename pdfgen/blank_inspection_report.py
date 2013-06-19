from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyPdf import PdfFileReader, PdfFileWriter
from urllib2 import Request, urlopen
from StringIO import StringIO
import cStringIO

from orders.models import Customer, Order, OrderLineItem

def blank_inspection_report(request, order_number):
    report = Order.objects.get(order_number=order_number)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'

    outputPDF = PdfFileWriter()

    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100,100, "Hello world")
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file(settings.PDF_INSPECTION_REPORT_TEMPLATE, "rb"))
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    
    # finally, write "output" to a real file
    outputPDF.write(response)
    return response
