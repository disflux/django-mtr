from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import localtime

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas

from actstream import action

from parts.models import Part

def part_label(request, part_number):
    part = get_object_or_404(Part, part_number=part_number)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="label.pdf"'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setPageSize((105*mm, 26*mm))


    
    # Draw Part Number


    p.setFont("Helvetica", 20)
    p.drawCentredString(52*mm, 18*mm, part.part_number)
    barcode = createBarcodeDrawing('Code128', value=part.part_number,  barWidth=0.40*mm, barHeight=13*mm, humanReadable=False)
    barcode.drawOn(p, 3*mm, 2*mm)


    
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    #action.send(request.user, verb="generated a label", target=report)
    return response
