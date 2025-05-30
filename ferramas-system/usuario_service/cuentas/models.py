# usuario_service/cuentas/models.py

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

SEXOS = [ ('M','Masculino'), ('F','Femenino'), ('O','Otro'), ]
ROLES = [ ('admin','Administrador'), ('vendedor','Vendedor'),
          ('bodeguero','Bodeguero'), ('contador','Contador'), ]

class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'admin')      # <— forzamos rol=admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return super().create_superuser(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    objetos      = UsuarioManager()   # <— asocia tu manager custom
    nombres      = models.CharField(max_length=150, blank=True, default='')
    apellidos    = models.CharField(max_length=150, blank=True, default='')
    direccion    = models.CharField(max_length=255, blank=True, default='')
    celular      = models.CharField(max_length=20, blank=True, default='')
    nacionalidad = models.CharField(max_length=50, blank=True, default='')
    comuna       = models.CharField(max_length=120, blank=True, default='')
    rut          = models.CharField(max_length=12, unique=True, blank=True, default='')
    rol          = models.CharField(max_length=20, choices=ROLES, default='vendedor')
    sexo         = models.CharField(max_length=1, choices=SEXOS, default='O')

    class Meta:
        db_table = "registroPersonal"
