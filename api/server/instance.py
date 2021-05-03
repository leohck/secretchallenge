from flask import Flask
from flask_restx import Api


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
            debug=False
        )


server = Server()  # Instancia o servidor para ser usado na aplicação
