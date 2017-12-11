from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^$', RedirectView.as_view(pattern_name='locations')),
    url(r'^locatie/$', ProgramLocationView.as_view(), name='locations'),
    url(r'^locatie/(?P<slug>[^/]+)/$', ProgramLocationView.as_view(), name='location'),
    url(r'^tijd/$', ProgramTimeView.as_view(), name='times'),
    url(r'^tijd/(?P<slug>[^/]+)/$', ProgramTimeView.as_view(), name='time'),
    url(r'^soort/$', ProgramTypeView.as_view(), name='types'),
    url(r'^soort/(?P<slug>[^/]+)/$', ProgramTypeView.as_view(), name='type'),
    url(r'^(?P<slug>[^/]+)/$', ProgramDetailView.as_view(), name='program_detail'),
]
