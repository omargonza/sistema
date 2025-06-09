"""
WSGI config for sistema_ordenes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Usar settings de producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_ordenes.settings.prod')

application = get_wsgi_application()
application = WhiteNoise(application, root=str(BASE_DIR / "staticfiles"), prefix='static/')
