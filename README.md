## Desafio aiqfome

# Descrição

Foram escolhidas Python e Flask como ferramentas por maior praticidade. Como o desafio descreve dois tipos de dados (usuários e produtos), sendo que um deles é resgatado de uma API externa, com uma relação N-N entre eles (favoritos), foram criadas duas tabelas no banco de dados: uma para usuários e outra para favoritos, cada uma com sua blueprint. Além disso, há um arquivo separado para gerenciar as conexões com o banco de dados.

# Instalação

Usou-se pipenv para garantir o versionamento correto de todas as ferramentas. Primeiramente, deve instalar python3.7 ou mais recente, assim como pipenv. E.g.:

```
$ pip install --user pipenv
```

Após isso, dentro do diretório principal do projeto, usa-se o seguinte comando para instalar as dependências:

```
$ pipenv install
```

O banco de dados usa as variáveis de ambiente DB_HOST, DB_NAME, DB_USER, DB_PASSWORD e DB_PORT.

# Execução

Para executar a aplicação, basta executar um dos seguintes comandos. Em Windows:

```
$ set "FLASK_APP=.\src\__init__.py" && pipenv run flask run
```

E em Linux:

```
$ export FLASK_APP=./src/__init__.py && pipenv run flask run
```

# Uso

Os endpoints da API estão exemplificados nos decoradores das funções nos arquivos `users.py` e `favorites.py`. As funções `create_user` e `edit_user` ainda requerem parâmetros adicionais via json ou form. E.g.:

```
$ curl http://localhost:5000/users/10 --header "Content-Type: application/json" --request EDIT --data '{"user_name": "Pedro Salgado", "user_email": "trezelistras@funarte.gov.br"}'
```

# Discussão

O uso de uma API externa para os produtos favoritos cria um potencial gargalo de performance na aplicação. Para a função `get_user_favorites`, obtem-se toda a lista de produtos e filtra-se os resultados, para evitar chamar a API de produtos múltiplas vezes. Para a função `add_user_favorite`, obtem-se apenas o produto que deve ser verificado. Ainda existe espaço para exploração de otimizações. Uma solução possível seria usar uma forma de cache que é atualizada preguiçosamente.