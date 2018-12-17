import threading as thr
from numpy.random import choice
import time
import random


class Game(thr.Thread):
    def __init__(self, playerA, playerB, ladder, queue):
        thr.Thread.__init__(self)
        self.players = playerA, playerB
        self.ladder = ladder
        self.queue = queue

    def run(self):
        self.play()

    def play(self):
        """
        play a game and rank/derank the players
        :return: winner, loser
        """
        total_p = sum([j.winrate for j in self.players])
        p = self.players[0].winrate / total_p
        player_one = self.players[0]
        player_two = self.players[1]
        print(f'{time.time()} - {player_one} ({player_one.rank}) '
              f'VS {player_two} ({player_two.rank})')
        winner, loser = choice(self.players, 2, p=(p, 1 - p),
                               replace=False)
        self.ladder.victory(winner, self.queue)
        self.ladder.defeat(loser, self.queue)
        #print('winner', winner, winner.stars, winner.winrate)
        #print('loser', loser, loser.stars, loser.winrate)
        time.sleep(random.random())