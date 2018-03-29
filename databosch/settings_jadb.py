from .settings_common import *

ALLOWED_HOSTS += ['jadb.created.today']
ROOT_URLCONF = 'jadb.urls'
WSGI_APPLICATION = 'databosch.wsgi_jadb.application'
DEFAULT_FROM_EMAIL = 'jj@rtts.eu'
SITE_ID = 5
