"""
URL configuration for rcdproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clientes/', include('clientes.urls')),
    path('api/obras/', include('obras.urls')),
    path('api/transportistas/', include('transportistas.urls')),
    path('api/empresas/', include('empresas_gestoras.urls')),
    path('api/supervisores/', include('supervisor_obra.urls')),
    path('api/puntolimpio/', include('puntolimpio.urls')),
    path('api/materiales/', include('materiales.urls')),
    path('api/visitas/', include('visitas.urls')),
    path('api/tecnicos/', include('tecnicos.urls')),
    path('api/coordinacionretiro/', include('coordinacionretiro.urls')),
    path('api/capacitaciones/', include('capacitacion.urls')),
    path('api/formularios/', include('formularios.urls')),
    path('api/notificaciones/', include('notificaciones.urls')),
    path('api/usuarios/', include('usuarios.urls')),
]
