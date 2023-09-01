from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

PASSWORD = config('PASSWORD')
HOST = config('HOST')

DATABASES = {
    'default':  dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

#PRODUCTION SETTINGS
CSRF_TRUSTED_ORIGINS = ['https://rendapp.up.railway.app']
CORS_ORIGIN_ALLOW_ALL = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

#MEDIA AND STATIC
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

#MAIL
MAILJET_API_KEY = config('MAILJET_API_KEY')
MAILJET_SECRET_KEY = config('MAILJET_SECRET_KEY')

ANYMAIL = {
    "MAILJET_API_KEY": MAILJET_API_KEY,
    "MAILJET_SECRET_KEY": MAILJET_SECRET_KEY,
}
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
DEFAULT_FROM_EMAIL = 'vbellotech@gmail.com'
SERVER_EMAIL = 'vbellotech@gmail.com'


