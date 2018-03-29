from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^$', page, name='homepage'),
    url(r'^nieuws/([^/]+)/$', news, name='news'),
    url(r'^project/([^/]+)/$', project, name='project'),
    url(r'^programma/([^/]+)/$', program, name='program'),
    url(r'^(.*)/$', page, name='page'),
]
