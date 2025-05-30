# frontend/users_frontend/urls.py

from django.urls import path
from .views import (
    base_view, login_view, registroPersonal, logout_view,
    personal_list, personal_detail,
    personal_edit, personal_delete,
)

urlpatterns = [
    path('',                  base_view,           name='base'),
    path('login/',            login_view,          name='login'),
    path('registro/',         registroPersonal,    name='registroPersonal'),
    path('personal/',         personal_list,       name='personal_list'),
    path('personal/<int:id>/',personal_detail,     name='personal_detail'),
    path('personal/<int:id>/edit/',   personal_edit,   name='personal_edit'),
    path('personal/<int:id>/delete/', personal_delete, name='personal_delete'),
    path('logout/',           logout_view,         name='logout'),

    
]
