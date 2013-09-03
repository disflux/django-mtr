from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'documents.views.documents_index'),
    
    url(r'^email/$', 'documents.views.email_document'),
    url(r'^attach_document/$', 'documents.views.attach_document'),
    url(r'^remove_document/$', 'documents.views.remove_document'),
    url(r'^viewdoc/(?P<document_uuid>\w+)/(?P<lot_number>\d+)$', 'pdfgen.doc_overlay.doc_overlay'),
    url(r'^(?P<uuid>\w+)/$', 'documents.views.document'),
    
)
