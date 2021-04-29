from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Titulo

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'cotacoes/index.html'
    # context_object_name = 'lista_titulos'

    def get_queryset(self):
        return Titulo.objects.order_by('codigo')

class DetalharTituloView(generic.DetailView):
    model = Titulo
    # template_name = 'cotacoes/titulo_detail.html'

class MonitorarTituloView(generic.DetailView):
    model = Titulo
    template_name = 'cotacoes/monitorar.html'
