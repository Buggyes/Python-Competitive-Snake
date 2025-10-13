import numpy as np

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
grey = (127, 127, 127)

def translateColors(arr):
    result = np.zeros(arr.shape + (3,), dtype=np.uint8)
    result[arr == 0] = black
    result[arr == 1] = white
    result[arr == 2] = green
    result[arr == 3] = blue
    result[arr == 4] = red
    result[arr == 5] = grey
    return result