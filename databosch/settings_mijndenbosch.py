from .settings_common import *

CONTACT_FORM_RECIPIENTS = ['jj@rtts.eu', 'noel@mijndenbosch.nl']
ROOT_URLCONF = 'mijndenbosch.urls'
WSGI_APPLICATION = 'databosch.wsgi_mijndenbosch.application'
DEFAULT_FROM_EMAIL = 'info@mijndenbosch.nl'
LOGIN_REDIRECT_URL = '/aanmelden/'
SITE_ID = 3
