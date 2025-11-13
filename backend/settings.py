import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# 🌍 Общие настройки
# =======================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.vercel.app',
    '.su-college.com',
    '.herokuapp.com',
    'su-college-back-0fa585fe0710.herokuapp.com',
]

# =======================
# 🌐 Языки и локализация
# =======================
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Russian'),
    ('ky', 'Kyrgyz'),
    ('en', 'English'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

USE_I18N = True
USE_TZ = True
TIME_ZONE = 'Asia/Bishkek'

# =======================
# 🔒 CORS и безопасность
# =======================
INSTALLED_APPS = [
    'unfold',  # before django.contrib.admin
    'unfold.contrib.filters',  # optional, if special filters are needed
    'unfold.contrib.forms',  # optional, if special form elements are needed
    'unfold.contrib.inlines',  # optional, if special inlines are needed
    # 'unfold.contrib.import_export',  # optional, if django-import-export package is used
    # 'unfold.contrib.guardian',  # optional, if django-guardian package is used
    # 'unfold.contrib.simple_history',  # optional, if django-simple-history package is used
    # 'unfold.contrib.location_field',  # optional, if django-location-field package is used
    # 'unfold.contrib.constance',  # optional, if django-constance package is used
    'django.contrib.admin',  # required
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'corsheaders',
    'storages',

    # твои приложения
    'teachers',
    'news_app',
    'council_app',
    'projects_app',
    'resources_app',
    'vacancies_app',
    'schedule_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://www.su-college.com",
    "https://su-college.com",
    "http://localhost:5173",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

# =======================
# 🧱 Django настройки
# =======================
ROOT_URLCONF = 'backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'backend.wsgi.application'

# =======================
# 💾 База данных
# =======================
# Локально SQLite, на Heroku автоматически PostgreSQL
if 'DATABASE_URL' in os.environ:
    # На Heroku используем PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Локально используем SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =======================
# 🔐 Валидация паролей
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =======================
# 🌍 REST Framework
# =======================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# =======================
# 🖼️ Медиа и статика
# =======================

# ========== DigitalOcean Spaces ==========
USE_SPACES = os.getenv('USE_SPACES', 'False') == 'True'

if USE_SPACES:
    # Настройки для DigitalOcean Spaces (S3-compatible)
    AWS_ACCESS_KEY_ID = os.getenv('SPACES_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('SPACES_SECRET')
    AWS_STORAGE_BUCKET_NAME = os.getenv('SPACES_NAME')
    AWS_S3_REGION_NAME = os.getenv('SPACES_REGION', 'nyc3')
    AWS_S3_ENDPOINT_URL = os.getenv('SPACES_ENDPOINT')
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
    
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    
    # Используем STORAGES (Django 4.2+)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    
    # Статика
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    # Локальные настройки (без Spaces)
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =======================
# 🔒 Настройки безопасности для продакшена
# =======================
# Включаем только на Heroku (когда есть DATABASE_URL в окружении)
IS_HEROKU = 'DATABASE_URL' in os.environ

if not DEBUG and IS_HEROKU:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
