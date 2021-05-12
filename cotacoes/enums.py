from enum import Enum

class Intervalo(Enum):
    # um_minuto = '1 min'
    quinze_minutos = '15 min'
    trinta_minutos = '30 mins'
    quarenta_cinco_minutos = '45 mins'
    uma_hora = '1 hora'


class Status(Enum):
    ativo = 'Ativo'
    inativo = 'Inativo'