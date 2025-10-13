import numpy as np
import random as rnd

gameStarted = False

def placeSnakes(space):
    size = np.shape(space)
    nSnakes = 2
    while (True):
        finished = False
        for i in range(0, size[0]):
            if finished:
                break
            for j in range(0, size[1]):
                if space[i][j] == 0:
                    if nSnakes > 0:
                        roll = rnd.randint(0,10)
                        if(roll > 8):
                            space[i][j] = 2
                            nSnakes -= 1
                    else:
                        finished = True
                        break
        if finished:
            break
    return space

def createSpace(sizeX, sizeY):
    global gameStarted
    space = np.ndarray((sizeX, sizeY))
    for i in range(0, sizeX):
        for j in range(0, sizeY):
            if(i == 0 or i == sizeX-1):
                space[i][j] = 1
            else:
                if(j == 0 or j == sizeY-1):
                    space[i][j] = 1
                else:
                    space[i][j] = 0
    if not gameStarted:
        space = placeSnakes(space)
        gameStarted = True
    return space
