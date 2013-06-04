from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'documents.views.documents_index'),
    
    url(r'^email/$', 'documents.views.email_document'),
    url(r'^attach_document/$', 'documents.views.attach_document'),
    url(r'^(?P<uuid>\w+)/$', 'documents.views.document'),
    
)
