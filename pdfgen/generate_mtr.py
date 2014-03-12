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

    
class MTR:
    
    def __init__(self, properties):
        for k, v in properties.iteritems():
            setattr(self, k, v)
            
        if self.cert_type == 'STUD':
            self.cert_header = 'Weld Stud'
            self.specification = 'A108'
        if self.cert_type == 'DBA':
            self.cert_header = 'Deformed Bar Anchor'
            self.specification = 'A496'
            
        self.template = settings.PDF_MTR_TEMPLATE    
        
    
    def generate_pdf(self):
        template = PdfFileReader(file(self.template, "rb"))
        outputPDF = PdfFileWriter()
        packet = StringIO()
        p = canvas.Canvas(packet, pagesize=letter)
    
        # Write Cert type
        p.setFillColorRGB(255,255,255)
        p.rect(50*mm, 247*mm, 120*mm, 13*mm, fill=1, stroke=0)
        p.rect(75*mm, 164*mm, 8.5*mm, 5*mm, fill=1, stroke=0)
        p.setFillColorRGB(0,0,0)
        p.line(53.75*mm, 247*mm, 161.25*mm, 247*mm)
        p.setFont("Helvetica", 25)
        p.drawCentredString(107*mm, 250*mm, "%s Certification" % self.cert_header)
        
        # write chemical properties
        p.setFont("Helvetica", 10)
        p.drawCentredString(47*mm, 158*mm, str(self.aisi_grade.upper()))
        p.drawCentredString(79*mm, 166.5*mm, str(self.specification))
        p.drawCentredString(54*mm, 192*mm, str(self.part_number))
        p.drawCentredString(132*mm, 192*mm, str(self.heat_number))
        p.drawCentredString(58*mm, 184*mm, str(self.part_number.description))
        p.drawCentredString(73*mm, 154*mm, str(self.carbon))
        p.drawCentredString(73*mm, 149.5*mm, str(self.manganese))
        p.drawCentredString(73*mm, 145.5*mm, str(self.sulfur))
        p.drawCentredString(73*mm, 141.5*mm, str(self.silicon))
        p.drawCentredString(73*mm, 137*mm, str(self.phosphorus))
        p.drawCentredString(73*mm, 133*mm, str(self.chromium))
        
        # write physical properties
        p.drawCentredString(100*mm, 95*mm, str(self.tensile_strength))
        p.drawCentredString(100*mm, 91*mm, str(self.yield_strength))
        p.drawCentredString(100*mm, 87*mm, str(self.reduction_of_area))
        p.drawCentredString(100*mm, 83*mm, str(self.elongation))
        
        p.save()
        # add the "watermark" (which is the new pdf) on the existing page
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        page = template.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        outputPDF.addPage(page)
        return outputPDF
