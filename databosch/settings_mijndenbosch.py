from .settings_common import *

ROOT_URLCONF = 'databosch.urls_mijndenbosch'
WSGI_APPLICATION = 'databosch.wsgi_mijndenbosch.application'
DEFAULT_FROM_EMAIL = 'info@mijndenbosch.nl'
LOGIN_REDIRECT_URL = '/aanmelden/'
SITE_ID = 3
