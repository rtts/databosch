from .settings_common import *

ALLOWED_HOSTS += ['www.databosch.nl']
ROOT_URLCONF = 'databosch.urls_databosch'
WSGI_APPLICATION = 'databosch.wsgi_databosch.application'
SITE_ID = 1
