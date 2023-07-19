import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.response import Response
from .models import UsuarioTareas, GruposUsuarioTareas
from .forms import GruposUsuarioTareasForm, UsuarioTareasForm

import environ

env = environ.Env()
environ.Env.read_env(env_file='config/.env.production')

# Login
###########################################################################

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tarea-list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    grupos = GruposUsuarioTareas.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Obtener el grupo seleccionado en el formulario de registro
            grupo_id = request.POST.get('grupo')

            # Asignar el grupo al usuario en el modelo UsuarioTareas
            grupo = GruposUsuarioTareas.objects.get(id=grupo_id)
            UsuarioTareas.objects.create(user=user, grupo=grupo)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'grupos': grupos})

def logout_view(request):
    logout(request)
    return redirect('login')

# Group
###########################################################################

def grupos_create(request):
    if request.method == 'POST':
        form = GruposUsuarioTareasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tarea-list')
    else:
        form = GruposUsuarioTareasForm()
    return render(request, 'grupo_create.html', {'form': form})

def grupos_update(request, grupo_id):
    grupo = GruposUsuarioTareas.objects.get(id=grupo_id)
    if request.method == 'POST':
        form = GruposUsuarioTareasForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('tarea-list')
    else:
        form = GruposUsuarioTareasForm(instance=grupo)
    return render(request, 'grupo_update.html', {'form': form})

def usuario_update(request, usuario_id):
    usuario = UsuarioTareas.objects.get(user_id=usuario_id)
    if request.method == 'POST':
        form = UsuarioTareasForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('tareas-list')
    else:
        form = UsuarioTareasForm(instance=usuario)
    return render(request, 'usuario_update.html', {'form': form})

# API
###########################################################################

def tarea_list(request):
    grupos = GruposUsuarioTareas.objects.all()
    # Obtener el token de autenticación del usuario actual
    token = request.COOKIES.get('tu_token_de_autenticacion')

    # Obtener el ID del usuario actual
    user_id = request.user.id
    usuario_tareas = UsuarioTareas.objects.filter(user_id=user_id)
    grupo_id = usuario_tareas.first().grupo_id
    usuarios = UsuarioTareas.objects.filter(grupo_id=grupo_id)
    # Realizar una solicitud GET al API para obtener las tareas del usuario actual
    response = requests.get(env("API_Link")+'tareas/', headers={'Authorization': f'Token {token}'}, params={'usuario': user_id})

    # Obtener la lista de tareas del cuerpo de la respuesta
    tareas = response.json()
    
    response2 = requests.get(env("API_Link")+'tareas/asignadas/', headers={'Authorization': f'Token {token}'}, params={'usuario': user_id})
    tareas_asig = response2.json()
    
    # Renderizar la plantilla con la lista de tareas
    return render(request, 'tareas.html', {'tareas': tareas, 'grupos': grupos, 'usuarios': usuarios, 'tareas_asig': tareas_asig})

def crear_tarea(request):
    if request.method == 'POST':
        # Obtener los datos de la nueva tarea del formulario enviado por el usuario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_limite = request.POST.get('fecha_limite')
        
        # Obtener el objeto UsuarioTareas del usuario actual
        usuario_tareas = UsuarioTareas.objects.get(user=request.user)
        usuario_tareas_id = usuario_tareas.id
        
        print(usuario_tareas_id)
        # Lógica para consumir la API y crear la nueva tarea
        url = env("API_Link")+'tareas/'
        nueva_tarea = {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_limite': fecha_limite,
            'usuario': usuario_tareas_id
        }
        response = requests.post(url, data=nueva_tarea)
        print(response)
        # Verificar el código de respuesta de la solicitud
        if response.status_code == 201:
            print('Tarea creada exitosamente')
            return redirect('tarea-list')
            # Realizar las acciones necesarias después de la creación exitosa
        else:
            print('Error al crear la tarea')
            # Realizar las acciones necesarias en caso de error

    return render(request, 'crear_tarea.html')

