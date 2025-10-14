import numpy as np
import random as rnd
import snake

gameStarted = False
board = []
snakes = []

def placeSnakes(space):
    size = np.shape(space)
    nSnakes = 2
    while (True):
        finished = False
        for i in range(2, size[0]):
            if finished:
                break
            farFromWall = False
            for j in range(0, size[1]):
                if space[i][j] == 0:
                    if not farFromWall:
                        farFromWall = True
                    elif nSnakes > 0 and farFromWall:
                        roll = rnd.randint(0,1000)
                        if(roll > 950):
                            if nSnakes == 2: snakes.append(snake.Snake(i, j, True))
                            else: snakes.append(snake.Snake(i, j, False))
                            nSnakes -= 1
                            break
                    else:
                        finished = True
                        break
        if finished:
            break
    return space

def createSpace(sizeX, sizeY):
    global gameStarted
    global board
    if gameStarted:
        return board
    board = np.ndarray((sizeX, sizeY))
    for i in range(0, sizeX):
        for j in range(0, sizeY):
            if(i == 0 or i == sizeX-1):
                board[i][j] = 1
            else:
                if(j == 0 or j == sizeY-1):
                    board[i][j] = 1
                else:
                    board[i][j] = 0
    board = placeSnakes(board)
    gameStarted = True
    return board
