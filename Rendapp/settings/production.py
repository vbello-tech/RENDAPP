from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': 'V0IBvvzHtbxwylN9xL75',
       'HOST': 'containers-us-west-42.railway.app',
       'PORT': '6652',
   }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhzn9oqey',
    'API_KEY': '894294618768234',
    'API_SECRET': '8fqL8OfZKqSJChXcObtsRWqefPQ'
}

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True



