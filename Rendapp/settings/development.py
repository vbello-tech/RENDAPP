from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
"""


ANYMAIL = {
    "MAILJET_API_KEY": '8c2d3b7759f49b463ebd62dbd415a380',
    "MAILJET_SECRET_KEY": '158c6fbdb8ccf038f6bfe1b55df84b16',
}
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
DEFAULT_FROM_EMAIL = 'vbellotech@gmail.com'
SERVER_EMAIL = 'vbellotech@gmail.com'
