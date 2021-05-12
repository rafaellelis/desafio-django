from decimal import Decimal, ROUND_HALF_UP
from celery import shared_task
from .models import ConfiguracaoTitulo
from .enums import Status
from .services import enviarEmail, obter_stock_price


@shared_task(name="titulo_task")
def titulo_task(titulo_id):
    configuracao = ConfiguracaoTitulo.objects.get(pk=titulo_id)

    if configuracao.status == Status.ativo:
        print("""Executando tarefa para o título {setup_title}.""".format(setup_title=str(configuracao.titulo)))
        gravarMonitoramento(configuracao)


def gravarMonitoramento(configuracao: ConfiguracaoTitulo):
    titulo = configuracao.titulo
    monitoramento = obter_stock_price(titulo)

    if monitoramento is not None:
        monitoramento.save()
        valor = Decimal(monitoramento.valor.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        if valor > configuracao.limite_superior or valor < configuracao.limite_inferior:
            enviarEmail(configuracao, valor)


