from .base import *

DEBUG = True

INSTALLED_APPS.append('debug_toolbar')

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_1kLoQNn9SVTZ25CghCwPQmXz')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_Y9Z36QsHRrO51HIQiAeZo7DO')

#SITE_URL = 'http://127.0.0.1:8000'
#PAYPAL_NOTIFY_URL = '<your ngrok URL>'
#PAYPAL_RECEIVER_EMAIL = '<your paypal merchant email>'

PAYPAL_TEST = True
#SITE_URL = 'http://1e5f29c0.ngrok.io'
SITE_URL = 'http://arnold-j-social-staging.herokuapp.com/'
PAYPAL_NOTIFY_URL = 'http://arnold-j-social-staging.herokuapp.com/' \
                    '/a-very-hard-to-guess-url/'
PAYPAL_RECEIVER_EMAIL = 'arnold-j831@sky.com'