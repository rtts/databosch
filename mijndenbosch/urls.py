from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', homepage, name='homepage'),
    url(r'^bedankt/$', bedankt, name='bedankt'),
    url(r'^aanmelden/$', leden, name='leden'),
    url(r'^overmijndenbosch/$', about, name='about'),
    url(r'^burgermeesters/$', burgemeesters, name='burgemeesters'),
    url(r'^initiatieven/$', initiatieven, name='initiatieven'),
    url(r'^netwerk/([0-9]+)/$', bijeenkomst, name='bijeenkomst'),
]
