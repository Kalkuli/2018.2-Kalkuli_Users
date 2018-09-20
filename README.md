[![Build Status](https://travis-ci.org/Kalkuli/2018.2-Kalkuli_Users.svg?branch=master
)](https://travis-ci.com/Kalkuli/2018.2-Kalkuli_Users)

# Configurando o ambiente
Para instruções de como instalar o Docker e o Docker-compose clique [aqui](https://github.com/Kalkuli/2018.2-Kalkuli_Front-End/blob/master/README.md).


<br>

## Colocando no ar
Com o Docker e Docker-Compose instalados, basta apenas utilizar os comandos:

```chmod +x entrypoint.sh```

```docker-compose -f docker-compose-dev.yml build```

e

```docker-compose -f docker-compose-dev.yml up```

Acesse o servidor local no endereço apresentado abaixo:

http://localhost:5003/


Agora você já pode começar a contribuir!


## Testando

Para rodar os testes utilize o comando:

```docker-compose -f docker-compose-dev.yml run base python manage.py test```

E para saber a cobertura dos testes utilize:

```docker-compose -f docker-compose-dev.yml run base python manage.py cov```

Para acessar a visualização do HTML coverage no browser, acesse a pasta htmlcov e abra o arquivo index.html no navegador, ou utilize o comando:

```google-chrome ./htmlcov/index.html```