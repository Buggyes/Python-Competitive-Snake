import numpy as np

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Traduz as cores de uma matriz para o esquema RGB
def translateColors(arr, snakes):
    result = np.zeros(arr.shape + (3,), dtype=np.uint8)
    result[arr == 0] = black # chão
    result[arr == 1] = white # paredde
    result[arr == 2] = red # maçã
    
    # Jogador = verde
    # CPU = azul
    for s in snakes:
        if s.isPlayer:
            for b in s.body:
                result[b.posY][b.posX] = green
        else:
            for b in s.body:
                result[b.posY][b.posX] = blue
    return result