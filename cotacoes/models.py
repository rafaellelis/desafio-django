from django.db import models

# Create your models here.
class Titulo(models.Model):
    codigo = models.CharField('Código do título', max_length=10, null=False, blank=False)
    descricao = models.CharField('Descrição do título', max_length=100, null=False, blank=False)

    def __str__(self):
        return "Título: %s" % self.descricao

    def possuiConfiguracao(self):
        return hasattr(self, 'configuracaoTitulo')


class ConfiguracaoTitulo(models.Model):
    titulo = models.OneToOneField(Titulo, on_delete=models.CASCADE, primary_key=True,)
    limite_superior = models.DecimalField('Limite superior para venda', max_digits=8, decimal_places=2, null=False, blank=False)
    limite_inferior = models.DecimalField('Limite inferior para compra', max_digits=8, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return str(self.titulo) + ': ' + str(self.limite_inferior) + ' / ' + str(self.limite_superior)

class Monitoramento(models.Model):
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    valor = models.DecimalField('Valor do título', max_digits=8, decimal_places=2, null=False, blank=False)
    timestamp = models.DateTimeField("Timestamp da coleta", null=False, blank=False)

    def __str__(self):
        return self.titulo.codigo + ': ' + self.valor + ' ' + self.timestamp


class ConfiguracaoApp(models.Model):
    intervalo_consulta = models.PositiveIntegerField('Intervalo definido para coleta dos dados', default=15, null=False, blank=False)
    
    @classmethod
    def create(cls):
        config = cls(intervalo_consulta = 15)
        return config

    def __str__(self):
        return str(self.intervalo_consulta) + ' minutos'