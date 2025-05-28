import dj_database_url
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

ALLOWED_HOSTS = ['*']  # O tu dominio de Render

# Seguridad para producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # (el resto de tus middlewares...)
]

# Configuración de base de datos con dj-database-url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')  # Render te da esta variable automáticamente
    )
}
