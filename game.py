import numpy as np
import random as rnd
import snake

gameStarted = False
gameFinished = False
board = []
snakes = []
appleTimer = 1
ongoingTimer = appleTimer
playerScore = 0
aiScore = 0
winningScore = 30

def placeSnakes(space):
    size = np.shape(space)
    nSnakes = 2
    while (True):
        finished = False
        i = rnd.randint(2, size[0]-2)
        j = rnd.randint(2, size[1]-2)
        if space[i][j] == 0:
            if nSnakes == 2: snakes.append(snake.Snake(i, j, True))
            else: snakes.append(snake.Snake(i, j, False))
            nSnakes -= 1
        if nSnakes == 0:
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

def moveSnakes(playerDir, space):
    global snakes
    global board
    global playerScore
    global aiScore
    deadSnakes = []
    for s in snakes:
        s.acceptInput(playerDir, space, snakes)
        s.move()
        outcome = s.checkOutcome(board, snakes)
        if outcome == "wall" or outcome == "snake":
            deadSnakes.append(s)
            break
        if outcome == "apple":
            board = s.grow(board)
            if s.isPlayer:
                playerScore += 1
            else:
                aiScore += 1
    for s in deadSnakes:
        snakes.remove(s)
        if s.isPlayer:
            aiScore = winningScore
        else:
            playerScore = winningScore

def spawnApple():
    global board
    size = np.shape(board)
    while(True):
        i = rnd.randint(1,size[0]-1)
        j = rnd.randint(1,size[1]-1)
        if board[i][j] == 0:
            board[i][j] = 2
            break

def subtractTimer(timeLen):
    global ongoingTimer
    ongoingTimer -= timeLen
    if ongoingTimer <= 0:
        spawnApple()
        ongoingTimer = appleTimer

def checkScore():
    global playerScore
    global aiScore
    global winningScore
    global gameFinished
    
    if playerScore >= winningScore and aiScore >= winningScore:
        gameFinished = True
        return 'draw'
    if playerScore >= winningScore:
        gameFinished = True
        return 'player'
    if aiScore >= winningScore:
        gameFinished = True
        return 'ai'
    return ''