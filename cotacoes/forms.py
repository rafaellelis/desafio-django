from django import forms

from .models import ConfiguracaoTitulo

class ConfiguracaoForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(ConfiguracaoForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     self.fields['titulo'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        limite_inferior = cleaned_data.get("limite_inferior")
        limite_superior = cleaned_data.get("limite_superior")

        if limite_inferior >= limite_superior:
            msg = "Limite inferior deve ter um valor menor que o limite superior."
            self.add_error('limite_inferior', msg)

    class Meta:
        model = ConfiguracaoTitulo
        fields = ('limite_inferior', 'limite_superior', 'intervalo')
