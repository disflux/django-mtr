from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from StringIO import StringIO

from documents.models import Document, DocumentType
from pdfgen.forms import MTRForm
from pdfgen.generate_mtr import MTR
from reports.models import Report, ReportDocument

def mtr_generator(request):
    lot_number = request.GET.get('lot_number', None)
    if lot_number:
        report = Report.objects.get(lot_number=lot_number)
        
    if request.method == 'POST':
        mtrform = MTRForm(request.POST)
        if mtrform.is_valid():
            new_mtr = MTR(properties=mtrform.cleaned_data)
            pdf = new_mtr.generate_pdf()
            fp = StringIO()
            pdf.write(fp)
            file = InMemoryUploadedFile(fp, None, "%s.pdf" % report.lot_number,
                                        'application/pdf', fp.len, None)
            doc_type = DocumentType.objects.get(name='Material Test Report')
            doc = Document(type=doc_type, file=file, created_by=request.user)
            doc.save()
            rd = ReportDocument(report=report, document=doc, primary_document=True, created_by=request.user, internal_cert=True)
            rd.save()
            report.save()
            messages.success(request, 'Document upload successful.') 
            return HttpResponseRedirect(reverse('reports.views.report',
                                                    args=[report.lot_number]))
    
    else:
        mtrform = MTRForm(initial={
                                    'part_number': report.part_number,
                                    'heat_number': report.heat_number,
                                    'size': report.part_number.description,
                                  })
    
                                  
    
    
    return render_to_response('pdfgen/new_mtr.html',
                              {
                              'form': mtrform,
                              },
                              context_instance=RequestContext(request))    