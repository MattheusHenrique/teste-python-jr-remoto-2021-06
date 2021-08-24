# MagPy
API para registro de projetos python. 

## Visão geral da API:
Uma REST API para times de desenvolvimento que buscam sempre usar as tecnologias
mais recentes e procuram uma forma eficiente de registrar seus projetos e as suas
respectivas dependencias. A API ajudara o time a ter o controle de seus projetos e tambem poder fornecer facilmente as dependencias utilizados em projetos internos para terceiros.
Mais uma maneira de gerenciar suas dependencias além de um Pipfile.

## Recursos da API:
Registre seus projetos e suas dependencias utilizando essa ferramenta. A api recebe um projeto com seu nome e uma lista de pacotes. Cada pacote tem seu nome que deve ser especificado e sua versão que podera ser 
opcional. A api verifica se os pacotes e sua versão existem, caso a versão não seja especificada a API ira buscar a ultima versão existente na API do pypi. Os pacotes obrigatoriamente devem estar disponiveis
no pypi. 


## Instalação local do projeto:
- Clone esse repositorio.
- Use `./manage.py migrate` para criar o banco de dados.
- Em seguida: `./manage.py runserver` para iniciar o servidor.
- O servidor estará ativo por padrão em http://localhost:8000/
- Caso não funcione recomenda-se instalar as dependencias contindas 
em requiremenst.txt `pip install -r requiremenst.txt`


## Testar a API:
Existem algumas camadas de teste nessa API. Os testes que envolvem
modelos, serializers e metodos para executa-los: `./manage.py tests`
Para testar de forma geral existem os arquivos `tests-api.js` e
`tests-open.js`. Você pode executar esses testes com o [k6](https://k6.io/). Para instalar o k6
basta [baixar o binário](https://github.com/loadimpact/k6/releases) para o seu
sistema operacional (Windows, Linux ou Mac).

Exemplo de teste: `k6 run tests-open.js`.
Certifique-se de estar com o servidor rodando na porta 8000.
Caso seja necessario trocar a porta basta editar os arquivos .js

### Endpoits:

### `GET /api/projects/`
Retorna os projetos registrados na API. `Response 200`

Exemplo:
```
GET /api/projects/

HTTP 200 OK
[
    {
        "name": "titan",
        "packages": [
            {
                "name": "Django",
                "version": "3.2.6"
            },
            {
                "name": "graphene",
                "version": "2.0"
            }
        ]
    }
]
```

### `POST /api/projects/`
Endpoint de criação de novos projetos. Recebe um request com o nome do
projeto, a lista de suas dependencias com seus nomes e 
versões(caso não especificada ira registrar com a ultima 
versão disponivel no pypi) Se os dados forem enviados com um 
formato invalido ou o nome de alguma dependecia ou sua respectiva 
versão não existam a API lançara um erro especificando o problema 
e o status HTTP 400 (BAD REQUEST). 
O status para sucesso é HTTP 201

<br>
EXEMPLOS:
<br>

#### Pacote sem versão especificada:

Corpo da requisição:

```
POST /api/projects
{
    "name": "titan",
    "packages": [
        {"name": "Django"},
        {"name": "graphene", "version": "2.0"}
    ]
}
```

Response:
```
HTTP 201 Created
{
    "name": "titan",
    "packages": [
        {"name": "Django", "version": "3.2.5"},  // Usou a versão mais recente
        {"name": "graphene", "version": "2.0"}   // Manteve a versão especificada
    ]
}
```
<br>

#### Pacote com o nome incorreto:

Corpo da requisição:
```
POST /api/projects/
{
    "name": "titan",
    "packages": [
        {"name": "pypypypypypypypypypypy"}
    ]
}
```
Response:
```
HTTP 400 Bad Request
{
    "error": "One or more packages doesn't exist"
}
```
<br>

#### Pacote com versão não existente:

Corpo da requisição:
```
POST /api/projects
{
    "name": "titan",
    "packages": [
        {"name": "graphene", "version": "1900"}
    ]
}
```
Reponse:
```
HTTP 400 Bad Request
{
    "error": "One or more packages doesn't exist"
}
```
<br>

### `GET /api/projects/<project_name>/`
Devolve o projeto e seus pacotes.

exemplo:
<br>

Response:
```
GET /api/projects/titan/
HTTP 200 OK

{
    "name": "titan",
    "packages": [
        {
            "name": "Django",
            "version": "3.2.6"
        },
        {
            "name": "graphene",
            "version": "2.0"
        }
    ]
}
```

<br>

### `DELETE /api/projects/<project_name>/`
Deleta o projeto especificado na rota e retorna o codigo HTTP 204.

Response:
```
HTTP 204 No Content
[]
```

### `GET /api/swagger/` e `GET /api/redoc/`
Documentação gerada automaticamente.


### Dependencias:
```django = "~=3.2"
djangorestframework = "~=3.12"
requests = "~=2.25"
psycopg2 = "~=2.9"
gunicorn = "~=20.1"
whitenoise = "~=5.2"
django-heroku = "~=0.3"
drf_yasg = "~=1.20"
```


## Autor
Mattheus Henrique
Email: ma77heusdev@gmail.com

## Considerações finais
O projeto está aberto para contribuições. Basta
fazer um fork do projeto e mandar o seu PR.


