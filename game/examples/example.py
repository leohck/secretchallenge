from game.controller import Controller


#  Instancia a classe Controller
game_controller = Controller()

#  Executa 100 partidas
game_controller.run_matches(100)

#  Executa + 100 partidas
game_controller.run_matches(100)

#  Executa + 100 partidas
game_controller.run_matches(100)

#  Analisa as 300 partidas e retorna a analise em formato de dicionario
analysis = game_controller.analyze_matches()

print(analysis)

# Resultado
"""
{
    'matches': 300,
    'timeout_matches': 4,
    'average_rounds_match': 107,
    'most_winning_behavior': 'impulsivo',
    'behaviors':
     [
        {'behavior': 'impulsivo', 'won_matches': 93, 'win_rate': 31.0},
        {'behavior': 'cauteloso', 'won_matches': 74, 'win_rate': 24.666666666666668},
        {'behavior': 'aleatorio', 'won_matches': 71, 'win_rate': 23.666666666666668},
        {'behavior': 'exigente', 'won_matches': 62, 'win_rate': 20.666666666666668}
    ]
}
"""

