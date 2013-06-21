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
from documents.models import Document
    
def prepare_internal_cert(uuid, customer, wo, po, quantity, invoice):
    document = Document.objects.get(uuid=uuid)
    f = urlopen(Request(document.file.url)).read()
    existing_pdf = PdfFileReader(StringIO(f))
    outputPDF = PdfFileWriter()

    packet = StringIO()
    # create a new PDF with Reportlab
    p = canvas.Canvas(packet, pagesize=letter)
    p.setFont("Helvetica", 10)
    # Write Customer name
    p.drawCentredString(54*mm,208*mm, customer)
    # Write Customer PO #
    p.drawCentredString(144*mm, 208*mm, po)
    # Write Work Order #
    p.drawCentredString(56*mm,200*mm, wo)
    # Write Invoice #
    p.drawCentredString(136*mm,200*mm, invoice)
    # Write Quantity
    p.drawCentredString(136*mm, 185*mm, quantity) 
    p.save()
    # add the "watermark" (which is the new pdf) on the existing page
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    outputPDF.addPage(page)
    return outputPDF

def generate_cert_packet(request, order_number):
    order = Order.objects.get(order_number=order_number)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="label.pdf"'
    
    outputPDF = PdfFileWriter()
    
    buffer = cStringIO.StringIO()
    p = canvas.Canvas(buffer)
    
    # Draw Header
    p.setFont("Helvetica", 40)
    p.drawCentredString(107.5*mm, 280*mm, settings.PDF_COMPANY_NAME)
    p.setFont("Helvetica", 10)
    p.drawCentredString(107.5*mm, 275*mm, "%s . %s . %s" %
                        (
                            settings.PDF_COMPANY_STREET,
                            settings.PDF_COMPANY_LOCALITY,
                            settings.PDF_COMPANY_ZIPCODE
                        ))
    p.drawCentredString(107.5*mm, 271*mm, "%s .  Fax: %s" %
                        (settings.PDF_COMPANY_PHONE, settings.PDF_COMPANY_FAX))
    p.line(0*mm, 269*mm, 215*mm, 269*mm)
    p.setFont("Helvetica", 25)
    p.drawCentredString(107.5*mm, 257*mm, "Material Test Reports")
    
    # Draw Information Box
    p.setFont("Helvetica", 15)
    p.drawString(40*mm, 240*mm, "Customer:")
    p.drawString(90*mm, 240*mm, order.customer.name)
    p.line(89*mm, 239*mm, 160*mm, 239*mm)
    p.drawString(40*mm, 234*mm, "Order #:")
    p.drawString(90*mm, 234*mm, order.order_number)
    p.line(89*mm, 233*mm, 160*mm, 233*mm)
    p.drawString(40*mm, 228*mm, "Customer PO #:")
    p.drawString(90*mm, 228*mm, order.customer_po)
    p.line(89*mm, 227*mm, 160*mm, 227*mm)
    
    # Draw mtr information table
    p.setFont("Helvetica", 12)
    p.line(10*mm, 192*mm, 195*mm, 192*mm)
    p.drawString(12*mm, 195*mm, "Line #")
    p.drawCentredString(45*mm, 200*mm, "%s Lot #" %
                        settings.PDF_COMPANY_SHORT_NAME)
    p.drawCentredString(45*mm, 195*mm, "(MFG Lot/Heat #)")
    p.drawString(70*mm, 195*mm, "Part #")
    p.drawString(100*mm, 195*mm, "Description")
    p.setFont("Helvetica", 8)
    
    # Loop over the line items
    i = 0
    start = 185
    for li in order.line_items.all():
        vert_position = start-(i*7)
        p.drawString(15*mm, vert_position*mm, str(li.line_number))
        p.drawCentredString(45*mm, (vert_position+3)*mm, str(li.report.lot_number))
        if li.report.mfg_lot_number:
            p.drawCentredString(45*mm, vert_position*mm, "(%s)" % str(li.report.mfg_lot_number))
        else:
            p.drawCentredString(45*mm, vert_position*mm, "(%s)" % str(li.report.heat_number))
        p.drawCentredString(77*mm, vert_position*mm, str(li.report.part_number))
        p.drawString(100*mm, vert_position*mm, str(li.report.part_number.description))
        p.line(12*mm, (vert_position-1)*mm, 195*mm, (vert_position-1)*mm)
        i += 1
    
    p.save()
    
    # Merge the report PDFs
    cover_input = PdfFileReader(cStringIO.StringIO(buffer.getvalue()))
    buffer.close()
    outputPDF.addPage(cover_input.getPage(0))
    
    for li in order.line_items.all():
        documents = li.report.get_all_primary_documents()
        for doc in documents:
            if doc is not None:
                if doc['type'] == 'WS':
                    # This is an internal cert, prepare it
                    pdf = prepare_internal_cert(doc['uuid'], 
                                                order.customer.name, 
                                                order.order_number, 
                                                order.customer_po, 
                                                str(li.quantity), 
                                                str(order.invoice_number))   
                else:    
                    f = urlopen(Request(doc['url'])).read()
                    mem = StringIO(f)
                    pdf = PdfFileReader(mem)
                
                
                for pageNum in xrange(pdf.getNumPages()):
                    current = pdf.getPage(pageNum)
                    outputPDF.addPage(current)    
    
    outputPDF.write(response)
    return response