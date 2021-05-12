from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset, Div, HTML

from .models import ConfiguracaoTitulo


class ConfiguracaoForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        limite_inferior = cleaned_data.get("limite_inferior")
        limite_superior = cleaned_data.get("limite_superior")

        if limite_inferior >= limite_superior:
            msg = "Limite inferior deve ter um valor menor que o limite superior."
            self.add_error("limite_inferior", msg)

    class Meta:
        model = ConfiguracaoTitulo
        fields = ("limite_inferior", "limite_superior", "intervalo")

        # widgets = {
        #     "limite_inferior": forms.TextInput(attrs={"data-mask": "#.##0,00", "data-mask-reverse": "true"}),
        #     "limite_superior": forms.TextInput(attrs={"data-mask": "#.##0,00", "data-mask-reverse": "true"}),
        # }


class TituloFilterFormHelper(FormHelper):
    form_method = "GET"
    layout = Layout(
        Div(Div("codigo", css_class="col-6"), Div("descricao", css_class="col-6"), css_class="row"),
        HTML("<br />"),
        Submit("submit", "Aplicar filtro"),
        Reset("reset", "Limpar Filtro"),
    )
