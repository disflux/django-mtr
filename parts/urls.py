from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'parts.views.parts_index'),
    
    url(r'^(?P<part_number>\w+)/$', 'parts.views.part'),
    
)
