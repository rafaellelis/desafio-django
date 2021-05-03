from celery import shared_task

from .models import ConfiguracaoTitulo


@shared_task(name="titulo_task")
def titulo_task(titulo_id):
    configuracao = ConfiguracaoTitulo.objects.get(pk=titulo_id)
    # Do heavy computation with variables in setup model here.

    print('''Running task for setup {setup_title}.'''.format(
        setup_title=str(configuracao.titulo)))