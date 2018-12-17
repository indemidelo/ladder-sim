class Player(object):
    def __init__(self, battletag, winrate, rank=25, stars=0):
        self.battletag = battletag
        self.winrate = winrate
        self.rank = rank
        self.stars = stars
        self.winstreak = 0
        self.result = None
        self.busy = False

    def __repr__(self):
        return self.battletag

