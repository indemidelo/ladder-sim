import threading as thr
from numpy.random import choice


class Game(thr.Thread):
    def __init__(self, playerA, playerB):
        thr.Thread.__init__(self)
        self.players = playerA, playerB
        self.playerA = playerA
        self.playerB = playerB

    def run(self):
        return self.play()

    def play(self):
        """
        play a game and rank/derank the players
        :return: winner, loser
        """
        total_p = sum([j.winrate for j in self.players])
        p = self.players[0].winrate / total_p
        winner, loser = choice(self.players, 2, p=(p, 1 - p), replace=False)
        winner.victory()
        loser.defeat()
        return winner, loser
