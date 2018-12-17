from src.Ladder import Ladder
from src.Rules import Rules
from src.Player import Player
import random

starting_rank = 20
rank_floors = 20, 15, 10, 5
rules = Rules(starting_rank, rank_floors)
ladder = Ladder(rules)
ladder.initialize()

n_players = 1000
for j in range(n_players):
    rank = random.sample(range(1, starting_rank), 1)[0]
    random_winrate = random.random()
    p = Player(f'{j}#{j}', random_winrate, rank, stars=3)
    ladder.ranks[rank].players.append(p)

# ladder.ranks[rank_giulio].players.append(giulio)

ladder.start()
