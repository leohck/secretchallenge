from random import choice, shuffle
from game.estate import Estate
from game.player import Player


class Match:
    """
    Jogo
    """

    MAX_ESTATES = 20
    MAX_ROUNDS = 1000
    BENEFIT_AMOUNT = 100

    def __init__(self, id_):
        self.__id_ = id_
        self.__round = 1
        self.estates = self.__generate_estates()
        self.players = self.__generate_players()
        self.__analytics = {
            "rounds": self.__round,
            "winner": ""
        }

    @property
    def id_(self):
        return self.__id_

    @property
    def round(self):
        return self.__round

    @property
    def analytics(self):
        return self.__analytics

    def __str__(self):
        return f'ID: {self.__id_} | ROUND: {self.__round}'

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
                    current_player_sequence.index(player.id_),
                    current_player_sequence.index(winner.id_)
                )
                winner = players[current_player_sequence[highest_order]]
        return winner

    def run(self):
        winner = None
        players = self.__get_random_players_sequence()
        while self.__round < self.MAX_ROUNDS:
            for player in players.values():
                #  1 - INICIAR JOGADA

                #  JOGAR DADO
                rolled_dice = self.roll_dice()

                #  2 - ANDAR NO TABULEIRO
                self.__change_player_position(player, rolled_dice)

                #  3 - VER PROPRIEDADE EM QUE PAROU
                estate = self.estates[player.position]

                #  4 - COMPRAR OU PAGAR ALUGUEL DA PROPRIEDADE
                #  4.1 - COMPRAR PROPRIEDADE
                if not estate.owner:
                    if player.can_buy_estate(estate):
                        player.buy_estate(estate)
                    else:
                        pass
                #  4.2 - PAGAR ALUGUEL
                elif estate.owner != player:
                    player.pay_rent(estate)
                    estate.owner.receive_rent_payment(estate)

                #  5 - FIM DA JOGADA

            #  REMOVE OS JOGADORES QUE NÃO ESTÃO APTOS A CONTINUAR JOGANDO
            players = self.__remove_losing_players(players)

            #  CHECA SE RESTA APENAS 1 JOGADOR NA PARTIDA
            """
            Caso a partida possua apenas 1 jogador restante, a mesma é encerrada e o jogador é considerado o vencedor
            """
            if len(players) == 1:
                k = list(players)
                winner = players[k[0]]

            if winner:
                break

            self.__round += 1

        winner = self.__get_winner_player(players) if winner is None else winner
        self.__analytics["rounds"] = self.__round
        self.__analytics["winner"] = winner.behavior[1]

        return self.__analytics
