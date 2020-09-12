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
  
        button_1 = pygame.Rect(300, 225, 200, 50)
        button_2 = pygame.Rect(300, 325, 200, 50)
        button_3 = pygame.Rect(300, 425, 200, 50)
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
                    if button_1.collidepoint(event.pos):
                        game()
                    if button_2.collidepoint(event.pos):
                        options()
                    if button_3.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
 
        pygame.display.update()

def game():
    clock = pygame.time.Clock()
    mixer.music.set_volume(WorkingOptions.volume)
    if(not WorkingOptions.isVolumeOn):
        mixer.music.set_volume(0)

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
    #Player creation
    class Player(Entity):
        def __init__(self):
            super().__init__()
            self.img = WorkingOptions.playerImg
            self.x = 350
            self.y = 450
            self.xChange = 0
            self.speed = 6
            self.bulletIMG = WorkingOptions.bulletImg
        def update(self):
            self.x += self.xChange
            self.blit()
            
    PlayerEntity = Player()    
    #Class to spawn bullet
    class Bullet(Entity):
        def __init__(self):
            super().__init__()
            self.img = PlayerEntity.bulletIMG
            self.x = 0
            self.y = 500
            self.yChange = 10
            self.state = "ready"
            self.bulletSound = os.path.join(THIS_FOLDER, 'Audio\\fireSquash.wav')
        def fire(self, x):
            if self.state == "ready":
                #play bullet sound
                if (WorkingOptions.isVolumeOn): mixer.Sound(self.bulletSound).play()
                #Get x coord of ship
                self.state = "fire"
                self.x = x + 45
            if self.state == "fire":
                self.y -= self.yChange
                screen.blit(pygame.image.load(self.img), (int(self.x),int(self.y)))
        def getState(self):
            return self.state
        def reset(self):
            self.x = 0
            self.y = 500
            self.state = "ready"
    ammo = 3
    BulletList = []
    for bullets in range(ammo):
        BulletList.append(Bullet())

    class Enemy(Entity):
        def __init__(self):
            super().__init__()
            self.img = defaultImgFile
            self.x = random.randint(0,736)
            self.y = random.randint(50,150)
            self.speed = 1
            self.startingDirection = [-1,1][random.randrange(2)]
            self.yChange = 40
            self.destroySound = os.path.join(THIS_FOLDER, 'Audio\\pop.wav')
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

    #Timer
    countTime = 0
    def show_time():
        pygame.draw.rect(screen, (0, 102, 102), pygame.Rect(600, 50, 180, 40))
        score = font.render("Time: "+str(int(math.trunc(countTime/30))), True, (255,255,255))
        screen.blit(score,(605,55))

    #Score handling
    score_value = 0
    def show_score():
        pygame.draw.rect(screen, (0, 102, 102), pygame.Rect(5, 5, 180, 40))
        score = font.render("Score: "+ str(score_value), True, (255,255,255))
        screen.blit(score,(10,10))

    #Level Handler
    global shots_value
    shots_value = 0
    def show_shots():
        pygame.draw.rect(screen, (0, 102, 102), pygame.Rect(5, 50, 180, 40))
        shots = font.render("Shots: "+ str(shots_value), True, (255,255,255))
        screen.blit(shots,(10,55))

    #Level Handler
    global level_value
    level_value = 1
    def show_level():
        pygame.draw.rect(screen, (0, 102, 102), pygame.Rect(600, 5, 180, 40))
        lvl = font.render("Level: "+ str(level_value), True, (255,255,255))
        screen.blit(lvl,(605,10))
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
        #collision based on center of 64x64px enemy
        #TODO rework to take inpput of enemy width and heigth and generalize centering mechanism
        distance = math.sqrt(math.pow((EnemyX + 32) - bulletX, 2) + (math.pow((EnemyY + 32) - bulletY, 2)))
        if distance < 32:
            return True
        else:
            return False
    
    #Game Over handling
    global isGameOver
    global end_time
    isGameOver = False
    end_time = 0
    def game_over():
        global isGameOver
        if(not isGameOver):
            end_time = str(int(math.trunc(countTime/30)))
        ClearEnemies()
        isGameOver = True
        over_text = pygame.font.Font(os.path.join(THIS_FOLDER, 'Fonts\\OpenSans-ExtraBold.ttf'), 70).render("GAME OVER", True, (214, 2, 230))
        screen.blit(over_text,(200,100))
        over_text = pygame.font.Font(os.path.join(THIS_FOLDER, 'Fonts\\OpenSans-Semibold.ttf'), 35).render("Time: "+end_time+" | Accuracy: "+str((score_value/shots_value)*100), True, (214, 2, 230))
        screen.blit(over_text,(200,250))

    def PauseGame():
        Pause = True
        text = pygame.font.Font(os.path.join(THIS_FOLDER, 'Fonts\\OpenSans-ExtraBold.ttf'), 70).render("GAME PAUSED", True, (255, 0, 0))
        while(Pause):
            screen.blit(text,(170,200))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_p):
                        Pause = False    
            pygame.display.update()
            clock.tick(30)

    #Main repeater
    running = True
    while running:
        countTime += 1
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
                if event.key == pygame.K_RIGHT:
                    PlayerEntity.setXChange(PlayerEntity.getSpeed())
                if event.key == pygame.K_SPACE:
                    for x in BulletList:
                        if x.getState() == "ready":
                            x.fire(PlayerEntity.getX())
                            shots_value += 1
                            break
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    running = False
                if(event.key == pygame.K_p):
                    PauseGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerEntity.setXChange(0)

        #Create boundaries for PLAYER
        if PlayerEntity.getX() < 0:
            PlayerEntity.setX(0)
        elif PlayerEntity.getX() > 655:
            PlayerEntity.setX(655)
        
        #Iterates through copied list
        for x in EnemyList[:]:
            #Game Over
            if  x.getY() > 420:
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
            for bullets in BulletList:
                collision = isCollision(x.getX(),x.getY(),bullets.getX(),bullets.getY())
                if collision:
                    score_value +=1
                    #play bullet sound
                    if (WorkingOptions.isVolumeOn): mixer.Sound(x.destroySound).play() 
                    bullets.reset()
                    EnemyList.remove(x)
                    #Set level upgrades, single check (to centralize & organize)
                    checkLevel()
            x.blit()
        #Bullet boundry
        for x in BulletList:
            if x.getY() <= -10:
                x.reset()
            #Bullet movement
            if x.getState() == "fire":
                x.fire(x.getX())
        if(isGameOver):
            game_over()
        #push to player/coronaEnemy func
        PlayerEntity.update()
        show_score()
        show_shots()
        show_level()
        show_time()
        pygame.display.update()
        clock.tick(30)

