'''

Ribbert's Ribbeting Adventure
by Kaitlyn Liu
andrewID : kaitlynl

'''

#####################################################
# Import stuff here
import math
import random
import copy
from cmu_112_graphics import *
#from mapGenerator import *
from mobAI import *
from mobAI import *


################################################
# My code

class DungeonRoom(object):
    # can potentially add rounds of mobs
    def __init__(self,mobs,loot,walls):
        self.initialMobs = mobs
        self.liveMobs = mobs
        self.background = None
        self.loot = loot
        self.layout = None
        self.walls = walls
    
    def mobSlain(self,mob):
        self.liveMobs.remove(mob)
    

class BossRoom(DungeonRoom):
    def bossSlain(self):
        pass


spawnRoom = DungeonRoom(None,None,(1,1,0,1))
spawnRoom.background = 'https://tinyurl.com/xkfjz8zr'

potionRoom = DungeonRoom(None,None,(1,1,1,1))

leftBossRoom = BossRoom("Boss","bossLoot",(0,1,0,0))

rightBossRoom = BossRoom("Boss","bossLoot",(0,0,0,1))
testRoom = DungeonRoom(None,None,(1,1,0,1))
testRoom.background = "stoneBG.png"


shopRoom1 = DungeonRoom(None,None,(0,1,0,0))
shopRoom2 = DungeonRoom(None,None,(0,1,0,0))

##############################################
# Enemies
dragon = Mob("dragon",500)


###############################################
# Graphics stuff

# CITATION: sprite code based on class notes and Image/PIL TA Mini-Lecture
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

fakeMap = [[leftBossRoom, None, None,       None, shopRoom2],
              [None,          None, None,       None, None],
              [None,          None, potionRoom, None, None],
              [None,          None, None,       None, None],
              [None,          None, testRoom,       None, None],
              [None,          testRoom, testRoom,  testRoom, None]]

def mobImageInit(mob,app):
    mob.sprite = app.loadImage(f'{mob.name}_.png')
    mob.sprite = app.scaleImage(mob.sprite,5)
    mob.spriteWidth, mob.spriteHeight = mob.sprite.size
    mob.sprites = dict()
    for dir in ["idle0", "walk1", "run3", "jump4", "turn5", "hurt6", "death7"]:
        index = int(dir[-1:])
        newDir = dir[:-1]
        topLeftY = index * mob.spriteHeight / 7
        botRightY = (index + 1) * mob.spriteHeight / 7
        tempSprites = []
        for i in range(8):
            topLeftX = mob.spriteWidth * i / 8
            botRightX = mob.spriteWidth * (i+1) / 8
            sprite = mob.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
            tempSprites.append(sprite)
        mob.sprites[newDir] = tempSprites



def appStarted(app):
    app.map = fakeMap
    app.curRoom = (5,2)
    app.charX = app.width//2
    app.timerDelay = 50
    app.charY = app.height//2
    app.direction = "left"
    app.charSpriteCounter = 0
    app.isMoving = False
    app.movingRight = False
    app.movingLeft = False
    app.movingUp = False
    app.movingDown = False
    app.curRoomCX = app.width/2
    app.curRoomCY = app.height/2
    app.newRoom = 0
    initImages(app)
    app.mobs = [dragon]
    for mob in app.mobs:
        mobImageInit(mob,app)

def redrawAll(app,canvas):
    canvas.create_image(app.curRoomCX,app.curRoomCY,image = 
                        ImageTk.PhotoImage(app.bgImage))
    spriteImage = app.sprites[app.direction][app.charSpriteCounter]
    canvas.create_image(app.charX,app.charY,image = ImageTk.PhotoImage(spriteImage))
    for mob in app.mobs:
        mobSprite = mob.sprites[mob.type][mob.spriteCounter]
        canvas.create_image(mob.cx,mob.cy,image = ImageTk.PhotoImage(mobSprite))
    if app.newRoom > 0:
        canvas.create_rectangle(0,0,app.width,app.height, fill = "black")





