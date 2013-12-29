from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

MANAGERS = \
ADMINS = (
    (get_env_variable('ADMIN_NAME'), get_env_variable('ADMIN_EMAIL')),
)

# this SECRET_KEY is for development only and should not be used in production!
SECRET_KEY = 'o6gdkz#yeiex-ifc8q7ut(*t8l8z7+)4bj)jvq8k2nzu0y(=uu'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'default.sqlite3'),
    },
}

MINIMUM_CONFIRMATIONS = 2

# django-debug-toolbar
if False:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda r: True,
    }
