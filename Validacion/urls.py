from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('tareas/', views.tarea_list, name='tarea-list'),
    path('tareas/create/', views.crear_tarea, name='crear_tarea'),
    path('tareas/<int:tarea_id>/edit/', views.tarea_edit, name='tarea-edit'),
    path('tareas/<int:tarea_id>/update/', views.tarea_update, name='tarea-update'),
    path('tareas/<int:tarea_id>/delete/', views.tarea_delete, name='tarea-delete'),
    path('grupos/create/', views.grupos_create, name='grupos-create'),
    path('grupos/update/<int:grupo_id>/', views.grupos_update, name='grupos-update'),
    path('usuario/update/<int:usuario_id>/', views.usuario_update, name='usuario-update'),
    path('tareas/asignar/', views.asignar_tarea, name='asignar_tarea'),
    path('tareas/asignar/<int:asignar_tarea_id>/delete/', views.asginar_tarea_delete, name='asignar-tarea-delete'),
]
