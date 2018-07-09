from trueskill import Rating
from trueskill import rate
from sys import argv


class Ranking:
  def __init__(self):
    self._players = {}

  def open(self, path):
    with open(path) as f:
      for line in f:
        winners_text, losers_text = line.strip().split(' ')
        winners = winners_text.split(',')
        losers = losers_text.split(',')
        self._match(winners, losers)

  def _add_player(self, player):
    if not player in self._players:
      self._players[player] = Rating()

  def _match(self, winner_names, loser_names):
    winners = ()
    for winner_name in winner_names:
      if winner_name == "":
        print(winner_names)
      self._add_player(winner_name)
      winners += (self._players[winner_name],)
    losers = ()
    for loser_name in loser_names:
      if loser_name == "":
        print(loser_names)
      self._add_player(loser_name)
      losers += (self._players[loser_name],)
    (winners, losers) = rate((winners, losers), (0, 1))
    for i in range(len(winner_names)):
      self._players[winner_names[i]] = winners[i]
    for i in range(len(loser_names)):
      self._players[loser_names[i]] = losers[i]

  def score(self, name):
    if not name in self._players:
      return 0
    player = self._players[name]
    return player.mu - 3 * player.sigma

  def print_ranking(self):
    ranking = sorted(
        self._players.keys(),
        key=lambda name: self.score(name), reverse=True)
    for i in range(len(ranking)):
      print(i + 1, ranking[i], self.score(ranking[i]))


def main():
  ranking = Ranking()
  ranking.open(argv[1])
  ranking.print_ranking()

if __name__ == '__main__':
  main()
