"""
Django settings for irsc project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os,awsses

from django.utils.translation import ugettext_lazy as _
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#APPEND_SLASH = False
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's2$nm@2c5gfs#xd_vrzupf=6yyv-_)kd*m_uv0xc^^yfxy3*ly'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   
# GEOIP_PATH = os.path.join(BASE_DIR,'ip')


aws_sns_ip = [
        #US-EAST-1
        '207.171.167.101',
        '207.171.167.25',
        '207.171.167.26',
        '207.171.172.6',
        '54.239.98.0/24',
        '54.240.217.16/29',
        '54.240.217.8/29',
        '54.240.217.64/28',
        '54.240.217.80/29',
        '72.21.196.64/29',
        '72.21.198.64/29',
        '72.21.198.72',
        '72.21.217.0/24',
        #US-WEST-1
        '204.246.160.32/28',
        '204.246.162.32/28',
        '54.240.198.0/24',

        #US-WEST-2
        '205.251.233.32/28',
        '205.251.233.48/29',
        '205.251.233.160/28',
        '205.251.233.176/29',
        '205.251.234.32/28',
        '54.240.230.176/29',
        '54.240.230.184/29',
        '54.240.230.240/29',

        #EU-WEST-1
        '87.238.84.64/29',
        '87.238.80.64/29',
        '54.240.197.0/24',
        '54.239.99.0/24',

        #EU-CENTRAL-1
        '54.239.6.0/24',

        #AP-SOUTHEAST-1
        '203.83.220.24/29',
        '203.83.220.152/29',
        '54.240.199.0/24',

        #AP-SOUTHEAST-2
        '54.240.194.0/27',
        '54.240.194.16/28',
        '54.240.194.64/27',
        '54.240.194.80/28',
        '54.240.194.128/27',
        '54.240.194.144/28',
        '54.240.193.0/29',
        '54.240.193.128/29',

        #AP-NORTHEAST-1
        '27.0.1.24/29',
        '27.0.1.152/29',
        '54.240.200.0/24',
        '27.0.3.144/29',
        '27.0.3.152/29',

        #SA-EAST-1
        '177.72.241.96/28',
        '177.72.241.112/28',
        '177.72.241.160/28',
        '177.72.241.176/28',
        '177.72.242.96/28',
        '177.72.242.112/28',
        '177.72.241.16/29',
        '177.72.242.16/29',
        '177.72.247.128/28',
        '177.72.247.144/29',

        #some
        '34.221.192.214',
        '52.38.66.198',
        '34.216.25.49',
]

ALLOWED_HOSTS = ['irsc.us-west-2.elasticbeanstalk.com','irsc2.ghdcpf7vep.us-west-2.elasticbeanstalk.com','irsc22.etiumbh7a8.us-west-2.elasticbeanstalk.com','127.0.0.1','localhost','road-safety.co.in','www.road-safety.co.in','ww2.road-safety.co.in','irsc.road-safety.co.in'] + aws_sns_ip




# Application definition

LOGIN_REDIRECT_URL = 'social_login'
AUTH_USER_MODEL = 'irscuser.User'
SOCIAL_AUTH_USER_MODEL = 'irscuser.User'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = 'social_login'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'irscuser.apps.IrscuserConfig',
    'drivingtest.apps.DrivingtestConfig',
    'isafe.apps.IsafeConfig',
    'cityhead.apps.CityheadConfig',
    'home.apps.HomeConfig',
    'morthportal.apps.MorthportalConfig',
    'policyportal.apps.PolicyportalConfig',
    'policyportal2020.apps.Policyportal2020Config',
    'hackhome.apps.HomeConfig',
    'ICSM19.apps.Icsm19Config',
    'social_django',
    'modeltranslation',
    'import_export',
    'newsportal',
    'certificate_app',

]




AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',
 'social_core.backends.google.GoogleOpenId',
 'social_core.backends.google.GoogleOAuth2',
 'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'irsc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['home/templates','gsl/templates','ICSM19/templates','hackhome/templates','isafe/templates/','drivingtest/templates/','cityhead/templates','newsportal/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
'https://www.googleapis.com/auth/plus.login',
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

WSGI_APPLICATION = 'irsc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'demos',
            'USER':'postgres',
            'PASSWORD':'9592864914',
            'HOST':'localhost',
        }
    }
else:
    DATABASES = {
        'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME':awsses.RDS_NAME,
        'USER':awsses.RDS_USER,
        'PASSWORD':awsses.RDS_PASSWORD,
        'HOST':awsses.RDS_HOST,
        'PORT':'5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


EMAIL = 'irsc.gov@gmail.com'

PASSWORD = 'Jhabar@123'

#Email Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = PASSWORD
EMAIL_USE_TLS = True

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('hi', _('Hindi')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'hi')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

#set S3 as the place to store your files.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = awsses.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = awsses.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = awsses.S3_BUCKET_NAME
AWS_QUERYSTRING_AUTH = False #This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'

#static media settings

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

#Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}



# Celery
BROKER_URL = "sqs://%s:%s@" % (awsses.AWS_ACCESS_KEY_ID, awsses.AWS_SECRET_ACCESS_KEY)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'celery'
CELERY_RESULT_BACKEND = None # Disabling the results backend
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULE = {}
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',
    'polling_interval': 1,
    'visibility_timeout': 20000,
}




#-----Google Ouath--------------------#
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =awsses.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = awsses.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET


TOKEN_URL = 'http://localhost:8000/intern/register-token'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = EMAIL
# EMAIL_HOST_PASSWORD = PASSWORD
# EMAIL_USE_TLS = True

# LOGIN_URL = 'certificate_app:login'

FP_TOKEN_URL = 'http://localhost:8000/intern/forgot-password-token'