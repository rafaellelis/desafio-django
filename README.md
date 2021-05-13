<br />
<p align="center">

  <h3 align="center">Desafio INOA</h3>

  <p align="center">
    O objetivo dessa aplicação é monitorar os preços de ativos da B3.
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## Sobre o projeto

O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos.

**Os seguintes requisitos funcionais foram implementados:**

- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável, para consulta posterior;

- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo;

- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior;

- Ao iniciar a aplicação, obter a lista de ativos disponíveis na fonta pública.


### Ferramentas necessárias

* [Python3](https://www.python.org/downloads/)
* [Pip3](https://pypi.org/project/pip/)
* [Docker](https://www.docker.com/products/docker-desktop)


<!-- GETTING STARTED -->
## Primeiro passos

Siga os seguintes passos para rodar o projeto localmente:

### Pré-requisitos

* Instalar o Redis via Docker
  ```sh
  docker run -d -p 6379:6379 redis
  ```
Para o esquema de agendamento de tarefas, optei por usar o [Celery Beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html) em conjunto com o Redis. A escolha do Redis se deu ele atuar como um broker de envio e recebimento de mensagens de fácil instalação e configuração.

* Criar uma chave na [HG brasil](https://hgbrasil.com/). As informações de preço da ação são obtidos a partir da [API de dados econômicos da HG brasil](https://hgbrasil.com/status/finance). A escolha se deu por essa API fornecer dados das cotações dos ativos em tempo real (com atrasos de 15 minutos a 1 hora) e por possuir um plano gratuito.

### Instalação

1. Clone o repositório
   ```sh
   git clone https://github.com/rafaellelis/desafio-django.git
   ```
2. Instale as dependências
   ```sh
   pip install -r requirements.txt
   ```
3. Criar dentro da pasta do projeto (**desafioInoa**) um arquivo **.env** e configurar as seguintes variáveis:
   ```dosini
    HG_BRASIL_KEY=<chave criada no HG brasil>

    EMAIL_RECIPIENT_DEFAULT='<destinatório para envio dos alertas de preço>'
    EMAIL_HOST='<host para envio do e-mail>'
    EMAIL_PORT='<porta para envio do e-mail>'

    # Informações opcionais para autenticação SMTP para o EMAIL_HOST.
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER='<usuario de login>'
    EMAIL_HOST_PASSWORD='<senha>'
   ```
4. Aplique as configurações de banco
   ```sh
   python manage.py migrate
   ```


<!-- USAGE EXAMPLES -->
## Executando

1. Inicie o servidor:
   ```sh
    python manage.py runserver
   ```
2. Inicie o serviço do Celery Beat para execução das tarefas nos intervalos configurados na aplicação:
   ```sh
    celery -A desafioInoa worker --beat --scheduler django --loglevel=info
   ```
   Esse comando só deve ser utilizado em ambiente de desenvolvimento, não sendo recomendado o uso em produção.
