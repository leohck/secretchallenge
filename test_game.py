"""
Created by: Leonardo Black
29/04/2021

Teste Unitário Orientado a Requisito.

Estes testes garantem que as implementações da aplicação estejam em conformidade com os Requisitos passados.
E que futuras alterações e features não quebrem a aplicação.

Requisitos:
    - Jogadores = 4
    - Propriedades = 20
    - N° maximo de rodadas = 1000
    - Beneficio por dar uma volta no tabuleiro = 100
    - Cada propriedade tem um custo de venda, um valor de aluguel, um proprietário caso já estejam compradas
    - Saldo incial dos jogadores = 300
    - O jogador impulsivo compra qualquer propriedade sobre a qual ele parar.
    - O jogador exigente compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
    - O jogador cauteloso compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
    - O jogador aleatório compra a propriedade que ele parar em cima com probabilidade de 50
    - O Jogador só pode comprar propriedades caso ela não tenha dono e o jogador tenha o dinheiro.
    - Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
    - Ao cair em uma propriedade que tem proprietário, o jogador deve pagar ao proprietário o valor do aluguel da propriedade.
"""

import unittest
from unittest import TestCase
from game.estate import Estate
from game.player import Player, BEHAVIORS
from game.match import Match


class TestPlayer(TestCase):
    """
    Testes unitarios da classe Player (Jogador)
    """

    def setUp(self):
        self.players = {
            "impulsivo": Player(1, 1),
            "exigente": Player(2, 2),
            "cauteloso": Player(3, 3),
            "aleatorio": Player(4, 4)
        }
        self.estate = Estate(1, 500)

    def test_player_initial_balance(self):
        """
        Testa se o saldo inicial do jogador == 300

        :return: None
        """
        self.assertEqual(300, self.players["impulsivo"].balance)

    def test_if_player_can_buy_estates_correctly(self):
        """
        Testa se o jogador pode comprar uma propriedade somente se ela não possuir um proprietario e ele tiver o dinheiro da compra

        :return: None
        """
        self.estate.change_owner(self.players["impulsivo"])
        can_buy = False
        for player in self.players.values():
            can_buy = player.can_buy_estate(self.estate)
        self.assertFalse(can_buy, "No Player can buy a property if it already has an owner")

        self.estate.change_owner(None)
        can_buy = False
        for player in self.players.values():
            can_buy = player.can_buy_estate(self.estate)
        self.assertFalse(can_buy, "No Player can buy a property if he has no money")

    def test_behavior_assingment(self):
        """
        Testa se o comportamento atribuido para o jogador está correto, baseado na regra:
            - 1 Impulsivo
            - 2 Exigente
            - 3 Cauteloso
            - 4 Aleatorio

        :return: None
        """
        self.assertEqual(1, self.players["impulsivo"].behavior[0])
        self.assertEqual(2, self.players["exigente"].behavior[0])
        self.assertEqual(3, self.players["cauteloso"].behavior[0])
        self.assertEqual(4, self.players["aleatorio"].behavior[0])
        self.assertEqual(BEHAVIORS[1][1], self.players["impulsivo"].behavior[1])
        self.assertEqual(BEHAVIORS[2][1], self.players["exigente"].behavior[1])
        self.assertEqual(BEHAVIORS[3][1], self.players["cauteloso"].behavior[1])
        self.assertEqual(BEHAVIORS[4][1], self.players["aleatorio"].behavior[1])

    def test_behavior_implementation(self):
        """
        Testa se a implementação dos comportamentos dos jogadores esta correta baseada nas regras:
            - O jogador IMPULSIVO compra qualquer propriedade sobre a qual ele parar.
            - O jogador EXIGENTE compra qualquer propriedade, desde que o valor do aluguel dela seja maior do que 50.
            - O jogador CAUTELOSO compra qualquer propriedade desde que ele tenha uma reserva de 80 saldo sobrando depois de realizada a compra.
            - O jogador ALEATORIO compra a propriedade que ele parar em cima com probabilidade de 50%

        :return: None
        """

        #  IMPULSIVO
        self.estate.price = self.players["impulsivo"].balance
        self.assertTrue(self.players["impulsivo"].can_buy_estate(self.estate),
                        "If the player has more or exactly the required balance he must be able to buy the estate")

        #  EXIGENTE
        self.estate.price = 201
        self.assertTrue(self.players["exigente"].can_buy_estate(self.estate),
                        "If the rent price is greater than 50, the player must be able to buy the estate")

        self.estate.price = 50
        self.assertFalse(self.players["exigente"].can_buy_estate(self.estate),
                         "If the rent price is less than 50, the player must be not able to buy the estate")

        # CAUTELOSO
        self.estate.price = self.players["cauteloso"].balance - 80
        self.assertTrue(self.players["cauteloso"].can_buy_estate(self.estate),
                        "If the result of (Player BALANCE - Estate SALE PRICE) is equal or greater than 80, the player must be able to buy the estate")

        self.estate.price = self.players["cauteloso"].balance + 81
        self.assertFalse(self.players["cauteloso"].can_buy_estate(self.estate),
                         "If the result of (Player BALANCE - Estate SALE PRICE) is less than 80, the player must be not able to buy the estate")

        #  ALEATORIO
        #  Teste unitário não implementado

    def test_check_if_correct_rent_price_as_payed(self):
        """
        Testa se o pagamento do aluguel foi feito corretamente.
            - O Jogador inquilino devera perder o dinheiro do aluguel
            - o Jogador proprietário devera receber o dinhero do aluguel
        :return: None
        """
        self.players["aleatorio"].buy_estate(self.estate)
        renter_actual_balance = self.estate.owner.balance

        occupant_actual_balance = self.players["impulsivo"].balance
        self.players["impulsivo"].pay_rent(self.estate)
        self.assertEqual(
            occupant_actual_balance - self.estate.rent_price, self.players["impulsivo"].balance,
            "The Player (Occupant) balance after a rent payment must be the result of "
            "(Player BALANCE - Estate RENT PRICE)"
        )
        self.estate.owner.receive_rent_payment(self.estate)
        self.assertEqual(
            renter_actual_balance + self.estate.rent_price, self.estate.owner.balance,
            "The Player (Renter) balance after a receipt of rent payment must be the result of "
            "(Player BALANCE + Estate RENT PRICE)"
        )

    def test_if_player_loss_money_and_own_estate_on_buy(self):
        self.estate.change_owner(None)
        self.estate.price = 250
        player = self.players["impulsivo"]
        initial_balance = player.balance
        if player.can_buy_estate(self.estate):
            player.buy_estate(self.estate)
        self.assertTrue(
            player.balance == initial_balance - self.estate.sale_price,
            "The Player must lose money from the purchase when buying a estate"
        )
        self.assertTrue(
            self.estate in player.estates,
            "The Player must be the owner of the estate after purchasing it"
        )


