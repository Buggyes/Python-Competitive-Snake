from enums import Direction
from math import sqrt
import random as rnd

# No python se tem o paradigma de que se você quer que uma variável seja exclusiva de uma instância de uma classe,
# você declara ela dentro do construtor (__init__()) usando "self". Isso evita situações onde duas classes mexem
# na mesma variável como se fosse a própria.

# "Nó" da cobra, ou parte do corpo da cobra.
class SnakeNode:
    def __init__(self, posX: int, posY: int, dir: Direction):
        self.posX = posX
        self.posY = posY
        self.direction = dir

class Snake:
    def __init__(self, posX: int, posY: int, isPlayer: bool):
        self.direction = Direction.right
        self.body = [SnakeNode(posX,posY, Direction.right)]
        self.isPlayer = isPlayer

    # Esse método considera a direção da ponta da cobra, pois havia situações onde a cobra crescia dentro dela mesma
    # e isso causava problemas na jogabilidade.
    def grow(self, board):
        tip = self.body[0]
        if len(self.body) == 1:
            if tip.direction == Direction.up:
                self.body.insert(0, SnakeNode(tip.posX-1, tip.posY, Direction.up))
            if tip.direction == Direction.down:
                self.body.insert(0, SnakeNode(tip.posX+1, tip.posY, Direction.down))
            if tip.direction == Direction.left:
                self.body.insert(0, SnakeNode(tip.posX, tip.posY-1, Direction.left))
            if tip.direction == Direction.right:
                self.body.insert(0, SnakeNode(tip.posX, tip.posY+1, Direction.right))
        else:
            tail = self.body[1]
            if tail.posX < tip.posX:
                self.body.insert(0, SnakeNode(tip.posX-1, tip.posY, Direction.up))
            if tail.posX > tip.posX:
                self.body.insert(0, SnakeNode(tip.posX+1, tip.posY, Direction.down))
            if tail.posY < tip.posY:
                self.body.insert(0, SnakeNode(tip.posX, tip.posY-1, Direction.left))
            if tail.posY > tip.posY:
                self.body.insert(0, SnakeNode(tip.posX, tip.posY+1, Direction.right))
        
        head = self.body[-1]
        board[head.posY][head.posX] = 0
        return board
    
    # Sempre que a cobra se move, ela checa o resultado do movimento
    # é implementado individualmente para cada cobra, pois é mais simples
    # de administrar onde cada cobra está
    def checkOutcome(self, space, snakes):
        head = self.body[-1]
        collision = space[head.posY][head.posX]
        if collision == 1:
            return "wall"
        if collision == 2:
            return "apple"
        for s in snakes:
            for i in range(0, len(s.body)-1):
                if head.posX == s.body[i].posX and head.posY == s.body[i].posY:
                    return "snake"
        return "free"

    # A cobra se move...
    # Cada parte do corpo é movida em fila junto com a cobra.
    # Isso evita problemas onde se perde a cabeça da cobra, ou o corpo dela se solta.
    def move(self):
        prevPositions = []
        for n in self.body:
            prevPositions.append((n.posX, n.posY))
        head = self.body[-1]
        
        if self.direction == Direction.up:
            head.posX -= 1
        elif self.direction == Direction.down:
            head.posX += 1
        elif self.direction == Direction.left:
            head.posY -= 1
        elif self.direction == Direction.right:
            head.posY += 1

        for i in range(len(self.body)-1):
            self.body[i].posX, self.body[i].posY = prevPositions[i+1]
    
    # Muda a direção da cobra...
    def changeDirection(self, dir: Direction):
        canChange = False

        if dir == Direction.up and self.direction != Direction.down:
            canChange = True
        elif dir == Direction.down and self.direction != Direction.up:
            canChange = True
        elif dir == Direction.left and self.direction != Direction.right:
            canChange = True
        elif dir == Direction.right and self.direction != Direction.left:
            canChange = True

        if canChange:
            self.direction = dir

    # Verifica se a direção é oposta da que a cobra está indo
    # (USADO APENAS NA BUSCA MINIMAX)
    def isOppositeDirection(self, dir: Direction):
        if dir == Direction.up and self.direction == Direction.down:
            return True
        elif dir == Direction.down and self.direction == Direction.up:
            return True
        elif dir == Direction.left and self.direction == Direction.right:
            return True
        elif dir == Direction.right and self.direction == Direction.left:
            return True
        return False


    def evaluateBoard(self, botSnake, playerSnake, space):
        head = botSnake.body[-1]

        # Procura maçãs
        applePositions = []
        for i in range(0,space.shape[0]):
            for j in range(0,space.shape[1]):
                if space[i][j] == 2:
                    applePositions.append((i, j))
        if not applePositions:
            # Se não houver maçãs, e a cobra for de tamanho 2 ou maior,
            # ela começa a perseguir e tentar encurralar o jogador.
            if len(botSnake.body) > 1:
                playerHead = playerSnake.body[-1]
                distOfPlayer = abs((head.posX - playerHead.posX)**2 + (head.posY - playerHead.posY)**2)
                score = -distOfPlayer
                return score
            return 0

        appleY, appleX = applePositions[-1]

        #Se usa o teorema de pitágoras para calcular a distância da cobra e da maçã
        #(outros métodos provaram ser problemáticos)
        distOfApple = abs((head.posX - appleX)**2 + (head.posY - appleY)**2)
        score = -distOfApple
        return score

    def simulateMove(self, snake, otherSnake, direction, space):
        newSnake = Snake(snake.body[-1].posX, snake.body[-1].posY, snake.isPlayer)
        newSnake.direction = direction
        newSnake.body = [SnakeNode(n.posX, n.posY, n.direction) for n in snake.body]
        newSnake.move()

        head = newSnake.body[-1]
        
        # 2 = maçã
        if space[head.posY][head.posX] == 2:
            return newSnake
        
        # 1 = parede
        if space[head.posY][head.posX] == 1:
            return None  # wall hit

        # Aqui, nós fatiamos o array (arr[:-1]) para usar todo o corpo da cobra menos a cabeça,
        # para a IA não enlouquecer toda vez que ela procurar colisões com o corpo
        for node in newSnake.body[:-1]:
            if node.posX == head.posX and node.posY == head.posY:
                return None

        # Fazemos o menos para a cobra adversária
        for node in otherSnake.body:
            if node.posX == head.posX and node.posY == head.posY:
                bumpChance = rnd.randint(0, 100)
                # por motivos de balanceamento, a IA tem 10% de chance
                # dela se jogar no corpo do jogador quando ela está próxima
                if bumpChance >= 90:
                    return None

        return newSnake

    # Método Minimax (explicado em apresentação)
    def minimax(self, botSnake, playerSnake, space, depth, maximizing):
        if depth == 0:
            return self.evaluateBoard(botSnake, playerSnake, space), None

        bestMove = None
        if maximizing:
            maxEval = float('-inf')
            for direction in Direction:
                if not self.isOppositeDirection(direction):
                    newBot = self.simulateMove(botSnake, playerSnake, direction, space)
                    if not newBot:
                        continue
                    evalScore, _ = self.minimax(newBot, playerSnake, space, depth - 1, False)
                    if evalScore > maxEval or (evalScore == maxEval and direction == self.direction):
                        maxEval = evalScore
                        bestMove = direction
            return maxEval, bestMove
        else:
            minEval = float('inf')
            for direction in Direction:
                if not self.isOppositeDirection(direction):
                    newPlayer = self.simulateMove(playerSnake, botSnake, direction, space)
                    if not newPlayer:
                        continue
                    evalScore, _ = self.minimax(botSnake, newPlayer, space, depth - 1, True)
                    if evalScore < minEval:
                        minEval = evalScore
            return minEval, None

    def searchApple(self, space, snakes):
        player = next(s for s in snakes if s.isPlayer)
        if player:
            _, direction = self.minimax(self, player, space, 5, True)
            if direction:
                self.changeDirection(direction)

    # A gente distingue o jogador e a IA para não ficar fazendo buscas Minimax a toa
    def acceptInput(self, dir: Direction, space, snakes):
        if self.isPlayer:
            self.changeDirection(dir)
        else:
            self.searchApple(space, snakes)
