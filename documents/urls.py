from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^email/$', 'documents.views.email_document'),
)
