from src.oldPlayer import Player, Rules
from queue import Queue
import json

rules_2k18 = Rules(starting_rank=20,
                   rank_floors=(5, 10, 15, 20))
res = Queue()
giulio = Player('indemidelo#2190', .55, res, rules_2k18)

giulio.initialize()
giulio.start()
res.get()

N = 10000

players_queues = [Queue() for _ in range(N)]
playerbase = list()
for j in range(N):
    p = Player(f'{j}#{j}', .55, players_queues[j], rules_2k18)
    p.initialize()
    playerbase.append(p)


[p.start() for p in playerbase]

results = [q.get() for q in players_queues]
results_dict = {r['battletag']: r for r in results}
with open('results.json', 'w') as jsonfile:
    json.dump(results_dict, jsonfile, indent=4, sort_keys=True)

with open('results.csv', 'w') as csvfile:
    csvfile.write('player;total_games;win_rate\n')
    for r in results:
        csvfile.write(f'{r["battletag"]};'
                      f'{r["win"]+r["loss"]};'
                      f'{round(r["win"]/(r["win"]+r["loss"]), 3)}\n')
