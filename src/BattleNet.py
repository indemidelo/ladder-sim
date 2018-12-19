import threading as thr
import multiprocessing as mp
import time
import random


class BattleNet(mp.Process):
    def __init__(self, ready_to_play, queueing_players,
                 results_queue, updates):
        """

        :param results: (Queue) of results
        :param new_games: (Queue) of new games requests
        """
        super(BattleNet, self).__init__()
        self.players = dict()
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
        thr.Thread(target=send_to_hs,
                   args=(self.ready_to_play,
                         self.queueing_players)).start()
        thr.Thread(target=get_game_results,
                   args=(self.results_queue,
                         self.updates)).start()
        thr.Thread(target=process_results,
                   args=(self.updates,
                         self.ready_to_play)).start()


def send_to_hs(ready_to_play, queueing_players):
    while 1:
        if not ready_to_play.empty():
            p = ready_to_play.get()
            queueing_players.put(p)
            print(f'{time.time()} - {p} sent to hs')


def get_game_results(results_queue, updates):
    while 1:
        if not results_queue.empty():
            res = results_queue.get()
            print(f'{time.time()} - get {res} from hs')
            updates.put(res)
            print(f'{time.time()} - {res} sent to update')


def process_results(updates, ready_to_play):
    while 1:
        if not updates.empty():
            res = updates.get()
            update_players(res, ready_to_play)
            print(f'{time.time()} - update triggered by'
                  f' {res} completed')


def update_players(result, ready_to_play):
    ready_to_play.put(result['winner'])
    time.sleep(random.random() * 10)
    ready_to_play.put(result['loser'])
