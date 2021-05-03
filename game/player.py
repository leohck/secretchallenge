from random import choice
from game.estate import Estate


#  CONSTANTE QUE ARMAZENA OS TIPOS DE COMPORTAMENTO
BEHAVIORS = {
    1: (1, "impulsivo"),
    2: (2, "exigente"),
    3: (3, "cauteloso"),
    4: (4, "aleatorio")
}


class Player:
    """
    Jodador
    """

    def __init__(self, id_, behavior, balance=300):
        """

        :param id_: ID do jogador
        :param behavior: Tipo de comportamento
        :param balance: Saldo
        :attr estates: Lista de propriedades que o jogador possui
        :attr position: Posição em que o Jogador está no tabuleiro
        """
        assert (1 <= behavior <= 4), "The behavior param should be a number between 1 and 4"
        self.__id_ = id_
        self.__behavior = BEHAVIORS[behavior]
        self.__balance = balance
        self.__estates = []
        self.position = 0

    @property
    def id_(self):
        return self.__id_

    @property
    def balance(self):
        return self.__balance

    @property
    def estates(self):
        return self.__estates

    @property
    def behavior(self):
        return self.__behavior

    def __str__(self):
        return f'ID: {self.__id_} | {self.__behavior[1]} | R$ {self.balance}'

    def __repr__(self):
        return f'Player ({self.__id_})'

    def __eq__(self, other):
        return self.__id_ == other.__id_

    def __gt__(self, other):
        return self.balance > other.balance

    def can_buy_estate(self, estate):
        """
        Recebe uma instancia da propriedade e analisa se o jogador podera compra-lá, baseado nas seguintes regras:
            - O jogador IMPULSIVO compra qualquer propriedade sobre a qual ele parar.
            - O jogador EXIGENTE compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
            - O jogador CAUTELOSO compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
            - O jogador ALEATORIO compra a propriedade que ele parar em cima com probabilidade de 50%

        :param estate: Instancia da classe Estate (Propriedade)
        :flag can_buy: Flag que contem o resultado da analise, inicialmente o resultado é Negativo
        :return: boolean Se o Jogador pode ou não comprar a Propriedade
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        if estate.owner or estate.sale_price > self.balance:
            return False

        can_buy = False
        if self.behavior[0] == 1:
            """ Impulsivo """
            if estate.sale_price <= self.balance:
                can_buy = True
        elif self.behavior[0] == 2:
            """ Exigente """
            if estate.sale_price <= self.balance and estate.rent_price > 50:
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

        :param estate: Instancia da classe Estate (Propriedade)
        :return: None
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        self.__balance -= estate.price
        self.__estates.append(estate)
        estate.change_owner(self)

    def pay_rent(self, estate):
        """
        Realiza o pagamento de aluguel da Propriedade.

        :param estate: instancia da classe Estate (Propriedade)
        :return: None
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        self.__balance -= estate.rent_price

    def receive_rent_payment(self, estate):
        """
        Recebe o pagamento de aluguel da Propriedade.

        :param estate: instancia da classe Estate (Propriedade)
        :return: None
        """
        assert isinstance(estate, Estate), "param estate is not a valid Estate, e.g it isn't a instance of Estate"
        assert estate in self.estates, "the player must be the owner of the estate to receive rent payments"
        self.__balance += estate.rent_price

    def receive_benefit(self, amount):
        """
        Recebe um beneficio que sera adicionado na conta

        :param amount: Valor do Beneficio
        :return: None
        """
        self.__balance += amount
