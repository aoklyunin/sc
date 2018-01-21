"""
WSGI config for repo_name project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise

sys.path.append('/opt/bitnami/apps/django/django_projects/sc')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/sc/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sc_main.settings.production")
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
