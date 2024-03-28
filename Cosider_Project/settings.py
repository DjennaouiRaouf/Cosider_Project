import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'colorfield',
    'djangoql',
    'safedelete',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'import_export',
    'api_sm',
    'api_sch',
    'forms',





]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True



ROOT_URLCONF = 'Cosider_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Cosider_Project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sm.sqlite3',
    },
}
'''

DATABASES = {
    'default': {
        "ENGINE": "mssql",
        "NAME": "sm",
        "USER":"",
        "PASSWORD":"",
        "HOST": "localhost",
        "PORT":"1433",
        "OPTIONS": {"driver": "ODBC Driver 13 for SQL Server",
                    'MARS_Connection': 'True',  # Enable Multiple Active Result Sets
                    'host_is_server': 'True',  # Optimize connection settings
        },
        'CONN_MAX_AGE': 600,

    },
    'ca_ch': {
        "ENGINE": "mssql",
        "NAME": "ca_ch",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 13 for SQL Server",
                    'MARS_Connection': 'True',  # Enable Multiple Active Result Sets
                    'host_is_server': 'True',  # Optimize connection settings
                    },
                'CONN_MAX_AGE': 600,

    },

}
'''


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


SESSION_ENGINE = "django.contrib.sessions.backends.db"


LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates','build', 'static'),
    os.path.join(BASE_DIR, "media"),
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
     ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],

}



