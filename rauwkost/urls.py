from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^$', RedirectView.as_view(pattern_name='locations')),
    url(r'^locaties/$', ProgramLocationView.as_view(), name='locations'),
    url(r'^locaties/(?P<slug>[^/]+)/$', ProgramLocationView.as_view(), name='location'),
    url(r'^tijden/$', ProgramTimeView.as_view(), name='times'),
    url(r'^soorten/$', ProgramTypeView.as_view(), name='types'),
    url(r'^(.*)/$', page, name='page'),
]
