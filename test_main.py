import unittest
from unittest import TestCase
from main import Player, Estate


class TestPlayer(TestCase):
    def setUp(self):
        self.players = {
            "impulsivo": Player(1, 1),
            "exigente":  Player(2, 2),
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
        self.assertEqual('Impulsivo', self.players["impulsivo"].behavior[1])
        self.assertEqual('Exigente', self.players["exigente"].behavior[1])
        self.assertEqual('Cauteloso', self.players["cauteloso"].behavior[1])
        self.assertEqual('Aleatorio', self.players["aleatorio"].behavior[1])

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
        self.estate.sale_price = self.players["impulsivo"].balance
        self.assertTrue(self.players["impulsivo"].can_buy_estate(self.estate),
                        "If the player has more or exactly the required balance he must be able to buy the estate")

        #  EXIGENTE
        self.estate.rent_price = 51
        self.assertTrue(self.players["exigente"].can_buy_estate(self.estate),
                        "If the rent price is greater than 50, the player must be able to buy the estate")

        self.estate.rent_price = 50
        self.assertFalse(self.players["exigente"].can_buy_estate(self.estate),
                         "If the rent price is less than 50, the player must be not able to buy the estate")

        # CAUTELOSO
        self.estate.sale_price = self.players["cauteloso"].balance - 80
        self.assertTrue(self.players["cauteloso"].can_buy_estate(self.estate),
                        "If the result of (Player BALANCE - Estate SALE PRICE) is equal or greater than 80, the player must be able to buy the estate")

        self.estate.sale_price = self.players["cauteloso"].balance + 81
        self.assertFalse(self.players["cauteloso"].can_buy_estate(self.estate),
                         "If the result of (Player BALANCE - Estate SALE PRICE) is less than 80, the player must be not able to buy the estate")

        #  ALEATORIO
        #  Teste unitário não implementado
        #  TODO: Implementar teste unitário do Player (comportamento aleatorio)


if __name__ == "__main__":
    unittest.main()
