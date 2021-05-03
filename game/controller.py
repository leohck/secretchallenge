from collections import Counter
from game.match import Match


class Controller:
    """
    Controlador do Jogo
    """

    def __init__(self):
        self.data = {
            "matches": 0,
            "rounds": [],
            "winners": []
        }

    def analyze_matches(self):
        """
        Faz a analise dos dados das partidas e retorna um dicionario contendo a analise.
        para utilizar este metodo é necessario que execute as partidas antes (self.run_matches)
        :return: Dict
        """
        assert self.data["rounds"], "You need to run the matches before analyzing the data"

        matches = self.data['matches']
        rounds_counter = Counter(self.data['rounds'])
        winners_counter = Counter(self.data['winners'])

        timeout_matches = rounds_counter[1000]
        average_rounds_match = round(sum(self.data["rounds"]) / len(self.data["rounds"]))
        most_winning_behavior = max(winners_counter, key=winners_counter.get)

        winners = dict(sorted(winners_counter.items(), key=lambda kv: kv[1], reverse=True))
        behaviors = []
        for behavior, won_matches in winners.items():
            win_rate = round((won_matches * 100) / matches, 2)
            behaviors.append(
                {
                    'behavior': behavior,
                    'won_matches': won_matches,
                    'win_rate': win_rate
                }
            )

        analyzed_data = {
            'matches': matches,
            'timeout_matches': timeout_matches,
            'average_rounds_match': average_rounds_match,
            'most_winning_behavior': most_winning_behavior,
            'behaviors': behaviors
        }
        return analyzed_data

    def run_matches(self, matches=300, analyze=False):
        """
        Executa n partidas e se necessario retorna a analise desse conjunto de partidas.
        :param matches: Numero de partidas
        :param analyze: Flag para saber se é necessario retornar a analise ou não
        :return: Dict or None
        """
        self.data["matches"] += matches
        for i in range(matches):
            analysis = Match(i).run()
            self.data['rounds'].append(analysis['rounds'])
            self.data['winners'].append(analysis['winner'])
        if analyze:
            return self.analyze_matches()
