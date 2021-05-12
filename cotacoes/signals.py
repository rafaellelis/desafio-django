
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from .enums import Status
from .models import ConfiguracaoTitulo, Monitoramento


@receiver(post_save, sender=ConfiguracaoTitulo)
def create_or_update_periodicidade(sender, instance, created, **kwargs):
    if created:
        instance.configurar_periodicidade_tarefa()
    elif instance.tarefa is not None:
        instance.tarefa.interval = instance.agendar
        instance.tarefa.enabled = instance.status == Status.ativo
        instance.tarefa.save()


@receiver(post_delete, sender=ConfiguracaoTitulo)
def delete_configuracao_titulo(sender, instance, *args, **kwargs):
    # remove a tarefa
    PeriodicTask.objects.get(pk=instance.tarefa.id).delete()
    #remove os monitoramentos
    Monitoramento.objects.filter(titulo_id=instance.titulo_id).delete()