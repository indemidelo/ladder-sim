from src.Game import Game
import multiprocessing as mp
import time


class Hearthstone(mp.Process):
    def __init__(self, queueing_players, pairs_ready):
        super(Hearthstone, self).__init__()
        self.queueing_players = queueing_players
        self.pairs_ready = pairs_ready

    def run(self):
        mp.Process(target=self.recv_players).start()

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


class HearthstoneGames(mp.Process):
    def __init__(self, pairs_ready, results):
        super(HearthstoneGames, self).__init__()
        self.pairs_ready = pairs_ready
        self.results = results

    def run(self):
        mp.Process(target=self.fire_games).start()

    def fire_games(self):
        while 1:
            if not self.pairs_ready.empty():
                p1, p2 = self.pairs_ready.get()
                Game(p1, p2, self.results).start()
                print(f'{time.time()} - {p1} is playing with {p2}')
