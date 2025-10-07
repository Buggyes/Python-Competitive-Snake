import numpy as np

def createSpace(sizeX, sizeY):
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
    return space

