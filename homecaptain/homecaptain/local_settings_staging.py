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
    '52.14.116.20'
]
GOOGLE_OAUTH_CLIENT_ID = "405077832351-lp98abenhf75jsj416g6126osglhhk2u.apps.googleusercontent.com"

AWS_ACCESS_KEY_ID = "AKIAI2UYZ7H3RBEBZK7A"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = 'homecaptainstaging'
AWS_PROPERTY_PHOTOS_BUCKET_NAME = AWS_BUCKET_NAME

GEOCODIO_API_KEY = "bc153b336dd3651b6137cbebb5d55bcc5eccb53"
SENDGRID_API_KEY = "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"
