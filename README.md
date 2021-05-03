[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-3610/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-3710/)
[![Python 3.7](https://img.shields.io/badge/python-3.8-green.svg)](https://www.python.org/downloads/release/python-3810/)
[![Python 3.7](https://img.shields.io/badge/python-3.9-green.svg)](https://www.python.org/downloads/release/python-394/)

[![Build Status](https://travis-ci.com/leohck/secretchallenge.svg?branch=master)](https://travis-ci.com/leohck/secretchallenge)

# Desafio Secreto


Utilizando a linguagem de programação Python,
desenvolver um jogo semelhante ao Banco Imobiliário, obedecendo os requisitos propostos.

<hr>

# 1 - Requisitos
    - Jogadores = 4
    - Propriedades = 20
    - N° maximo de rodadas = 1000
    - Beneficio por jogador dar uma volta no tabuleiro = 100
    - Cada propriedade tem um custo de venda, um valor de aluguel, um proprietário caso já estejam compradas
    - Saldo incial dos jogadores = 300
    - O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
    - O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
    - O jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
    - O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50
    - O Jogador só pode comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro.
    - Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
    - Ao cair em uma propriedade que tem proprietário, o jogador deve pagar ao proprietário o valor do aluguel da propriedade.

<hr>

# 2 - Perguntas que a aplicação deve responder após ser executada
- Quantas partidas terminam por time out (1000 rodadas)?
- Quantos turnos em média demora uma partida?
- Qual a porcentagem de vitórias por comportamento dos jogadores?
- Qual o comportamento que mais vence?

<hr>

# 3 - Dependências
- Python 3.6+

- flask
- flask-restx
- Flask-HTTPAuth

<hr>

# 4 - Executar
Para subir a aplicação com API REST com sucesso, é recomendado que você crie uma virtualenv e instale as depêndencias 
do arquivo requirements.txt antes de executar o arquivo api.py

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python api.py`

Após executar a aplicação estará disponivel na porta 5000 **(localhost:5000)**

Recomendo visitar a documentação para realizar o teste, para isso, acesse a url: **(localhost:5000/docs)**
<hr>

# 5 - Docker
Caso prefira testar a aplicação utilizando docker, rode o comando:

`docker run --name lblackpythondxapi --publish 5000:5000 leohck/desafiobrasilprev:v1.1`

Esse container esta hospedado no meu repositório do DockerHub (leohck)