#Set up settings
class GameOptions(object):
    def __init__(self):
        self.players = ["Dr. Gahagen","Jason Pace","Dr. Beals"]
        self.activePlayer = "Dr. Gahagen"
        self.playerImg = os.path.join(THIS_FOLDER, 'Players\\GahagenPlayer.png')
        self.bulletImg = os.path.join(THIS_FOLDER, 'Players\\GahagenShot.png')
        self.volume = 0.1 #Float 0 to 1
        self.isVolumeOn = True

    def update(self, activePlayer):
        self.activePlayer = activePlayer
    def setActivePlayer(self, newPlayer):
        self.activePlayer = newPlayer
        if(self.activePlayer == "Dr. Gahagen"):
            self.playerImg = os.path.join(THIS_FOLDER, 'Players\\GahagenPlayer.png')
            self.bulletImg = os.path.join(THIS_FOLDER, 'Players\\GahagenShot.png')
        if(self.activePlayer == "Jason Pace"):
            self.playerImg = os.path.join(THIS_FOLDER, 'Players\\JasonPacePlayer.png')
            self.bulletImg = os.path.join(THIS_FOLDER, 'Players\\DefaultShot.png')
        if(self.activePlayer == "Dr. Beals"):
            self.playerImg = os.path.join(THIS_FOLDER, 'Players\\BealsPlayer.png')
            self.bulletImg = os.path.join(THIS_FOLDER, 'Players\\DefaultShot.png')

    def save(self):
        with open(os.path.join(THIS_FOLDER, 'GameOptions.txt'),'wb') as f:
            f.write(cPickle.dumps(self.__dict__))
    def load(self):
        with open(os.path.join(THIS_FOLDER, 'GameOptions.txt'),'rb') as f:
            dataPickle = f.read()
        self.__dict__ = cPickle.loads(dataPickle)

#Initially create useable instance of options and load for use globally
WorkingOptions = GameOptions()

#ToDo add mechanism to check if file contains all attributes
#If not working, delete gameoptions txt file. Probably contains older class version

#currently saves options first since there is no front end saving option

try:
    WorkingOptions.load()
except:
    WorkingOptions.save()


