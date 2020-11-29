"""
FILE TO CONTAIN SETTINGS REQUIRED FOR TESTING ON BITBUCKET PIPELINES
"""
DATABASES = {
    #https://confluence.atlassian.com/bitbucket/how-to-run-common-databases-in-bitbucket-pipelines-891130454.html
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            #"init_command": "SET storage_engine=INNODB",
        }
    },
}
DOMAIN = 'local.homecaptain.com'
GOOGLE_OAUTH_CLIENT_ID = ""
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AWS_ACCESS_KEY_ID = "AKIAI2UYZ7H3RBEBZK7A"
AWS_SECRET_ACCESS_KEY = "joMwQ+kAd5JHXYKQu9UxR5V9JgPZdIjvnR0dTRTv"
AWS_BUCKET_NAME = 'homecaptainlocal'
AWS_PROPERTY_PHOTOS_BUCKET_NAME = AWS_BUCKET_NAME
SAMPLE_MLS_DATA_FILE = ""
COUNT_OF_MLS_PROPERTIES_TO_PARSE = 0
GEOCODIO_API_KEY = ""
SENDGRID_API_KEY = ""
