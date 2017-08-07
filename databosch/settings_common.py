import os

try:
    import uwsgi
    DEBUG = False
except ImportError:
    DEBUG = True

ADMINS = [('JJ Vens', 'jj@rtts.eu')]
ALLOWED_HOSTS = ['databosch.created.today', 'mijndenbosch.nl', 'jadb.created.today', 'localhost']
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
SECRET_KEY = 'yp9k@_(2+k^waqwds&6)h)2%z()&uo@1+0_wb!y98cy31(%7$+'
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/databosch/uploads'
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/databosch/static'
CKEDITOR_JQUERY_URL = '/static/jquery.min.js'
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = '/accounts/login/'

SANITIZER_ALLOWED_TAGS = [
    'a', 'b', 'blockquote', 'code', 'del', 'em', 'h1', 'h2', 'h3', 'i', 'ins', 'li', 'ol', 'p', 'pre', 'sup', 'sub', 'strong', 'ul', 'br', 'hr',
]

SANITIZER_ALLOWED_ATTRIBUTES = [
    'href', 'title',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'elementspath',
        # 'contentsCss': STATIC_URL + 'ckeditor.css',
        'width': '100%',
        'toolbar': 'Custom',
        'allowedContent': True, # this allows iframes, embeds, scripts, etc...
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['Source'],
        ]
    }
}

THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (400, 400), 'crop': False},
        'medium': {'size': (600, 600), 'crop': False},
        'large': {'size': (800, 800), 'crop': False},
    },
}

INSTALLED_APPS = [
    'maakdenbosch',
    'mijndenbosch',
    'jadb',
    'effect',
    'de_locatie',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_cleanup', # this has to be disabled during data migrations
    'embed_video',
    'ckeditor',
    'sanitizer',
    'easy_thumbnails',
]

if DEBUG:
    INSTALLED_APPS += [
        #'debug_toolbar',
        'django_extensions',
    ]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
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
        'USER': 'databosch',
        'NAME': 'databosch',
    }
}
