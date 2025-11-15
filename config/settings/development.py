from .base import *

# Debug activé en développement
DEBUG = True

# Secret Key pour le développement
SECRET_KEY = 'django-insecure-2wkka6l2m@x@*u03^21s!_bvv6@3l6-pjv$b$41m)8cl(lg7rg'

# Hosts autorisés en développement
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# Database SQLite pour le développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # ne pas changer
        'NAME': 'dige',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',  # ou localhost
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'isolation_level': None,
        },
    }
}


# Configuration email pour le développement
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django Debug Toolbar (si installé)
INSTALLED_APPS += [
    #
]

MIDDLEWARE += [
    #
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Configuration CORS pour le développement
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Static files configuration développement
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging en développement
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}