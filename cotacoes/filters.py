import django_filters
from .models import Titulo

class TituloFilter(django_filters.FilterSet):
    class Meta:
        model = Titulo
        fields = ['codigo', 'descricao']