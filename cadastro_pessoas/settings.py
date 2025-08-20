import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Modelo customizado de usuário
AUTH_USER_MODEL = 'usuarios.Usuario'

# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Deve vir antes do django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'publico',
    'empresa',
    'frequencia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cadastro_pessoas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'empresa.context_processors.empresa_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'cadastro_pessoas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Cuiaba'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configurações de Email
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# URL do site para links de ativação
SITE_URL = config('SITE_URL', default='http://127.0.0.1:8000')

# Configurações de timeout para evitar travamento
EMAIL_TIMEOUT = 10  # Timeout de 10 segundos
EMAIL_USE_SSL = False  # Usar TLS em vez de SSL

# Configurações do Celery
CELERY_BROKER_URL = 'memory://'  # Broker em memória para desenvolvimento
CELERY_RESULT_BACKEND = None  # Sem backend para desenvolvimento simples
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'

# Configurações específicas para tarefas de email
CELERY_TASK_ROUTES = {
    'usuarios.tasks.enviar_email_verificacao_task': {'queue': 'default'},
}

# Configurações de filas
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

# Configurações para evitar timeouts
CELERY_TASK_ALWAYS_EAGER = True  # Executar tarefas sincronamente para desenvolvimento
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True

# Configurações de timeout mais agressivas
CELERY_TASK_SOFT_TIME_LIMIT = 30  # Timeout suave de 30 segundos
CELERY_TASK_TIME_LIMIT = 60  # Timeout hard de 1 minuto
CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

# Configurações de Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'celery': {
            'format': '[CELERY] {levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'email': {
            'format': '[EMAIL] {levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'celery_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/celery.log',
            'formatter': 'celery',
        },
        'email_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/email.log',
            'formatter': 'email',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console', 'celery_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'usuarios.tasks': {
            'handlers': ['console', 'email_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'usuarios.views': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
} 

# Configurações de autenticação
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


# Configurações de mídia para upload de arquivos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# ===== CONFIGURAÇÕES DO JAZZMIN =====
JAZZMIN_SETTINGS = {
    # Título da janela do navegador
    "site_title": "Dojô Uemura",
    "site_header": "Dojô Uemura",
    "site_brand": "Dojô Uemura",
    "site_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    
    # Cores do tema
    "accent": "accent-primary",
    "brand_colour": "primary",
    "colour_scheme": "light",
    
    # Menu lateral
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "empresa.Empresa": "fas fa-building",
        "usuarios.Usuario": "fas fa-user-tie",
        "usuarios.Atleta": "fas fa-child",
        "usuarios.Modalidade": "fas fa-fist-raised",
        "usuarios.Matricula": "fas fa-graduation-cap",
        "usuarios.TipoMatricula": "fas fa-tags",
        "usuarios.StatusMatricula": "fas fa-check-circle",
    },
    
    # Customização do menu
    "custom_links": {
        "usuarios": [{
            "name": "Dashboard",
            "url": "/usuarios/dashboard/",
            "icon": "fas fa-tachometer-alt",
            "permissions": ["auth.view_user"]
        }],
    },
    
    # Ordem dos apps no menu
    "order_with_respect_to": ["auth", "empresa", "usuarios", "publico"],
    
    # Configurações de interface
    "changeform_format": "horizontal_tabs",
    "show_ui_builder": True,
    "use_bootswatch": True,
    "bootswatch_theme": "flatly",
}

# Configurações de interface do Jazzmin
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}