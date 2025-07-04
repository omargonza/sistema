# Generated by Django 5.2.1 on 2025-05-14 01:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrdenTrabajo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField()),
                ("horaInicio", models.TimeField()),
                ("horaFin", models.TimeField(blank=True, null=True)),
                ("vehiculo", models.CharField(blank=True, max_length=100, null=True)),
                ("kmInicial", models.IntegerField(blank=True, null=True)),
                ("kmFinal", models.IntegerField(blank=True, null=True)),
                ("descripcion", models.TextField()),
                ("tablero", models.CharField(blank=True, max_length=100, null=True)),
                ("zona", models.CharField(max_length=100)),
                ("circuito", models.CharField(blank=True, max_length=100, null=True)),
                ("materiales", models.TextField(blank=True, null=True)),
                (
                    "tecnicos",
                    models.ManyToManyField(
                        related_name="ordenes_trabajo", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
