# archivo: frontend/users_frontend/views.py

import requests
from django.shortcuts      import render, redirect
from django.conf           import settings
from django.contrib        import messages
from django.contrib.auth   import logout as django_logout
# URLs del microservicio de usuarios
MICROSERVICE_BASE  = getattr(settings, 'USUARIOS_SERVICE', 'http://usuarios:8000')
MICROSERVICE_LOGIN = f'{MICROSERVICE_BASE}/api/usuarios/login/'
MICROSERVICE_USERS = f'{MICROSERVICE_BASE}/api/usuarios/usuarios/'  # CRUD usuarios


# ——— Vistas de autenticación y gestión de personal ———

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            resp = requests.post(
                MICROSERVICE_LOGIN,
                json={'username': username, 'password': password},
                timeout=5
            )
        except requests.RequestException:
            messages.error(request, 'Error de conexión con el servicio de usuarios.')
            return render(request, 'users_frontend/login.html')

        if resp.status_code == 200:
            token = resp.json().get('token')
            request.session['token']    = token
            request.session['username'] = username

            # Obtener rol desde el listado
            try:
                users_resp = requests.get(
                    MICROSERVICE_USERS,
                    headers={'Authorization': f'Token {token}'},
                    timeout=5
                )
                users = users_resp.json()
                role = next((u['rol'] for u in users if u['username']==username), None)
            except Exception:
                role = None
            request.session['role'] = role
            

            return redirect('base')
        else:
            messages.error(request, 'Credenciales inválidas.')
    return render(request, 'users_frontend/login.html')




def base_view(request):
    return render(request, 'base.html')


def registroPersonal(request):
    token = request.session.get('token')
    role  = request.session.get('role')
    if not token:
        return redirect('login')
    if role != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('base')

    if request.method == 'POST':
        data = {
            'username':     request.POST['username'],
            'password':     request.POST['password'],
            'email':        request.POST['email'],
            'nombres':      request.POST['nombres'],
            'apellidos':    request.POST['apellidos'],
            'rut':          request.POST['rut'],
            'celular':      request.POST['celular'],
            'direccion':    request.POST['direccion'],
            'nacionalidad': request.POST['nacionalidad'],
            'comuna':       request.POST['comuna'],
            'rol':          request.POST['rol'],
            'sexo':         request.POST['sexo'],
        }
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
        try:
            resp = requests.post(MICROSERVICE_USERS, json=data, headers=headers, timeout=5)
        except requests.RequestException:
            messages.error(request, 'No se pudo conectar al servicio de usuarios.')
        else:
            if resp.status_code == 201:
                messages.success(request, '✔️ Trabajador creado con éxito.')
            elif resp.status_code == 400:
                err = resp.json()
                if 'rut' in err:
                    messages.error(request, '❌ Ya existe un trabajador con ese RUT.')
                elif 'username' in err:
                    messages.error(request, '❌ Ya existe un trabajador con ese nombre de usuario.')
                elif 'email' in err:
                    messages.error(request, '❌ Ya existe un trabajador con ese email.')
                else:
                    messages.error(request, '❌ Verifica los datos e inténtalo de nuevo.')
            else:
                messages.error(request, '❌ Error inesperado.')
        return redirect('personal_list')

    return render(request, 'users_frontend/registroPersonal.html', {
        'usuario': request.session.get('username')
    })


def personal_list(request):
    token = request.session.get('token')
    role  = request.session.get('role')
    if not token or role != 'admin':
        messages.error(request, 'Acceso denegado.')
        return redirect('base')

    resp = requests.get(MICROSERVICE_USERS, headers={'Authorization': f'Token {token}'}, timeout=5)
    usuarios = resp.json() if resp.status_code == 200 else []
    return render(request, 'users_frontend/personal_list.html', {
        'usuarios': usuarios
    })


def personal_detail(request, id):
    token = request.session.get('token')
    role  = request.session.get('role')
    if not token or role != 'admin':
        messages.error(request, 'Acceso denegado.')
        return redirect('base')

    resp = requests.get(f'{MICROSERVICE_USERS}{id}/', headers={'Authorization': f'Token {token}'}, timeout=5)
    usuario = resp.json() if resp.status_code == 200 else None
    return render(request, 'users_frontend/personal_detail.html', {
        'usuario': usuario
    })


# frontend/users_frontend/views.py

def personal_edit(request, id):
    token = request.session.get('token')
    role  = request.session.get('role')
    if not token or role != 'admin':
        messages.error(request, 'Acceso denegado.')
        return redirect('base')

    # Si llegan datos (POST), actualiza
    if request.method == 'POST':
        data = {
            'username':     request.POST['username'],
            'email':        request.POST['email'],
            'nombres':      request.POST['nombres'],
            'apellidos':    request.POST['apellidos'],
            'rut':          request.POST['rut'],
            'celular':      request.POST['celular'],
            'direccion':    request.POST['direccion'],
            'nacionalidad': request.POST['nacionalidad'],
            'comuna':       request.POST['comuna'],
            'rol':          request.POST['rol'],
            'sexo':         request.POST['sexo'],
        }
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
        }

        # Usamos PATCH en lugar de PUT
        try:
            resp = requests.patch(
                f'{MICROSERVICE_USERS}{id}/',
                json=data,
                headers=headers,
                timeout=5
            )
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión: {e}')
            return redirect('personal_edit', id=id)

        # DEBUG: imprime en consola respuesta del microservicio
        print(f'[DEBUG] PATCH /usuarios/{id}/ ->', resp.status_code, resp.text)

        if resp.status_code in (200, 204):
            messages.success(request, '✔️ Trabajador actualizado con éxito.')
            return redirect('personal_list')
        else:
            messages.error(request, '❌ No se pudo actualizar. Verifica los datos.')
            # opcional: caer al GET para volver a mostrar formulario
            # o bien recargar la misma vista mostrando errores

    # Si es GET, traemos datos y mostramos el formulario
    resp = requests.get(
        f'{MICROSERVICE_USERS}{id}/',
        headers={'Authorization': f'Token {token}'},
        timeout=5
    )
    usuario = resp.json() if resp.status_code == 200 else {}
    return render(request, 'users_frontend/personal_edit.html', {
        'usuario': usuario
    })


def personal_delete(request, id):
    token = request.session.get('token')
    role  = request.session.get('role')
    if not token or role!='admin':
        messages.error(request, 'Acceso denegado.')
        return redirect('base')

    if request.method == 'POST':
        resp = requests.delete(
            f'{MICROSERVICE_USERS}{id}/',
            headers={'Authorization':f'Token {token}'},
            timeout=5
        )
        if resp.status_code in (204,200):
            messages.success(request, '✔️ Trabajador eliminado.')
        else:
            messages.error(request, '❌ No se pudo eliminar.')
        return redirect('personal_list')
    return redirect('personal_detail', id=id)


def logout_view(request):
    django_logout(request)
    request.session.flush()
    return redirect('base')


