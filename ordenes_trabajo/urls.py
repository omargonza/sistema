from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView # <-- ¡Importa esto!


urlpatterns = [
    # Redirecciona la raíz '/' a la página de login
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'), # <-- ¡Añade esta línea!
    # 'permanent=False' significa que es una redirección temporal (302), útil durante el desarrollo.
    # 'pattern_name='login'' usa el nombre de tu URL para el login.
    path('admin/', admin.site.urls),
    path('ordenes/lista/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/nueva/', views.crear_orden, name='crear_orden'),
     # Y la nueva URL para generar PDF:
    path('ordenes/<int:pk>/pdf/', views.generar_pdf_orden, name='generar_pdf_orden'),
    path('ordenes/<int:pk>/', views.detalle_orden, name='detalle_orden'),
    path('ordenes/<int:pk>/editar/', views.editar_orden, name='editar_orden'),
    path('ordenes/<int:pk>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
       path('registro/', views.registro, name='registro'),
    path('accounts/login/', views.login_view, name='login'),  # URL para la página de login
    path('accounts/logout/', LogoutView.as_view(next_page='lista_ordenes'), name='logout'),
]
