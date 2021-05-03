from enum import Enum

class Intervalo(Enum):
    quinze_minutos = '15 min'
    trinta_minutos = '30 mins'
    quarenta_cinco_minutos = '45 mins'
    uma_hora = '1 hora'


class StatusConfiguracao(Enum):
    ativa = 'Ativa'
    inativa = 'Inativa'