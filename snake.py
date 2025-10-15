from enum import Enum

class Direction(Enum):
    up=1
    down=2
    left=3
    right=4

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
    
    def grow(self, space):
        tip = self.body[0]
        
        if tip.direction == Direction.up:
            self.body.insert(0, SnakeNode(tip.posX-1, tip.posY, Direction.up))
        if tip.direction == Direction.down:
            self.body.insert(0, SnakeNode(tip.posX+1, tip.posY, Direction.down))
        if tip.direction == Direction.left:
            self.body.insert(0, SnakeNode(tip.posX, tip.posY-1, Direction.left))
        if tip.direction == Direction.right:
            self.body.insert(0, SnakeNode(tip.posX, tip.posY+1, Direction.right))
        
        head = self.body[-1]
        space[head.posY][head.posX] = 0
        return space
        
    def checkOutcome(self, space):
        head = self.body[-1]
        collision = space[head.posY][head.posX]
        if collision == 1:
            return "wall"
        if collision == 2:
            return "apple"
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
        self.direction = dir

    def searchApple(self, space):
        #search goes here
        a = 1

    def acceptInput(self, dir: Direction, space):
        if self.isPlayer:
            self.changeDirection(dir)
        else:
            self.searchApple(space)
