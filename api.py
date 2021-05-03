from flask_httpauth import HTTPBasicAuth
from flask_restx import Api, Resource
from flask import Flask, jsonify
from game.controller import Controller


class Server:
    def __init__(self):
        """
        Gera instancia do flask e flask_restplus para serem utilizadas no projeto
        self.app recebe o nome do arquivo como o nome da aplicação
        self.api recebe as configurações do SWAGGER
        """
        self.app = Flask(__name__)
        self.api = Api(
            app=self.app,
            version='1.1',
            title='BrasilPrev',
            description='Leonardo Black - Desafio PythonDX ',
            doc='/docs'
        )
        self.app.config['RESTPLUS_MASK_SWAGGER'] = False

    def run(self):
        """
        Roda o servidor da aplicação em modo debug e localhost
        para colocar a aplicação visivel no ip, precisa incluir nos parametros (host='0.0.0.0')
        e desabilitar o debug (debug=False) ou apenas excluir o parametro
        """
        self.app.run(
            host='0.0.0.0',
            debug=False
        )


server = Server()

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


if __name__ == '__main__':
    server.run()
