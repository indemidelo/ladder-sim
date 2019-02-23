from src.Game import Game
import multiprocessing as mp
import time


class Hearthstone(mp.Process):
    def __init__(self, queueing_players, pairs_ready):
        super(Hearthstone, self).__init__()
        self.queueing_players = queueing_players
        self.pairs_ready = pairs_ready
        self.lobby = dict()

    def instantiate_lobby(self):
        self.lobby = {j: [] for j in range(26)}

    def run(self):
        self.instantiate_lobby()
        mp.Process(target=self.recv_players).start()

    def ready_to_play(self, p_one, p_two, sv=False):
        msg = f'{time.time()} - {p_one} paired with {p_two}'
        if sv:
            msg += f' during svuotamento'
        self.pairs_ready.put((p_one, p_two))
        self.log.write(f'{msg}\n')
        p_one.wait_time = 0
        p_two.wait_time = 0

    def recv_players(self):
        self.log = open(f'log/{time.time()}_pairings.log', 'a')
        count = 0
        while 1:
            if not self.queueing_players.empty():
                p_one = self.queueing_players.get()
                if self.lobby[p_one.rank]:
                    p_two = self.lobby[p_one.rank].pop(0)
                    self.ready_to_play(p_one, p_two)
                else:
                    self.lobby[p_one.rank].append(p_one)
                    # print(f'{time.time()} - {p_one} is waiting')
            count += 1
            if count == 1000:
                self.clear_lobby()
                count = 0

    def clear_lobby(self):
        lobby_list = [p for rank in list(self.lobby.values()) for p in rank]
        self.instantiate_lobby()
        if lobby_list:
            print('******* SVUOTAMENTO UTILE')
            sorted_lobby_list = sorted(lobby_list,
                                       key=lambda x: (-x.wait_time, x.rank))
            p1s = sorted_lobby_list[0::2]
            p2s = sorted_lobby_list[1::2]
            for p_one, p_two in zip(p1s, p2s):
                self.ready_to_play(p_one, p_two, sv=True)
            if len(p1s) > len(p2s):
                p0 = sorted_lobby_list[-1]
                p0.wait_time += 1
                self.lobby[p0.rank].append(p0)
        else:
            print('+++++++ SVUOTAMENTO INUTILE!!!')


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
