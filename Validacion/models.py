from django.db import models
from django.contrib.auth.models import User

class GruposUsuarioTareas(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'GruposUsuarioTareas'

class UsuarioTareas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GruposUsuarioTareas, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'UsuarioTareas'