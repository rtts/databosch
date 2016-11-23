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
    url(r'^accounts/register/$', Aanmelden.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', homepage, name='homepage'),
    url(r'^bedankt_oud/$', bedankt, name='bedankt'),
    url(r'^klaar/$', klaar, name='klaar'),
    url(r'^aanmelden/$', submit_mayor, name='submit_mayor'),
    url(r'^bedankt/$', thanks, name='thanks'),
    url(r'^stappenplan/$', aanmelden, name='aanmelden'),
    url(r'^overmijndenbosch/$', about, name='about'),
    url(r'^burgermeesters/$', mayors, name='mayors'),
    url(r'^burgermeester/([0-9]+)/$', mayor, name='mayor'),
    url(r'^burgermeesters_oud/$', burgermeesters, name='burgermeesters'),
    url(r'^burgermeester_oud/([0-9]+)/$', burgermeester, name='burgermeester'),
    url(r'^initiatieven/$', initiatieven, name='initiatieven'),
    url(r'^nieuws/$', news, name='news'),
    url(r'^bijeenkomst/([0-9]+)/$', bijeenkomst, name='bijeenkomst'),
    url(r'^toolkit/$', toolkit),
    url(r'^([^/]+)/$', netwerk, name='netwerk'),
]
