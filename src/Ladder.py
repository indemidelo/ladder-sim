import threading as thr


class Ladder(thr.Thread):
    def __init__(self, rules):
        thr.Thread.__init__(self)
        self.rank_floors = list()
        self.rules = rules

    def victory(self, player):
        stars = 2 if player.winstreak >= 3 else 1
        player.stars += stars
        if player.rank > 5:
            player.winstreak += 1
        if player.stars >= 6:
            self.rank_up(player)

    def rank_up(self, player):
        self.rank_floors[player.rank - 1].players.append(player)
        if player.rank == 0:
            player.playing = False
        else:
            player.stars -= 5
            if player.rank <= 5:
                player.winstreak = 0

    def defeat(self, player):
        player.stars -= 1
        player.winstreak = 0
        if player.stars == -1:
            self.rank_down(player)

    def rank_down(self, player):
        if player.rank in self.rules.rank_floors:
            player.stars = 0
        else:
            self.rank_floors[player.rank + 1].players.append(player)
            player.stars = 4

    def free_player(self, rank):
        player = False
        while not player:
            player = self.recursive_player_search(self.rank_floors[rank.rankid:])
        return player

    def recursive_player_search(self, rank_list):
        if len(rank_list) > 1: # con len = 1 arrivo a rank 25
            return None
        if rank_list[0].players:
            return rank_list[0].players.pop(0)
        else:
            return self.recursive_player_search(rank_list[1:])
