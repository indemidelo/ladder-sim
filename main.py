from src.BattleNet import BattleNet
from src.Hearthstone import Hearthstone
import multiprocessing as mp
# from queue import Queue
from src.Player import Player
import time


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
    ready_to_play = mp.Queue()
    queueing_players = mp.Queue()
    results_queue = mp.Queue()
    updates = mp.Queue()

    for j in range(6):
        p = Player(f'{j}#{j}', 0.55)
        ready_to_play.put(p)

    battlenet = BattleNet(ready_to_play, queueing_players,
                          results_queue, updates)
    hs = Hearthstone(queueing_players, results_queue)
    # hs = mp.Process(target=mock_hs, args=(results_queue, ))
    # hs.start()
    battlenet.start()
    hs.start()
