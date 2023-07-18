from django import forms
from .models import GruposUsuarioTareas, UsuarioTareas

class GruposUsuarioTareasForm(forms.ModelForm):
    class Meta:
        model = GruposUsuarioTareas
        fields = ['nombre']

class UsuarioTareasForm(forms.ModelForm):
    class Meta:
        model = UsuarioTareas
        fields = ['grupo']
