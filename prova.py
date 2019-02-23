import multiprocessing as mp
import threading as thr


class prova(mp.Process):
    def __init__(self, q, q2, q3, q4):
        super(prova, self).__init__()
        self.q = q
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def run(self):
        print('running')

    def initialize(self):
        self.to_hs = thr.Thread(target=self.send_to_hs,
                                args=(self.q,))

    def send_to_hs(self, q):
        q.put(1)

    def foo(self):
        pass


if __name__ == '__main__':
    q = mp.Queue()
    q2 = mp.Queue()
    q3 = mp.Queue()
    q4 = mp.Queue()
    p = prova(q, q2, q3, q4)
    p.start()
