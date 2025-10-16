import pygame
import numpy as np
import time
from enums import Direction
import game
import colorDict

sWidth = 600
sHeight = 600
ticksPerSec = 8

#Setup
pygame.init()
pygame.font.init()
scoreFont = pygame.font.SysFont('Comic Sans MS', int(sHeight/22))
screen = pygame.display.set_mode((sWidth, sHeight))
clock = pygame.time.Clock()
running = True
playerDir = Direction.right

while running:
    start = time.time()
    for event in pygame.event.get(): # Checks for player input
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerDir = Direction.up
            if event.key == pygame.K_DOWN:
                playerDir = Direction.down
            if event.key == pygame.K_LEFT:
                playerDir = Direction.left
            if event.key == pygame.K_RIGHT:
                playerDir = Direction.right

    space = game.createSpace(40,40) # Draws board
    if not game.gameFinished:
        game.moveSnakes(playerDir, space) # Moves all snakes
    space = colorDict.translateColors(space, game.snakes) # Translates the indexes into colors for display
    boardSurf = pygame.Surface((space.shape[0], space.shape[1])) # Translates the array into a surface so pygame can draw it
    pygame.surfarray.blit_array(boardSurf, space) # Converts what's in our array into our display array
    boardSurf = pygame.transform.scale(boardSurf, (sWidth, sHeight)) # Scales the surface to the window resolution

    result = game.checkScore()
    if (result == 'draw'):
        scoreSurf = scoreFont.render('Empate!',False,(0, 100, 100), (255, 255, 255))
    elif (result == 'player'):
        scoreSurf = scoreFont.render('Jogador Venceu!',False,(0, 100, 100), (255, 255, 255))
    elif (result == 'ai'):
        scoreSurf = scoreFont.render('CPU Venceu!',False,(0, 100, 100), (255, 255, 255))
    else:
        scoreSurf = scoreFont.render('Jogador:'+game.playerScore.__str__()+' | IA:'+game.aiScore.__str__(),False,(0, 0, 100), (255, 255, 255))

    if not game.gameFinished:
        screen.blit(boardSurf, (0, 0)) # Draws the surface into the screen
    screen.blit(scoreSurf, (0, 0))
    pygame.display.update() # Updates the changes
    clock.tick(ticksPerSec) # limits FPS

    if not game.gameFinished:
        end = time.time()
        timeLen = start - end
        game.subtractTimer(timeLen*-1) # subtracts timer and creates apples if it reaches 0

pygame.quit()
