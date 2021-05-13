import django_tables2 as tables
from .models import Monitoramento, ConfiguracaoTitulo, Status, Titulo
from django.db.models import Exists, OuterRef


class TituloTable(tables.Table):
    codigo = tables.Column(linkify=True)
    acoes = tables.TemplateColumn(template_name="cotacoes/tables/acoes_column.html")

    class Meta:
        attrs = {"class": "table table-striped table-hover"}
        model = Titulo
        fields = ("codigo", "descricao", "status", "acoes")
        template_name = "django_tables2/bootstrap4.html"

    def order_acoes(self, queryset, is_descending):
        configuracao = ConfiguracaoTitulo.objects.filter(titulo=OuterRef("pk"))
        queryset = queryset.annotate(config=~Exists(configuracao)).order_by(("-" if is_descending else "") + "config")
        return (queryset, True)


class MonitoramentoTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-hover"}
        model = Monitoramento
        template_name = "django_tables2/bootstrap4.html"
        fields = ("timestamp", "valor", "ultima_atualizacao", "variacao")
