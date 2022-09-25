from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
"""

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': 'b7FPfaNadSuRD0fOQZ1b',
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


#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#MAILJET
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
ANYMAIL = {
    "MAILJET_API_KEY": '8c2d3b7759f49b463ebd62dbd415a380',
    "MAILJET_SECRET_KEY": '158c6fbdb8ccf038f6bfe1b55df84b16',
}
DEFAULT_FROM_EMAIL = 'vbellotech@gmail.com'



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


db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)


