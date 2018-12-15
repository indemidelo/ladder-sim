import threading as thr


class Ladder(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
