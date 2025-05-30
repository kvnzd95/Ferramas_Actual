# frontend/ferramas/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Toda la lógica de users_frontend (base, login, registro, logout)
    path('',       include('users_frontend.urls')),
]
