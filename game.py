"""
Created by: Leonardo Black
29/04/2021
Desafio Python ** - **
"""

from random import choice, shuffle


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
        :attr owner: Proprietário (Player)
        """
        self.__id_ = id_
        self.__owner = None
        self.price = price

    @property
    def id_(self):
        return self.__id_

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        assert value > 0, "The Price must be greater than zero"
        self._price = value
        self.__sale_price = self.price
        self.__rent_price = self.sale_price / 4

    @property
    def sale_price(self):
        return self.__sale_price

    @property
    def rent_price(self):
        return self.__rent_price

    @property
    def owner(self):
        return self.__owner

    def change_owner(self, new_owner):
        self.__owner = new_owner

    def __str__(self):
        return f'ID: {self.__id_} | SALE PRICE: R$ {self.sale_price} | RENT PRICE: R$ {self.rent_price} | OWNER ID: {self.owner.id_ if self.owner else "No Owner"}'

    def __repr__(self):
        return f'Estate ({self.__id_})'


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
        self.__behavior = self.__new_behavior(behavior)
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

    @staticmethod
    def __new_behavior(behavior):
        """
        Recebe o numero do tipo de comportamento do jogador e retorna sua caracteristica.
            - 1 Impulsivo
            - 2 Exigente
            - 3 Cauteloso
            - 4 Aleatorio

        :param behavior: Numero do Comportamento do jogador
        :return: Tupla contendo o id do comportamento e sua caracteristica.
        """
        behaviors = {
            1: (1, "Impulsivo"),
            2: (2, "Exigente"),
            3: (3, "Cauteloso"),
            4: (4, "Aleatorio")
        }
        return behaviors[behavior]

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


class Game:
    """
    Jogo
    """

    MAX_ESTATES = 20
    MAX_ROUNDS = 1000
    BENEFIT_AMOUNT = 100

    def __init__(self, id_):
        self.__id_ = id_
        self.round = 1
        self.estates = self.__generate_estates()
        self.players = self.__generate_players()
        self.__analytics = {
            "game": self.__id_,
            "rounds": self.round,
            "winner": ""
        }

    @property
    def id_(self):
        return self.__id_

    @property
    def analytics(self):
        return self.__analytics

    def __str__(self):
        return f'ID: {self.__id_} | ROUND: {self.round}'

    def __repr__(self):
        return f'Game ({self.__id_})'

    def __generate_estates(self):
        """
        Gera um dicionario contendo Propriedades(Estate) para serem vinculadas ao jogo
        :return: Dicionario de Estate (Propriedades)
        """
        estates = {}
        estates_rank = (
            ("A", 600),
            ("B", 300),
            ("C", 150)
        )
        for a in range(1, self.MAX_ESTATES + 1):
            estates[a] = Estate(a, choice(estates_rank)[1])
        return estates

    @staticmethod
    def __generate_players():
        """
        Gera um dicionario com 4 Jogadores(Player) para serem vinculados ao jogo

        :return: Lista de Player (Jogadores)
        """
        players = {
            1: Player(1, 1),
            2: Player(2, 2),
            3: Player(3, 3),
            4: Player(4, 4),
        }
        return players

    def __get_random_players_sequence(self):
        """
        Obtem uma sequência de jogadores definida aleatoriamente.
        Baseado na lista de jogadores já existente

        :return: Dicionario de Player (Jogadores)
        """
        keys = list(self.players.keys())
        shuffle(keys)
        random_sequence_players = dict()
        for key in keys:
            random_sequence_players.update({key: self.players[key]})
        return random_sequence_players

    @staticmethod
    def roll_dice():
        """
        Joga o dado.

        :return: Integer (1 ~ 6)
        """
        return choice((1, 2, 3, 4, 5, 6))

    def __benefit_player(self, player):
        """
        Deposita uma quantia de dinheiro na conta do Jogador informado.

        :param player: Jogador (Player) que irá receber o beneficio
        :return: None
        """
        player.receive_benefit(self.BENEFIT_AMOUNT)

    def __change_player_position(self, player, positions):
        """
        Atualiza a posição do jogador no tabuleiro

        :param player: Jogador (Player)
        :param positions: Numero de posições que o jogador deverá andar
        :return: None
        """
        next_position = player.position + positions
        # player.position = next_position if next_position < self.max_estates else next_position - self.max_estates
        if next_position > self.MAX_ESTATES:
            player.position = next_position - self.MAX_ESTATES
            self.__benefit_player(player)
            # print(f'COMPLETOU A VOLTA NO TABULEIRO E RECEBEU R$ {self.BENEFIT_AMOUNT}')
        else:
            player.position = next_position

    @staticmethod
    def __remove_losing_players(players):
        """
        Caso o saldo do jogador seja menor que 0:
                - Ele perde suas propriedades;
                - É removido da partida
        Apos isso as propriedades deste ex-jogador poderão ser compradas por outros jogadores

        :param players: Lista de Jogadores
        :return: Lista de Player (Jogadores)
        """
        players_to_remove = []
        for player in players.values():
            if player.balance < 0:
                players_to_remove.append(player)
        for player in players_to_remove:
            for estate in player.estates:
                estate.change_owner(None)
            players.pop(player.id_)
            # print(f'JOGADOR ({player}) PERDEU!')
        return players

    @staticmethod
    def __get_winner_player(players):
        """
        Define o jogador vencedor baseado em quem tem o maior saldo.
        Como criterio de desempate é considerada a ordem de turno dos jogadores.

        :param players: Lista de jogadores
        :return: Player
        """
        winner = None
        current_player_sequence = list(players)
        for player in players.values():
            if not winner:
                winner = player
            if player > winner:
                winner = player
            elif player.balance == winner.balance:
                highest_order = min(
                    current_player_sequence.index(player.__id_),
                    current_player_sequence.index(winner.__id_)
                )
                winner = players[current_player_sequence[highest_order]]
        return winner

    def run(self):
        winner = None
        players = self.__get_random_players_sequence()
        # print("====== INICIO DO JOGO ======")
        while self.round <= self.MAX_ROUNDS:
            # print("====== RODADA: %i =======" % self.round)
            for player in players.values():
                #  1 - INICIAR JOGADA
                # print(f'--------- JOGADOR ({player}) ----------')

                #  JOGAR DADO
                # print('Jogou o dado...')
                rolled_dice = self.roll_dice()
                # print(f'Andou {rolled_dice} casas')

                #  2 - ANDAR NO TABULEIRO
                self.__change_player_position(player, rolled_dice)
                # print(f'Posição Atual: {player.position}')

                #  3 - VER PROPRIEDADE EM QUE PAROU
                estate = self.estates[player.position]
                # print(f'Parou na Propriedade ({estate})')

                #  4 - COMPRAR OU PAGAR ALUGUEL DA PROPRIEDADE
                #  4.1 - COMPRAR PROPRIEDADE
                if not estate.owner:
                    if player.can_buy_estate(estate):
                        player.buy_estate(estate)
                        # print(f'Comprou a Propriedade no valor de R$ {estate.sale_price}')
                    else:
                        pass
                        # print('Não comprou a Propriedade')
                #  4.2 - PAGAR ALUGUEL
                elif estate.owner != player:
                    player.pay_rent(estate)
                    estate.owner.receive_rent_payment(estate)
                    # print(f'Pagou o aluguel da Propriedade no valor de R$ {estate.rent_price} '
                    #       f'Para o Jogador: ({estate.owner.id_})')

                #  5 - FIM DA JOGADA
                # print(f'JOGADOR ({player})')
                # print('---------------------------------' * 2)

            #  REMOVE OS JOGADORES QUE NÃO ESTÃO APTOS A CONTINUAR JOGANDO
            players = self.__remove_losing_players(players)

            #  CHECA SE RESTA APENAS 1 JOGADOR NA PARTIDA
            """
            Caso a partida possua apenas 1 jogador restante, a mesma é encerrada e o jogador é considerado o vencedor
            """
            if len(players) == 1:
                k = list(players)
                winner = players[k[0]]

            # print("====== FIM RODADA ======")

            if winner:
                break

            self.round += 1

        # print("====== FIM DO JOGO ======")
        winner = self.__get_winner_player(players) if winner is None else winner
        # print(f'JOGADOR: {winner} GANHOU!')
        self.__analytics["rounds"] = self.round
        self.__analytics["winner"] = winner

        return self.__analytics
