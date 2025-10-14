import pygame
import numpy as np
from snake import Direction
import game
import colorDict

sWidth = 600
sHeight = 600

#Setup
pygame.init()
screen = pygame.display.set_mode((sWidth, sHeight))
clock = pygame.time.Clock()
running = True
playerDir = Direction.right

while running:
    for event in pygame.event.get():
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

    space = game.createSpace(20,20) # Draws board
    game.moveSnakes(playerDir, space) # Moves all snakes
    space = colorDict.translateColors(space, game.snakes) # Translates the indexes into colors for display
    surf = pygame.Surface((space.shape[0], space.shape[1])) # Translates the array into a surface so pygame can draw it
    pygame.surfarray.blit_array(surf, space) # Converts what's in our array into our display array
    surf = pygame.transform.scale(surf, (sWidth, sHeight)) # Scales the surface to the window resolution
    screen.blit(surf, (0, 0)) # Draws the surface into the screen
    pygame.display.update() # Updates the changes

    clock.tick(8) # limits FPS

pygame.quit()
