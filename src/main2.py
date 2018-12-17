from src.Ladder import Ladder
from src.Rules import Rules
from src.Player import Player
import random

rules = Rules(0, (25, 20, 15, 10, 5))

rank_giulio = 10
giulio = Player('giulio', 0.9, rank_giulio)

ladder = Ladder(rules=rules, giulio=giulio)
ladder.initialize()

for j in range(2):
    #rank = random.sample(range(1, 25), 1)[0]
    rank = 0
    p = Player(f'{j}#{j}', random.random(), rank, stars=3)
    ladder.ranks[rank].players.append(p)

#ladder.ranks[rank_giulio].players.append(giulio)

ladder.start()
