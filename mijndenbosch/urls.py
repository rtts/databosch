from django.conf import settings
from django.conf.urls import url, include
from django.http import HttpResponse
from .forms import *
from .views import *

def toolkit(request):
    response = HttpResponse()
    response['Content-Disposition'] = "attachment; filename=toolkit.zip"
    response['X-Accel-Redirect'] = "{}toolkit.zip".format(settings.STATIC_URL)
    return response

urlpatterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', homepage, name='homepage'),
    url(r'^bedankt_oud/$', bedankt, name='bedankt'),
    url(r'^klaar/$', klaar, name='klaar'),
    url(r'^bedankt/$', thanks, name='thanks'),
    url(r'^aanmelden/$', submit, name='aanmelden'),
    url(r'^aanmelden/persoon/$', submit_person, name='submit_person'),
    url(r'^aanmelden/netwerk/$', submit_entity, name='submit_entity'),
    url(r'^aanmelden/bijeenkomst/$', submit_meeting, name='submit_meeting'),
    url(r'^aanmelden/deelnemers/$', submit_participants, name='submit_participants'),
    url(r'^aanmelden/burgermeester/$', submit_mayor, name='submit_mayor'),
    url(r'^overmijndenbosch/$', about, name='about'),
    url(r'^burgermeesters/$', mayors, name='mayors'),
    url(r'^speerpunten/$', ideas, name='ideas'),
    url(r'^burgermeester/([0-9]+)/$', mayor, name='mayor'),
    url(r'^burgermeesters_oud/$', burgermeesters, name='burgermeesters'),
    url(r'^burgermeester_oud/([0-9]+)/$', burgermeester, name='burgermeester'),
    url(r'^initiatieven/$', initiatieven, name='initiatieven'),
    url(r'^nieuws/$', news, name='news'),
    url(r'^bijeenkomst/([0-9]+)/$', bijeenkomst, name='bijeenkomst'),
    url(r'^toolkit/$', toolkit),
    url(r'^([^/]+)/$', netwerk, name='netwerk'),
]
