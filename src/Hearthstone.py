from src.Game import Game
import multiprocessing as mp
import time


class Hearthstone(mp.Process):
    def __init__(self, queueing_players, pairs_ready):
        super(Hearthstone, self).__init__()
        self.queueing_players = queueing_players
        self.pairs_ready = pairs_ready
        self.lobby = {j: [] for j in range(26)}
        self.tennis_order = {j: breath_wide_order(range(26), j)
                             for j in range(26)}

    def run(self):
        mp.Process(target=self.recv_players).start()

    def recv_players(self):
        self.log = open(f'log/{time.time()}_pairings.log', 'a')
        while 1:
            if not self.queueing_players.empty():
                p_one = self.queueing_players.get()
                opp_rank = self.rank_search(p_one.rank)
                if opp_rank:
                    p_two = self.lobby[opp_rank].pop(0)
                    self.pairs_ready.put((p_one, p_two))
                    msg = f'{time.time()} - {p_one} paired with {p_two}'
                    self.log.write(f'{msg}\n')
                else:
                    self.lobby[p_one.rank].append(p_one)
                    # print(f'{time.time()} - {p_one} is waiting')

    def rank_search(self, rank):
        for j in self.tennis_order[rank]:
            if self.lobby[j]:
                return j
        return None


def breath_wide_order(array, index):
    max_j = max(len(array[:index]), len(array[index:]))
    new_order = [array[index]]
    for j in range(1, max_j + 1):
        if index - j >= 0:
            new_order.append(array[index - j])
        if index + j < len(array):
            new_order.append(array[index + j])
    return new_order


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
                # print(f'{time.time()} - {p1} is playing with {p2}')
