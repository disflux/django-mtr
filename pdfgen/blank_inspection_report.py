from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyPdf import PdfFileReader, PdfFileWriter
from StringIO import StringIO

from reports.models import Report

def blank_inspection_report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'

    outputPDF = PdfFileWriter()

    packet = StringIO()
    # create a new PDF with Reportlab
    p = canvas.Canvas(packet, pagesize=letter)
    p.drawString(37*mm,239*mm, report.origin_po)
    if report.origin_wo:
        p.drawString(37*mm,237*mm, "WO# %s" % report.origin_wo)
    p.drawCentredString(95*mm,239*mm, str(report.created_at.date()))
    p.drawCentredString(153*mm,239*mm, report.vendor.name)
    if report.heat_number:
        p.drawString(135*mm,228*mm, "HEAT # %s" % report.heat_number)
    if report.mfg_lot_number:
        p.drawString(135*mm,224*mm, "MFG Lot # %s" % report.mfg_lot_number)
    p.drawString(135*mm,220*mm, "%s Lot # %s" %
                   (settings.PDF_COMPANY_SHORT_NAME, report.lot_number))
    p.setFont("Helvetica", 9)
    if report.raw_material is False:
        p.drawCentredString(43*mm,95*mm, report.part_number.part_number)
    else:
        p.drawCentredString(43*mm,176*mm, report.part_number.part_number)
        p.drawCentredString(45*mm,170*mm, str(report.specification))
    p.save()
    
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
