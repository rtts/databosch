import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'yp9k@_(2+k^waqwds&6)h)2%z()&uo@1+0_wb!y98cy31(%7$+'
DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'algemeen.Persoon'
ROOT_URLCONF = 'databosch.urls'
WSGI_APPLICATION = 'databosch.wsgi.application'
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/databosch/uploads'
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/databosch/static'
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static')]
CKEDITOR_JQUERY_URL = '/static/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'elementspath',
        'contentsCss': STATIC_URL + 'ckeditor.css',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['Source'],
        ]
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'ckeditor',
    'algemeen',
    'maakdenbosch',
    'mijndenbosch',
    'noelsportfolio',
    'noelswebsite',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'databosch',
    }
}
