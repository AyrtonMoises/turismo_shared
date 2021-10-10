# Turismo Shared
Um espaço para publicação de opiniões sobre viagens a pontos turísticos ao redor do mundo usando o framework Django 

### Instalação
#### Clonar repositório
```
git clone https://github.com/AyrtonMoises/turismo_shared.git
```

#### Ambiente virtual
```
python3 -m venv myenv
source myenv/bin/activate
```

#### Instalação pacotes
```
pip install -r requirements.txt
crie suas variáveis de ambiente dentro de um arquivo .env na pasta setup
Exemplo:
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_URL=postgres://usuario:senha@127.0.0.1:5432/sua_database
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=SMTP
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=senha_app_conta_gmail
DEFAULT_FROM_EMAIL=seu_email@gmail.com
```

#### Migrações
```
python manage.py makemigrations
python manage.py migrate
```
### Arquivos estáticos
```
python manage.py collectstatic
```

#### Testes
```
python manage.py test
```

#### Execução
```
python manage.py runserver
```

#### Acesse no Browser
http://localhost:8000/

#### Crie um usuário para acessar a área administrativa
```
python manage.py createsuperuser
```
