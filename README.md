# Bem vindo ao teste DBA - Backend

Siga as instruções abaixo.

## Passos
1. Faça um fork deste respositório;
2. Siga atentamente as instruções da prova em avaliação, localizada no diretório avaliacao;
3. Quando finalizar o teste faça um pull request
4. Aguarde os próximos passos

## Sobre a avaliação
- Serão avaliados os seguintes pontos:
- Organização do código;
- Técnicas de framework
- Objetividade
- Prazo de entrega

##criação do container Docker

- #sudo docker run -p 8080:80 --name teste-dev -it ubuntu

- comando -it para o modo interativo com o bash
- comando -d para rodar em segundo plano

##executando
- #sudo docker exec -it teste-dev bash

##copiando arquivos do PC host para o container 
- # sudo docker cp teste-dev-backend teste-dev:/home

