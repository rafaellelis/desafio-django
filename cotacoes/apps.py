import sys
from django.apps import AppConfig

class CotacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cotacoes'

    def ready(self):
        from cotacoes import signals
        if 'runserver' in sys.argv:
            from cotacoes.services import cria_titulos_iniciar
            cria_titulos_iniciar()
        