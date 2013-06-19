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

from reports.models import Report

def blank_inspection_report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'

    outputPDF = PdfFileWriter()

    packet = StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(37*mm,239*mm, report.origin_po)
    can.drawCentredString(95*mm,239*mm, str(report.created_at.date()))
    can.drawCentredString(153*mm,239*mm, report.vendor.name)
    can.drawString(135*mm,228*mm, "HEAT # %s" % report.heat_number)
    can.drawString(135*mm,224*mm, "MFG Lot # %s" % report.mfg_lot_number)
    can.drawString(135*mm,220*mm, "TSA Lot # %s" % report.lot_number)
    can.setFont("Helvetica", 9)
    can.drawCentredString(43*mm,95*mm, report.part_number.part_number)
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file(settings.PDF_INSPECTION_REPORT_TEMPLATE, "rb"))
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    outputPDF.addPage(page)
    
    # finally, write "output" to a real file
    outputPDF.write(response)
    return response
