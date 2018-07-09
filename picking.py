from copy import deepcopy
from sys import argv

from ranking import Ranking

class Picked:
  def __init__(self, size, picked):
    self._picked = [False] * size
    for p in picked:
      self._picked[p] = True

  def next(self, pos):
    pos += 1
    while pos < len(self._picked) and self._picked[pos]:
      pos += 1
    if pos >= len(self._picked):
      return None
    return pos


class Selection:
  def __init__(self, size, max, picked):
    self.selection = [-1] * size
    self._max = max
    self._picked = Picked(max, picked)

  def next(self):
    if self.selection[0] == -1:
      self.selection[0] = self._picked.next(-1)
      self._fill(1)
      return True
    return self._next_pos(len(self.selection)-1)

  def _fill(self, pos):
    for i in range(pos, len(self.selection)):
      self.selection[i] = self._picked.next(self.selection[i - 1])
      if self.selection[i] is None:
        return False
    return True

  def _next_pos(self, pos):
    if pos == -1:
      return False
    self.selection[pos] = self._picked.next(self.selection[pos])
    if self.selection[pos] is None or not self._fill(pos + 1):
      return self._next_pos(pos - 1)
    return True


class Picker:
  def __init__(self, ranking, size, players):
    self._ranking = ranking
    self._size = size
    self._players = players
    self._best_diff = 999999
    self._best = None

  def pick(self, teams, picked):
    if teams == 0:
      best = -999999
      worst = 999999
      for team in picked:
        score = 0
        for player in team:
          score += self._ranking.score(self._players[player])
        if score > best:
          best = score
        if score < worst:
          worst = score
      diff = best - worst
      if diff < self._best_diff:
        self._best = deepcopy(picked)
        self._best_diff = diff
      return
    all_picked = [player for team in picked for player in team]
    selection = Selection(self._size, len(self._players), all_picked)
    while selection.next():
      picked.append(selection.selection)
      self.pick(teams - 1, picked)
      picked.pop()

  def print(self):
    for team in self._best:
      for player in team:
        print(self._players[player], end=' ')
      print()


def main():
  ranking = Ranking()
  ranking.open(argv[1])
  teams = int(argv[2])
  players = []
  for i in range(3, len(argv)):
    players.append(argv[i])
  if len(players) % teams > 0:
    print('Jogadores sobrando: ', len(players) % teams)
    return
  picker = Picker(ranking, len(players) // teams, players)
  picker.pick(teams, [])
  picker.print()

if __name__ == '__main__':
  main()
