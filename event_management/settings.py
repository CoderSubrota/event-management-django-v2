import environ 
env = environ.Env()
environ.Env.read_env()
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_r0ib69s^06^0+gf4=m%d!^^!(!+_zp=0&qi(258+nm-)_f!tc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1','event-management-qcfb.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'debug_toolbar',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'event_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR ,"templates"],
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

WSGI_APPLICATION = 'event_management.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', 
]


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# sqlite3 database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# postgres sql database 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'events_databases',   
        'USER': 'postgres',
        'PASSWORD': 'subrota12',
        'HOST': 'localhost',  
        'PORT': '5432',
    }
}

# Replace the SQLite DATABASES configuration with PostgreSQL:

# DATABASES = {
#     'default': dj_database_url.config(
#         # Replace this value with your local database's connection string.
#         default='postgresql://event_management_rl21_user:XnPaWuAtrRkdzhIwpIxJgdMPem05qSuF@dpg-cuar0k2n91rc738v11rg-a.oregon-postgres.render.com/event_management_rl21',
#         conn_max_age=600
#     )
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

CSRF_TRUSTED_ORIGINS = [
    "https://event-management-qcfb.onrender.com",
]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "event-management-qcfb.onrender.com"
    # ...
]
 
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# sending email setting 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = env('EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD') 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FRONTEND_URL = "http://127.0.0.1:8000/"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

