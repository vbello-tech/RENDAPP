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
       'PASSWORD': 'Y0udseVvOSczwZ2fQ7dg',
       'HOST': 'containers-us-west-72.railway.app',
       'PORT': '7594',
   }
}

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # new
#DEFAULT_FROM_EMAIL = 'vbellotech@gmail.com'
EMAIL_HOST = 'smtp.mailjet.com' # new
EMAIL_HOST_USER = 'in-v3.mailjet.com'
EMAIL_HOST_PASSWORD = '8c2d3b7759f49b463ebd62dbd415a380' # api_key
EMAIL_PORT = 587 # new
EMAIL_USE_TLS = True # new


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



