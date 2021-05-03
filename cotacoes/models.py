import json

from django.db import models
from .enums import StatusConfiguracao, Intervalo
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils import timezone


class Titulo(models.Model):
    codigo = models.CharField(
        'Código do título', max_length=10, null=False, blank=False)
    descricao = models.CharField(
        'Descrição do título', max_length=100, null=False, blank=False)

    def __str__(self):
        return "Título: %s" % (self.codigo + '-' + self.descricao)

    def possuiConfiguracao(self):
        return hasattr(self, 'configuracaotitulo')


class ConfiguracaoTitulo(models.Model):
    titulo = models.OneToOneField(
        Titulo, on_delete=models.CASCADE, primary_key=True,)
    limite_superior = models.DecimalField(
        'Limite superior para venda', max_digits=8, decimal_places=2, null=False, blank=False)
    limite_inferior = models.DecimalField(
        'Limite inferior para compra', max_digits=8, decimal_places=2, null=False, blank=False)
    status = EnumChoiceField(
        StatusConfiguracao, default=StatusConfiguracao.ativa)
    created_at = models.DateTimeField(auto_now_add=True)
    intervalo = EnumChoiceField(
        Intervalo, default=Intervalo.quinze_minutos)
    tarefa = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def configurar_periodicidade_tarefa(self):
        self.tarefa = PeriodicTask.objects.create(
            name=str(self.titulo),
            task='titulo_task',
            interval=self.agendar,
            args=json.dumps([self.titulo_id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def agendar(self):
        if self.intervalo == Intervalo.quinze_minutos:
            return IntervalSchedule.objects.get(every=15, period='minutes')
        if self.intervalo == Intervalo.trinta_minutos:
            return IntervalSchedule.objects.get(every=30, period='minutes')
        if self.intervalo == Intervalo.quarenta_cinco_minutos:
            return IntervalSchedule.objects.get(every=45, period='minutes')
        if self.intervalo == Intervalo.uma_hora:
            return IntervalSchedule.objects.get(every=1, period='hours')

        raise NotImplementedError(
            '''Intervalo {interval} não foi adicionado.'''.format(
                interval=self.intervalo.value))

    def __str__(self):
        return str(self.titulo) + ': ' + str(self.limite_inferior) + ' / ' + str(self.limite_superior)


class Monitoramento(models.Model):
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    valor = models.DecimalField(
        'Valor do título', max_digits=8, decimal_places=2, null=False, blank=False)
    timestamp = models.DateTimeField(
        "Timestamp da coleta", null=False, blank=False)

    def __str__(self):
        return self.titulo.codigo + ': ' + self.valor + ' ' + self.timestamp


class ConfiguracaoApp(models.Model):
    intervalo_consulta = models.PositiveIntegerField(
        'Intervalo definido para coleta dos dados', default=15, null=False, blank=False)

    @classmethod
    def create(cls):
        config = cls(intervalo_consulta=15)
        return config

    def __str__(self):
        return str(self.intervalo_consulta) + ' minutos'
