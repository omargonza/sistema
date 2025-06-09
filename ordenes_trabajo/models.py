from django.db import models
from django.contrib.auth.models import User
import json

class Material(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    unidad = models.CharField(max_length=20, default="mtrs") # Podrías agregar otros campos como unidad de medida, descripción, etc.

    def __str__(self):
        return self.nombre

class OrdenTrabajo(models.Model):
    TIPO_MANTENIMIENTO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('obra', 'Obra'),
        ('relevamiento', 'Relevamiento'),
    ]

    fecha = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    vehiculo = models.CharField(max_length=100)
    kmInicial = models.IntegerField()
    kmFinal = models.IntegerField()
    descripcion = models.TextField()
    tablero = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)
    circuito = models.CharField(max_length=100)
    tipo_mantenimiento = models.CharField(
        max_length=20,
        choices=TIPO_MANTENIMIENTO_CHOICES,
        default='preventivo'
    )
    # Campo para técnicos como JSON
    tecnicos = models.TextField(
        blank=True,
        null=True,
        help_text="Se guarda una lista de técnicos como JSON (nombre y legajo)."
    )

    def get_tecnicos_json(self):
        """
        Devuelve una lista de diccionarios con los técnicos,
        por ejemplo: [{'nombre': 'Juan', 'legajo': '123'}, ...]
        """
        try:
            return json.loads(self.tecnicos or '[]')
        except json.JSONDecodeError:
            return []

    def get_tecnicos_como_texto(self):
        """
        Devuelve un string con los técnicos para mostrar de forma legible:
        Ejemplo: 'Juan (123), Pedro (456)'
        """
        try:
            lista = json.loads(self.tecnicos or '[]')
            return ', '.join(f"{t['nombre']} ({t['legajo']})" for t in lista)
        except (json.JSONDecodeError, KeyError, TypeError):
            return "No se asignaron técnicos."

    def __str__(self):
        return f"Orden #{self.id} - {self.fecha} - {self.get_tecnicos_como_texto()}"

class MaterialOrden(models.Model):
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='materiales_usados')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ('orden_trabajo', 'material') # Para evitar duplicados del mismo material por orden

    def __str__(self):
        return f"{self.cantidad} x {self.material.nombre} en la Orden {self.orden_trabajo.pk}"