# cuentas/api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def login_cliente(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'OK, envía POST'}, status=200)
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'detail': 'JSON inválido'}, status=400)
    user = authenticate(request,
                        username=data.get('username'),
                        password=data.get('password'))
    if not user:
        return JsonResponse({'detail': 'Credenciales inválidas'}, status=401)
    login(request, user)
    return JsonResponse({'detail': 'Login correcto'})

@csrf_exempt
def registro_cliente(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'OK, envía POST'}, status=200)
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'detail': 'JSON inválido'}, status=400)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse({'detail': 'Faltan campos'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Usuario ya existe'}, status=400)
    user = User.objects.create_user(username=username, password=password, email=data.get('email',''))
    return JsonResponse({'detail': 'Usuario creado', 'id': user.id}, status=201)
