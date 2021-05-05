import requests

from celery import shared_task
from .models import ConfiguracaoTitulo, Monitoramento, Titulo
from .enums import Status
from decimal import Decimal
from django.conf import settings
from datetime import datetime
from pytz import timezone


@shared_task(name="titulo_task")
def titulo_task(titulo_id):
    configuracao = ConfiguracaoTitulo.objects.get(pk=titulo_id)

    if configuracao.status == Status.ativo:
        print('''Executando tarefa para o título {setup_title}.'''.format(
            setup_title=str(configuracao.titulo)))
        gravarMonitoramento(configuracao.titulo)


def gravarMonitoramento(titulo: Titulo):
    simbolo = titulo.codigo
    url = "{url}/stock_price?key={key}&symbol={simbolo}".format(
        url=settings.HG_BRASIL_API_URL,
        key=settings.HG_BRASIL_KEY,
        simbolo=simbolo)

    request = requests.get(url)
    if request.status_code == 200:
        response = request.json()
        dados_acao = response['results'][simbolo]

        naive_dt = datetime.strptime(dados_acao['updated_at'], '%Y-%m-%d %H:%M:%S')
        datetime_brasil = timezone('America/Recife').localize(naive_dt)

        monitoramento = Monitoramento(
            titulo=titulo,
            valor=Decimal(dados_acao['price']),
            ultima_atualizacao=datetime_brasil,
            variacao=Decimal(dados_acao['change_percent']))
        monitoramento.save()
