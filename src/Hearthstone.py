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

    def run(self):
        thr.Thread(target=recv_players,
                   args=(self.queueing_players, self.pairs_ready)).start()
        thr.Thread(target=fire_games,
                   args=(self.pairs_ready, self.results)).start()


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


def recv_players(queueing_players, pairs_ready):
    while 1:
        p1 = queueing_players.get()
        p2 = queueing_players.get()
        pairs_ready.put((p1, p2))
        print(f'{time.time()} - {p1} paired with {p2}')


def fire_games(pairs_ready, results):
    while 1:
        if not pairs_ready.empty():
            p1, p2 = pairs_ready.get()
            Game(p1, p2, results).start()
            print(f'{time.time()} - {p1} is playing with {p2}')
