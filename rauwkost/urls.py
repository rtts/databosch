from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import *
from .views2018 import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    #url(r'^$', RedirectView.as_view(pattern_name='locations')),
    url(r'^$', PageView.as_view(), {'slug': ''}),
    url(r'^2018/$', HomepageView.as_view(), name='homepage'),

    url(r'^2018/locatie/$', ProgramLocationView.as_view(), name='locations'),
    url(r'^2018/locatie/(?P<slug>[^/]+)/$', ProgramLocationView.as_view(), name='location'),
    url(r'^2018/tijd/$', ProgramTimeView.as_view(), name='times'),
    url(r'^2018/tijd/(?P<slug>[^/]+)/$', ProgramTimeView.as_view(), name='time'),
    url(r'^2018/soort/$', ProgramTypeView.as_view(), name='types'),
    url(r'^2018/soort/(?P<slug>[^/]+)/$', ProgramTypeView.as_view(), name='type'),
    url(r'^2018/(?P<slug>[^/]+)/$', ProgramDetailView.as_view(), name='program_detail'),
    url(r'^pagina/(?P<slug>[^/]+)/$', PageView.as_view(), name='page'),
]
