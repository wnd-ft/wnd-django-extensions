# Bare ``settings.py`` for running tests for wnd_django_extension

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sample_app.sqlite',
    }
}

INSTALLED_APPS = (
    'sample_app',
)
