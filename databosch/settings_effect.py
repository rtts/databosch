import os
import effect
from .settings_common import *

ALLOWED_HOSTS += ['www.effectfestival.nl']
ROOT_URLCONF = 'effect.urls'
WSGI_APPLICATION = 'databosch.wsgi_effect.application'
SITE_ID = 7
ALLOWED_HOSTS += ['effect.created.today', 'effectfestival.nl', 'www.effectfestival.nl']
INSTALLED_APPS += ['sass_processor']
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(effect.__file__)), 'static')
