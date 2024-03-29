from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    #url(r'^$', RedirectView.as_view(pattern_name='locations')),
    #url(r'^$', FrontPageView.as_view()),
    url(r'^$', EmptyView.as_view()),
    url(r'^download/(?P<filename>[^/]+)$', download, name='download'),
    url(r'^locaties/$', LocationsView.as_view(), name='locations'),
    url(r'^bende/$', TeamView.as_view(), name='team'),
    url(r'^consent/$', ConsentView.as_view(), name='consent'),
    url(r'^nieuws/(?P<slug>[^/]+)/$', BlogView.as_view(), name='blog'),
    url('^(?P<year>[0-9]+)/$', ProgramLocationView.as_view(), name='homepage'),
    url(r'^(?P<year>[0-9]+)/locatie/$', ProgramLocationView.as_view(), name='locations'),
    url(r'^(?P<year>[0-9]+)/locatie/(?P<slug>[^/]+)/$', ProgramLocationView.as_view(), name='location'),
    url(r'^(?P<year>[0-9]+)/tijd/$', ProgramTimeView.as_view(), name='times'),
    url(r'^(?P<year>[0-9]+)/tijd/(?P<slug>[^/]+)/$', ProgramTimeView.as_view(), name='time'),
    url(r'^(?P<year>[0-9]+)/soort/$', ProgramTypeView.as_view(), name='types'),
    url(r'^(?P<year>[0-9]+)/soort/(?P<slug>[^/]+)/$', ProgramTypeView.as_view(), name='type'),
    url(r'^(?P<year>[0-9]+)/(?P<slug>[^/]+)/$', ProgramDetailView.as_view(), name='program_detail'),
      url(r'^(?P<slug>[^/]+)/$', PageView.as_view(), name='page'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

