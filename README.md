# Serviço de Gerenciamento de Usuários

<div style="text-align: center"> 

<a href="https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Users"><img src="https://travis-ci.org/Kalkuli/2018.2-Kalkuli_Users.svg?branch=master" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Users/test_coverage"><img src="https://api.codeclimate.com/v1/badges/2962e7551cfa698bdf87/test_coverage" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Users/maintainability"><img src="https://api.codeclimate.com/v1/badges/2962e7551cfa698bdf87/maintainability" /></a>
<a href="https://opensource.org/licenses/GPL-3.0"><img src="https://img.shields.io/badge/license-GPL-%235DA8C1.svg"/></a>

</div> 


# Ambientes

### Produção
Para acessar o ambiente de produção utilize o link abaixo: 
```https://kalkuli-users.herokuapp.com/```
 ### Homologação
Para acessar o ambiente de homologação clique no link abaixo:
```https://kalkuli-users-hom.herokuapp.com/```

***

<br>

## Configurando o ambiente
Para instruções de como instalar o Docker e o Docker-compose clique [aqui](https://github.com/Kalkuli/2018.2-Kalkuli_Front-End/blob/master/README.md).

***

<br>

## Colocando no ar
Com o _Docker_ e _Docker-Compose_ instalados, basta apenas utilizar os comandos:

```
chmod +x entrypoint.sh

docker-compose -f docker-compose-dev.yml build

docker-compose -f docker-compose-dev.yml up
```

Acesse o servidor local no endereço apresentado abaixo:   

[localhost:5003](http://localhost:5003/)   

Agora você já pode começar a contribuir!

***

<br>

## Configurando o Banco de Dados Local

Agora iremos configurar o Banco de Dados da aplicação. Siga um dos dois passos a seguir.

* Caso seja a primeira vez utilizando o serviço, utilize os comandos abaixo para criar o banco e atualizá-lo:


```
docker-compose -f docker-compose-dev.yml run base python manage.py recreatedb

docker-compose -f docker-compose-dev.yml run base python manage.py db upgrade
```

<br>

* Caso o banco já tenha sido criado localmente, e você deseja apenas atualizá-lo, utilize o seguite comando:

```
docker-compose -f docker-compose-dev.yml run base python manage.py db upgrade
```

<br>

* Case tenha feito alguma alteração nas models, utilize os seguintes comando para manter o controle de versão do banco.

```
docker-compose -f docker-compose-dev.yml run base python manage.py db migrate

docker-compose -f docker-compose-dev.yml run base python manage.py db upgrade
```

***

<br>


## Testando

Para rodar os testes utilize o comando:

```docker-compose -f docker-compose-dev.yml run base python manage.py test```

E para saber a cobertura dos testes utilize:

```docker-compose -f docker-compose-dev.yml run base python manage.py cov```

Para acessar a visualização do HTML coverage no browser, acesse a pasta htmlcov e abra o arquivo index.html no navegador, ou utilize o comando:

```google-chrome ./htmlcov/index.html```