from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyPdf import PdfFileReader, PdfFileWriter
from StringIO import StringIO
from urllib2 import Request, urlopen
from actstream import action

from reports.models import Report
from documents.models import Document

def doc_overlay(request, document_uuid, lot_number):
    report = Report.objects.get(lot_number=lot_number)
    document = Document.objects.get(uuid=document_uuid)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inspection_report.pdf"'

    outputPDF = PdfFileWriter()
    packet = StringIO()
    
    # read your existing PDF
    f = urlopen(Request(document.file.url)).read()
    mem = StringIO(f)
    existing_pdf = PdfFileReader(mem)
    pages = existing_pdf.getNumPages()
    first_page = existing_pdf.getPage(0)
    width = float(first_page.mediaBox.getWidth())
    height = float(first_page.mediaBox.getHeight())
    
    # create a new PDF with Reportlab
    p = canvas.Canvas(packet, pagesize=letter)
    p.setFillColorRGB(255,255,255)
    p.rect(0*mm, 276*mm, 220*mm, 3*mm, fill=1, stroke=0)
    p.setFillColorRGB(0,0,0)
    p.setFont("Helvetica", 7)
    p.drawCentredString(width/2.0,height-9.0, "%s LOT # %s / %s (doc# %s)" % 
                                (settings.PDF_COMPANY_SHORT_NAME,
                                report.lot_number, str(report.created_at.date()), document.uuid))

                                
    
    p.save()
    
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    
    # add the "watermark" (which is the new pdf) on the existing page
    for x in range(0,pages):
        page = existing_pdf.getPage(x)
        page.mergePage(new_pdf.getPage(0))
        outputPDF.addPage(page)
    
    # finally, write "output" to a real file
    outputPDF.write(response)
    action.send(request.user, verb="viewed document", action_object=document, target=report)
    return response
