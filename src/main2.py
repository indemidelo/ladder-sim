from src.Ladder import Ladder
from src.Rules import Rules
from src.Player import Player
import random

rules = Rules(25, (25, 20, 15, 10, 5))

rank_giulio = 10
giulio = Player('giulio', 0.9, rank_giulio)

ladder = Ladder(rules=rules, giulio=giulio)
ladder.initialize()

for j in range(1000):
    #rank = random.sample(range(1, 5 + 1), 1)[0]
    rank = 10
    p = Player(f'{j}#{j}', random.random(), rank)
    ladder.ranks[rank].players.append(p)

ladder.ranks[rank_giulio].players.append(giulio)

ladder.start()
