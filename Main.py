import pygame
import os
import random
import math
import sys
import _pickle as cPickle
from pygame import mixer

#Initializing pygame game
pygame.init()
#Creating game window
screen = pygame.display.set_mode((800,600))
#Title and ICO
pygame.display.set_caption("ABAC the Game")

#Finds local file
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))+"\\Resources"

#Default fonts
titleFontFile = os.path.join(THIS_FOLDER, 'Fonts\\Lobster_1.3.otf')
TitleFont = pygame.font.Font(titleFontFile, 40)
font = pygame.font.Font('freesansbold.ttf',32)
smallFontFile = os.path.join(THIS_FOLDER, 'Fonts\\OpenSans-Bold.ttf')
smallFont = pygame.font.Font(smallFontFile, 20)

#Icon 
iconFile = os.path.join(THIS_FOLDER, 'MenuItems\\ABAClogo.png')
icon = pygame.image.load(iconFile)
pygame.display.set_icon(icon)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    #Background
    mmbgFile = os.path.join(THIS_FOLDER, 'Backgrounds\\MainMenuBgnd.png')
    mmbackground = pygame.image.load(mmbgFile)

    while True:
 
        screen.fill((0,0,0))
        screen.blit(mmbackground, (0,0))
        draw_text('ABAC the Game', TitleFont, (15, 106, 54), screen, 275, 15)
        draw_text('Coronavirus Defense', TitleFont, (23, 136, 235), screen, 240, 65)
       #MainMenu Text & Box 
        mmRect = pygame.Rect(275, 125, 250, 50)
        pygame.draw.rect(screen, (23, 136, 235), pygame.Rect(270, 120, 260, 60))
        pygame.draw.rect(screen, (237, 237, 237), mmRect)
        draw_text('Main Menu', font, (255, 0, 0), screen, 310, 135)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(300, 225, 200, 50)
        button_2 = pygame.Rect(300, 325, 200, 50)
        button_3 = pygame.Rect(300, 425, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(295, 220, 210, 60))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(295, 320, 210, 60))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(295, 420, 210, 60))
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        draw_text("Start Game", font, (255,255,255), screen, 312, 235)
        draw_text("Options", font, (255,255,255), screen, 335, 335)
        draw_text("Exit", font, (255,255,255), screen, 365, 435)

        
        draw_text("Created by Garret Pierzchajlo", smallFont, (0,0,0), screen, 500, 570)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()

