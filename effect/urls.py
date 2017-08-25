from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^$', page, name='homepage'),
    url(r'^news/([^/]+)/$', news, name='news'),
    url(r'^(.*)/$', page, name='page'),
]
