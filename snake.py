from enums import Direction

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
            self.minimaxScore = 0
    
    def grow(self, board):
        tip = self.body[0]
        if self.body.__len__() == 1:
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
            for i in range(0, s.body.__len__()-1):
                if head.posX == s.body[i].posX and head.posY == s.body[i].posY:
                    return "snake"
        return "free"

    def move(self):
        prevPositions = [(node.posX, node.posY) for node in self.body]
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

    def evaluateBoard(self, botSnake, playerSnake, space):
        head = botSnake.body[-1]
        # Find apple position
        applePositions = [(x, y) for x in range(space.shape[0]) for y in range(space.shape[1]) if space[x][y] == 2]
        if not applePositions:
            return 0  # no apples

        appleX, appleY = applePositions[0]

        # manhattan distance from head to apple
        distToApple = abs(head.posX - appleX) + abs(head.posY - appleY)

        # distance from player snake (penalize if too close)
        playerHead = playerSnake.body[-1]
        distToPlayer = abs(head.posX - playerHead.posX) + abs(head.posY - playerHead.posY)

        # score combines distance from apple and safety
        score = -distToApple + (0.5 * distToPlayer)
        return score

    def simulateMove(self, snake, direction, space):
        newSnake = Snake(snake.body[-1].posX, snake.body[-1].posY, snake.isPlayer)
        newSnake.body = [SnakeNode(n.posX, n.posY, n.direction) for n in snake.body]
        newSnake.changeDirection(direction)
        newSnake.move()

        # check collision with wall
        head = newSnake.body[-1]
        if space[head.posY][head.posX] == 1:
            return None  # wall hit

        # check self-collision
        for node in newSnake.body[:-1]:
            if node.posX == head.posX and node.posY == head.posY:
                return None

        return newSnake

    def minimax(self, botSnake, playerSnake, space, depth, maximizing):
        if depth == 0:
            return self.evaluateBoard(botSnake, playerSnake, space), None

        bestMove = None
        if maximizing:
            maxEval = float('-inf')
            for direction in Direction:
                newBot = self.simulateMove(botSnake, direction, space)
                if not newBot:
                    continue
                evalScore, _ = self.minimax(newBot, playerSnake, space, depth - 1, False)
                if evalScore > maxEval:
                    maxEval = evalScore
                    bestMove = direction
            return maxEval, bestMove
        else:
            minEval = float('inf')
            for direction in Direction:
                newPlayer = self.simulateMove(playerSnake, direction, space)
                if not newPlayer:
                    continue
                evalScore, _ = self.minimax(botSnake, newPlayer, space, depth - 1, True)
                if evalScore < minEval:
                    minEval = evalScore
            return minEval, None

    def searchApple(self, space, snakes):
        player = next(s for s in snakes if s.isPlayer)
        self.minimaxScore, direction = self.minimax(self, player, space, 2, True)
        if direction:
            self.changeDirection(direction)

    def acceptInput(self, dir: Direction, space, snakes):
        if self.isPlayer:
            self.changeDirection(dir)
        else:
            self.searchApple(space, snakes)
