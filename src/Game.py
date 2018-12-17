import threading as thr
from numpy.random import choice
import time
import random


class Game(thr.Thread):
    def __init__(self, playerA, playerB, ladder):
        thr.Thread.__init__(self)
        self.players = playerA, playerB
        self.ladder = ladder

    def run(self):
        self.play()

    def play(self):
        """
        play a game and rank/derank the players
        :return: winner, loser
        """
        print(f'{time.time()} - sto giocando')
        total_p = sum([j.winrate for j in self.players])
        p = self.players[0].winrate / total_p
        winner, loser = choice(self.players, 2, p=(p, 1 - p),
                               replace=False)
        self.ladder.victory(winner)
        self.ladder.defeat(loser)
        #print('winner', winner, winner.stars, winner.winrate)
        #print('loser', loser, loser.stars, loser.winrate)
        time.sleep(random.random())
