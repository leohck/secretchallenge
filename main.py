"""
Created by: Leonardo Black
02/05/2021

Arquivo responsavel por iniciar as partidas e analisa-las

Saida:
    - Quantas partidas terminam por time out (1000 rodadas);
    - Quantos turnos em média demora uma partida;
    - Qual a porcentagem de vitórias por comportamento dos jogadores;
    - Qual o comportamento que mais vence
"""

from game.controller import Controller


if __name__ == '__main__':
    """
    Executa as 300 partidas e imprime no console os dados referentes às execuções.
    """
    gc = Controller()
    gc.run_matches(300)
    analysis = gc.analyze_data()
    print(f'Numero de partidas rodadas: {analysis["matches"]}')

    print(
        'Quantas partidas terminam por time out(1000 rodadas)? \n'
        f'{analysis["timeout_matches"]}'
    )

    print(
        'Quantos turnos em média demora uma partida? \n'
        f'{analysis["average_rounds_match"]}'
    )

    print('Qual a porcentagem de vitórias por comportamento dos jogadores? ')
    for behavior in analysis["behaviors"]:
        print(f'{behavior["behavior"]}: {behavior["win_rate"]:.2f}%')

    print(
        'Qual é o comportamento que mais vence? \n'
        f'{analysis["most_winning_behavior"]}'
    )
