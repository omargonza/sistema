# Generated by Django 5.2.1 on 2025-06-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes_trabajo', '0004_alter_material_unidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentrabajo',
            name='tipo_mantenimiento',
            field=models.CharField(choices=[('preventivo', 'Preventivo'), ('correctivo', 'Correctivo'), ('obra', 'Obra'), ('relevamiento', 'Relevamiento')], default='preventivo', max_length=20),
        ),
    ]
