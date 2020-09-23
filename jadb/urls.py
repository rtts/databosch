from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'^$', Entities.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

