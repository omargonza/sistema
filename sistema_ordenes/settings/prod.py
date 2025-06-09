from .base import *
from dj_database_url import parse as db_url
from decouple import config
import os

# DEBUG: Activado o no (default: False)
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# Hosts permitidos, separados por coma en la variable de entorno
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])

# URL de la base de datos externa (vacío por defecto)
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Configuración para base de datos externa (Postgres, MySQL, etc)
    DATABASES = {
        'default': db_url(DATABASE_URL)
    }
    print("⚙️ Usando base de datos externa:", DATABASE_URL)
else:
    # Configuración para SQLite local (default si no hay DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    print("⚙️ Usando base de datos local SQLite")

# Seguridad para producción (HTTPS y cabeceras)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Archivos estáticos para producción con Whitenoise
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
