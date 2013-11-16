from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import localtime

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas

from inventory.models import InventoryLocation

def location_labels(request):
    locations = InventoryLocation.objects.all()
    count = InventoryLocation.objects.count()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="label.pdf"'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    page_length = count * 26 #26 mm in height per label
    p.setPageSize((105*mm, page_length*mm))
    
    i = count
    for location in locations:
        p.setFont("Helvetica", 20)
        p.drawCentredString(52*mm, ((i*26)+18)*mm, location.location_code)
        barcode = createBarcodeDrawing('Code128', value=location.location_code,  barWidth=0.40*mm, barHeight=13*mm, humanReadable=False)
        barcode.drawOn(p, 26*mm, ((i*26)+2)*mm)
        i -= 1

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    #action.send(request.user, verb="generated a label", target=report)
    return response
