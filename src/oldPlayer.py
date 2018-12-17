import threading as thr
import random
import json


class Rules(object):
    def __init__(self, starting_rank, rank_floors,
                 starting_stars=0):
        self.starting_rank = starting_rank
        self.rank_floors = rank_floors
        self.starting_stars = starting_stars


class Player(thr.Thread):
    def __init__(self, battletag, win_rate, results, rules,
                 max_games=None):
        thr.Thread.__init__(self)
        self.battletag = battletag
        self.win_rate = win_rate
        self.rules = rules
        self.max_games = max_games or float('inf')
        self.rank = rules.starting_rank
        self.win_streak = 0
        self.win = 0
        self.loss = 0
        self.stars = rules.starting_stars
        self.playing = False
        self.results = results

    def initialize(self):
        self.playing = True

    def run(self):
        while all((self.playing,
                   self.win + self.loss < self.max_games)):
            self.play_a_game()

    def __repr__(self):
        to_repr = {'battletag': self.battletag,
                   'win': self.win,
                   'loss': self.loss,
                   'stars': self.stars,
                   'rank': self.rank,
                   'winstreak': self.win_streak}
        return json.dumps(to_repr)

    def play_a_game(self):
        if random.random() <= self.win_rate:
            self.victory()
            #print(self)
        else:
            self.defeat()
            #print(self)

    def victory(self):
        self.win += 1
        stars = 2 if self.win_streak >= 3 else 1
        self.stars += stars
        if self.rank > 5:
            self.win_streak += 1
        if self.stars >= 6:
            self.rank_up()

    def defeat(self):
        self.loss += 1
        self.stars -= 1
        self.win_streak = 0
        if self.stars == -1:
            self.rank_down()

    def rank_up(self):
        self.rank -= 1
        if self.rank == 0:
            profile = {'battletag': self.battletag,
                       'win': self.win,
                       'loss': self.loss,
                       'winrate': self.win/(self.win+self.loss)}
            self.results.put(profile)
            self.playing = False
        else:
            self.stars -= 5
            if self.rank <= 5:
                self.win_streak = 0

    def rank_down(self):
        if self.rank in self.rules.rank_floors:
            self.stars = 0
        else:
            self.rank += 1
            self.stars = 4
