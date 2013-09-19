import os
DIRNAME = os.path.dirname(__file__)

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

# PDF Generation settings
PDF_INSPECTION_REPORT_TEMPLATE = os.path.join(DIRNAME,
                                              '../templates/pdfgen/inspection_report.pdf')
PDF_BARCODE_STYLE = 'Code128' # Options: Code128, Code39
PDF_COMPANY_NAME = 'TSA MFG'
PDF_COMPANY_SHORT_NAME = 'TSA'
PDF_COMPANY_STREET = '14901 Chandler Rd'
PDF_COMPANY_LOCALITY = 'Omaha, NE'
PDF_COMPANY_ZIPCODE = '68138'
PDF_COMPANY_PHONE = '800-228-2948'
PDF_COMPANY_FAX = '402-895-3297'

# sorl-thumbnail Settings
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_QUALITY = 95
THUMBNAIL_COLORSPACE = 'GRAY'
THUMBNAIL_FORMAT = 'PNG'

# Database Backup Settings
AWS_ACCESS_KEY = AWS_ACCESS_KEY_ID
AWS_SECRET_KEY = AWS_SECRET_ACCESS_KEY
EASYDUMP_MANIFESTS = {
    'default': {
        'database': 'default',
        's3-bucket': 'tsa_database_dumps',
        'reduced-redundancy': False
    }
}


# Interfax FAX Settings
INTERFAX_USER = ''
INTERFAX_PASSWORD = ''
INTERFAX_TEST_NUMBER = ''

# Uncomment the following line to store static files on Amazon S3
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

