import threading as thr
from src.Game import Game
import time


class RankFloor(thr.Thread):
    def __init__(self, rankid, ladder):
        thr.Thread.__init__(self)
        self.id = rankid
        self.players = list()
        self.ladder = ladder

    def initialize(self):
        pass

    def run(self):
        while 1:
            self.cycle()

    def cycle(self):
        if len(self.players) > 1:
            playerA = self.players.pop(0)
            playerB = self.players.pop(0)
            self.play_a_game(playerA, playerB)
        elif len(self.players) == 1:
            playerA = self.players.pop(0)
            playerB = self.ladder.free_player(self)
            self.play_a_game(playerA, playerB)
        else:
            time.sleep(2)

    def play_a_game(self, playerA, playerB):
        winner, loser = Game(playerA, playerB)
        self.ladder.victory(winner)
        self.ladder.defeat(loser)
