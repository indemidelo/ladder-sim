import multiprocessing as mp
import time


class BattleNet(mp.Process):
    def __init__(self, ready_to_play, queueing_players):
        """

        :param results: (Queue) of results
        :param new_games: (Queue) of new games requests
        """
        super(BattleNet, self).__init__()
        self.players = dict()
        self.ready_to_play = ready_to_play
        self.queueing_players = queueing_players

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

    def send_to_hs(self):
        while 1:
            if not self.ready_to_play.empty():
                p = self.ready_to_play.get()
                self.queueing_players.put(p, block=True)
                # print(f'{time.time()} - {p} sent to hs')


class BattleNetResults(mp.Process):
    def __init__(self, results_queue, updates):
        super(BattleNetResults, self).__init__()
        self.results_queue = results_queue
        self.updates = updates

    def run(self):
        mp.Process(target=self.get_game_results).start()

    def get_game_results(self):
        while 1:
            if not self.results_queue.empty():
                res = self.results_queue.get()
                # print(f'{time.time()} - get {res} from hs')
                self.updates.put(res)
                # print(f'{time.time()} - {res} sent to update')


class BattleNetUpdates(mp.Process):
    def __init__(self, rules, ready_to_play, updates):
        super(BattleNetUpdates, self).__init__()
        self.rules = rules
        self.ready_to_play = ready_to_play
        self.updates = updates
        self.ranks_distribution = {j: 0 for j in range(26)}

    def run(self):
        mp.Process(target=self.process_results).start()

    def process_results(self):
        self.log = open(f'log/{time.time()}_playerbase.log', 'a')
        self.climbing = open(f'log/{time.time()}_climbing.log', 'a')
        while 1:
            if not self.updates.empty():
                res = self.updates.get()
                winner = res['winner']
                loser = res['loser']
                self.update_players(winner, loser)
                # print(f'{time.time()} - update triggered by'
                # f' {res} completed')

    def update_players(self, winner, loser):
        self.victory(winner)
        self.defeat(loser)
        self.log.write(f'{self.ranks_distribution}\n')
        if winner.rank > 0:
            self.ready_to_play.put(winner)
        # time.sleep(random.random() * 10)
        self.ready_to_play.put(loser)

    def update_rank_distribution(self, player, winner=True):
        if winner:
            self.ranks_distribution[player.rank + 1] = max(0, self.ranks_distribution[player.rank + 1] - 1)
        else:
            self.ranks_distribution[player.rank - 1] = max(0, self.ranks_distribution[player.rank - 1] - 1)
        self.ranks_distribution[player.rank] += 1

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
        self.update_rank_distribution(player, winner=True)
        if player.rank == 0:
            player.playing = False
            msg = f'{time.time()} - Player {player} ' \
                f'just reached legend!'
            print(msg)
            self.climbing.write(f'{msg}\n')
        else:
            player.stars -= 5
            msg = f'{player} just reached rank {player.rank}'
            print(msg)
            self.climbing.write(f'{msg}\n')
            if player.rank <= 5:
                player.winstreak = 0

    def rank_down(self, player):
        if player.rank in self.rules.rank_floors:
            player.stars = 0
        else:
            player.rank += 1
            player.stars = 4
            self.update_rank_distribution(player, winner=False)
