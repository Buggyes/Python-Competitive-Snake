from enum import Enum

#Enum criado para facilitar o processo de distinguir a direção que as cobras estão indo
#É melhor do que ficar usando 1,2,3,4 para definir as direções
class Direction(Enum):
    up=1
    down=2
    left=3
    right=4