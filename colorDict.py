import numpy as np

white = (255, 255, 255)
red = (255, 0, 0)

def translateColors(arr):
    result = np.zeros(arr.shape + (3,), dtype=np.uint8)
    result[arr == 0] = white
    result[arr == 1] = red
    return result