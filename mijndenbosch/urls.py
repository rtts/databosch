from django.conf.urls import url, include
from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from .views import *

urlpatterns = [
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', homepage, name='homepage'),
    url(r'^bedankt/$', bedankt, name='bedankt'),
    url(r'^aanmelden/$', aanmelden, name='leden'),
    url(r'^rapporteren/$', rapporteren, name='rapporteren'),
    url(r'^overmijndenbosch/$', about, name='about'),
    url(r'^burgermeesters/$', burgemeesters, name='burgemeesters'),
    url(r'^initiatieven/$', initiatieven, name='initiatieven'),
    url(r'^nieuws/$', news, name='news'),
    url(r'^netwerk/([0-9]+)/$', bijeenkomst, name='bijeenkomst'),
]
