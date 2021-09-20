# Rules
# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square 
# cells, each of which is in one of two possible states, live or dead, (or populated and 
# unpopulated, respectively). Every cell interacts with its eight neighbours, which are 
# the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, 
# the following transitions occur:
# 
# 1.Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2.Any live cell with two or three live neighbours lives on to the next generation.
# 3.Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4.Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
# These rules, which compare the behavior of the automaton to real life, can be condensed into the following:
# 
# 1.Any live cell with two or three live neighbours survives.
# 2.Any dead cell with three live neighbours becomes a live cell.
# 3.All other live cells die in the next generation. Similarly, all other dead cells stay dead.
# The initial pattern constitutes the seed of the system. The first generation is created by
# applying the above rules simultaneously to every cell in the seed, live or dead; births and
# deaths occur simultaneously, and the discrete moment at which this happens is sometimes
# called a tick. Each generation is a pure function of the preceding one. The rules continue
# to be applied repeatedly to create further generations.


import pygame

# Grid Size
xSize = 70
ySize = 40

pausedFPS = 60
unpausedFPS = 4

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
GRAY2 = (90, 90, 90)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

pygame.display.set_caption('leGameOfLife')
clock = pygame.time.Clock()



dispMult = 20
xDisplay = xSize * dispMult
yDisplay = ySize * dispMult

gameDisplay = pygame.display.set_mode((xDisplay,yDisplay + dispMult*2))

LIVE = True
DEAD = False


map = []


def initMap():
    map.clear()
    for y in range(ySize):
        tmp = []
        for x in range(xSize):
            tmp.append(DEAD)
        map.append(tmp)


def drawMap():
    for y in range(ySize):
        for x in range(xSize):
            if   map[y][x] == LIVE:
                pygame.draw.rect(gameDisplay, YELLOW, [x * dispMult , y * dispMult, dispMult, dispMult])
            elif map[y][x] == DEAD:
                pygame.draw.rect(gameDisplay, GRAY2, [x * dispMult , y * dispMult, dispMult, dispMult])
            pygame.draw.rect(gameDisplay, GRAY, [x * dispMult , y * dispMult, dispMult, dispMult], 1)  


def getNeighbours(y, x):
    
    neighbours = 0

    if(y != 0)         and                      (map[y-1][x] == LIVE): # TOP
        neighbours += 1
    if(y != 0)         and (x != (xSize-1)) and (map[y-1][x+1] == LIVE): # TOP RIGHT
        neighbours += 1
    if(x != (xSize-1)) and                      (map[y][x+1] == LIVE): # RIGHT
        neighbours += 1
    if(y != (ySize-1)) and (x != (xSize-1)) and (map[y+1][x+1] == LIVE): # BOTTOM RIGHT
        neighbours += 1
    if(y != (ySize-1)) and                      (map[y+1][x] == LIVE): # BOTTOM
        neighbours += 1     
    if(y != (ySize-1)) and (x != 0)         and (map[y+1][x-1] == LIVE): # BOTTOM LEFT
        neighbours += 1     
    if(x != 0)         and                      (map[y][x-1] == LIVE): # LEFT
        neighbours += 1             
    if(y != 0)         and (x != 0)         and (map[y-1][x-1] == LIVE): # TOP LEFT
        neighbours += 1     

    return neighbours


def gameUpdate():
    neighboursMap = []

    for y in range(ySize):
        neighboursMap.append([])
        for x in range(xSize):
            neighboursMap[y].append(getNeighbours(y, x))
    
    for y in range(ySize):
        for x in range(xSize):
            if   (map[y][x] == LIVE) and (neighboursMap[y][x] != 2) and (neighboursMap[y][x] != 3):
                map[y][x] = DEAD
            elif (map[y][x] == DEAD) and (neighboursMap[y][x] == 3):
                map[y][x] = LIVE


def changeCell(mouseY, mouseX):
    curY = mouseY // dispMult
    curX = mouseX // dispMult
    map[curY][curX] = not map[curY][curX]


def main(): 
    initMap()

    pygame.init()

    PAUSE = True

    font = pygame.font.SysFont(None, 25)
    text = font.render('Left Click: Flip Cell , R: Reset Grid , N: Next State , SPACE: Un/Pause , PAUSED', True, WHITE)

    while True:
        gameDisplay.fill(BLACK)
        drawMap()
        gameDisplay.blit(text, (10 , yDisplay + dispMult/2))

        buttonPress = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if buttonPress == False:
                    if (event.key == pygame.K_SPACE):
                        PAUSE = not PAUSE
                        buttonPress = True
                        if PAUSE == True:
                            text = font.render('Left Click: Flip Cell , R: Reset Grid , N: Next State , SPACE: Un/Pause , PAUSED', True, WHITE)
                        else:
                            text = font.render('Left Click: Flip Cell , R: Reset Grid , N: Next State , SPACE: Un/Pause , UNPAUSED', True, WHITE)
                    elif (event.key == pygame.K_r):
                        initMap()
                        PAUSE = True
                        buttonPress = True
                    elif (event.key == pygame.K_n) and (PAUSE == True):
                        gameUpdate()
                        buttonPress = True
            if event.type == pygame.MOUSEBUTTONUP:
                if buttonPress == False:
                    if (event.button == 1):
                        buttonPress = True
                        mouseX, mouseY = pygame.mouse.get_pos()
                        if (mouseY // dispMult) < ySize:
                            changeCell(mouseY, mouseX)

        if PAUSE == False:
            gameUpdate()

        pygame.display.update()

        if PAUSE == True:
            clock.tick(pausedFPS)
        else:
            gameUpdate()
            clock.tick(unpausedFPS)

if __name__ == "__main__":
    main()