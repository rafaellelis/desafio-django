import requests

from django.core.mail import send_mail
from django.utils.formats import localize
from cotacoes.models import ConfiguracaoTitulo, Monitoramento, Titulo
from datetime import datetime
from decimal import Decimal
from pytz import timezone
from django.conf import settings
from smtplib import SMTPException
from bs4 import BeautifulSoup


def cria_titulos_iniciar():
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
            

def obter_stock_price(titulo: Titulo):
    simbolo = titulo.codigo
    url = "{url}/stock_price?key={key}&symbol={simbolo}".format(
        url=settings.HG_BRASIL_API_URL, key=settings.HG_BRASIL_KEY, simbolo=simbolo
    )

    request = requests.get(url)
    
    if request.status_code == 200:
        response = request.json()
        dados_acao = response["results"][simbolo]
        valor = Decimal(dados_acao["price"])

        naive_dt = datetime.strptime(dados_acao["updated_at"], "%Y-%m-%d %H:%M:%S")
        datetime_brasil = timezone("America/Recife").localize(naive_dt)

        monitoramento = Monitoramento(
            titulo=titulo,
            valor=valor,
            ultima_atualizacao=datetime_brasil,
            variacao=Decimal(dados_acao["change_percent"]),
        )

        return monitoramento
    
    return None

def enviarEmail(configuracao: ConfiguracaoTitulo, valor: Decimal):
    subject = "[IMPORTANTE] Alerta de compra/venda de ações"
    ultrapassou_limite_inferior = True if valor < configuracao.limite_inferior else False

    message = "A ação {titulo} alcançou o valor de R$ {valor} e assim ultrapassou o limite {tipo_limite} configurado (R$ {valor_configurado}). É recomenada a {tipo_acao} desse título.".format(
        titulo=str(configuracao.titulo),
        valor=localize(valor),
        tipo_limite="inferior" if ultrapassou_limite_inferior else "superior",
        valor_configurado=localize(
            configuracao.limite_inferior if ultrapassou_limite_inferior else configuracao.limite_superior
        ),
        tipo_acao="COMPRA" if ultrapassou_limite_inferior else "VENDA"
    )

    destinatario=settings.EMAIL_RECIPIENT_DEFAULT 
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False)
    except SMTPException as e:
        print("Ocorreu um erro no envio do e-mail: ", e)
