# archivo: usuario_service/usuario_service/cuentas/views.py

import json
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .models import Usuario
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import UsuarioSerializer

@csrf_exempt
def login_cliente(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método no permitido'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'JSON inválido'}, status=400)

    user = authenticate(
        username=payload.get('username'),
        password=payload.get('password')
    )
    if user is None:
        return JsonResponse({'detail': 'Credenciales inválidas'}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({
        'token': token.key,
        'rol':   user.rol,            # <— incluimos el rol aquí
    })
@csrf_exempt
def registro_cliente(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'JSON inválido'}, status=400)

    username = data.get('username')
    password = data.get('password')
    email    = data.get('email', '')
    # Validaciones básicas
    if not username or not password:
        return JsonResponse({'detail': 'Faltan campos'}, status=400)
    if Usuario.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Usuario ya existe'}, status=400)

    # Crear usuario con rol de cliente
    user = Usuario.objects.create_user(
        username=username,
        password=password,
        email=email,
        rol='cliente'
    )
    return JsonResponse({'detail': 'Usuario creado', 'id': user.id}, status=201)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset         = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            perms = [IsAuthenticated, IsAdminUser]
        else:
            perms = [IsAuthenticated]
        return [perm() for perm in perms]   # importante el () aquí

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
