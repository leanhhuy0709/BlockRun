""" 
Block Run Game
python run.py
"""
#const

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
COLORS = [(255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 255, 255), (255, 0, 255), 
          (192, 192, 192), (132, 112, 255)
          ]

#library
import pygame as pg, random as rd, sys, time
from pygame.locals import *
import threading

rd.seed(time.time())
pg.init()
pg.display.set_caption("Block Run")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pg.font.SysFont("cambria", 30, True)

pg.mixer.music.set_volume(0.7)
musics = ['Renai Circulation.mp3', 'Return Of The Heroes.mp3', 'Summertime.mp3', 'The Other Side.mp3', 'Unstoppable.mp3']
rd.shuffle(musics)
stopMusics = False
def playMusics():
    while not stopMusics:
        # Check if the current song is finished
        if not pg.mixer.music.get_busy():
            # If the song is finished, remove it from the list
            current_song = musics.pop(0)
            # Load the next song
            pg.mixer.music.load('music/' + current_song)
            # Play the next song
            pg.mixer.music.play()

t = threading.Thread(target=playMusics)
t.start()

class playerBlock:
    x = int(SCREEN_WIDTH/20)*10
    y = int(SCREEN_HEIGHT/20)*10
    color = (255, 0, 0)
    #color = rd.choice(COLORS)
    size = 10
    direct = "R"
    point = 0
    def init(color = (255, 0, 0), size = 10, direct = "R"):
        playerBlock.color = color
        playerBlock.size = size
        playerBlock.direct = direct
    def draw():
        pg.draw.rect(screen, playerBlock.color, ((playerBlock.x, playerBlock.y), (playerBlock.size, playerBlock.size)))
    def move():
        if playerBlock.direct == "U": 
            playerBlock.y = playerBlock.y - 10
        elif playerBlock.direct == "L":
            playerBlock.x = playerBlock.x - 10
        elif playerBlock.direct == "D":
            playerBlock.y = playerBlock.y + 10
        elif playerBlock.direct == "R":
            playerBlock.x = playerBlock.x + 10
        playerBlock.x = (playerBlock.x + SCREEN_WIDTH)% SCREEN_WIDTH
        playerBlock.y = (playerBlock.y + SCREEN_HEIGHT) % SCREEN_HEIGHT
         
class enemyBlock:
    x = 0
    y = 0
    color = (255, 0, 0)
    size = 10
    direct = "R"
    delay = 0
    def init(self):
        temp = rd.randint(1, 4)
        if temp == 1: 
            self.x = int(rd.randint(0, SCREEN_WIDTH)/10)*10 - 10
            self.y = 0
            self.direct = "D"
        elif temp == 2: 
            self.x = int(rd.randint(0, SCREEN_WIDTH)/10)*10 - 10
            self.y = SCREEN_HEIGHT - 10
            self.direct = "U"
        elif temp == 3: 
            self.x = 0
            self.y = int(rd.randint(0, SCREEN_HEIGHT)/10)*10 - 10
            self.direct = "R"
        else: 
            self.x = SCREEN_WIDTH - 10
            self.y = int(rd.randint(0, SCREEN_HEIGHT)/10)*10 - 10
            self.direct = "L"
        self.color = rd.choice(COLORS)
        self.size = 10
        self.delay = rd.randint(10, 50)
    def draw(self):
        pg.draw.rect(screen, self.color, ((self.x, self.y), (self.size, self.size)))
    def move(self):
        if self.delay > 0: 
            self.delay -= 1
            return
        if self.direct == "U": 
            self.y = self.y - 10
        elif self.direct == "L":
            self.x = self.x - 10
        elif self.direct == "D":
            self.y = self.y + 10
        elif self.direct == "R":
            self.x = self.x + 10
        if self.x < 0 or self.x > SCREEN_WIDTH - 10 or self.y < 0 or self.y > SCREEN_HEIGHT - 10:
            self.init()
            playerBlock.point += 1
    
class Food:
    x = 0
    y = 0
    color = (255, 0, 0)
    size = 10
    delay = 10
    def init(self):
        self.x = int(rd.randint(0, SCREEN_WIDTH)/10)*10 - 10
        self.y = int(rd.randint(0, SCREEN_HEIGHT)/10)*10 - 10
        self.color = (255, 0, 0)
        self.delay = rd.randint(10, 100)
    def draw(self):
        if self.delay == 0:
            pg.draw.rect(screen, self.color, ((self.x, self.y), (self.size, self.size)))
        else:
            self.delay -= 1
        
class Icon:
    x = 50
    y = 70
    color = (255, 255, 0)
    shape = [[0, 0], [0, 10], [0, 20], [0, 30], [0, 40],
             [10, 0], [10, 10], [10, 20], [10, 30], [10, 40],
             [20, 0], [20, 10], [20, 20], [20, 30], [20, 40],
             [30, 0], [30, 10], [30, 20], [30, 30], [30, 40],
             [40, 0], [40, 10], [40, 20], [40, 30], [40, 40],
             ]
    def init(self):
        self.x = int(rd.randint(SCREEN_WIDTH/4, SCREEN_WIDTH*3/4)/10)*10 - 10
        self.y = int(rd.randint(SCREEN_HEIGHT/4, SCREEN_HEIGHT*3/4)/10)*10 - 10
        self.color = rd.choice(COLORS)
    def draw(self):
        """
        for i in self.shape:
            pg.draw.rect(screen, self.color, ((self.x + i[0], self.y + i[1]), (10, 10)))      
        """
        
        points = [ (165, 151), (200, 20), (235, 151), (371, 144), (257, 219),
                 (306, 346), (200, 260), (94, 346), (143, 219), (29, 144)   ]

        # Draw the star
        pg.draw.polygon(screen, self.color, list(map(lambda iter: (iter[0]*0.3 + self.x, iter[1]*0.3 + self.y), points)))
        
