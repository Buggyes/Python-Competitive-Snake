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
    
    def grow(self):
        tip = self.body.__getitem__(self.body.__len__()-1)
        
        if tip.direction == Direction.up:
            self.body.append(SnakeNode(tip.posY, tip.posX-1, Direction.up))
        if tip.direction == Direction.down:
            self.body.append(SnakeNode(tip.posY, tip.posX+1, Direction.down))
        if tip.direction == Direction.left:
            self.body.append(SnakeNode(tip.posY-1, tip.posX, Direction.left))
        if tip.direction == Direction.right:
            self.body.append(SnakeNode(tip.posY+1, tip.posX, Direction.right))

    def checkOutcome(self, space):
        head = self.body[-1]
        collision = space[head.posY][head.posX]
        if collision == 1:
            return "wall"
        if collision == 2:
            return "apple"
        return "free"

    def move(self):
        if self.direction == Direction.up:
            temp = self.body[0]
            self.body.pop(0)
            temp.posX -= 1
            temp.direction = Direction.up
            self.body.append(temp)

        elif self.direction == Direction.down:
            temp = self.body[0]
            self.body.pop(0)
            temp.posX += 1
            temp.direction = Direction.down
            self.body.append(temp)

        elif self.direction == Direction.left:
            temp = self.body[0]
            self.body.pop(0)
            temp.posY -= 1
            temp.direction = Direction.left
            self.body.append(temp)

        elif self.direction == Direction.right:
            temp = self.body[0]
            self.body.pop(0)
            temp.posY += 1
            temp.direction = Direction.right
            self.body.append(temp)
    
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
