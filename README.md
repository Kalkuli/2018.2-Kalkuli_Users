# Serviço de Gerenciamento de Usuários

<div style="text-align: center"> 

<a href="https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Users"><img src="https://travis-ci.org/Kalkuli/2018.2-Kalkuli_Users.svg?branch=master" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Users/test_coverage"><img src="https://api.codeclimate.com/v1/badges/2962e7551cfa698bdf87/test_coverage" /></a>
<a href="https://codeclimate.com/github/Kalkuli/2018.2-Kalkuli_Users/maintainability"><img src="https://api.codeclimate.com/v1/badges/2962e7551cfa698bdf87/maintainability" /></a>
<a href="https://opensource.org/licenses/GPL-3.0"><img src="https://img.shields.io/badge/license-GPL-%235DA8C1.svg"/></a>

</div> 

# Configurando o ambiente
Para instruções de como instalar o Docker e o Docker-compose clique [aqui](https://github.com/Kalkuli/2018.2-Kalkuli_Front-End/blob/master/README.md).


<br>

### Colocando no ar
Com o _Docker_ e _Docker-Compose_ instalados, basta apenas utilizar os comandos:

```
chmod +x entrypoint.sh

docker-compose -f docker-compose-dev.yml build

docker-compose -f docker-compose-dev.yml up
```

Abra outro terminal, e execute o comando:


```
docker-compose -f docker-compose-dev.yml run base python manage.py recreate_db
```

Acesse o servidor local no endereço apresentado abaixo:   

[localhost:5003](http://localhost:5003/)   

Agora você já pode começar a contribuir!


## Testando

Para rodar os testes utilize o comando:

```docker-compose -f docker-compose-dev.yml run base python manage.py test```

E para saber a cobertura dos testes utilize:

```docker-compose -f docker-compose-dev.yml run base python manage.py cov```

Para acessar a visualização do HTML coverage no browser, acesse a pasta htmlcov e abra o arquivo index.html no navegador, ou utilize o comando:

```google-chrome ./htmlcov/index.html```