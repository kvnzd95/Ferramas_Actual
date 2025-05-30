# archivo: usuario_service/usuario_service/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad y debug
SECRET_KEY = 'django-insecure-8jpeu($h8dmw^a2@^35xxmba77b#4dnhy2xh*ep!nd+n&2k3tb'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Puedes restringirlo más en producción

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Aplicaciones instaladas
INSTALLED_APPS = [
    'corsheaders',               # CORS arriba de cualquier app que sirva respuestas
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',            # Django REST Framework
    'rest_framework.authtoken',  # Token auth para DRF

    'cuentas',                   # Tu app de usuarios
    "drf_yasg",
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # Debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'usuario_service.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],               # Si necesitas carpetas globales, agrégalas aquí
        'APP_DIRS': True,         # Busca en templates/ de cada app
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

WSGI_APPLICATION = 'usuario_service.wsgi.application'

# Base de datos (MySQL en Docker)
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'Usuario',        # ← aquí
        'USER':     'Usuario',        # ← aquí
        'PASSWORD': 'Usuario123',     # ← aquí
        'HOST':     'mysql',
        'PORT':     '3306',
    }
}

# Auth User Model
AUTH_USER_MODEL = 'cuentas.Usuario'

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# CORS: permitir orígenes del frontend
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# O bien, más restrictivo:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://frontend:8000",
# ]

# DRF: Token Authentication + JSON/Form parsers + permisos
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ],
}

# Archivos estáticos por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
