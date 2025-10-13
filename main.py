import pygame
import numpy as np
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    space = game.createSpace(20,20)
    space = colorDict.translateColors(space)
    surf = pygame.Surface((space.shape[0], space.shape[1]))
    pygame.surfarray.blit_array(surf, space)
    surf = pygame.transform.scale(surf, (sWidth, sHeight))
    screen.blit(surf, (0, 0))
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
