# core/settings.py
# ─────────────────────────────────────────────
# Production-ready settings for ShopHub
# ─────────────────────────────────────────────

from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────
SECRET_KEY   = config('SECRET_KEY', default='your-secret-key-here')
DEBUG        = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['*']

# ── Installed Apps ────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',

    # Our apps
    'accounts',
    'sellers',
    'products',
    'orders',
    'payments',
]

# ── Middleware ────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ── Templates ─────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# ── Database ──────────────────────────────────
# Uses DATABASE_URL on Railway, falls back to local PostgreSQL
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     config('DB_NAME',     default='multivendor_db'),
            'USER':     config('DB_USER',     default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST':     config('DB_HOST',     default='localhost'),
            'PORT':     config('DB_PORT',     default='5432'),
        }
    }

# ── Custom User Model ─────────────────────────
AUTH_USER_MODEL = 'accounts.User'

# ── Password Validators ───────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Localization ──────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True

# ── Static Files ──────────────────────────────
STATIC_URL    = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT   = BASE_DIR / 'staticfiles'

# Whitenoise serves static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media Files ───────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
  # ── Cloudinary Image Storage ──────────────────
import cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY':    config('CLOUDINARY_API_KEY',    default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ── Auth ──────────────────────────────────────
AUTH_USER_MODEL       = 'accounts.User'
LOGIN_URL             = '/accounts/login/'
LOGIN_REDIRECT_URL    = '/'
LOGOUT_REDIRECT_URL   = '/'

# ── Crispy Forms ──────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

# ── Stripe ────────────────────────────────────
STRIPE_PUBLIC_KEY      = config('STRIPE_PUBLIC_KEY',      default='')
STRIPE_SECRET_KEY      = config('STRIPE_SECRET_KEY',      default='')
STRIPE_WEBHOOK_SECRET  = config('STRIPE_WEBHOOK_SECRET',  default='')

# ── Celery ────────────────────────────────────
CELERY_BROKER_URL    = config('CELERY_BROKER_URL',    default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND= config('CELERY_RESULT_BACKEND',default='redis://localhost:6379/0')

# ── Email ─────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ── Default Primary Key ───────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
