from django.conf.urls import url, include
from django.shortcuts import redirect
from .views import *

urlpatterns = [
    url(r'^$', lambda r: redirect('cultureel')),
    url(r'^cultureel/$', Cultureel.as_view(), name='cultureel'),
    url(r'^maatschappelijk/$', Maatschappelijk.as_view(), name='maatschappelijk'),
    url(r'^persoonlijk/$', Persoonlijk.as_view(), name='persoonlijk'),
    url(r'^initiatieven/$', Initiatieven.as_view(), name='initiatieven'),
]