def game():
    clock = pygame.time.Clock()

    #Background
    bgFile = os.path.join(THIS_FOLDER, 'Backgrounds\\GardenBackground.png')
    background = pygame.image.load(bgFile)

    #Background sound

    bgMusicFile = os.path.join(THIS_FOLDER, 'Audio\\ForestBackground16BPCM.wav')
    mixer.music.load(bgMusicFile)
    mixer.music.play(-1)

    #Defauly Image (unassigned, for subclass mostly)
    defaultImgFile = os.path.join(THIS_FOLDER, 'Enemies\\DefaultImg.png')
    class Entity(object):
        def __init__(self):
            self.img = defaultImgFile
            self.x = 0
            self.y = 0
            self.xChange = 0
            self.yChange = 0
            self.speed = 0
        def getX(self):
            return self.x
        def getY(self):
            return self.y
        def getXChange(self):
            return self.xChange
        def getYChange(self):
            return self.yChange
        def getSpeed(self):
            return self.speed
        def setX(self, x):
            self.x = x
        def setY(self, y):
            self.y = y
        def setXChange(self, xChange):
            self.xChange = xChange
        def setYChange(self, yChange):
            self.yChange = yChange
        def setSpeed(self, speed):
            self.speed = speed
        def blit(self):
            screen.blit(pygame.image.load(self.img), (int(self.x), int(self.y)))
    
    #Class to spawn bullet
    class Bullet(Entity):
        def __init__(self):
            super().__init__()
            self.img = os.path.join(THIS_FOLDER, 'Players\\DefaultImg.png')
            self.x = 0
            self.y = 500
            self.yChange = 10
            self.state = "ready"
        def fire(self, x):
            if self.state == "ready":
                #play bullet sound
                mixer.Sound(os.path.join(THIS_FOLDER, 'Audio\\fireSquash.wav')).play()
                #Get x coord of ship
                self.state = "fire"
                self.x = x
            if self.state == "fire":
                self.y -= self.yChange
                screen.blit(pygame.image.load(self.img), (int(x+30),int(self.y+10)))
        def getState(self):
            return self.state
        def reset(self):
            self.x = 0
            self.y = 500
            self.state = "ready"
    BulletEntity = Bullet()


    #Player creation
    class Player(Entity):
        def __init__(self):
            super().__init__()
            self.img = os.path.join(THIS_FOLDER, 'Players\\GahagenPlayer.png')
            self.x = 350
            self.y = 500
            self.xChange = 0
            self.speed = 6
            self.bullet = os.path.join(THIS_FOLDER, 'Players\\GahagenShot.png')
        def update(self):
            self.x += self.xChange
            self.blit()
            
    PlayerEntity = Player()
    BulletEntity.img = PlayerEntity.bullet

    class Enemy(Entity):
        def __init__(self):
            super().__init__()
            self.img = defaultImgFile
            self.x = random.randint(0,736)
            self.y = random.randint(50,150)
            self.speed = 1
            self.startingDirection = [-1,1][random.randrange(2)]
            self.yChange = 40
        def getSpeed(self):
            return self.speed
            
    #coronaEnemy
    coronaEnemyFile = os.path.join(THIS_FOLDER, 'Enemies\\CoronaEnemy.png')
    class Coronavirus(Enemy):
        def __init__(self):
            super().__init__()
            self.img = coronaEnemyFile
            self.yChange = 40
            self.speed = random.uniform(2,3) * self.startingDirection

    #coronaSuperEnemy
    coronaEnemyFile = os.path.join(THIS_FOLDER, 'Enemies\\CoronaEnemy.png')
    class SuperCoronavirus(Enemy):
        def __init__(self):
            super().__init__()
            #self.img = coronaEnemyFile
            self.yChange = 40
            self.speed = random.uniform(4,6) * self.startingDirection

    #List of all enemy objects, append to add enemy to the game, autoremoved on collision
    EnemyList = []

    def ClearEnemies(): 
        for x in EnemyList[:]:
            EnemyList.remove(x)

    #Initial Enemy Spawning
    initialEnemies = 10
    for i in range(initialEnemies):
        EnemyList.append(Coronavirus())

    #Level Handler
    global level_value
    level_value = 1
    def handleLevel():
        lvlRect = pygame.Rect(5, 50, 180, 40)
        pygame.draw.rect(screen, (0, 102, 102), lvlRect)
        lvl = font.render("Level: "+ str(level_value), True, (255,255,255))
        screen.blit(lvl,(10,55))
    #Score handling
    score_value = 0
    def show_score():
        button_1 = pygame.Rect(5, 5, 180, 40)
        pygame.draw.rect(screen, (0, 102, 102), button_1)
        score = font.render("Score: "+ str(score_value), True, (255,255,255))
        screen.blit(score,(10,10))
    def checkLevel():
        #move all level spawning, including initial possibly here
        global level_value
        if(score_value == 10):  
            level_value = 2
            newCV = 12
            for i in range(newCV):
                EnemyList.append(Coronavirus())
        elif(score_value == 22):
            level_value = 3
            newCV = 5
            for i in range(newCV):
                EnemyList.append(Coronavirus())
            newSuperCV = 2
            for i in range(newCV):
                EnemyList.append(SuperCoronavirus())

    def isCollision(EnemyX, EnemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(EnemyX - bulletX, 2) + (math.pow(EnemyY - bulletY, 2)))
        if distance < 30:
            return True
        else:
            return False

    
    #Game Over handling
    global isGameOver
    isGameOver = False
    def game_over():
        ClearEnemies()
        global isGameOver
        isGameOver = True
        over_text = pygame.font.Font(os.path.join(THIS_FOLDER, 'Fonts\\OpenSans-ExtraBold.ttf'), 70).render("GAME OVER", True, (214, 2, 230))
        screen.blit(over_text,(200,200))

    #Main repeater
    running = True
    while running:
        #RGB & set background
        screen.fill((0, 0, 0))
        screen.blit(background, (0,0))

        #Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    PlayerEntity.setXChange(-(PlayerEntity.getSpeed()))
                    #playerX_change = -(movespeed)
                if event.key == pygame.K_RIGHT:
                    PlayerEntity.setXChange(PlayerEntity.getSpeed())
                   # playerX_change = movespeed
                if event.key == pygame.K_SPACE:
                    if BulletEntity.getState() == "ready":
                        BulletEntity.fire(PlayerEntity.getX())
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerEntity.setXChange(0)

        #Create boundaries for PLAYER
        if PlayerEntity.getX() < 0:
            PlayerEntity.setX(0)
        elif PlayerEntity.getX() > 736:
            PlayerEntity.setX(736)
        
        #Iterates through copied list
        for x in EnemyList[:]:
            #Game Over
            if  x.getY() > 440:
                game_over()
                break
            #coronaEnemy Movement
            x.setX(x.getX()+x.getSpeed())
            #Create boundaries for coronaEnemy
            if x.getX() <= 0:
                x.setSpeed(-x.getSpeed())
                x.setY(x.getY()+x.getYChange())
            elif x.getX() >= 736:
                x.setSpeed(-x.getSpeed())
                x.setY(x.getY()+x.getYChange())
            #Collisions
            collision = isCollision(x.getX(),x.getY(),BulletEntity.getX(),BulletEntity.getY())
            if collision:
                BulletEntity.reset()
                score_value +=1
                #play bullet sound
                explosionSoundFile = os.path.join(THIS_FOLDER, 'Audio\\pop.wav')
                explosion_sound = mixer.Sound(explosionSoundFile)
                explosion_sound.play()
                EnemyList.remove(x)
                #Set level upgrades, single check (to centralize & organize)
                checkLevel()
            x.blit()
        #Bullet boundry
        if BulletEntity.getY() <= -10:
            BulletEntity.reset()
        #Bullet movement
        if BulletEntity.getState() == "fire":
            BulletEntity.fire(BulletEntity.getX())
        if(isGameOver):
            game_over()
        #push to player/coronaEnemy func
        PlayerEntity.update()
        show_score()
        handleLevel()
        pygame.display.update()
        clock.tick(30)

