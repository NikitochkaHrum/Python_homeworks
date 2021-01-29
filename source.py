import numpy as np


class Data:
    def __init__(self, arr, k, incomp):
        self.n = k
        self.arr = arr
        self.inc = incomp
        self.gone = 0

    def get_next_batch(self, tec=None):
        if self.gone + self.n <= len(self.arr):
            tec = self.arr[self.gone:self.gone + self.n]
        else:
            tec = self.arr[self.gone: len(self.arr)]
        return tec

    def __iter__(self):
        return self

    def __next__(self):
        current = self.get_next_batch()
        self.gone += self.n
        if self.gone > len(self.arr) and self.inc or self.gone > len(self.arr)+self.n and not self.inc:
            raise StopIteration()
        return current
