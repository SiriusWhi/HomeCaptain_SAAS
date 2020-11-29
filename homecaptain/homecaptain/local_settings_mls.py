from celery.schedules import crontab
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'homecaptain',
        'USER': 'homecaptain',
        'PASSWORD': 'HomeCaptain18',
        'HOST': 'hc-staging-db-for-mls.cuqgyzdqxkdt.us-east-2.rds.amazonaws.com',
        'PORT': '',
        'OPTIONS': {
            #"init_command": "SET storage_engine=INNODB",
        }
    },
}
SCHEME = 'https'
DOMAIN = 'staging.homecaptain.com'
OTHER_ALLOWED_HOSTS = [
]
GOOGLE_OAUTH_CLIENT_ID = "405077832351-lp98abenhf75jsj416g6126osglhhk2u.apps.googleusercontent.com"

AWS_ACCESS_KEY_ID = "AKIAI2UYZ7H3RBEBZK7A"
AWS_SECRET_ACCESS_KEY = "joMwQ+kAd5JHXYKQu9UxR5V9JgPZdIjvnR0dTRTv"
AWS_BUCKET_NAME = 'homecaptainstaging'
AWS_PROPERTY_PHOTOS_BUCKET_NAME = AWS_BUCKET_NAME

SAMPLE_MLS_DATA_FILE = "bjl.xml"
COUNT_OF_MLS_PROPERTIES_TO_PARSE = 500
GEOCODIO_API_KEY = "bc153b336dd3651b6137cbebb5d55bcc5eccb53"
CELERY_BEAT_SCHEDULE = {
    'parse-latest-mls-feed': {
        'task': 'parse-mls-feed',
        'schedule': crontab(hour='*/12'),
    },
}