# IMAGE CITATION: 
# character sprite: https://www.pngegg.com/en/png-nehup
# stone background: I made this, but I used a stone brick texture -
# (https://pahiroarts.artstation.com/projects/n3n5o) - and edited it
def initImages(app):
    app.bgImage = app.loadImage('stoneBG.png')
    app.bgImage = app.bgImage.resize((app.width,app.height))
    app.bgWidth,app.bgHeight = app.bgImage.size
    app.charSprite = app.loadImage('charSprite.png')
    app.charSprite = app.scaleImage(app.charSprite,.1)
    app.charSpriteWidth, app.charSpriteHeight = app.charSprite.size
    app.sprites = dict()
    for dir in ["down0","right1","left2","up3"]:
        index = int(dir[-1:])
        newDir = dir[:-1]
        topLeftY = index * app.charSpriteHeight / 4
        botRightY = (index + 1) * app.charSpriteHeight / 4
        tempSprites = []
        for i in range(4):
            topLeftX = app.charSpriteWidth * i / 4
            botRightX = app.charSpriteWidth * (i+1) / 4
            sprite = app.charSprite.crop((topLeftX,topLeftY,botRightX,botRightY))
            tempSprites.append(sprite)
        app.sprites[newDir] = tempSprites

def timerFired(app):
    if app.newRoom > 0:
        app.newRoom -= 1
    if app.isMoving:
        app.charSpriteCounter = (app.charSpriteCounter + 1) % 4
        moveChar(app,15)
    for mob in app.mobs:
        mob.spriteCounter = (mob.spriteCounter + 1) % 8

def moveChar(app,amount):
    leftWall = app.width/12
    rightWall = 11 * app.width/12
    topWall = app.height/8
    botWall = 7 * app.height/8
    # accounts for diagonal motion needing to move less
    if ((app.movingRight or app.movingLeft) and (app.movingUp or app.movingDown)):
        amount = amount / math.sqrt(2)
    changeX = amount * app.movingRight - amount * app.movingLeft
    changeY = amount * app.movingDown - amount * app.movingUp
    newX = app.charX + changeX
    newY = app.charY + changeY
    # only move if in bounds
    if (newX <= rightWall and newX >= leftWall and 
        newY >= topWall and newY <= botWall):
        app.charX = newX
        app.charY = newY
    elif newX > rightWall and app.curRoom[1] + 1 < len(app.map[0]):
        app.charX = 1 * app.width/12 + 1
        app.bgImage = app.loadImage(app.map[app.curRoom[0]][app.curRoom[1]+1].background)
        app.newRoom = 10
        app.isMoving = False
    elif newX < leftWall and app.curRoom[1] - 1 >= 0:
        app.charX = 11 * app.width/12 - 1
        app.bgImage = app.loadImage(app.map[app.curRoom[0]][app.curRoom[1]-1].background)
        app.newRoom = 10
        app.isMoving = False
    elif newY < topWall and app.curRoom[0] - 1 >= 0:
        app.charY = 7 * app.height/8 - 1
        app.bgImage = app.loadImage(app.map[app.curRoom[0]-1][app.curRoom[1]].background)
        app.newRoom = 10
        app.isMoving = False
    elif newY > botWall and app.curRoom[0] + 1 < len(app.map):
        app.charY = app.height/8 + 1
        app.bgImage = app.loadImage(app.map[app.curRoom[0]+1][app.curRoom[1]].background)
        app.newRoom = 10
        app.isMoving = False
        
            
# allows the character to move diagonally and not just in a straight line
def keyPressed(app,event):
    app.isMoving = True
    if event.key == "d":
        app.direction = "right"
        app.movingRight = True
    elif event.key == "a":
        app.direction = "left"
        app.movingLeft = True
    elif event.key == "w":
        app.direction = "up"
        app.movingUp = True
    elif event.key == "s":
        app.direction = "down"
        app.movingDown = True

def keyReleased(app,event):
    if event.key == "d":
        app.movingRight = False
    elif event.key == "a":
        app.movingLeft = False
    elif event.key == "w":
        app.movingUp = False
    elif event.key == "s":
        app.movingDown = False
    # None of the movement keys are being pressed
    if (app.movingRight == False and app.movingLeft == False and 
        app.movingUp == False and app.movingDown == False):
        app.isMoving = False

runApp(width = 1000, height = 500)
