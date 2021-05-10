import requests

from bs4 import BeautifulSoup
from django.apps import AppConfig
from django.conf import settings


class CotacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cotacoes'

    def ready(self):
        from cotacoes import signals

        Titulo = self.get_model('Titulo')
        url = settings.HG_BRASIL_SYMBOLS
        req = requests.get(url)
        
        data = BeautifulSoup(req.text, "html.parser")
        divTag = data.find("div", {"class": "card-body pt-2"})
        
        ulTag = divTag.find("ul")
        liTags = ulTag.find_all("li")
        print("Número de ações encontradas: ", len(liTags))

        for li in liTags:
            acoes = li.text.rsplit("-", 1)
            obj, created = Titulo.objects.get_or_create(codigo=acoes[1].strip(), descricao=acoes[0].strip())
            if created:
                print('Novo título criado: ', str(obj))