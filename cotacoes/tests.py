from django.test import TestCase

from cotacoes.enums import Intervalo, Status
from django.utils.formats import localize
from pytz import timezone
from cotacoes.models import ConfiguracaoTitulo, Monitoramento, Titulo
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch
from django.core import mail
from django_celery_beat.models import IntervalSchedule, PeriodicTask


VALOR_SUPERIOR = Decimal("24.70")
VALOR_INFERIOR = Decimal("8.70")

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_obter_stock_price(*args, **kwargs):
    naive_dt = datetime.strptime("2021-05-10 20:08:47", "%Y-%m-%d %H:%M:%S")
    datetime_brasil = timezone("America/Recife").localize(naive_dt)

    if args[0].codigo == "PETR4":
        return Monitoramento.objects.create(titulo=args[0], valor=VALOR_SUPERIOR, ultima_atualizacao=datetime_brasil, variacao=Decimal("1.31"))
    elif args[0].codigo == "PETR3":
        return Monitoramento.objects.create(titulo=args[0], valor=VALOR_INFERIOR, ultima_atualizacao=datetime_brasil, variacao=Decimal("1.31"))

    return None

# Create your tests here.
class CheckStockPriceTestCase(TestCase):
    def setUp(self):
        Titulo.objects.create(codigo="PETR4", descricao="Petrobras 4")

    @patch(
        "requests.get",
        return_value=MockResponse(
            status_code=200,
            json_data={
                "results": {"PETR4": {"price": "24.7", "updated_at": "2021-05-10 20:08:47", "change_percent": "1.31"}}
            },
        ),
    )
    def test_obter_stock_price_success(self, mocked):
        titulo = Titulo.objects.get(codigo="PETR4")

        from . import services

        monitoramento = services.obter_stock_price(titulo)

        self.assertEqual(monitoramento.valor, VALOR_SUPERIOR)
        self.assertEqual(
            monitoramento.ultima_atualizacao,
            timezone("America/Recife").localize(datetime.strptime("2021-05-10 20:08:47", "%Y-%m-%d %H:%M:%S")),
        )
        self.assertEqual(monitoramento.variacao, Decimal("1.31"))


class GravaMonitoramentoComEnvioEmailTestCase(TestCase):
    def setUp(self):
        Titulo.objects.create(codigo="PETR4", descricao="Petrobras 4")
        Titulo.objects.create(codigo="PETR3", descricao="Petrobras 3")

    @patch("cotacoes.services.obter_stock_price", autospec=True, side_effect=mocked_obter_stock_price)
    def test_gravarMonitoramento_superior_com_envio_email_success(self, mock_services):
        titulo = Titulo.objects.get(codigo="PETR4")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("20.00"), limite_inferior=Decimal("10.00"))

        mail.outbox = []

        from cotacoes import tasks
        tasks.gravarMonitoramento(configuracao)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].body,
            "A ação {titulo} alcançou o valor de R$ {valor} e assim ultrapassou o limite {tipo_limite} configurado (R$ {valor_configurado}). É recomenada a {tipo_acao} desse título.".format(
                titulo=str(configuracao.titulo),
                valor=localize(VALOR_SUPERIOR),
                tipo_limite="superior",
                valor_configurado=localize(configuracao.limite_superior),
                tipo_acao="VENDA",
            ),
        )


    @patch("cotacoes.services.obter_stock_price", autospec=True, side_effect=mocked_obter_stock_price)
    def test_gravarMonitoramento_inferior_com_envio_email_success(self, mock_services):
        titulo = Titulo.objects.get(codigo="PETR3")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("25.00"), limite_inferior=Decimal("15.00"))

        mail.outbox = []

        from cotacoes import tasks
        tasks.gravarMonitoramento(configuracao)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].body,
            "A ação {titulo} alcançou o valor de R$ {valor} e assim ultrapassou o limite {tipo_limite} configurado (R$ {valor_configurado}). É recomenada a {tipo_acao} desse título.".format(
                titulo=str(configuracao.titulo),
                valor=localize(VALOR_INFERIOR),
                tipo_limite="inferior",
                valor_configurado=localize(configuracao.limite_inferior),
                tipo_acao="COMPRA",
            ),
        )

