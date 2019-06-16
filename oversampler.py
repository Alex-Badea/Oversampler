from functools import reduce
from operator import add
from bthelper import genseq
from math import sqrt, inf, floor
from PIL import Image as Im

class Oversampler:
    def __init__(self, ss, pool):
        self._ss = ss
        self._cells = self._gencells(pool)

    def _gencells(self, pool):
        cells = []
        s = self._ss ** 2
        maxi = len(pool) - 1
        ids = genseq([0 for _ in range(s)], lambda e: e==maxi, lambda e: e+1, lambda e: e)
        for i in ids:
            cells.append(_Cell([pool[j] for j in i]))
        return cells

    def _seekclosest(self, col):
        closest = None
        dist = inf
        for i in range(len(self._cells)):
            if self._cells[i].dist(col) < dist:
                closest = self._cells[i]
                dist = self._cells[i].dist(col)
        return closest

    def sample(self, im):
        im2 = Im.new('RGB', (im.size[0] * self._ss, im.size[1] * self._ss))
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                pix = im.getpixel((i,j))
                cell = self._seekclosest(pix)
                cell.place(im2, i, j)
            print('\b\b\b' + str(floor((i+1)/im.size[0]*100)) + '%', end='')
        return im2

class _Cell:
    def __init__(self, cols):
        self._cols = cols
        self._avgcol = list(reduce(
            lambda a,e: map(add, a, map(lambda e_: e_/len(cols), e)), cols, [0, 0, 0]))

    @property
    def avgcol(self):
        return self._avgcol

    def _getcol(self, i, j):
        ss = floor(sqrt(len(self._cols)))
        return self._cols[ss * i + j]

    def dist(self, col):
        v1 = self._avgcol
        v2 = col
        return sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2)

    def place(self, im, x, y):
        ss = floor(sqrt(len(self._cols)))
        for i in range(ss):
            for j in range(ss):
                im.putpixel((x*ss+i, y*ss+j), tuple(self._getcol(i,j)))