import pygame
import numpy as np
import time
from enums import Direction
import game
import colorDict

#Define as especificações da janela
sWidth = 600
sHeight = 600
ticksPerSec = 8

#Setup PyGame
pygame.init()
pygame.font.init()
scoreFont = pygame.font.SysFont('Comic Sans MS', int(sHeight/22))
screen = pygame.display.set_mode((sWidth, sHeight))
clock = pygame.time.Clock()
running = True
playerDir = Direction.right

while running:
    start = time.time()
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

    space = game.createSpace(40,40)
    if not game.gameFinished:
        game.moveSnakes(playerDir, space) # Move todas as cobras
    space = colorDict.translateColors(space, game.snakes) # Traduz os índices que estão no mapa para cores
    boardSurf = pygame.Surface((space.shape[0], space.shape[1])) # Traduz o array em uma "surface" que pode ser usada para renderizar na janela pelo PyGame
    pygame.surfarray.blit_array(boardSurf, space) # Converte o que está no array para display
    boardSurf = pygame.transform.scale(boardSurf, (sWidth, sHeight)) # Escalona a surface para a resolução da janela

    #Cada frame checamos se a partida acabou
    result = game.checkScore()
    if (result == 'draw'):
        scoreSurf = scoreFont.render('Empate!                           ',False,(0, 100, 100), (255, 255, 255))
    elif (result == 'player'):
        scoreSurf = scoreFont.render('Jogador Venceu!                   ',False,(0, 100, 100), (255, 255, 255))
    elif (result == 'ai'):
        scoreSurf = scoreFont.render('CPU Venceu!                       ',False,(0, 100, 100), (255, 255, 255))
    else:
        scoreSurf = scoreFont.render('Jogador:'+game.playerScore.__str__()+' | CPU:'+game.aiScore.__str__(),False,(0, 0, 100), (255, 255, 255))

    if not game.gameFinished:
        screen.blit(boardSurf, (0, 0)) # Renderiza a surface na janelatela
    screen.blit(scoreSurf, (0, 0)) # Renderiza o placar na janela
    pygame.display.update() # Atualiza a janela
    clock.tick(ticksPerSec) # limita o FPS (se não o jogo roda rápido demais)

    if not game.gameFinished:
        end = time.time()
        timeLen = start - end
        game.subtractTimer(timeLen*-1) # subtrai o timer e coloca uma maçã no mapa se ele chega a 0

pygame.quit()
