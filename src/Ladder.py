import time
from src.RankFloor import RankFloor


class Ladder(object):
    def __init__(self, rules, giulio):
        self.ranks = list()
        self.rules = rules
        self.giulio = giulio

    def initialize(self):
        self.ranks = [RankFloor(k, self) for k in range(25+1)]

    def start(self):
        [rank.start() for rank in self.ranks]

    def victory(self, player):
        stars = 2 if player.winstreak >= 3 else 1
        player.stars += stars
        if player.battletag == 'giulio':
            print(f'{player} just won a game!', player.stars)
        if player.rank > 5:
            player.winstreak += 1
        if player.stars >= 6:
            self.rank_up(player)
        else:
            self.ranks[player.rank].players.append(player)

    def rank_up(self, player):
        player.rank -= 1
        self.ranks[player.rank].players.append(player)
        if player.rank == 0:
            player.playing = False
            print(f'{time.time()} - Player {player.battletag} just reached legend!')
            for k in self.ranks:
                print(f'In rank {k.id} there are {len(k.players)} players')
            print(f'Giulio achieved rank {self.giulio.rank}')
        else:
            player.stars -= 5
            print('conto stelle', player.stars)
            print(f'{player.battletag} just reach rank {player.rank}')
            if player.rank <= 5:
                player.winstreak = 0

    def defeat(self, player):
        player.stars -= 1
        player.winstreak = 0
        if player.battletag == 'giulio':
            print(f'{player} just lost a game!', player.stars)
        if player.stars == -1:
            self.rank_down(player)
        else:
            self.ranks[player.rank].players.append(player)

    def rank_down(self, player):
        if player.rank in self.rules.rank_floors:
            player.stars = 0
        else:
            player.rank += 1
            self.ranks[player.rank].players.append(player)
            player.stars = 4
            #print(f'{player.battletag} dropped to rank {player.rank}')

    def free_player(self, rank):
        player = False
        while not player:
            #print('ranks', self.ranks)
            #print('rankid', rank.id)
            player = self.recursive_player_search(self.ranks[rank.id: ])
        return player

    def recursive_player_search(self, rank_list):
        if rank_list:  # con len = 1 arrivo a rank 25
            return None
        if rank_list[0].players:
            print(f'{time.time()} - Free player found in rank {rank_list[0].id}')
            return rank_list[0].players.pop(0)
        else:
            print(f'{time.time()} - Free player not found in rank {rank_list[0].id}')
            return self.recursive_player_search(rank_list[1:])