class TestEstate(TestCase):
    """
    Testes unitários da classe Estate (Propriedade)
    """

    def setUp(self):
        self.estate = Estate(1, 1)

    def test_check_if_estate_has_id(self):
        """
        Checa se a Propriedade possui um ID

        :return: None
        """
        self.assertTrue(self.estate.id_, "The Estate must have an ID")

    def test_check_if_estate_has_price(self):
        """
        Checa se a Propriedade possui um valor, valor de venda e valor de aluguel.
        Os mesmos precisam ser maior que 0.

        :return: None
        """
        self.assertTrue(self.estate.price, "The Estate must have an Price greater than zero")
        self.assertTrue(self.estate.sale_price, "The Estate must have an Sale Price greater than zero")
        self.assertTrue(self.estate.rent_price, "The Estate must have an Rent Price greater than zero")


class TestMatch(TestCase):
    """
    Testes unitários da classe Game (Jogo)
    """

    def setUp(self):
        self.game = Match(1)

    def test_check_number_of_players_in_game(self):
        """
        Testa se o jogo possui exatamente 4 jogadores

        :return: None
        """
        self.assertEqual(4, len(self.game.players), "The Game must have exactly 4 Players")

    def test_check_number_of_estates_in_game(self):
        """
        Testa se o jogo possui exatamente 20 Propriedades

        :return: None
        """
        self.assertEqual(20, len(self.game.estates), "The Game must have exactly 20 Estates")

    def test_check_max_number_of_rounds_in_game(self):
        """
        Testa se o limite máximo de rodadas é igual a 1000

        :return: None
        """
        self.assertEqual(1000, self.game.MAX_ROUNDS, "The Game must have a maximum of 1000 rounds")

    def test_amount_of_benefit(self):
        """
        Testa se o valor no beneficio por dar uma volta no tabuleiro é igual a 100

        :return: None
        """
        self.assertEqual(100, self.game.BENEFIT_AMOUNT, "The benefit amount must be 100")


if __name__ == "__main__":
    unittest.main()
