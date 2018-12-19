import threading as thr
import multiprocessing as mp
import time
import random


class BattleNet(mp.Process):
    def __init__(self, rules, ready_to_play, queueing_players,
                 results_queue, updates):
        """

        :param results: (Queue) of results
        :param new_games: (Queue) of new games requests
        """
        super(BattleNet, self).__init__()
        self.players = dict()
        self.rules = rules
        self.ready_to_play = ready_to_play
        self.queueing_players = queueing_players
        self.results_queue = results_queue
        self.updates = updates

    def new_player(self, player):
        """
        Register a new player
        :param player: (Player)
        :return:
        """
        if player.battletag in self.players:
            print(f'{time.time()} - Player {player.battletag}'
                  f' already exists')
        else:
            self.players.update({player.battletag: player})
            print(f'{time.time()} - Player {player.battletag}'
                  f' added')

    def player_login(self, player):
        """
        Player log in
        :param player: (Player)
        :return:
        """
        player.logged_in = True
        print(f'{time.time()} - Player {player.battletag}'
              f' logged in')

    def player_logout(self, player):
        """
        Player log out
        :param player: (Player)
        :return:
        """
        player.logged_in = False
        print(f'{time.time()} - Player {player.battletag}'
              f' logged out')

    def run(self):
        mp.Process(target=self.send_to_hs).start()
        mp.Process(target=self.get_game_results).start()
        mp.Process(target=self.process_results).start()

    def send_to_hs(self):
        while 1:
            if not self.ready_to_play.empty():
                p = self.ready_to_play.get()
                self.queueing_players.put(p)
                print(f'{time.time()} - {p} sent to hs')

    def get_game_results(self):
        while 1:
            if not self.results_queue.empty():
                res = self.results_queue.get()
                print(f'{time.time()} - get {res} from hs')
                self.updates.put(res)
                print(f'{time.time()} - {res} sent to update')

    def process_results(self):
        while 1:
            if not self.updates.empty():
                res = self.updates.get()
                self.update_players(res)
                print(f'{time.time()} - update triggered by'
                      f' {res} completed')

    def update_players(self, result):
        self.victory(result['winner'])
        self.defeat(result['loser'])
        self.ready_to_play.put(result['winner'])
        time.sleep(random.random() * 10)
        self.ready_to_play.put(result['loser'])

    def victory(self, player):
        stars = 2 if player.winstreak >= 3 else 1
        player.stars += stars
        if player.rank > 5:
            player.winstreak += 1
        if player.stars >= 6:
            self.rank_up(player)

    def defeat(self, player):
        player.stars -= 1
        player.winstreak = 0
        if player.stars == -1:
            self.rank_down(player)

    def rank_up(self, player):
        player.rank -= 1
        if player.rank == 0:
            player.playing = False
            print(f'{time.time()} - Player {player.battletag} '
                  f'just reached legend!')
        else:
            player.stars -= 5
            print(f'{player.battletag} just reach '
                  f'rank {player.rank}')
            if player.rank <= 5:
                player.winstreak = 0

    def rank_down(self, player):
        if player.rank in self.rules.rank_floors:
            player.stars = 0
        else:
            player.rank += 1
            player.stars = 4
