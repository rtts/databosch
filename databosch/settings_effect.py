import os
import effect
from .settings_common import *

ROOT_URLCONF = 'effect.urls'
WSGI_APPLICATION = 'databosch.wsgi_effect.application'
SITE_ID = 7
INSTALLED_APPS += ['sass_processor']
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(effect.__file__)), 'static')