#Set up settings
class GameOptions(object):
    def __init__(self):
        self.players = ["Gahagen"]
        self.activePlayer = "Gahagen"    

    def update(self, activePlayer):
        self.activePlayer = activePlayer
    def save(self):
        with open(os.path.join(THIS_FOLDER, 'GameOptions.txt'),'wb') as f:
            f.write(cPickle.dumps(self.__dict__))

    def load(self):
        with open(os.path.join(THIS_FOLDER, 'GameOptions.txt'),'rb') as f:
            dataPickle = f.read()

        self.__dict__ = cPickle.loads(dataPickle)

#Initially create useable instance of options and load for use globally
WorkingOptions = GameOptions()
try:
    WorkingOptions.load()
except:
    WorkingOptions.save()


def options():
    #Background
    mmbackground = pygame.image.load(os.path.join(THIS_FOLDER, 'Backgrounds\\MainMenuBgnd.png'))
    leftarrow = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\LeftArrow.png'))
    rightarrow = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\RightArrow.png'))
    leftarrowRECT = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\LeftArrow.png')).convert().get_rect()
    rightarrowRECT = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\RightArrow.png')).convert().get_rect()

    running = True
    while running:

        screen.fill((0,0,0))
        screen.blit(mmbackground, (0,0))
        #MainMenu Text & Box 
        mmRect = pygame.Rect(275, 95, 250, 50)
        pygame.draw.rect(screen, (23, 136, 235), pygame.Rect(270, 90, 260, 60))
        pygame.draw.rect(screen, (237, 237, 237), mmRect)
        draw_text('Options', font, (255, 0, 0), screen, 330, 105)
        

        #Option 1... Outer box, inner box, text
        #option 1 presents list of players
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(295, 220, 210, 60))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(300, 225, 200, 50))
        draw_text("Gahagen", font, (255,255,255), screen, 312, 235)
        screen.blit(leftarrow, (227, 218))
        screen.blit(rightarrow, (510, 218))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                print('Mouse button clicked')
                print("Most pos " + str(event.pos))
                mx, my = event.pos
                #Mouse event is captured w pos, but not recognizing collision
                if leftarrowRECT.collidepoint(mx, my):
                    print('Left Arrow Clicked')
                if rightarrowRECT.collidepoint(mx, my):
                    print('Right Arrow Clicked')

        
        pygame.display.update()

main_menu()