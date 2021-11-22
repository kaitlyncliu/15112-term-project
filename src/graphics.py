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
ghost = Ghost("ghost",250)

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

def appStarted(app):
    # map/general game mechanic variables
    app.count = 0
    app.timerDelay = 70
    app.map = fakeMap
    app.curRoom = (5,2)
    app.curRoomCX = app.width/2
    app.curRoomCY = app.height/2
    app.newRoom = 0

    # character variables
    app.charX = app.width//2
    app.charY = app.height//2
    app.direction = "left"
    app.charSpriteCounter = 0
    app.isMoving = False
    app.movingRight = False
    app.movingLeft = False
    app.movingUp = False
    app.movingDown = False
    app.curProjStrength = 0
    app.charProj = []
    initImages(app)
    app.charHP = 5

    # mobs
    app.mobs = [dragon,ghost]
    for mob in app.mobs:
        mobImageInit(mob,app)

# IMAGE CITATION: 
# character sprite: https://www.pngegg.com/en/png-nehup
# stone background: I made this, but I used a stone brick texture -
# (https://pahiroarts.artstation.com/projects/n3n5o) - and edited it
# poop: https://www.artstation.com/artwork/Yea8bb
def initImages(app):
    # background --
    app.bgImage = app.loadImage('stoneBG.png')
    app.bgImage = app.bgImage.resize((app.width,app.height))
    app.bgWidth,app.bgHeight = app.bgImage.size
    # character projectiles --
    app.poopImage = app.loadImage('poop.png')
    app.poopImage = app.scaleImage(app.poopImage,.5)
    app.poopRad = app.poopImage.size[0]/2
    # character
    app.charSprite = app.loadImage('charSprite.png')
    app.charSprite = app.scaleImage(app.charSprite,.1)
    app.charSpriteWidth, app.charSpriteHeight = app.charSprite.size
    app.sprites = dict()
    # Lives
    app.life = app.loadImage('Heart.png')
    app.life = app.scaleImage(app.life,2)
    app.lifeWidth, app.lifeHeight = app.life.size
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
    app.charWidth, app.charHeight = app.sprites["left"][0].size


# IMAGE CITATION: mob sprites from: https://analogstudios.itch.io/dungeonsprites
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
    mob.width,mob.height = mob.sprites["idle"][0].size


def redrawAll(app,canvas):
    # --background
    canvas.create_image(app.curRoomCX,app.curRoomCY,image = 
                        ImageTk.PhotoImage(app.bgImage))
    # --character
    spriteImage = app.sprites[app.direction][app.charSpriteCounter]
    if app.charHP > 0:
        canvas.create_image(app.charX, app.charY, image = ImageTk.PhotoImage(spriteImage))
    # draw projectiles the character has shot
    for proj in app.charProj:
        canvas.create_image(proj.cx, proj.cy, image = ImageTk.PhotoImage(app.poopImage))
    # --mobs
    for mob in app.mobs:
        mobSprite = mob.sprites[mob.type][mob.spriteCounter]
        canvas.create_image(mob.cx, mob.cy, image = ImageTk.PhotoImage(mobSprite))
        for proj in mob.proj:
            canvas.create_oval(proj.cx-6,proj.cy-6,proj.cx+6,proj.cy+6, fill = "white")
    # screen for room switch
    if app.newRoom > 0:
        canvas.create_rectangle(0,0,app.width,app.height, fill = "black")
    for i in range(app.charHP):
        x0 = 20 + i*(app.lifeWidth + 10)
        y0 = 20
        x1 = 20 + (i+1)*(app.lifeWidth + 10)
        y1 = app.lifeHeight
        canvas.create_image((x0+x1)/2,(y0+y1)/2, image = ImageTk.PhotoImage(app.life))

def timerFired(app):
    app.count += 1
    if app.newRoom > 0:
        app.newRoom -= 1
    if app.isMoving:
        app.charSpriteCounter = (app.charSpriteCounter + 1) % 4
        moveChar(app,15)
    i = 0
    while i < len(app.charProj):
        proj = app.charProj[i]
        proj.time += 1
        proj.move(app)
        if proj.cx < 50 or proj.cx > app.width-50 or proj.cy < 50 or proj.cy > app.height-50:
            app.charProj.pop(i)
        else:
            i += 1
    for mob in app.mobs:
        mob.spriteCounter = (mob.spriteCounter + 1) % 8
        mob.move(app,7)
        # slows down mob atks
        if app.count % 10 == 0:
            mob.atk(app,10)
            if ((mob.cx) >= (app.charX - app.charWidth/2) and
                (mob.cx) <= (app.charX + app.charWidth/2) and
                (mob.cy) >= (app.charY - app.charHeight/2) and
                (mob.cy) >= (app.charY + app.charHeight/2)):
                app.charHP -= 1
        k = 0
        while k < len(mob.proj):
            proj = mob.proj[k]
            proj.move()
            # the projectiles hit the character
            if ((proj.cx + 5) >= (app.charX - app.charWidth/2) and 
                (proj.cx + 5) <= (app.charX + app.charWidth/2) and
                (proj.cy + 5) >= (app.charY - app.charHeight/2) and
                (proj.cy + 5) <= (app.charY + app.charHeight/2)):
                mob.proj.pop(k)
                app.charHP -= 1
            else:
                k += 1
        j = 0
        while j < len(app.charProj):
            proj = app.charProj[j]
            if ((proj.cx + app.poopRad) >= (mob.cx - mob.width/2) and 
                (proj.cx + app.poopRad) <= (mob.cx + mob.width/2) and
                (proj.cy + app.poopRad) >= (mob.cy - mob.height/2) and
                (proj.cy + app.poopRad) <= (mob.cy + mob.height/2)):
                mob.gotHit(proj.strength*25)
                app.charProj.pop(j)
            else:
                j += 1
        h = 0
        while h < len(app.mobs):
            if app.mobs[h].type == "death":
                app.mobs.pop(h)
            else:
                h += 1
    if app.curProjStrength < 20:
        app.curProjStrength += 1

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
    else:
        if newX > rightWall and app.curRoom[1] + 1 < len(app.map[0]):
            app.charX = 1 * app.width/12 + 1
            app.bgImage = app.loadImage(app.map[app.curRoom[0]][app.curRoom[1]+1].background)
        elif newX < leftWall and app.curRoom[1] - 1 >= 0:
            app.charX = 11 * app.width/12 - 1
            app.bgImage = app.loadImage(app.map[app.curRoom[0]][app.curRoom[1]-1].background)
        elif newY < topWall and app.curRoom[0] - 1 >= 0:
            app.charY = 7 * app.height/8 - 1
            app.bgImage = app.loadImage(app.map[app.curRoom[0]-1][app.curRoom[1]].background)
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
    elif event.key == "r":
        app.charHP = 5
    # None of the movement keys are being pressed
    if (app.movingRight == False and app.movingLeft == False and 
        app.movingUp == False and app.movingDown == False):
        app.isMoving = False

def mousePressed(app,event):
    app.curProjStrength = 0

def mouseReleased(app,event):
    app.charProj.append(Projectile(app.curProjStrength, app.charX, app.charY))
    newProj = app.charProj[-1]
    difX = event.x - newProj.cx
    difY = event.y - newProj.cy
    newProj.angle = math.atan2(difY,difX)
    newProj.vx = 8*newProj.strength*math.cos(newProj.angle)
    newProj.vy = 8*newProj.strength*math.sin(newProj.angle)

runApp(width = 1000, height = 500)