def asignar_tarea(request):
    token = request.COOKIES.get('tu_token_de_autenticacion')
    
    # Obtener el ID del usuario actual
    user_id = request.user.id
    
    # Los usuarios
    usuario_tareas = UsuarioTareas.objects.filter(user_id=user_id)
    grupo_id = usuario_tareas.first().grupo_id
    usuarios = UsuarioTareas.objects.filter(grupo_id=grupo_id)
    
    
    # Las tareas
    response = requests.get(env("API_Link")+'tareas/', headers={'Authorization': f'Token {token}'}, params={'usuario': user_id})

    # Obtener la lista de tareas del cuerpo de la respuesta
    tareas = response.json()
    
    context = {
        'usuarios':usuarios,
        'tareas':tareas
    }
    
    if request.method == 'POST':
        # Obtener los datos de la nueva tarea del formulario enviado por el usuario
        mensaje = request.POST.get('mensaje')
        tarea_id = request.POST.get('tarea')
        asignado_a_id = request.POST.get('asignado_a')
        
        # Lógica para consumir la API y crear la nueva tarea
        url = env("API_Link")+'tareas/asignadas/'
        nueva_asignacion = {
            'mensaje': mensaje,
            'tarea': tarea_id,
            'asignado_a': [asignado_a_id]
        }
        response = requests.post(url, data=nueva_asignacion)
        print(response)
        # Verificar el código de respuesta de la solicitud
        if response.status_code == 201:
            print('Tarea creada exitosamente')
            return redirect('tarea-list')
            # Realizar las acciones necesarias después de la creación exitosa
        else:
            print('Error al crear la tarea')
            # Realizar las acciones necesarias en caso de error

    return render(request, 'asignar_tarea.html', context)

def tarea_edit(request, tarea_id):
    # Obtener el token de autenticación del usuario actual
    token = request.COOKIES.get('tu_token_de_autenticacion')

    # Obtener la tarea específica utilizando el ID proporcionado
    response = requests.get(env("API_Link")+f'tareas/{tarea_id}/', headers={'Authorization': f'Token {token}'})
    tarea = response.json()

    # Renderizar el formulario de edición de la tarea
    return render(request, 'tarea_edit.html', {'tarea': tarea})

def tarea_update(request, tarea_id):
    # Obtener el token de autenticación del usuario actual
    token = request.COOKIES.get('tu_token_de_autenticacion')

    # Obtener los datos actualizados de la tarea del formulario enviado por el usuario
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    fecha_limite = request.POST.get('fecha_limite')

    # Realizar una solicitud GET al API para obtener la tarea específica
    response_get = requests.get(env("API_Link")+f'tareas/{tarea_id}/', headers={'Authorization': f'Token {token}'})
    tarea = response_get.json()

    # Actualizar los datos de la tarea con los valores del formulario
    tarea['nombre'] = nombre
    tarea['descripcion'] = descripcion
    tarea['fecha_limite'] = fecha_limite

    # Realizar una solicitud PUT al API para actualizar la tarea
    response_put = requests.put(env("API_Link")+f'tareas/{tarea_id}/', headers={'Authorization': f'Token {token}'}, data=tarea)

    # Redireccionar a la lista de tareas después de la actualización
    return redirect('tarea-list')

def tarea_delete(request, tarea_id):
    # Obtener el token de autenticación del usuario actual
    token = request.COOKIES.get('tu_token_de_autenticacion')

    # Realizar una solicitud DELETE al API para eliminar la tarea
    response = requests.delete(env("API_Link")+f'tareas/{tarea_id}/', headers={'Authorization': f'Token {token}'})

    # Redireccionar a la lista de tareas después de la eliminación
    return redirect('tarea-list')


def asginar_tarea_delete(request, asignar_tarea_id):
    # Obtener el token de autenticación del usuario actual
    token = request.COOKIES.get('tu_token_de_autenticacion')

    # Realizar una solicitud DELETE al API para eliminar la tarea
    response = requests.delete(env("API_Link")+f'tareas/asignadas/{asignar_tarea_id}/', headers={'Authorization': f'Token {token}'})

    # Redireccionar a la lista de tareas después de la eliminación
    return redirect('tarea-list')