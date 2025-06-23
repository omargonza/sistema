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
from .models import OrdenTrabajo, Material
from .forms import OrdenTrabajoForm, MaterialOrdenFormSet, MaterialOrden
# ====================================================================
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
import logging
from django.contrib import messages
logger = logging.getLogger(__name__)

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


MATERIALES_DISPONIBLES = [
    {"nombre": "Cable unipolar marron 2.5mm", "unidad": "m"},
    {"nombre": "Cable unipolar marron 4mm", "unidad": "m"},
    {"nombre": "Cable unipolar marron 6mm", "unidad": "m"},
    {"nombre": "Cable unipolar azul 2.5mm", "unidad": "m"},
    {"nombre": "Cable unipolar azul 4mm", "unidad": "m"},
    {"nombre": "Cable unipolar azul 6mm", "unidad": "m"},
    {"nombre": "Cable unipolar verde 2.5mm", "unidad": "m"},
    {"nombre": "Cable unipolar verde 4mm", "unidad": "m"},
    {"nombre": "Cable unipolar verde 6mm", "unidad": "m"},
    {"nombre": "Terminal ojal  azul", "unidad": "unidad"},
    {"nombre": "Terminal ojal amarillo", "unidad": "unidad"},
    {"nombre": "Terminal ojal rojo", "unidad": "unidad"},
    {"nombre": "Terminal ojal  16mm", "unidad": "unidad"},
    {"nombre": "Terminal ojal  10mm", "unidad": "unidad"},
    {"nombre": "Terminal ojal 6mm", "unidad": "unidad"},
    {"nombre": "Terminal ojal  2.5mm", "unidad": "unidad"},
    {"nombre": "Manguitos  azul", "unidad": "unidad"},
    {"nombre": "Manguito  amarillo", "unidad": "unidad"},
    {"nombre": "Manguito  rojo", "unidad": "unidad"},
    {"nombre": "Tubo PVC 20mm", "unidad": "m"},
    {"nombre": "Llave térmomagnetica tripolar 16A", "unidad": "unidad"},
    {"nombre": "Llave térmomagnetica tripolar 20A", "unidad": "unidad"},
    {"nombre": "Llave térmomagnetica monofasica 16A", "unidad": "unidad"},
    {"nombre": "Llave térmomagnetica monofasica 20A", "unidad": "unidad"},
    {"nombre": "Sintenax 4*10", "unidad": "m"},
    {"nombre": "Sintenax 4*16", "unidad": "m"},
    {"nombre": "Sintenax 4*25", "unidad": "m"},
    {"nombre": "Soporte metálico", "unidad": "pieza"},
    {"nombre": "Balasto 400w", "unidad": "unidad"},
    {"nombre": "Balasto 250w", "unidad": "unidad"},
    {"nombre": "Balasto 150w", "unidad": "unidad"},
    {"nombre": "Lampara Sodio 400w", "unidad": "unidad"},
    {"nombre": "Lampara Sodio 250w", "unidad": "unidad"},
    {"nombre": "Lampara Sodio 150w", "unidad": "unidad"},
    {"nombre": "Lampara Mercurio 400w", "unidad": "unidad"},
    {"nombre": "Lampara Mercurio 250w", "unidad": "unidad"},
    {"nombre": "Lampara Mercurio 150w", "unidad": "unidad"},
    {"nombre": "Capacitor 50mf", "unidad": "unidad"},
    {"nombre": "Capacitor 32mf", "unidad": "unidad"},
    {"nombre": "Capacitor 25mf", "unidad": "unidad"},
    {"nombre": "Capacitor 20mf", "unidad": "unidad"},
    {"nombre": "Ignitor ", "unidad": "unidad"},
    {"nombre": "Cinta aisladora", "unidad": "unidad"},
    {"nombre": "Guantes", "unidad": "unidad"},
    
]



@login_required
def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenTrabajoForm(request.POST)
        #material_formset = MaterialOrdenFormSet(request.POST)
        action = request.POST.get('action')

        # Capturar técnicos dinámicos desde los inputs del form
        nombres = request.POST.getlist('tecnico_nombre[]')
        legajos = request.POST.getlist('tecnico_legajo[]')
        lista_tecnicos = [
            {'nombre': nombre.strip(), 'legajo': legajo.strip()}
            for nombre, legajo in zip(nombres, legajos)
            if nombre.strip() or legajo.strip()
        ]
        
        material_nombres = request.POST.getlist('material_nombre[]')
        material_cantidades = request.POST.getlist('material_cantidad[]')
        materiales_usados = [
            {"nombre": nombre.strip(), "cantidad": cantidad.strip()}
            for nombre, cantidad in zip(material_nombres, material_cantidades)
            if nombre.strip() and cantidad.strip()
        ]

        if orden_form.is_valid():
            orden = orden_form.save(commit=False)
            orden.tecnicos = json.dumps(lista_tecnicos, ensure_ascii=False)
            context = {
                'orden': orden,
                'materiales_usados': materiales_usados,
                'tecnicos': lista_tecnicos,
            }
            if action == "descargar":
                # Solo genera el PDF, sin guardar en la base
              
            
                # Guarda la orden y los materiales
              orden.save()
               

            # Generar el PDF
            template_path = 'ordenes_trabajo/orden_pdf.html'
            template = get_template(template_path)
            html = template.render(context)
            response_stream = BytesIO()
            pdf = pisa.CreatePDF(html, dest=response_stream)

            if not pdf.err:
                pdf_bytes = response_stream.getvalue()
                disposition = 'inline' if action == 'generar' else 'attachment'
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = f'{disposition}; filename="Orden_Trabajo.pdf"'
                return response
            else:
                return HttpResponse('Error al generar el PDF.', status=500)

        else:
         context = {
                'orden_form': orden_form,
                'tecnicos': lista_tecnicos,
                'materiales_disponibles': MATERIALES_DISPONIBLES,
            }
        return render(request, 'ordenes_trabajo/crear_orden.html', context)

    else:
        # GET: mostrar formulario vacío
        orden_form = OrdenTrabajoForm()
        context = {
            'orden_form': orden_form,
            'tecnicos': [],
            'materiales_disponibles': MATERIALES_DISPONIBLES,
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
def editar_orden(_, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    return HttpResponse(f"Aquí se mostrará el formulario para editar la orden de trabajo con ID: {orden.pk}")


@login_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)

    if request.method == 'POST':
        orden.delete()
        messages.success(request, f"La orden #{pk} fue eliminada correctamente.")
        return redirect('lista_ordenes')  # cambiá al nombre real de tu vista de listado

    return render(request, 'ordenes_trabajo/confirmar_eliminacion.html', {'orden': orden})


@login_required
def generar_pdf_orden(_, pk):
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