def options():
    #Background
    mmbackground = pygame.image.load(os.path.join(THIS_FOLDER, 'Backgrounds\\MainMenuBgnd.png'))
    leftarrow = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\LeftArrow.png'))
    rightarrow = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\RightArrow.png'))
    
    backarrow = pygame.image.load(os.path.join(THIS_FOLDER, 'MenuItems\\BackArrow.png'))
    backarrowRect = pygame.Rect(25, 25, 64, 64)

    arrowy1 = 218; Larrowx1 = 177; Rarrowx1 = 560
    leftarrowRECT1 = pygame.Rect(Larrowx1, arrowy1, 64, 64)
    rightarrowRECT1 = pygame.Rect(Rarrowx1, arrowy1, 64, 64)

    arrowy2 = 318; Larrowx2 = 177; Rarrowx2 = 560
    leftarrowRECT2 = pygame.Rect(Larrowx2, arrowy2, 64, 64)
    rightarrowRECT2 = pygame.Rect(Rarrowx2, arrowy2, 64, 64)

    #Temp Variables presave
    List_of_Players = WorkingOptions.players
    try:
        PlayerListPos = List_of_Players.index(WorkingOptions.activePlayer)
    except:
        PlayerListPos = 0
    isVolumeOn = WorkingOptions.isVolumeOn
    if (isVolumeOn): 
        isVolumeOnColor = (62,222,33) 
    else: 
        isVolumeOnColor = (255,0,0)
    volumeList = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] 
    try:
        volumeListPos = volumeList.index(100 * WorkingOptions.volume)
    except:
        volumeListPos = 10

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = event.pos
                    if(backarrowRect.collidepoint(mousePos)):
                        running = False
                    if(leftarrowRECT1.collidepoint(mousePos)):
                        #left arrow 1 (professor)
                        if PlayerListPos == 0:
                            PlayerListPos = (len(List_of_Players) - 1)
                        else:
                            PlayerListPos -= 1
                    if(rightarrowRECT1.collidepoint(mousePos)):
                        #right arrow 1 (professor)
                        if PlayerListPos == (len(List_of_Players) - 1):
                            PlayerListPos = 0
                        else:
                            PlayerListPos += 1
                    if(leftarrowRECT2.collidepoint(mousePos)):
                        #left arrow 2 (volume)
                        if volumeListPos == 0:
                            volumeListPos = (len(volumeList) - 1)
                        else:
                            volumeListPos -= 1
                    if(rightarrowRECT2.collidepoint(mousePos)):
                        #right arrow 2 (volume)
                        if volumeListPos == (len(volumeList) - 1):
                            volumeListPos = 0
                        else:
                            volumeListPos += 1
                    if(pygame.Rect(350, 525, 100, 50).collidepoint(mousePos)):
                        #Save button
                        WorkingOptions.setActivePlayer(List_of_Players[PlayerListPos])
                        WorkingOptions.isVolumeOn = isVolumeOn
                        WorkingOptions.volume = (volumeList[volumeListPos] / 100)
                        WorkingOptions.save()
                    if(pygame.Rect(275, 425, 250, 50).collidepoint(mousePos)):
                        #Toggle volume buttonn
                        if isVolumeOn:
                            isVolumeOn = False
                        else:
                            isVolumeOn = True
                        if (isVolumeOn): 
                            isVolumeOnColor = (62,222,33) 
                        else: 
                            isVolumeOnColor = (255,0,0)

        screen.fill((0,0,0))
        screen.blit(mmbackground, (0,0))

        #back arrow
        screen.blit(backarrow,(25,25))

        #MainMenu Text & Box 
        pygame.draw.rect(screen, (23, 136, 235), pygame.Rect(270, 90, 260, 60))
        pygame.draw.rect(screen, (237, 237, 237), pygame.Rect(275, 95, 250, 50))
        draw_text('Options', font, (255, 0, 0), screen, 330, 105)
        
        #Professor control... Outer box, inner box, text
        #option 1 presents list of players
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(245, 220, 310, 60))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(250, 225, 300, 50))
        draw_text(str(List_of_Players[PlayerListPos]), font, (255,255,255), screen, 262, 235)
        #option 1 left and right arrows
        screen.blit(leftarrow, (Larrowx1, arrowy1))
        screen.blit(rightarrow, (Rarrowx1, arrowy1))

        #Professor control... Outer box, inner box, text
        #option 1 presents list of players
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(270, 320, 260, 60))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(275, 325, 250, 50))
        draw_text("Sound "+str(volumeList[volumeListPos])+"%", font, (255,255,255), screen, 305, 335)
        #option 1 left and right arrows
        screen.blit(leftarrow, (Larrowx2, arrowy2))
        screen.blit(rightarrow, (Rarrowx2, arrowy2))

        #Sound toggle control
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(270, 420, 260, 60))
        pygame.draw.rect(screen, isVolumeOnColor, pygame.Rect(275, 425, 250, 50))
        draw_text('Toggle Sound', font, (255,255,255), screen, 280, 435)

        #Save button
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(345, 520, 110, 60))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(350, 525, 100, 50))
        draw_text("Save", font, (255,255,255), screen, 362, 535)


        pygame.display.update()

main_menu()