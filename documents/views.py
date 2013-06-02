from django.core.mail import EmailMessage 
from documents.models import Document
from reports.models import Report

def email_document(request):
    print request.POST
    doc_id = request.POST.get('doc-id', None)
    report_id = request.POST.get('report-id', None)
    recipient = request.POST.get('recipient', None)

    doc = Document.objects.get(id=doc_id)
    report = Report.objects.get(id=report_id)
    subject = "%s for lot # %s" % (doc.type, report.lot_number)
    body = "See attached document for the %s for lot # %s" % (doc.type, report.lot_number)
    body += "\n\nLot Number: %s" % report.lot_number
    body += "\nPart Number: %s" % report.part_number
    body += "\nDescription: %s" % report.part_number.description

    email = EmailMessage(subject, body, 'mtr@tsamfg.com', [recipient], headers={'Reply-To': 'derek.m@tsamfgomaha.com'})

    email.attach("MTR_%s.pdf" % report.lot_number, doc.file.read(), 'application/pdf')
    email.send()

    

