# Hermes

Projeto para o monitoramento de ações da B3 que permite o cadastro de paramêtros de túneis de negociação para o disparo de alertas por e-mail com oportunidades de compra e venda das ações configuradas.

### 🔧 Instalação

Para a execução da aplicação devemos baixar o projeto e seguir os passos abaixo.

Após baixar o projeto e garantir a instação do python e a criação do ambiente virtual venv devemos rodar os comando a seguir.

Instalar as dependências do projeto que estão listadas no arquivo requirements.txt
```
pip install -r requirements.txt
```
Aplicar as migrações no banco de dados
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Realizar a criação de um super usuário para acessar o painel administrativo /admin
```
python manage.py createsuperuser
```
Configurar o servidor de envio de e-mail no arquivo settings

Inicializar a aplicação com o comando
```
python manage.py runserver
```
A aplicação poderá ser acessada através da url localhost:8000 e localhost:8000/admin

Ao acessar a aplicação será necessário cadastrar um investidor, em seguida selecionar um investidar cadastrado, e cadastrar uma rotina de monitoração para este investidor

Para que a task agendas possam ser executadas é necessário iniciar o celery através do comando
```
python -m celery -A hermes worker --beat -l INFO
```
Obs.: O celery na sua versão 5 não funciona em ambiente windows, recomendo a ativação do wsl2 para utilização no windows, ou utilização do docker

## 🛠️ Construído com

* [Django] - O framework web usado
* [Celery] - Agendamento e execução das tasks
* [Redis] - Broker para gerenciamento das task
