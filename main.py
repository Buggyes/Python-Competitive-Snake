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

while running:
    playerDir = Direction.right
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

    space = game.createSpace(20,20)
    space = colorDict.translateColors(space, game.snakes)
    surf = pygame.Surface((space.shape[0], space.shape[1]))
    pygame.surfarray.blit_array(surf, space)
    surf = pygame.transform.scale(surf, (sWidth, sHeight))
    screen.blit(surf, (0, 0))
    pygame.display.update()

    clock.tick(10)  # limits FPS to 60

pygame.quit()
