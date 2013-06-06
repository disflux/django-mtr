from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages

from orders.forms import OrderForm, NewLineItemForm
from orders.models import Customer, Order, OrderLineItem
from reports.models import Report


def orders_index(request):
    orders = Order.objects.all()
    
    return render_to_response('orders/orders_index.html',
                              {'orders': orders,},
                              context_instance=RequestContext(request))
    

def order(request, order_number):
    
    order = Order.objects.get(order_number=order_number)
    newli = NewLineItemForm(None)
    
    if 'lineitem_button' in request.POST:
        newli = NewLineItemForm(request.POST)
        if newli.is_valid():
            li = newli.save(commit=False)
            li.order = order
            li.save()
            order.line_items.add(li)
            order.save()
            messages.success(request, 'Report attached')

            return HttpResponseRedirect(reverse('orders.views.order',
                                                    args=[order.order_number]))
    return render_to_response('orders/order.html', 
                              {
                                  'order': order,
                                  'new_lineitem_form': newli,
                              },
                              context_instance=RequestContext(request))
    
def new_order(request):
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            order = orderform.save()
            return HttpResponseRedirect(order.get_absolute_url())
    else:
        orderform = OrderForm()
    return render_to_response('orders/new_order.html',
                              {'orderform': orderform,},
                              context_instance=RequestContext(request))
                              
def generate_cert_packet(request, order_number):
    from reportlab.lib.units import mm
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from pyPdf import PdfFileReader, PdfFileWriter
    from urllib2 import Request, urlopen
    from StringIO import StringIO
    import cStringIO
    order = Order.objects.get(order_number=order_number)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="label.pdf"'
    
    outputPDF = PdfFileWriter()
    
    buffer = cStringIO.StringIO()
    p = canvas.Canvas(buffer)
    
    # Draw Header
    p.setFont("Helvetica", 40)
    p.drawCentredString(107.5*mm, 280*mm, "TSA MFG")
    p.setFont("Helvetica", 10)
    p.drawCentredString(107.5*mm, 275*mm, "14901 Chandler Rd . Omaha, NE . 68138")
    p.drawCentredString(107.5*mm, 271*mm, "800-228-2948   Fax: 402-895-3297")
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
    p.drawCentredString(45*mm, 200*mm, "TSA Lot #")
    p.drawCentredString(45*mm, 195*mm, "(MFG Lot #)")
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
        p.drawCentredString(45*mm, vert_position*mm, "(%s)" % str(li.report.mfg_lot_number))
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
        for doc in li.report.documents.all():
            f = urlopen(Request(doc.file.url)).read()
            mem = StringIO(f)
            pdf = PdfFileReader(mem)
            for pageNum in xrange(pdf.getNumPages()):
                current = pdf.getPage(pageNum)
                outputPDF.addPage(current)    
    
    outputPDF.write(response)
    

    return response

                              


