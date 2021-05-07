from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .forms import ConfiguracaoForm
from .models import Titulo, ConfiguracaoTitulo, Status

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'cotacoes/index.html'
    # context_object_name = 'lista_titulos'

    def get_queryset(self):
        return Titulo.objects.order_by('codigo')


class DetalharTituloView(generic.DetailView):
    model = Titulo
    # template_name = 'cotacoes/titulo_detail.html'


def configuracao_new(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    if request.method == "POST":
        form = ConfiguracaoForm(request.POST)
        if form.is_valid():
            configuracao = form.save(commit=False)
            configuracao.titulo = titulo
            configuracao.save(force_insert=True)
            return redirect('detalhaTitulo', pk=titulo_id)
    else:
        form = ConfiguracaoForm(initial={'titulo': titulo})
    return render(request, 'cotacoes/monitorar_form.html', {'form': form, 'titulo': titulo})


def configuracao_editar(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    if request.method == "POST":
        configuracao_bd = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
        form = ConfiguracaoForm(request.POST, instance=configuracao_bd)
        if form.is_valid():
            configuracao = form.save(commit=False)
            configuracao.titulo = titulo
            configuracao.save(force_update=True)
            return redirect('detalhaTitulo', pk=titulo_id)
    else:
        configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
        form = ConfiguracaoForm(instance=configuracao)
    return render(request, 'cotacoes/monitorar_form.html', {'form': form, 'titulo': titulo})


def configuracao_inativar(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.status = Status.inativo
    configuracao.save()
    return redirect('index')


def configuracao_reativar(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.status = Status.ativo
    configuracao.save()
    return redirect('index')


def configuracao_remover(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.delete()
    return redirect('index')