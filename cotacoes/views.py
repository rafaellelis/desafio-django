import pandas as pd

# import plotly.graph_objects as go
import plotly.express as px

from plotly.offline import plot

from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django_tables2 import RequestConfig

from .forms import ConfiguracaoForm, TituloFilterFormHelper
from .models import Titulo, ConfiguracaoTitulo, Status
from .tables import MonitoramentoTable, TituloTable
from .filters import TituloFilter

class IndexView(generic.ListView):
    model = Titulo
    table_class = TituloTable
    template_name = "cotacoes/index.html"

    def get_queryset(self):
        return Titulo.objects.order_by("codigo")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        filter = TituloFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = TituloFilterFormHelper()
        table = TituloTable(filter.qs, order_by=("acoes", "codigo"))
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context


def titulo_detail(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    monitoramentos = titulo.monitoramento_set.all()
    table = MonitoramentoTable(monitoramentos, order_by="-timestamp")

    plot_div = None
    if monitoramentos:
        df = pd.DataFrame([x.as_dict() for x in monitoramentos])
        fig = monta_grafico(titulo, df)
        # fig = go.Figure([go.Scatter(x=df['timestamp'], y=df['valor'])])
        plot_div = plot(fig, output_type="div", include_plotlyjs=False)

    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "cotacoes/titulo_detail.html", {"titulo": titulo, "table": table, "plot": plot_div})


def monta_grafico(titulo, df):
    fig = px.area(df, x="timestamp", y="valor")
    fig.update_xaxes(
        title_text="Dados",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="Esse ano", step="year", stepmode="todate"),
                    dict(count=1, label="1A", step="year", stepmode="backward"),
                    dict(label="Todos", step="all"),
                ]
            )
        ),
    )

    fig.update_yaxes(title_text="Valor da ação", tickprefix="R$")
    fig.update_layout(
        showlegend=False, title={"text": str(titulo), "y": 0.9, "x": 0.5, "xanchor": "center", "yanchor": "top"}
    )

    return fig


def configuracao_new(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    if request.method == "POST":
        form = ConfiguracaoForm(request.POST)
        if form.is_valid():
            configuracao = form.save(commit=False)
            configuracao.titulo = titulo
            configuracao.save(force_insert=True)
            return redirect("detalhaTitulo", titulo_id=titulo_id)
    else:
        form = ConfiguracaoForm(initial={"titulo": titulo})
    return render(request, "cotacoes/monitorar_form.html", {"form": form, "titulo": titulo})


def configuracao_editar(request, titulo_id):
    titulo = get_object_or_404(Titulo, pk=titulo_id)
    if request.method == "POST":
        configuracao_bd = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
        form = ConfiguracaoForm(request.POST, instance=configuracao_bd)
        if form.is_valid():
            configuracao = form.save(commit=False)
            configuracao.titulo = titulo
            configuracao.save(force_update=True)
            return redirect("detalhaTitulo", titulo_id=titulo_id)
    else:
        configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
        form = ConfiguracaoForm(instance=configuracao)
    return render(request, "cotacoes/monitorar_form.html", {"form": form, "titulo": titulo})


def configuracao_inativar(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.status = Status.inativo
    configuracao.save()
    return redirect("index")


def configuracao_reativar(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.status = Status.ativo
    configuracao.save()
    return redirect("index")


def configuracao_remover(request, titulo_id):
    configuracao = get_object_or_404(ConfiguracaoTitulo, pk=titulo_id)
    configuracao.delete()
    return redirect("index")
