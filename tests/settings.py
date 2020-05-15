DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'tests.apps.TestsConfig',
    'auto_rest.apps.AutoRestConfig',
    'rest_framework',
]

MIDDLEWARE = []

ROOT_URLCONF = 'tests.urls'

USE_TZ = True

TIME_ZONE = 'UTC'

SECRET_KEY = 'sy_8e3q=h!-%#w5p1(j(&czrh=43$z@t$@e@*t_c&5t$tdgul$'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]

STATIC_URL = '/static/'