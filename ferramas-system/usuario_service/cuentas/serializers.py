from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'password',
            'email',
            'nombres',
            'apellidos',
            'rut',           # ← añadido
            'celular',
            'direccion',
            'nacionalidad',
            'comuna',        # ← añadido
            'rol',
            'sexo',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email':    {'required': False},  # si no lo pides en el form
        }

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
