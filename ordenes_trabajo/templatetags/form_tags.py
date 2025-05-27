# ordenes_trabajo/templatetags/form_tags.py
from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    return field  # Si no es un campo de formulario, devolverlo sin modificar
