# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
- Use mailgun to send emails
'''
from django.utils import six

from .common import *  # noqa

import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://bc3bb944a4244c7a8cbd1a9bb74600f1:2639868d150a4bc4a901d817c740a18d@sentry.io/265798',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = "lh6ys+!cvm+s+2nl7^!n3-331rmytc!2+_4qmedh!dtk!o-khu"

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# django-secure
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("djangosecure","raven.contrib.django.raven_compat")

SECURITY_MIDDLEWARE = (
  #  'djangosecure.middleware.SecurityMiddleware',
)

#MIDDLEWARE_CLASSES = ()
# Make sure djangosecure.middleware.SecurityMiddleware is listed first
MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + MIDDLEWARE_CLASSES

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
#SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
 #   "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
#SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)
#SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
#    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
#SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
#SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='example.com')
ALLOWED_HOSTS = ["social-creative.online", "www.social-creative.online"]
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn",)


HTTP_ACCEPT = True

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='sc_main <noreply@domain_name')
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env('DJANGO_MAILGUN_API_KEY')
MAILGUN_SERVER_NAME = env('DJANGO_MAILGUN_SERVER_NAME')
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default='[sc_main] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DATABASE_URL")

# CACHING
# ------------------------------------------------------------------------------
# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "{0}/{1}".format(env.cache_url('REDIS_URL', default="redis://127.0.0.1:6379"), 0),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
    }
}
# Custom Admin URL
#ADMIN_URL = env('DJANGO_ADMIN_URL')

# Your production stuff: Below this line define 3rd party library settings
