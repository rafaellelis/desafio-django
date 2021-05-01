from django.contrib import admin

# Register your models here.
from .models import Titulo, ConfiguracaoTitulo, Monitoramento

admin.site.register(Titulo)
admin.site.register(ConfiguracaoTitulo)
admin.site.register(Monitoramento)