from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Titulo

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detalhaTitulo(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    return render(request, 'cotacoes/detalhaTitulo.html', {'titulo': titulo})

def listaTitulos(request):
    lista_titulos = Titulo.objects.order_by('codigo')
    context = {'lista_titulos': lista_titulos}
    return render(request, 'cotacoes/index.html', context)