import json

from django.db import models
from .enums import Status, Intervalo
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils import timezone
from decimal import Decimal


class Titulo(models.Model):
    codigo = models.CharField(
        'Código', max_length=10, null=False, blank=False)
    descricao = models.CharField(
        'Descrição', max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = EnumChoiceField(Status, default=Status.ativo)

    def __str__(self):
        return "%s" % (self.codigo + ' - ' + self.descricao)

    def possuiConfiguracao(self):
        return hasattr(self, 'configuracaotitulo')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalhaTitulo', args=[str(self.id)])


class ConfiguracaoTitulo(models.Model):
    titulo = models.OneToOneField(
        Titulo, on_delete=models.CASCADE, primary_key=True,)
    limite_superior = models.DecimalField(
        'Limite superior para venda (R$)', max_digits=8, decimal_places=2, null=False, blank=False)
    limite_inferior = models.DecimalField(
        'Limite inferior para compra (R$)', max_digits=8, decimal_places=2, null=False, blank=False)
    status = EnumChoiceField(Status, default=Status.ativo)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
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
        # if self.intervalo == Intervalo.um_minuto:
        #     return IntervalSchedule.objects.get(every=1, period=IntervalSchedule.MINUTES)
        if self.intervalo == Intervalo.quinze_minutos:
            intervalo = IntervalSchedule.objects.get_or_create(every=15, period=IntervalSchedule.MINUTES)
            return intervalo
        if self.intervalo == Intervalo.trinta_minutos:
            intervalo = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.MINUTES)
            return intervalo
        if self.intervalo == Intervalo.quarenta_cinco_minutos:
            intervalo = IntervalSchedule.objects.get_or_create(every=40, period=IntervalSchedule.MINUTES)
            return intervalo
        if self.intervalo == Intervalo.uma_hora:
            intervalo = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)
            return intervalo

        raise NotImplementedError(
            '''Intervalo {interval} não foi adicionado.'''.format(
                interval=self.intervalo.value))

    def __str__(self):
        return str(self.titulo) + ': ' + str(self.limite_inferior) + ' / ' + str(self.limite_superior)


class Monitoramento(models.Model):
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    valor = models.DecimalField(
        'Valor do título', max_digits=10, decimal_places=2, null=False, blank=False)
    timestamp = models.DateTimeField(
        "Horário da coleta", null=False, blank=False, auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(
        "Data/Hora da última atualização do valor da ação", default=timezone.now)
    variacao = models.DecimalField(
        'Variação (%)', max_digits=4, decimal_places=2, default=Decimal('0.00'))

    def as_dict(self):
        return {'timestamp': self.timestamp, 'valor': self.valor}

    def __str__(self):
        return str(self.titulo.codigo) + ': ' + str(self.valor) + ' ' + str(self.timestamp)
