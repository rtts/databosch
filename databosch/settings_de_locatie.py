import os
import de_locatie
from .settings_common import *

ROOT_URLCONF = 'de_locatie.urls'
ALLOWED_HOSTS += ['locatie.created.today']
WSGI_APPLICATION = 'databosch.wsgi_de_locatie.application'
SITE_ID = 6
INSTALLED_APPS += ['sass_processor']
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(de_locatie.__file__)), 'static')
