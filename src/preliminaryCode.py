'''

TotallyUniqueDungeonGame
by Kaitlyn Liu
andrewID : kaitlynl

'''

#####################################################
# Import stuff here
import math
import random
import copy
from dataclasses import make_dataclass
from cmu_112_graphics import *


################################################
# My code

#
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

class Mob(object):
    def __init__(self,health):
        self.health = health

    def gotHit(self,dmg):
        self.health -= dmg

class Boss(Mob):
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

# 1 represents open door, 0 represents closed door
# room templates will be represented by (north, east, south, west)
# will make rooms into a class later
#  1
# 1 0
#  0
room1 = (1, 0, 0, 1)
#  1
# 1 1
#  1
room2 = (1, 1, 1, 1)
#  0
# 1 1
#  1
room3 = (0, 1, 1, 1)
#  1
# 0 0
#  0
room4 = (1, 0, 0, 0)
#  0
# 1 0
#  1
room5 = (0, 0, 1, 1)
#  0
# 1 1
#  0
room6 = (0, 1, 0, 1)
#  0
# 0 1
#  1
room7 = (0, 1, 1, 0)
#  1
# 0 1
#  0
room8 = (1, 1, 0, 0)

roomList = [room1,room2,room3,room4,room5,room6,room7,room8]

# checks to see if a new room is valid based on current dungeon map
def checkValidRoom(map, row, col, room):
    # there is already a room at the location or the room is out of bounds
    if (row >= len(map) or row < 0 or col >= len(map[0]) or col < 0
        or map[row][col] != None):
        return False
    dirs = [(-1,0),(0,1),(1,0),(0,-1)]
    # s of room above must be open if north of current room is open
    # w of room to the right open if e of current room is open
    # n of room below must be open if s current room open
    # e of room to the left open if w of current room is open
    # index + 2 to get the room that should be open
    for i in range(len(room)):
        connectingRoom = map[row+dirs[i][0]][col+dirs[i][1]]
        # room is empty, do nothing
        if connectingRoom == None:
            continue
        connectingRoomSide = connectingRoom[(i+2)%len(room)]
        if connectingRoomSide != room[i]:
            return False
    return True

defaultMap1 = [[leftBossRoom, None, None,       None, shopRoom2],
              [None,          None, None,       None, None],
              [None,          None, potionRoom, None, None],
              [None,          None, None,       None, None],
              [None,          None, None,       None, None],
              [None,          None, spawnRoom,  None, None]]


defaultMap2 = [ [shopRoom2,  None, None,       None, rightBossRoom],
                [None,       None, None,       None, None],
                [None,       None, potionRoom, None, None],
                [None,       None, None,       None, None],
                [None,       None, None,       None, None],
                [None,       None, spawnRoom,  None, None]    ]

mapsList = [defaultMap1,defaultMap2]

# this is incomplete but will keep placing rooms until the map is walkable and 
# the board is at least 75% full 
def makeFloor(map):
    map = copy.deepcopy(mapsList[random.randint(0,len(mapsList)-1)])
    # can successfully make it from the boss room to the spawn room
    # may or may not be possible to make it to potion room on each floor
    if map == defaultMap1:
        startRow = 0
        startCol = 0
    else:
        startRow = 0
        startCol = 4
    if walkable(map,startRow,startCol,(5,2)):
        return map
    else:
        for i in range(len(map)):
            for j in range(len(map[0])):
                randomRoom = roomList[random.randint(0,len(roomList)-1)]
                if checkValidRoom(map,i,j,randomRoom):
                    map[i][j] == randomRoom

# backtracker that checks if a path from the boss room to the spawn 
# exists on the map
def walkable(map, row, col, tgt):
    if (row,col) == tgt:
        return True
    else:
        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        for i in range(dirs):
            dir = dirs[i]
            newRow = row + dir[0]
            newCol = col + dir[1]
            if (newRow < len(map) and newRow >= 0 and newCol < len(map[0])
                and newCol >=0 and map[newRow][newCol] != None):
                result = walkable(map,newRow,newCol,tgt)
                if result != False:
                    return True
        return False




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
    app.map = fakeMap
    app.curRoom = (5,2)
    app.charX = app.width//2
    app.timerDelay = 40
    app.charY = app.height//2
    app.direction = "left"
    app.spriteCounter = 0
    app.isMoving = False
    app.movingRight = False
    app.movingLeft = False
    app.movingUp = False
    app.movingDown = False
    app.curRoomCX = app.width/2
    app.curRoomCY = app.height/2
    app.newRoom = 0
    initImages(app)

def redrawAll(app,canvas):
    canvas.create_image(app.curRoomCX,app.curRoomCY,image = 
                        ImageTk.PhotoImage(app.bgImage))
    spriteImage = app.sprites[app.direction][app.spriteCounter]
    canvas.create_image(app.charX,app.charY,image = ImageTk.PhotoImage(spriteImage))
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
        app.spriteCounter = (app.spriteCounter + 1) % 4
        moveChar(app,10)
    else:
        app.spriteCounter = 0

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
###############################################
# Test Functions

def testCheckValidRoom():
    print("Testing checkValidRoom...", end=" ")
    testMap = [[room7,room5,room7,room4],
               [room8,None,None,None],
               [None,None,None,None],
               [None,None,None,None]]

    assert(checkValidRoom(testMap, 0, 2, room3) == False)
    assert(checkValidRoom(testMap, 1, 1, room1) == True)
    assert(checkValidRoom(testMap, 0, 0, room1) == False)
    print("Passed!")

#################################################
testCheckValidRoom()