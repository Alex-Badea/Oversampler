from functools import reduce
from operator import add
from bthelper import genseq
from math import sqrt, floor
from PIL import Image as Im
from scipy.spatial import KDTree as Kdt
from time import time
import multiprocessing as mp
import numpy as np
from numpy import array as _

class Oversampler:
    def __init__(self, ss, colpool):
        self._ss = ss
        self._cells = self._gencells(colpool)
        self._cellskdt = Kdt(list(map(lambda e: e.avgcol, self._cells)))

    def _gencells(self, pool):
        cells = []
        s = self._ss ** 2
        maxi = len(pool) - 1
        ids = genseq([0 for _ in range(s)], lambda e: e==maxi, lambda e: e+1, lambda e: e)
        for i in ids:
            cells.append(_Cell([pool[j] for j in i]))
        return cells

    def _seekclosest(self, col):
        q = self._cellskdt.query(col)
        return self._cells[q[1]]

    def sample(self, im):
        t = time()
        im2 = Im.new('RGB', (im.size[0] * self._ss, im.size[1] * self._ss))
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                pix = im.getpixel((i,j))
                cell = self._seekclosest(pix)
                cell.place(im2, i, j)
            print('\b\b\b' + str(floor((i+1)/im.size[0]*100)) + '%', end='')
        print('sampling took {0:.2f} seconds'.format(time()-t))
        return im2

    def _seekclosestmat(self, col):
        return _(list(self._seekclosest(col))).reshape((self._ss,self._ss,3))

    def samplemp(self, im):
        t = time()
        imdata = im.getdata()
        n = self._ss

        pool = mp.Pool(processes=min(4, mp.cpu_count()))

        imdata = _(list(pool.map(self._seekclosestmat, imdata)))
        imdata = imdata.reshape((im.size[1], im.size[0], n, n, 3))
        imdata = imdata.transpose((0, 2, 1, 3, 4))
        imdata = imdata.reshape((-1, 3))

        im2 = Im.new('RGB', (im.size[0]*n, im.size[1]*n))
        im2.putdata([tuple(e) for e in imdata])
        print('sampling mp took {0:.2f} seconds'.format(time() - t))
        return im2

class _Cell:
    def __init__(self, cols):
        self._cols = cols
        self._avgcol = list(reduce(
            lambda a,e: map(add, a, map(lambda e_: e_/len(cols), e)), cols, [0,0,0]))

    def __iter__(self):
        for e in self._cols:
            yield e

    @property
    def avgcol(self):
        return self._avgcol

    def _getcol(self, i, j):
        ss = floor(sqrt(len(self._cols)))
        return self._cols[ss*i + j]

    def dist(self, col):
        v1 = self._avgcol
        v2 = col
        return sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2)

    def place(self, im, x, y):
        ss = floor(sqrt(len(self._cols)))
        for i in range(ss):
            for j in range(ss):
                im.putpixel((x*ss+i, y*ss+j), tuple(self._getcol(i,j)))