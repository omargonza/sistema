from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Crea superusuario automáticamente si no existe'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Gonza')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'aplicacionesgonza@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('✅ Superusuario creado automáticamente.'))
        else:
            self.stdout.write('ℹ️ El superusuario ya existe.')
