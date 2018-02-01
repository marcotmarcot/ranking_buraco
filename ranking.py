from trueskill import Rating
from trueskill import rate
from sys import argv

def score(player):
  return player.mu # - 3 * player.sigma


class Ranking:
  def __init__(self):
    self._players = {}

  def _add_player(self, player):
    if not self._players.has_key(player):
      self._players[player] = Rating()

  def match(self, winner_names, loser_names):
    winners = ()
    for winner_name in winner_names:
      self._add_player(winner_name)
      winners += (self._players[winner_name],)
    losers = ()
    for loser_name in loser_names:
      self._add_player(loser_name)
      losers += (self._players[loser_name],)
    (winners, losers) = rate((winners, losers), (0, 1))
    for i in range(len(winner_names)):
      self._players[winner_names[i]] = winners[i]
    for i in range(len(loser_names)):
      self._players[loser_names[i]] = losers[i]

  def print_ranking(self):
    ranking = sorted(
        self._players.keys(),
        key=lambda player: score(self._players[player]), reverse=True)
    for i in range(len(ranking)):
      print i + 1, ranking[i], score(self._players[ranking[i]])


def main():
  ranking = Ranking()
  with open(argv[1]) as f:
    for line in f:
      winners_text, losers_text = line.strip().split(' ')
      winners = winners_text.split(',')
      losers = losers_text.split(',')
      ranking.match(winners, losers)
  ranking.print_ranking()

if __name__ == '__main__':
  main()
