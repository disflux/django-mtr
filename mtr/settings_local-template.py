# Set DEBUG=True to enable debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

MEDIA_ROOT = '/home/derek/web/media/'

STATIC_ROOT = '/home/derek/web/previewstatic/static/'

# use gmail for sending email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
SERVER_EMAIL = ''

SECRET_KEY = ''

# Amazon AWS Access Credentials
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_IS_GZIPPED = True

# Uncomment the following line to store static files on Amazon S3
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

