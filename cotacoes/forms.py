from django import forms

from .models import ConfiguracaoTitulo

class ConfiguracaoForm(forms.ModelForm):
    
    class Meta:
        model = ConfiguracaoTitulo
        fields = ('limite_inferior', 'limite_superior', 'intervalo')
