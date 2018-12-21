import multiprocessing as mp
import time
from src.BattleNet import BattleNet
from src.BattleNet import BattleNetResults
from src.BattleNet import BattleNetUpdates
from src.Hearthstone import Hearthstone
from src.Hearthstone import HearthstoneGames
from src.Rules import Rules
from src.Player import Player


def mock_hs(results_queue):
    while 1:
        winner = Player('winner#0', 0.55)
        loser = Player('loser#99', 0.55)
        res = {'winner': winner, 'loser': loser}
        results_queue.put(res)
        time.sleep(1)


class BattleNetMock(mp.Process):
    def __init__(self, q1, q2, q3, q4):
        super(BattleNetMock, self).__init__()
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def initialize(self):
        pass

    def run(self):
        print('pluto')


if __name__ == '__main__':
    starting_rank = 20
    rank_floors = 20, 15, 10, 5
    rules = Rules(starting_rank, rank_floors)
    ready_to_play = mp.Queue()
    queueing_players = mp.Queue()
    results_queue = mp.Queue()
    pairs_ready = mp.Queue()
    updates = mp.Queue()

    for j in range(2):
        p = Player(f'{j}#{j}', 0.55)
        ready_to_play.put(p)

    battlenet = BattleNet(ready_to_play, queueing_players)
    battlenet_results = BattleNetResults(results_queue, updates)
    battlenet_updates = BattleNetUpdates(rules, ready_to_play, updates)
    hs = Hearthstone(queueing_players, pairs_ready)
    hs_games = HearthstoneGames(pairs_ready, results_queue)
    battlenet.start()
    battlenet_results.start()
    battlenet_updates.start()
    hs.start()
    hs_games.start()
