from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyPdf import PdfFileReader, PdfFileWriter
from StringIO import StringIO
from django.db.models import Avg, Max, Min
from actstream import action

from reports.models import Report

def generate_inspection_report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)

    outputPDF = PdfFileWriter()

    packet = StringIO()
    # create a new PDF with Reportlab
    p = canvas.Canvas(packet, pagesize=letter)
    p.drawString(25*mm,216*mm, report.origin_po)
    if report.origin_wo:
        p.drawString(45*mm,214*mm, "WO# %s" % report.origin_wo)
    p.drawCentredString(95*mm,216*mm, str(report.created_at.date()))
    p.drawCentredString(165*mm,216*mm, report.vendor.name)
    
    p.setFont("Helvetica", 9)
    if report.heat_number:
        p.drawString(155*mm,211*mm, "HEAT # %s" % report.heat_number)
    if report.mfg_lot_number:
        p.drawString(155*mm,209*mm, "MFG Lot # %s" % report.mfg_lot_number)
    p.drawString(155*mm,206*mm, "%s Lot # %s" %
                   (settings.PDF_COMPANY_SHORT_NAME, report.lot_number))
    p.setFont("Helvetica", 9)
    if report.raw_material is False:
        p.drawCentredString(43*mm,95*mm, report.part_number.part_number)
    else:
        p.drawCentredString(43*mm,176*mm, report.part_number.part_number)
        p.drawCentredString(45*mm,170*mm, str(report.part_number.specification))
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
    action.send(request.user, verb="generated an inspection report", target=report)
    return outputPDF
    

def blank_inspection_report(request, lot_number):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'
    report = Report.objects.get(lot_number=lot_number)
    outputPDF = generate_inspection_report(request, lot_number)
    outputPDF.write(response)
    return response

def batch_inspection_report(request):
    if 'po' in request.GET:
        po = int(request.GET.get('po'))
        lots = Report.objects.filter(origin_po=po).aggregate(high_lot=Max('lot_number'), low_lot=Min('lot_number'))
        start = int(lots['low_lot'])
        end = int(lots['high_lot'])
    else:    
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'
    outputPDF = PdfFileWriter()
    
    for cert in range(start, end+1):
        report = Report.objects.get(lot_number=cert)
        pdf = generate_inspection_report(request, report.lot_number)
        outputPDF.addPage(pdf.getPage(0))
    
    outputPDF.write(response)
    return response
        
        