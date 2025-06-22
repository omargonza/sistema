
from django import forms
from .models import OrdenTrabajo, MaterialOrden, Material

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = [
            "fecha",
            "horaInicio",
            "horaFin",
            "tablero",
            "circuito",
            "zona",
            "vehiculo",
            "kmInicial",
            "kmFinal",
            "descripcion",
            "tipo_mantenimiento",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "horaInicio": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "horaFin": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "tablero": forms.TextInput(attrs={"class": "form-control"}),
            "circuito": forms.TextInput(attrs={"class": "form-control"}),
            "zona": forms.TextInput(attrs={"class": "form-control"}),
            "vehiculo": forms.TextInput(attrs={"class": "form-control"}),
            "kmInicial": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ej. 12345"}),
            "kmFinal": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ej. 12378"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tipo_mantenimiento": forms.Select(attrs={"class": "form-select"}),
        }

class MaterialOrdenForm(forms.ModelForm):
    class Meta:
        model = MaterialOrden
        fields = ["material", "cantidad"]
        widgets = {
            "material": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

from django.forms import modelformset_factory

MaterialOrdenFormSet = modelformset_factory(
    MaterialOrden,
    form=MaterialOrdenForm,
    extra=1,
    can_delete=True,
)

