from .settings_common import *

ROOT_URLCONF = 'de_locatie.urls'
ALLOWED_HOSTS += ['locatie.created.today']
WSGI_APPLICATION = 'databosch.wsgi_de_locatie.application'
SITE_ID = 6
