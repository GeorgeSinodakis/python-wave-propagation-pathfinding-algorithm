import pygame
import math as m

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
CYAN = (173, 216, 230)
TURQUOISE = (64, 224, 208)

nodeSize = 20
nodesX = 50
nodesY = 30

manhattan = 1


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance = 0
        self.path = False

    def clearDistance(self):
        if self.distance != -1:
            self.distance = 0
        if [self.y, self.x] == end:
            self.distance = 1

    def setDistance(self, dist):
        if self.distance == 0:
            self.distance = dist

    def setObstacle(self):
        if [self.y, self.x] != end and [self.y, self.x] != start:
            self.distance = -1

    def clearObstacle(self):
        if self.distance == -1:
            self.distance = 0

    def setPath(self):
        if self.distance != -1:
            self.path = True

    def clearPath(self):
        self.path = False

    def isObstacle(self):
        return self.distance == -1

    def draw(self):
        xn = 1 + self.x * (nodeSize + 1)
        yn = 1 + self.y * (nodeSize + 1)
        if self.distance == -1:
            pygame.draw.rect(screen, BLACK, (xn, yn, nodeSize, nodeSize), 0)
        elif self.path:
            pygame.draw.rect(screen, YELLOW, (xn, yn, nodeSize, nodeSize), 0)
        else:
            c = int(255 - int(self.distance * 10 / manhattan) * int(255 / 10))
            pygame.draw.rect(screen, (c, c, c),
                             (xn, yn, nodeSize, nodeSize), 0)
        if [self.y, self.x] == start:
            img = font.render('S', True, BLACK)
            screen.blit(img, (xn, yn))
        if [self.y, self.x] == end:
            img = font.render('E', True, BLACK)
            screen.blit(img, (xn, yn))


screen = pygame.display.set_mode([nodesX * nodeSize + nodesX + 1, nodesY * nodeSize + nodesY + 1])
pygame.display.set_caption("Wave Propagation Path Finding Algorithm")
font = pygame.font.SysFont('arial.ttf', nodeSize + 5)

grid = [[Node(x, y) for x in range(nodesX)] for y in range(nodesY)]

start = [int(nodesY / 2), int(nodesX / 3)]
end = [int(nodesY / 2), int(nodesX * 2 / 3)]


def clearPaths():
    for y in range(nodesY):
        for x in range(nodesX):
            grid[y][x].clearPath()


def clearDistances():
    for y in range(nodesY):
        for x in range(nodesX):
            grid[y][x].clearDistance()


def clearObstacles():
    for y in range(nodesY):
        for x in range(nodesX):
            grid[y][x].clearObstacle()


def withinBounds(y, x):
    return (x >= 0) and (y >= 0) and (x < nodesX) and (y < nodesY)


def get4Neighbors(c):
    neighbors = []

    x = c[1]
    y = c[0] - 1
    if withinBounds(y, x) and not grid[y][x].isObstacle():
        neighbors.append([y, x])
    x = c[1]
    y = c[0] + 1
    if withinBounds(y, x) and not grid[y][x].isObstacle():
        neighbors.append([y, x])
    x = c[1] - 1
    y = c[0]
    if withinBounds(y, x) and not grid[y][x].isObstacle():
        neighbors.append([y, x])
    x = c[1] + 1
    y = c[0]
    if withinBounds(y, x) and not grid[y][x].isObstacle():
        neighbors.append([y, x])

    return neighbors


def get8Neighbors(c):
    neighbors = []

    for y in range(-1, 2):
        for x in range(-1, 2):
            if withinBounds(c[0]+y, c[1]+x) and (not grid[c[0]+y][c[1]+x].isObstacle()) and not (x == 0 and y == 0):
                neighbors.append([c[0]+y, c[1]+x])

    return neighbors


def setDistances():
    global manhattan
    manhattan = 1

    flag = True
    while flag:
        flag = False
        for y in range(nodesY):
            for x in range(nodesX):
                if grid[y][x].distance == manhattan:
                    for a in get4Neighbors([y, x]):
                        grid[a[0]][a[1]].setDistance(manhattan + 1)
                    flag = True
        manhattan += 1


def smallestNeighbor(c):
    d = 1000000
    current = []
    for a in get8Neighbors(c):
        if grid[a[0]][a[1]].distance < d:
            current = a
            d = grid[a[0]][a[1]].distance
    return current


def findPath():
    clearPaths()

    c = start
    grid[c[0]][c[1]].setPath()
    i = 0
    while True:
        if c == end:
            break
        if i > 1000:
            clearPaths()
            break
        c = smallestNeighbor(c)
        grid[c[0]][c[1]].setPath()
        i += 1


def draw():
    screen.fill(BLACK)
    for y in range(nodesY):
        for x in range(nodesX):
            grid[y][x].draw()


def update():
    clearDistances()
    setDistances()
    findPath()


def userInput():
    global start
    global end
    if pygame.mouse.get_pressed()[0]:
        x = int(pygame.mouse.get_pos()[0] / (nodeSize + 1))
        y = int(pygame.mouse.get_pos()[1] / (nodeSize + 1))
        if withinBounds(y, x):
            if pygame.key.get_pressed()[pygame.K_s]:
                start = [y, x]
            elif pygame.key.get_pressed()[pygame.K_e]:
                end = [y, x]
            else:
                grid[y][x].setObstacle()
    if pygame.key.get_pressed()[pygame.K_r]:
        for y in range(nodesY):
            for x in range(nodesX):
                grid[y][x].clearObstacle()


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    userInput()
    update()
    draw()

    pygame.display.flip()

pygame.quit()