enemys = []
def initEnemys(numberOfEnemys): 
    enemys.clear()   
    for i in range(numberOfEnemys):
        temp = enemyBlock()
        temp.init()
        enemys.append(temp)
def drawEnemys():
    for i in enemys:
        i.draw()
def moveEnemys():
    for i in enemys:
        i.move()
def addEnemy():
    temp = enemyBlock()
    temp.init()
    enemys.append(temp)
def isTouchPlayerBlockAndEnemy():
    for i in enemys:
        if i.x == playerBlock.x and i.y == playerBlock.y:
            return True
    return False   
initEnemys(10)   

icons = []
def initIcons(numberOfIcons):
    icons.clear()   
    for i in range(numberOfIcons):
        temp = Icon()
        temp.init()
        icons.append(temp)
def drawIcons():
    for i in icons:
        i.draw() 
initIcons(0)

foods = []
def initFoods(numberOfFoods):
    foods.clear()   
    for i in range(numberOfFoods):
        temp = Food()
        temp.init()
        foods.append(temp)
def isTouchPlayerBlockAndFood():
    for i in foods:
        if i.x == playerBlock.x and i.y == playerBlock.y:
            enemys.pop(0)
            i.init()
def drawFoods():
    for i in foods:
        i.draw()
initFoods(2)

def initGame(nOfEnemys, nOfIcons, nOfFoods):
    initEnemys(nOfEnemys)    
    initIcons(nOfIcons)    
    initFoods(nOfFoods)    

class Mouse:
    Down = [0, 0]
    Up = [0, 0]
    def getDirect():
        xValue = Mouse.Up[0] - Mouse.Down[0]
        yValue = Mouse.Up[1] - Mouse.Down[1]
        if xValue < 0 and yValue < 0:
            if abs(xValue) < abs(yValue): return "U"
            else: return "L"
        if xValue < 0 and yValue > 0:
            if abs(xValue) < abs(yValue): return "D"
            else: return "L"
        if xValue > 0 and yValue < 0:
            if abs(xValue) < abs(yValue): return "U"
            else: return "R"
        if xValue > 0 and yValue > 0:
            if abs(xValue) < abs(yValue): return "D"
            else: return "R"
        return "N"

def gameLoop():
    GameIsRunning = True
    stagePoint = 10
    while GameIsRunning:
        for event in pg.event.get():
            if event.type == QUIT:
                    stopMusics = True
                    t.join()
                    pg.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    playerBlock.direct = "U"
                elif event.key == K_DOWN:     
                    playerBlock.direct = 'D'
                elif event.key == K_LEFT:       
                    playerBlock.direct = 'L'
                elif event.key == K_RIGHT:     
                    playerBlock.direct = 'R'
            # Check for mouse button down event
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_pos = pg.mouse.get_pos()
                Mouse.Down = mouse_pos  
            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                Mouse.Up = mouse_pos
                if Mouse.getDirect() != "N":
                    playerBlock.direct = Mouse.getDirect()
                Mouse.Up = Mouse.Down = [0, 0]
        screen.fill((24, 71, 133))
        text = font.render(f'Enemy: {len(enemys)} Point: {playerBlock.point}', 1, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        playerBlock.draw()
        playerBlock.move()
        drawEnemys()
        moveEnemys()
        if playerBlock.point > stagePoint:
            addEnemy()
            stagePoint += 10
        drawFoods()
        isTouchPlayerBlockAndFood()
        drawIcons()
        if isTouchPlayerBlockAndEnemy() or len(enemys) == 0:
            GameIsRunning = False
        time.sleep(0.035)
        pg.display.update()

def tryAgain():
    while True:
        pointText = font.render(f'Point: {playerBlock.point}', 1, (255, 255, 255))
        pointTextRect = pointText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        tryAgainText = font.render(f'Try Again?', 1, (255, 255, 255))
        tryAgainTextRect = tryAgainText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        exitText = font.render(f'Exit', 1, (255, 255, 255))
        exitTextRect = exitText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        for event in pg.event.get():
            if event.type == QUIT:
                    stopMusics = True
                    t.join()
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_pos = pg.mouse.get_pos()
                if tryAgainTextRect.collidepoint(event.pos):
                    return True #Try again
                #if mouse_pos[0] >= tryAgainTextRect.left and mouse_pos[0] <= tryAgainTextRect.right and mouse_pos[1] >= tryAgainTextRect.top and mouse_pos[1] <= tryAgainTextRect.bottom:
                #    return True #Try again
                
                if mouse_pos[0] >= exitTextRect.left and mouse_pos[0] <= exitTextRect.right and mouse_pos[1] >= exitTextRect.top and mouse_pos[1] <= exitTextRect.bottom:
                    return False #Exit
                    
                
                
        screen.fill((24, 71, 133))
        screen.blit(pointText, pointTextRect)
        screen.blit(tryAgainText, tryAgainTextRect)
        screen.blit(exitText, exitTextRect)        
        
        pg.display.update()

    return False

while True:
    playerBlock.point = 0
    playerBlock.x = int(SCREEN_WIDTH/20)*10
    playerBlock.y = int(SCREEN_HEIGHT/20)*10
    initGame(10, 0, 3)    
    gameLoop()
    if not tryAgain(): break        
print(f"Your point: {playerBlock.point}")
stopMusics = True
t.join()

pg.quit()
sys.exit()
