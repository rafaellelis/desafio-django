from django.apps import AppConfig


class CotacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cotacoes'

    def ready(self):
        from .models import ConfiguracaoApp
        from cotacoes import signals
        configuracoes = ConfiguracaoApp.objects.all()
        if len(configuracoes) == 0:
            config = ConfiguracaoApp.objects.create()
            config.save(self)
        