class GravaMonitoramentoSemEnvioEmailTestCase(TestCase):
    def setUp(self):
        Titulo.objects.create(codigo="PETR4", descricao="Petrobras 4")

    @patch("cotacoes.services.obter_stock_price", autospec=True, side_effect=mocked_obter_stock_price)
    def test_gravarMonitoramento_sem_envio_email_success(self, mock_services):
        titulo = Titulo.objects.get(codigo="PETR4")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"))

        mail.outbox = []

        from cotacoes import tasks
        tasks.gravarMonitoramento(configuracao)
        self.assertEqual(len(mail.outbox), 0)
        

class CriaAtualizaTarefaTestCase(TestCase):
    def setUp(self):
        Titulo.objects.create(codigo="PETR5", descricao="Petrobras 5")
        IntervalSchedule.objects.create(every=1, period=IntervalSchedule.MINUTES)
        IntervalSchedule.objects.create(every=30, period=IntervalSchedule.MINUTES)


    def test_cria_tarefa_success(self):
        titulo = Titulo.objects.get(codigo="PETR5")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"), intervalo=Intervalo.um_minuto)
        configuracao.save()

        self.assertIsNotNone(configuracao.tarefa)
        self.assertEquals(configuracao.tarefa.interval.every, 1)
        self.assertEquals(configuracao.tarefa.interval.period, IntervalSchedule.MINUTES)


    def test_cria_tarefa_failed(self):
        titulo = Titulo.objects.get(codigo="PETR5")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"), intervalo=Intervalo.quinze_minutos)
        self.assertRaises(IntervalSchedule.DoesNotExist, configuracao.save)

    
    def test_altera_periodicidade_success(self):
        titulo = Titulo.objects.get(codigo="PETR5")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"), intervalo=Intervalo.um_minuto)
        configuracao.save()

        self.assertIsNotNone(configuracao.tarefa)
        self.assertEquals(configuracao.tarefa.interval.every, 1)
        self.assertEquals(configuracao.tarefa.interval.period, IntervalSchedule.MINUTES)

        configuracao.intervalo = Intervalo.trinta_minutos
        configuracao.save()

        self.assertIsNotNone(configuracao.tarefa)
        self.assertEquals(configuracao.tarefa.interval.every, 30)
        self.assertEquals(configuracao.tarefa.interval.period, IntervalSchedule.MINUTES)


    def test_altera_status_success(self):
        titulo = Titulo.objects.get(codigo="PETR5")
        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"), intervalo=Intervalo.um_minuto)
        configuracao.save()

        self.assertIsNotNone(configuracao.tarefa)
        self.assertTrue(configuracao.tarefa.enabled)

        configuracao.status = Status.inativo
        configuracao.save()

        self.assertIsNotNone(configuracao.tarefa)
        self.assertFalse(configuracao.tarefa.enabled)

class RemoveConfiguracaoTituloTestCase(TestCase):
    def setUp(self):
        Titulo.objects.create(codigo="PETR6", descricao="Petrobras 6")
        IntervalSchedule.objects.create(every=1, period=IntervalSchedule.HOURS)


    def test_remove_configuracao_titulo_success(self):
        titulo = Titulo.objects.get(codigo="PETR6")
        pk_titulo = titulo.pk
        self.assertIsNotNone(pk_titulo)

        configuracao = ConfiguracaoTitulo(titulo=titulo, limite_superior=Decimal("30.00"), limite_inferior=Decimal("10.00"), intervalo=Intervalo.uma_hora)
        configuracao.save()

        pk_tarefa = configuracao.tarefa.pk
        self.assertIsNotNone(pk_tarefa)
        self.assertIsNotNone(PeriodicTask.objects.get(pk=pk_tarefa))
        
        naive_dt = datetime.strptime("2021-05-10 20:08:47", "%Y-%m-%d %H:%M:%S")
        datetime_brasil = timezone("America/Recife").localize(naive_dt)
        Monitoramento.objects.create(titulo=titulo, valor=VALOR_SUPERIOR, ultima_atualizacao=datetime_brasil, variacao=Decimal("1.31"))

        self.assertEquals(len(titulo.monitoramento_set.all()), 1)

        configuracao.delete()
        self.assertEquals(len(titulo.monitoramento_set.all()), 0)
        self.assertEquals(len(PeriodicTask.objects.all()), 0)

