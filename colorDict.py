import numpy as np

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
grey = (127, 127, 127)

def translateColors(arr, snakes):
    result = np.zeros(arr.shape + (3,), dtype=np.uint8)
    result[arr == 0] = black # floor
    result[arr == 1] = white # wall
    result[arr == 2] = red # apple

    #Will be added if I have enough time
    #result[arr == 3] = grey # bomb
    
    for s in snakes:
        if s.isPlayer:
            for b in s.body:
                result[b.posY][b.posX] = green
        else:
            for b in s.body:
                result[b.posY][b.posX] = blue
    return result