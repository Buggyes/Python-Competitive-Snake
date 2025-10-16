from enums import Direction
from math import sqrt
import random as rnd

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
        if not isPlayer:
            self.pathMaxScore = float('-inf')
            self.pathMinScore = float('inf')
    
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

        # Find apple position
        applePositions = []
        for i in range(0,space.shape[0]):
            for j in range(0,space.shape[1]):
                if space[i][j] == 2:
                    applePositions.append((i, j))
        if not applePositions:
            return 0  # no apples

        appleY, appleX = applePositions[-1]

        #distance from head to apple
        distToApple = abs((head.posX - appleX)**2 + (head.posY - appleY)**2)

        score = -distToApple
        return score

    def simulateMove(self, snake, otherSnake, direction, space):
        newSnake = Snake(snake.body[-1].posX, snake.body[-1].posY, snake.isPlayer)
        newSnake.direction = direction
        newSnake.body = [SnakeNode(n.posX, n.posY, n.direction) for n in snake.body]
        newSnake.move()

        head = newSnake.body[-1]
        # check collision with wall
        if space[head.posY][head.posX] == 1:
            return None  # wall hit

        # check self-collision
        # here, we slice the array so we get everything except the head
        # so we don't accidentally make the AI freak out every frame
        for node in newSnake.body[:-1]:
            if node.posX == head.posX and node.posY == head.posY:
                return None

        for node in otherSnake.body:
            if node.posX == head.posX and node.posY == head.posY:
                bumpChance = rnd.randint(0, 100)
                if bumpChance >= 90:
                    return None

        return newSnake

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

    def acceptInput(self, dir: Direction, space, snakes):
        if self.isPlayer:
            self.changeDirection(dir)
        else:
            self.searchApple(space, snakes)
