
from django.db.models.signals import post_save
from django.dispatch import receiver

from .enums import StatusConfiguracao
from .models import ConfiguracaoTitulo


@receiver(post_save, sender=ConfiguracaoTitulo)
def create_or_update_periodicidade(sender, instance, created, **kwargs):
    if created:
        instance.configurar_periodicidade_tarefa()
    else:
        if instance.tarefa is not None:
            instance.tarefa.enabled = instance.status == StatusConfiguracao.ativa
            instance.tarefa.save()
