from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import OrdenTrabajo, Material, MaterialOrden
import json

class MaterialOrdenInline(admin.TabularInline):
    model = MaterialOrden
    extra = 1
    verbose_name = "Material utilizado"
    verbose_name_plural = "Materiales utilizados"
    autocomplete_fields = ['material']

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'vehiculo', 'zona', 'mostrar_tecnicos')
    list_filter = ('fecha', 'zona', 'vehiculo')
    search_fields = ('vehiculo', 'descripcion', 'zona', 'circuito')
    ordering = ('-fecha',)

    inlines = [MaterialOrdenInline]
    readonly_fields = ('tecnicos_como_tabla',)

    fieldsets = (
        ('Información general', {
            'fields': ('fecha', 'horaInicio', 'horaFin', 'vehiculo', 'kmInicial', 'kmFinal')
        }),
        ('Detalle del trabajo', {
            'fields': ('descripcion', 'tablero', 'zona', 'circuito')
        }),
        ('Técnicos asignados', {
            'fields': ('tecnicos_como_tabla',)
        }),
    )

    def mostrar_tecnicos(self, obj):
        return obj.get_tecnicos_como_texto()
    mostrar_tecnicos.short_description = 'Técnicos asignados'

    def tecnicos_como_tabla(self, obj):
        """
        Muestra los técnicos como una tabla HTML legible con columnas.
        """
        try:
            tecnicos = json.loads(obj.tecnicos)
            if not tecnicos:
                return "No se asignaron técnicos."

            html = "<table style='border-collapse: collapse; width: 100%;'>"
            html += "<thead><tr><th style='border: 1px solid #ccc; padding: 5px;'>Nombre</th><th style='border: 1px solid #ccc; padding: 5px;'>Legajo</th></tr></thead><tbody>"
            for t in tecnicos:
                html += f"<tr><td style='border: 1px solid #ccc; padding: 5px;'>{t['nombre']}</td><td style='border: 1px solid #ccc; padding: 5px;'>{t['legajo']}</td></tr>"
            html += "</tbody></table>"
            return mark_safe(html)
        except Exception:
            return "Error al mostrar técnicos."

    tecnicos_como_tabla.short_description = "Técnicos asignados (tabla)"

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'tecnicos' in fields:
            fields.remove('tecnicos')  # Oculta el JSON en crudo
        return fields

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')
    search_fields = ('nombre', 'codigo')
    ordering = ('nombre',)

@admin.register(MaterialOrden)
class MaterialOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden_trabajo', 'material', 'cantidad')
    list_filter = ('material',)
    search_fields = ('material__nombre', 'orden_trabajo__vehiculo')
    autocomplete_fields = ['material', 'orden_trabajo']
