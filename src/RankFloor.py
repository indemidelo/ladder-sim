import threading as thr
from src.Game import Game
import time


class RankFloor(thr.Thread):
    def __init__(self, rankid, ladder, queue):
        thr.Thread.__init__(self)
        self.id = rankid
        self.players_queue = queue
        self.players = list()
        self.ladder = ladder
        self.games_played = 0

    def initialize(self):
        pass

    def run(self):
        while 1:
            self.cycle()

    def cycle(self):
        #print(f'dimensione rank floor {self.id}: {len(self.players)}')
        if len(self.players) > 1:
            print(f'dimensione rank floor {self.id}: {len(self.players)}')
            playerA = self.players.pop(0)
            playerB = self.players.pop(0)
            #starttime=time.time()
            Game(playerA, playerB, self.ladder).start()
            #print(time.time()-starttime)
            self.games_played += 1
        elif len(self.players) == 1:
            print(f'dimensione rank floor {self.id}: {len(self.players)}')
            playerA = self.players.pop(0)
            playerB = self.ladder.free_player(self)
            Game(playerA, playerB, self.ladder).start()
            self.games_played += 1
        else:
            #print(f'{time.time()} - {self.id}: sto aspettando giocatori')
            #time.sleep(2)
            pass

