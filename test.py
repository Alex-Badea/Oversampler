from numpy import array as _
import numpy as np
import math
from PIL import Image as Im

# 3r 2c
I = [[255, 0, 0],
     [0, 255, 0],
     [0, 0, 255],
     [0, 255, 255],
     [255, 0, 255],
     [255, 255, 0]]
n = 5

im = Im.new('RGB', (3,2))
im.putdata([tuple(e) for e in I])
im.show()

I = im.getdata()

I = _([_((n**2)*e).reshape((n,n,3)) for e in I])

#adapt 1
I=I.reshape((im.size[1],im.size[0],n,n,3))

#adapt 2
I=I.transpose((0,2,1,3,4))

#adapt 3
I=I.reshape((-1,3))

im = Im.new('RGB', (im.size[0]*n,im.size[1]*n))
im.putdata([tuple(e) for e in I])
im.show()