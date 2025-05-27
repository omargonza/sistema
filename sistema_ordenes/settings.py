# sistema_ordenes/settings.py

from pathlib import Path
import os # Necesario para os.path.join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR usando pathlib (la forma moderna y recomendada)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3c2sjisamr3s88@=6b$7(@z7#%_$uoiw#2$*+%h@9!19pupon0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Indispensable para manejar archivos estáticos
    'ordenes_trabajo', # Tu aplicación de órdenes
    # 'xhtml2pdf', # Opcional: No siempre es necesario añadirlo aquí si solo lo usas en views
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

ROOT_URLCONF = 'sistema_ordenes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aquí puedes añadir directorios adicionales donde Django buscará plantillas.
        # Es útil para plantillas globales como un 'base.html' en la raíz del proyecto.
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <-- Añadido/Corregido
        'APP_DIRS': True, # Esto permite que Django busque plantillas dentro de las carpetas 'templates' de cada app.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # No estaba presente, útil para DEBUG=True
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema_ordenes.wsgi.application'


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

LANGUAGE_CODE = 'es-ar' # <-- Cambiado a español de Argentina para fechas y horas si usas i18n
TIME_ZONE = 'America/Argentina/Buenos_Aires' # <-- Cambiado a tu zona horaria real

USE_I18N = True # Habilita la internacionalización

USE_TZ = True # Habilita las zonas horarias en los datetimes de la base de datos


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/' # <-- Esta es la única definición de STATIC_URL que debe quedar

# STATICFILES_DIRS le dice a Django dónde encontrar tus archivos estáticos
# durante el desarrollo (cuando DEBUG=True).
# La carpeta 'static' en la raíz de tu proyecto.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT es el directorio donde 'collectstatic' recopilará todos los archivos estáticos
# para el despliegue en producción.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


LOGIN_REDIRECT_URL = '/ordenes/'    # O la URL a la que quieres redirigir después del login
LOGIN_URL = '/accounts/login/'      # URL de la página de login
LOGOUT_REDIRECT_URL = '/accounts/login/' # URL a la que quieres redirigir después del logout


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'