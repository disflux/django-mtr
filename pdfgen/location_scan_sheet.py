from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import localtime
from pyPdf import PdfFileReader, PdfFileWriter
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas

from inventory.models import InventoryLocation

def location_scan_sheet(request):
    locations = InventoryLocation.objects.all().order_by('location_code')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="locations.pdf"'
    p = canvas.Canvas(response)
    p.setPageSize((215*mm, 275*mm))
    i = 260
    column_a = [15]
    column_b = [65]
    column_c = [115]
    column_d = [165]
    horizontal = column_a
    for location in locations:
        
        p.setFont("Helvetica", 15)
        #p.drawCentredString(horizontal[0]*mm, (i+3)*mm, location.location_code)
        barcode = createBarcodeDrawing('Code128', value=location.location_code,  barWidth=0.25*mm, barHeight=8*mm, humanReadable=True)
        barcode.drawOn(p, horizontal[0]*mm, (i)*mm)
        
        i -= 16
        if i < 2:
            i = 260
            if horizontal == column_a:
                horizontal = column_b
            elif horizontal == column_b:
                horizontal = column_c
            elif horizontal == column_c:
                horizontal = column_d
            else:
                horizontal = column_a
                p.showPage()
    
    p.save()

    return response
