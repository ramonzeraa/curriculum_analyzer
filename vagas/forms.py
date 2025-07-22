from django import forms
from .models import Curriculo

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['vaga', 'nome', 'email', 'arquivo'] 