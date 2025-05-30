from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, login_cliente, registro_cliente

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    path('login/',    login_cliente,   name='login_cliente'),
    path('registro_cliente/', registro_cliente, name='registro_cliente'),
]
