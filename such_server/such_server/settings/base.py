import os
from django.core.exceptions import ImproperlyConfigured

from ..environment import VARIABLE_PREFIX


def get_env_variable(var_name, prefix=VARIABLE_PREFIX, as_bool=False):
    """
    Get the environment variable or raise exception
    """
    if prefix is not None:
        var_name = prefix + var_name

    try:
        value = os.environ[var_name]
        if as_bool:
            value = value.lower() == 'true'
        return value
    except KeyError:
        raise ImproperlyConfigured('Set the %s environment variable' % var_name)


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = []
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '../very_frontend/app'),
    os.path.join(PROJECT_DIR, '../very_frontend/.tmp'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'users.EmailUser'

ROOT_URLCONF = 'such_server.urls'

WSGI_APPLICATION = 'such_server.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, '../very_frontend/app'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'core',
    'users',
    'wallets',
    'markets',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['stdout'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

CLEARED_FUNDS_ACCOUNT = 'FUNDS'
MINIMUM_CONFIRMATIONS = 15

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None,
    'URL_ACCEPT_OVERRIDE': None,
    'URL_FORMAT_OVERRIDE': None,
}
