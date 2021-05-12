import django_filters
from .models import Titulo

class TituloFilter(django_filters.FilterSet):
    codigo = django_filters.CharFilter(lookup_expr='icontains')
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Titulo
        fields = ['codigo', 'descricao']