import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}
SECRET_KEY = '1%m#fx+rht9h%ojl+-3()xxg#^&$*8-k8bmq3p8$olgx7iz*5g'

ROOT_URLCONF = 'test_app.urls'
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'db_email_backend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DEFAULT_FILE_STORAGE = 'test_app.storage.TestStorage'

MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

try:
    import south
except:
    pass
else:
    INSTALLED_APPS += ('south',)
