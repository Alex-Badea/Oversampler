from oversampler import Oversampler as Ovs
from PIL import Image as Im

available_colors = [[202, 227, 255], # first color is unset pixel in ocean
    [255, 255, 255], # second color is unset pixel on land
    [255, 255, 255], # white
    [228, 228, 228], # light gray
    [136, 136, 136], # dark gray
    [78, 78, 78],    # darker gray
    [0, 0, 0],       # black
    [244, 179, 174], # light pink
    [255, 167, 209], # pink
    [255, 101, 101], # peach
    [229, 0, 0],     # red
    [254, 164, 96],  # light brown
    [229, 149, 0],   # orange
    [160, 106, 66],  # brown
    [245, 223, 176], # sand
    [229, 217, 0],   # yellow
    [148, 224, 68],  # light green
    [2, 190, 1],     # green
    [0, 101, 19],    # dark green
    [202, 227, 255], # sky blue
    [0, 211, 221],   # light blue
    [0, 131, 199],   # dark blue
    [0, 0, 234],     # blue
    [25, 25, 115],   # darker blue
    [207, 110, 228], # light violette
    [130, 0, 128]]   # violette

o = Ovs(1, available_colors)
im = Im.open('1.jpg')
im2 = o.sample(im)
im2.show()