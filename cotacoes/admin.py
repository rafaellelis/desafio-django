from django.contrib import admin

# Register your models here.
from .models import Titulo, Configuracao, Monitoramento

admin.site.register(Titulo)
admin.site.register(Configuracao)
admin.site.register(Monitoramento)