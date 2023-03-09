from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': '7nv31eSha6NM3ifBtIBm',
       'HOST': 'containers-us-west-35.railway.app',
       'PORT': '5585',
   }
}

"""

DATABASES = {
    'default':  dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
"""




STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUD_NAME = config('CLOUD_NAME')
API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUD_NAME,
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
}

#SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True


