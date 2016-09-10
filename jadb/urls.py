from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', Alles.as_view(), name='alles'),
    url(r'^cultureel/$', Cultureel.as_view(), name='cultureel'),
    url(r'^maatschappelijk/$', Maatschappelijk.as_view(), name='maatschappelijk'),
    url(r'^persoonlijk/$', Persoonlijk.as_view(), name='persoonlijk'),
    url(r'^organisaties/$', Initiatieven.as_view(), name='initiatieven'),
]
