# ordenes_trabajo/views.py

# ====================================================================
# === Todas las importaciones deben ir al principio del archivo ===
# ====================================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
import json

# Importaciones de tus modelos y formularios
from .models import OrdenTrabajo, Material, MaterialOrden
from .forms import OrdenTrabajoForm, MaterialOrdenFormSet
# ====================================================================
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_ordenes')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'ordenes_trabajo/login.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # inicia sesión automáticamente tras registrarse
            return redirect('lista_ordenes')  # Cambiá 'inicio' por la URL principal de tu app
    else:
        form = UserCreationForm()
    return render(request, 'ordenes_trabajo/registro.html', {'form': form})

@login_required
def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenTrabajoForm(request.POST)
        material_formset = MaterialOrdenFormSet(request.POST)
        action = request.POST.get('action')

        if orden_form.is_valid() and material_formset.is_valid():
            orden = orden_form.save(commit=False)

            # Capturar técnicos enviados desde el formulario (listas)
            nombres = request.POST.getlist('tecnico_nombre[]')
            legajos = request.POST.getlist('tecnico_legajo[]')

            lista_tecnicos = [] # Cambié el nombre de la variable para evitar confusión
            for nombre, legajo in zip(nombres, legajos):
                if nombre.strip() != '' or legajo.strip() != '':
                    lista_tecnicos.append({'nombre': nombre.strip(), 'legajo': legajo.strip()})

            # --- CAMBIO CRÍTICO AQUÍ ---
            # ¡Serializar la lista de Python a una cadena JSON antes de guardar!
            orden.tecnicos = json.dumps(lista_tecnicos)
            # --- FIN DEL CAMBIO CRÍTICO ---

            orden.save() # Ahora guarda la cadena JSON

            # Guardar materiales relacionados
            materiales = material_formset.save(commit=False)
            for material in materiales:
                material.orden_trabajo = orden
                material.save()
            material_formset.save_m2m()

            # Asegúrate de que el contexto para el PDF use el método que devuelve JSON parseado
            # (get_tecnicos_json() o get_tecnicos_como_texto())
            context = {
                'orden': orden,
                'materiales_usados': orden.materiales_usados.all(),
                'tecnicos': orden.get_tecnicos_json(), # Esto debería funcionar ahora
                # O si quieres el texto formateado directamente:
                # 'tecnicos_texto': orden.get_tecnicos_como_texto(),
            }

            template_path = 'ordenes_trabajo/orden_pdf_template.html'
            template = get_template(template_path)
            html = template.render(context)

            response_stream = BytesIO()
            pdf = pisa.CreatePDF(html, dest=response_stream)

            if not pdf.err:
                pdf_bytes = response_stream.getvalue()
                disposition = 'inline' if action == 'generar' else 'attachment'
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = f'{disposition}; filename="Orden_Trabajo_{orden.pk}.pdf"'
                return response
            else:
                return HttpResponse('Error al generar el PDF.', status=500)

        else:
            materiales = Material.objects.all()
            unidades = {str(m.id): m.unidad for m in materiales}

            context = {
                'orden_form': orden_form,
                'material_formset': material_formset,
                'materiales': materiales,
                'unidades': unidades,
            }
            return render(request, 'ordenes_trabajo/crear_orden.html', context)

    else:
        orden_form = OrdenTrabajoForm()
        material_formset = MaterialOrdenFormSet(queryset=Material.objects.none())
        materiales = Material.objects.all()
        unidades = {str(m.id): m.unidad for m in materiales}

        context = {
            'orden_form': orden_form,
            'material_formset': material_formset,
            'materiales': materiales,
            'unidades': unidades,
        }
        return render(request, 'ordenes_trabajo/crear_orden.html', context)



@login_required
def lista_ordenes(request):
    ordenes = OrdenTrabajo.objects.all()
    context = {'ordenes': ordenes}
    return render(request, 'ordenes_trabajo/lista_ordenes.html', context)



@login_required
def detalle_orden(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    context = {
        'orden': orden,
        'materiales_usados': orden.materiales_usados.all(),
        'tecnicos': orden.get_tecnicos_json(),  # Accedemos a los técnicos como lista
    }
    return render(request, 'ordenes_trabajo/detalle_orden.html', context)


@login_required
def editar_orden(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    return HttpResponse(f"Aquí se mostrará el formulario para editar la orden de trabajo con ID: {orden.pk}")


@login_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    return HttpResponse(f"Aquí se confirmará la eliminación de la orden de trabajo con ID: {orden.pk}")


@login_required
def generar_pdf_orden(request, pk):
    """
    Genera un PDF para una orden de trabajo específica.
    Recibe el 'pk' (clave primaria) de la Orden de Trabajo como parámetro.
    """
    orden = get_object_or_404(OrdenTrabajo, pk=pk)

    context = {
        'orden': orden,
        'materiales_usados': orden.materiales_usados.all(),
        'tecnicos': orden.get_tecnicos_json(),  # ✅ Lista de técnicos decodificada del campo JSON
    }

    template_path = 'ordenes_trabajo/orden_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    response_stream = BytesIO()
    
    pdf = pisa.CreatePDF(
        html, dest=response_stream
    )

    if not pdf.err:
        response = HttpResponse(response_stream.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Orden_Trabajo_{orden.pk}.pdf"'
        return response
    
    return HttpResponse('Error al generar el PDF.', status=500)
