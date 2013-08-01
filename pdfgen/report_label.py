from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas

from reports.models import Report

def report_label(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="label.pdf"'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setPageSize((150*mm, 105*mm))
    # Draw Logo/Image
    p.setFont("Helvetica", 40)
    p.drawString(10, 90*mm, settings.PDF_COMPANY_NAME)
    p.setFont("Helvetica", 10)
    p.drawString(10, 85*mm, "%s . %s . %s" %
                        (
                            settings.PDF_COMPANY_STREET,
                            settings.PDF_COMPANY_LOCALITY,
                            settings.PDF_COMPANY_ZIPCODE
                        ))
    p.drawString(25, 81*mm, "%s .  Fax: %s" % (settings.PDF_COMPANY_PHONE, settings.PDF_COMPANY_FAX)) 
    p.line(75*mm, 105*mm, 75*mm, 70*mm)

    # Draw Lot number
    p.setFont("Helvetica", 20)
    p.drawCentredString(110*mm, 98*mm, "Lot # %s" % report.lot_number)
    barcode = createBarcodeDrawing('Code128', value=report.lot_number,  barWidth=0.5*mm, barHeight=10*mm, humanReadable=True)
    barcode.drawOn(p,84*mm, 83*mm)
    p.line(75*mm, 82*mm, 150*mm, 82*mm)
    p.setFont("Helvetica", 13)
    if report.mfg_lot_number:
        p.drawString(78*mm, 77*mm, "MFG LOT # %s" % report.mfg_lot_number)
    if report.heat_number:
        p.drawString(78*mm, 72*mm, "HEAT # %s" % report.heat_number)
    
    
    # Draw Description
    p.setFont("Helvetica", 13)
    p.line(0,70*mm, 150*mm, 70*mm)
    p.drawString(10, 60*mm, report.part_number.description)
    p.line(0,55*mm, 150*mm, 55*mm)
    
    # Draw Part Number
    p.setFont("Helvetica", 10)
    p.drawString(10, 50*mm, "Part #")
    p.setFont("Helvetica", 25)
    p.drawString(10, 40*mm, report.part_number.part_number)
    barcode = createBarcodeDrawing('Code128', value=report.part_number.part_number,  barWidth=0.5*mm, barHeight=9*mm, humanReadable=False)
    barcode.drawOn(p, 0, 28*mm)
    p.line(0, 25*mm, 150*mm, 25*mm)
    
    # Draw Box Quantity if available
    if report.part_number.box_quantity:
        p.line(105*mm, 55*mm, 105*mm, 25*mm)
        p.setFont("Helvetica", 10)
        p.drawString(110*mm, 50*mm, "Quantity")
        p.setFont("Helvetica", 25)
        p.drawString(110*mm, 40*mm, str(report.part_number.box_quantity))
        barcode = createBarcodeDrawing('Code128', value=str(report.part_number.box_quantity),  barWidth=0.5*mm, barHeight=9*mm, humanReadable=False)
        barcode.drawOn(p, 103*mm, 28*mm)
    
    
    # Draw Other Info
    #p.line(110*mm, 0, 110*mm, 25*mm)
    p.setFont("Helvetica", 15)
    p.drawString(10, 20*mm, "Date")
    p.drawString(40*mm, 20*mm, str(report.created_at))
    p.line(0, 18*mm, 150*mm, 18*mm)
    p.drawString(10, 12*mm, "Vendor")
    p.drawString(40*mm, 12*mm, report.vendor.name)
    p.line(0,10*mm, 150*mm, 10*mm)
    if report.origin_po:
        p.drawString(10, 4*mm, "PO #")
        p.drawString(40*mm, 4*mm, report.origin_po)
    elif report.origin_wo:
        p.drawString(10, 4*mm, "WO #")
        p.drawString(40*mm, 4*mm, report.origin_wo)
    
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
