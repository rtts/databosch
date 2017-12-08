import os
import rauwkost
from .settings_common import *

ROOT_URLCONF = 'rauwkost.urls'
WSGI_APPLICATION = 'databosch.wsgi_rauwkost.application'
SITE_ID = 8
ALLOWED_HOSTS += ['www.rauwkost.online']
#MIDDLEWARE += ['tidy.middleware.TidyMiddleware']
INSTALLED_APPS += ['sass_processor']
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(rauwkost.__file__)), 'static')
