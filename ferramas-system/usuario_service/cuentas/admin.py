from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter  = ('rol', 'is_staff', 'is_active')
    fieldsets    = UserAdmin.fieldsets + (
        (None, {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol',)}),
    )
