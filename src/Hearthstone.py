from src.Game import Game
import multiprocessing as mp
import threading as thr
import time


class Hearthstone(mp.Process):
    def __init__(self, queueing_players, results):
        super(Hearthstone, self).__init__()
        self.queueing_players = queueing_players
        self.results = results
        self.pairs_ready = mp.Queue()

    def run(self):  # todo divide the class in processes
        mp.Process(target=self.recv_players).start()
        mp.Process(target=self.fire_games).start()

    def recv_players(self):
        p1, p2 = None, None
        while 1:
            if not p1 and not self.queueing_players.empty():
                p1 = self.queueing_players.get()
            if p1 and not self.queueing_players.empty():
                p2 = self.queueing_players.get()
            if p1 and p2:
                self.pairs_ready.put((p1, p2))
                print(f'{time.time()} - {p1} paired with {p2}')
                p1, p2 = None, None

    def fire_games(self):
        while 1:
            if not self.pairs_ready.empty():
                p1, p2 = self.pairs_ready.get()
                Game(p1, p2, self.results).start()
                print(f'{time.time()} - {p1} is playing with {p2}')


def recv_playersOLD(queueing_players, pairs_ready):
    while 1:
        try:
            p1 = queueing_players.get(timeout=1)
            print(f'{time.time()} - p1:{p1} in queue')
        except:
            continue
        try:
            p2 = queueing_players.get(timeout=1)
            print(f'{time.time()} - p2:{p2} in queue')
        except:
            queueing_players.put(p1)
            print(f'{time.time()} - p2 unavailable')
            continue
        pairs_ready.put((p1, p2))
        print(f'{time.time()} - {p1} paired with {p2}')