# usuario_service/usuario_service/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from cuentas.views import registro_cliente



urlpatterns = [
    path('admin/', admin.site.urls),

    # Login usando DRF TokenAuth:
    path('api/usuarios/login/', obtain_auth_token, name='api_login'),

    # Registro de cliente (tu view custom):
    path('api/usuarios/registro_cliente/', registro_cliente, name='api_registro_cliente'),

    # Resto de endpoints CRUD para usuarios:
    path('api/usuarios/', include('cuentas.urls')),

    # Navegación de la API Browsable:
    path('api-auth/', include('rest_framework.urls')),
]
