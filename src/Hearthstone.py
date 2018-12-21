from src.Game import Game
import multiprocessing as mp
import time


class Hearthstone(mp.Process):
    def __init__(self, queueing_players, pairs_ready):
        super(Hearthstone, self).__init__()
        self.queueing_players = queueing_players
        self.pairs_ready = pairs_ready
        self.lobby = {j: [] for j in range(26)}

    def run(self):
        mp.Process(target=self.recv_players).start()

    def recv_players(self):
        while 1:
            if not self.queueing_players.empty():
                p_one = self.queueing_players.get()
                if self.lobby[p_one.rank]:
                    p_two = self.lobby[p_one.rank].pop(0)
                    self.pairs_ready.put((p_one, p_two))
                    # print(f'{time.time()} - {p_one} paired with {p_two}')
                else:
                    self.lobby[p_one.rank].append(p_one)
                    # print(f'{time.time()} - {p_one} is waiting')

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
                #print(f'{time.time()} - {p1} is playing with {p2}')
