from functools import reduce
from operator import add
from bthelper import genseq
from math import sqrt, inf, floor
from PIL import Image

class Oversampler:
    def __init__(self, srsm, pool):
        self._srsm = srsm
        self._cells = self._gencells(srsm, pool)

    @staticmethod
    def _gencells(srsm, pool):
        cells = []
        sm = srsm**2
        maxidx = len(pool) - 1
        ids = genseq([0 for i in range(sm)], lambda e: e==maxidx, lambda e: e+1, lambda e: e)
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
        im2 = Image.new('RGB', (im.size[0]*self._srsm,im.size[1]*self._srsm))
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                pix = im.getpixel((i,j))
                cell = self._seekclosest(pix)
                cell.place(im2, i, j)
            print('\b\b\b' + str(floor((i+1)/im.size[0]*100)) + '%', end='')
        return im2

class _Cell:
    def __init__(self, colors):
        self._colors = colors
        self._averageColor = list(reduce(
            lambda a,e: map(add, a, map(lambda e_: e_/len(colors), e)), colors, [0,0,0]))

    def _getcol(self, i, j):
        srsm = floor(sqrt(len(self._colors)))
        return self._colors[srsm*i + j]

    def dist(self, col):
        v1 = self._averageColor
        v2 = col
        return sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2)

    def place(self, im, x, y):
        srsm = floor(sqrt(len(self._colors)))
        for i in range(srsm):
            for j in range(srsm):
                im.putpixel((x*srsm+i, y*srsm+j), tuple(self._getcol(i,j)))