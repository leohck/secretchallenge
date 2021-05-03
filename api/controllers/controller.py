from flask_httpauth import HTTPBasicAuth
from flask_restx import Resource
from flask import jsonify
from api.server.instance import server
from game.controller import Controller


app = server.app  # herda o App do flask instanciado no instance.py
api = server.api  # herda o Api do flask_restplus instanciado no instance.py
auth = HTTPBasicAuth()

#  Cria o namespace para o Jogo
game_ns = api.namespace('game', description='Game Namespace')


@auth.verify_password
def verify_basic_auth(username, password):
    """
    Verifica se o usuario esta autenticado baseado no protocolo HTTP Basic Auth
    :param username: usuario
    :param password: senha
    :return: usuario se o usuario e senha forem corretos
    """

    if username == 'brasilprev' and password == 'brasilprev':
        return username


@game_ns.route("/analyze/<int:number_of_matches>")
class Matches(Resource):
    @auth.login_required()
    def get(self, number_of_matches):
        gc = Controller()
        gc.run_matches(number_of_matches)
        data = gc.analyze_matches()
        return jsonify(data)
