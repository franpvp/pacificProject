from django import forms
from .models import RegistroUsuario

class RegistroUsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = RegistroUsuario
        fields = '__all__' 