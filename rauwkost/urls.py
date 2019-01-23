from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    #url(r'^$', RedirectView.as_view(pattern_name='locations')),
    url(r'^$', FrontPageView.as_view()),
    url(r'^download/(?P<slug>[^/]+)/$', DownloadView.as_view(), name='download'),
    url('^(?P<year>[0-9]+)/$', HomepageView.as_view(), name='homepage'),
    url(r'^(?P<year>[0-9]+)/locatie/$', ProgramLocationView.as_view(), name='locations'),
    url(r'^(?P<year>[0-9]+)/locatie/(?P<slug>[^/]+)/$', ProgramLocationView.as_view(), name='location'),
    url(r'^(?P<year>[0-9]+)/tijd/$', ProgramTimeView.as_view(), name='times'),
    url(r'^(?P<year>[0-9]+)/tijd/(?P<slug>[^/]+)/$', ProgramTimeView.as_view(), name='time'),
    url(r'^(?P<year>[0-9]+)/soort/$', ProgramTypeView.as_view(), name='types'),
    url(r'^(?P<year>[0-9]+)/soort/(?P<slug>[^/]+)/$', ProgramTypeView.as_view(), name='type'),
    url(r'^(?P<year>[0-9]+)/(?P<slug>[^/]+)/$', ProgramDetailView.as_view(), name='program_detail'),
    url(r'^pagina/(?P<slug>[^/]+)/$', PageView.as_view(), name='page'),
]
