"""
Created by: Leonardo Black
29/04/2021

Desafio Python ** - **
"""
"""
Jogo estilo banco imobiliário
Composto por:
    - 4 jogadores
    - 20 propriedades
    - 1000 n° maximo de rodadas
Regras:
    - Se saldo negativo o jogador é eliminado e caso tenha propriedades as mesmas podem ser compradas.
    - Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida, sendo ele o Vencedor
    - Se o jogo chegar a 1000 rodadas Vence o jogador com mais saldo.
    - Ao cair em uma propriedade sem proprietário, o jogador pode escolher entre comprar ou não a
        propriedade. Esse é a única forma pela qual uma propriedade pode ser comprada.
    - Ao cair em uma propriedade que tem proprietário, ele deve pagar ao proprietário o valor do aluguel da
        propriedade.
    - Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo
"""
from random import choice


class Estate:
    """
    Propriedade
    """
    def __init__(self, id_, price):
        """
        :param id_: ID da propriedade
        :param price: Valor da propriedade
        :attr sale_price: Preço de Venda
        :attr rent_price: Preço do aluguel
        :attr owner_id: Proprietário
        """
        self.id_ = id_
        self.price = price
        self.sale_price = self.price
        self.rent_price = self.sale_price / 4
        self.owner_id = None

    """ 
    As linhas abaixo permitem que o valor de compra e valor de aluguel da propriedade aumemtem 
    cada vez que ela é comprada, baseado no valor de venda. Na minha opinião isso deixaria o jogo mais interessante
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        self.sale_price = self.price + (value / 2)
        self.rent_price = self.sale_price / 4

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        self._owner_id = value
        if value:
            self.price = self.sale_price
    """

    def __str__(self):
        return f'ID: {self.id_} | SALE PRICE: {self.sale_price} | OWNER ID: {self.owner_id if self.owner_id else "No Owner"}'

    def __repr__(self):
        return f'Estate ({self.id_})'


class Player:
    """
    Jodador
    """
    def __init__(self, id_, behavior, balance=300):
        assert (1 <= behavior <= 4), "The behavior param should be a number between 1 and 4"
        """
        :param id_: ID do jogador
        :param behavior: Tipo de comportamento
        :param balance: Saldo
        :attr estates: Lista de propriedades que o jogador possui
        """
        self.id_ = id_
        self.behavior = self.set_behavior(behavior)
        self.balance = balance
        self.estates = []

    def __str__(self):
        return f'ID: {self.id_} | {self.behavior[1]} | {self.balance}'

    def __repr__(self):
        return f'Player ({self.id_})'

    @staticmethod
    def set_behavior(behavior):
        """
        Recebe o numero do tipo de comportamento do jogaodor e retorna sua caracteristica.
            - 1 Impulsivo
            - 2 Exigente
            - 3 Cauteloso
            - 4 Aleatorio
        :param behavior: Numero do Comportamento do jogador
        :return: Tupla contendo o numero do comportamento e sua caracteristica.
        """
        behaviors = [
            (1, "Impulsivo"),
            (2, "Exigente"),
            (3, "Cauteloso"),
            (4, "Aleatorio")
        ]
        return behaviors[behavior - 1]

    def can_buy_estate(self, estate):
        """
        Recebe uma instancia da propriedade e analisa se o jogador pode compra-lá, baseado nas seguintes regras:
            - O jogador IMPULSIVO compra qualquer propriedade sobre a qual ele parar.
            - O jogador EXIGENTE compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
            - O jogador CAUTELOSO compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
            - O jogador ALEATORIO compra a propriedade que ele parar em cima com probabilidade de 50%

        :param estate: Instancia da classe Estate (Propriedade)
        :flag can_buy: Flag que contem o resultado da analise, inicialmente o resultado é Negativo
        :return: boolean Se o Jogador pode ou não comprar a Propriedade
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        can_buy = False
        if self.behavior[0] == 1:
            """ Impulsivo """
            if estate.sale_price <= self.balance:
                can_buy = True
        elif self.behavior[0] == 2:
            """ Exigente """
            if estate.rent_price > 50:
                can_buy = True
        elif self.behavior[0] == 3:
            """ Cauteloso """
            if self.balance - estate.sale_price >= 80:
                can_buy = True
        elif self.behavior[0] == 4:
            """ Aleatorio """
            if estate.sale_price <= self.balance:
                if choice((False, True)):
                    can_buy = True
        return can_buy

    def buy_estate(self, estate):
        """
        Recebe uma instancia da propriedade e realiza a compra da mesma.
        após isso insere na lista de propriedades que o jogador pertence
        e seta o atributo owner_id da Propriedade com o seu própio ID

        :param estate: Instancia da classe Estate (Propriedade)
        :return: None
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        self.balance -= estate.price
        self.estates.append(estate)
        estate.owner_id = self.id_
