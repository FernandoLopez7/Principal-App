from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import GruposUsuarioTareas, UsuarioTareas

class UsuarioTareasInline(admin.TabularInline):
    model = UsuarioTareas

class GruposUsuarioTareasAdmin(admin.ModelAdmin):
    inlines = [UsuarioTareasInline]

class UsuarioTareasAdmin(admin.ModelAdmin):
    list_display = ['user', 'grupo']

admin.site.register(GruposUsuarioTareas, GruposUsuarioTareasAdmin)
admin.site.register(UsuarioTareas, UsuarioTareasAdmin)
