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

def location_labels(request):
    locations = InventoryLocation.objects.filter(location_code__startswith='ATR')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="locations.pdf"'
    p = canvas.Canvas(response)
    
    for location in locations:
        p.setPageSize((105*mm, 26*mm))
        p.setFont("Helvetica", 20)
        p.drawCentredString(52*mm, 18*mm, location.location_code)
        barcode = createBarcodeDrawing('Code128', value=location.location_code,  barWidth=0.38*mm, barHeight=13*mm, humanReadable=False)
        barcode.drawOn(p, 5*mm, 2*mm)
        p.showPage()
    
    p.save()

    return response
