import django_tables2 as tables
from .models import Monitoramento


class MonitoramentoTable(tables.Table):
    class Meta:
        model = Monitoramento
        template_name = "django_tables2/bootstrap4.html"
        fields = ("timestamp", "valor", "variacao")
