"""
WSGI config for dogetrader project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from dogetrader.environment import source_environment_vars
source_environment_vars()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
