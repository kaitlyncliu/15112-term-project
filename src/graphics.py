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
from mapGenerator import *
from mobAI import *
from bossAI import *
from items import *

##############################################

def initRooms(app):
    app.roomsList = []
    app.globalMobs = []
    # spawnRoom
    app.spawnRoom = DungeonRoom("spawnRoom")
    app.spawnRoom.obsLocations[(0,0)] = app.rockImage
    app.spawnRoom.obsLocations[(8,0)] = app.rockImage
    app.spawnRoom.obsLocations[(0,3)] = app.rockImage
    app.spawnRoom.obsLocations[(8,3)] = app.rockImage
    app.spawnRoom.obsLocations[(4,1)] = app.closedChest
    app.spawnRoom.items = [Bomb(200,150)]
    
    # regular mob room
    room1 = DungeonRoom("room1")
    room1.obsLocations[(4,1)] = app.rockImage
    room1.obsLocations[(5,1)] = app.rockImage
    room1.obsLocations[(3,2)] = app.rockImage
    room1.obsLocations[(4,2)] = app.rockImage
    room1.obsLocations[(7,0)] = app.rockImage
    room1.obsLocations[(7,1)] = app.rockImage
    room1.obsLocations[(7,2)] = app.rockImage
    room1.obsLocations[(1,1)] = app.rockImage
    room1.obsLocations[(1,2)] = app.rockImage
    room1.obsLocations[(1,3)] = app.rockImage
    room1.mobs = [Ghost(425,375),Ghost(575,125)]
    room1.items = [Bomb(110,400),Bomb(840,100)]
    for mob in room1.mobs:
        app.globalMobs.append(mob)
    room1.map = [[0,0,0,0,0,0,0,1,0],
                 [0,1,0,0,1,1,0,1,0],
                 [0,1,0,1,1,0,0,1,0],
                 [0,1,0,0,0,0,0,0,0],]
    app.roomsList.append(room1)

    room2 = DungeonRoom("room2")
    room2.mobs = [Dragon(500,200),Dragon(500,300),Ghost(500,250)]
    for mob in room2.mobs:
        app.globalMobs.append(mob)
    room2Obs = [((1,0),app.rockImage),((1,3),app.rockImage),((7,0),app.rockImage),((7,3),app.rockImage),((3,0),app.rockImage),((3,1),app.rockImage),((3,2),app.rockImage),((5,1),app.rockImage),((5,2),app.rockImage),((5,3),app.rockImage)]
    room2.obsLocations = dict(room2Obs)
    room2.map = [[0,1,0,1,0,0,0,1,0],
                 [0,0,0,1,0,1,0,0,0],
                 [0,0,0,1,0,1,0,0,0],
                 [0,1,0,0,0,1,0,1,0],]
    app.roomsList.append(room2)

    # treasureRoom
    app.treasureRoom = DungeonRoom("treasureRoom")
    app.treasureRoom.obsLocations[(4,1)] = app.closedChest
    app.treasureRoom.mobs = [Dragon(425,250),Dragon(575,250)]
    app.treasureRoom.map = [[0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,1,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],]
    for mob in app.treasureRoom.mobs:
        app.globalMobs.append(mob)

    # bossRoom
    app.bossRoom = DungeonRoom("bossRoom")
    bosses = [Golem(),Reaper()]
    app.bossRoom.mobs = [bosses[random.randint(0,1)]]
    for mob in app.bossRoom.mobs:
        app.globalMobs.append(mob)
    
    # shopRoom 
    app.shopRoom = DungeonRoom("shopRoom")

    # secretRoom
    app.secretRoom = DungeonRoom("secretRoom")
    app.secretRoomObs = [((4,1),app.closedChest)]
    app.secretRoom.obsLocations = dict(room2Obs)
    app.secretRoom.map = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,1,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],]

    
    # superSecretRoom
    app.superSecretRoom = DungeonRoom("superSecretRoom")
    app.secretRoomObs = [((4,1),app.closedChest)]
    app.secretRoom.obsLocations = dict(room2Obs)
    app.superSecretRoom.map = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,1,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],]


def fillRooms(app):
    rows = len(app.map)
    cols = len(app.map[0])
    centRow = rows//2
    centCol = cols//2
    app.map[centRow][centCol] = app.spawnRoom
    for row in range(rows):
        for col in range(cols):
            if app.map[row][col] == 1:
                randomRoom = random.randint(0,len(app.roomsList)-1)
                app.map[row][col] = copy.deepcopy(app.roomsList[randomRoom])
            elif app.map[row][col] == "bossRoom":
                app.map[row][col] = app.bossRoom
            elif app.map[row][col] == "shopRoom":
                app.map[row][col] = app.shopRoom
            elif app.map[row][col] == "treasureRoom":
                app.map[row][col] = app.treasureRoom
            elif app.map[row][col] == "secretRoom":
                app.map[row][col] = app.secretRoom
            elif app.map[row][col] == "superSecretRoom":
                app.map[row][col] == app.superSecretRoom

###############################################
# Graphics stuff


def appStarted(app):
    # map/general game mechanic variables
    app.count = 0
    app.paused = True
    app.timerDelay = 100
    app.level = 1
    app.targetRooms = getTargetRooms(app.level)
    app.map = startMakeRooms(app.targetRooms)
    app.win = False
    app.lose = False
    app.start = 0
    app.changeRoom = False
    app.help = False
    app.secretFound = None
    app.holeLoc = None
    app.dagger = True
    app.daggerWield = False

    # fill normal rooms with different room templates
    app.curRoom = (3,3)
    app.curRoomCX = app.width/2
    app.curRoomCY = app.height/2
    app.newRoom = 0
    initObstacles(app)
    initRooms(app)
    fillRooms(app)
    print(app.map)
    app.roomType = app.map[app.curRoom[0]][app.curRoom[1]]
    app.items = app.roomType.items
    app.bombs = []

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
    app.charBombs = 10
    app.charStrength = 20

    # mobs
    app.mobs = app.roomType.mobs
    for mob in app.globalMobs:
        mob.imageInit(app)
    for item in app.items:
        item.initImages(app)





# CITATION: sprite code based on class notes and Image/PIL TA Mini-Lecture
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# IMAGE CITATION: 
# lose image: https://d2skuhm0vrry40.cloudfront.net/2020/articles/2020-05-29-11-37/five-of-the-best-game-over-screens-1590748640300.jpg/EG11/resize/1200x-1/five-of-the-best-game-over-screens-1590748640300.jpg
# win image: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fvector%2Fpixel-art-8-bit-you-win-text-with-one-big-winner-golden-cup-on-black-background-gm1268272324-372239700&psig=AOvVaw2oeNDWuEqEaGBcL3PGYXNa&ust=1637796805682000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCOCjodjSr_QCFQAAAAAdAAAAABAD
# character sprite: https://www.pngegg.com/en/png-nehup
# stone background: I made this, but I used a stone brick texture -
# (https://pahiroarts.artstation.com/projects/n3n5o) - and edited it
# poop: https://www.artstation.com/artwork/Yea8bb
# start screen: text created by me, but background from here: https://lil-cthulhu.itch.io/pixel-art-mushroom-cave-background
# pause screen: same as start screen
# loading screen: same as start screen
# bomb: https://www.vectorstock.com/royalty-free-vector/black-bomb-pixel-art-colorful-vector-21005227
def initImages(app):
    # backgrounds and screens --
    app.winImage = app.loadImage("youWin.jpg")
    app.winImage = app.scaleImage(app.winImage,2)
    app.loseImage = app.loadImage("youLose.jpg")
    app.loseImage = app.scaleImage(app.loseImage,0.5)
    app.startImage = app.loadImage("startScreen.png")
    app.pauseImage = app.loadImage("pauseImage.png")
    app.loadingImage = app.loadImage("loadingImage.png")
    app.helpImage = app.loadImage("helpMenu.png")
    app.bgImage = app.loadImage('stoneBG.png')
    app.bgImage = app.bgImage.resize((app.width,app.height))
    app.bgWidth,app.bgHeight = app.bgImage.size
    app.holeImage = app.loadImage("ExplosionHole.png")

    # character projectiles --
    app.poopImage = app.loadImage('poop.png')
    app.poopImage = app.scaleImage(app.poopImage,.5)
    app.poopRad = app.poopImage.size[0]/2
    app.daggerImage = app.loadImage("sword.png")
    app.daggerImage = app.scaleImage(app.daggerImage,0.25)

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

# pixels where floor starts: x: 14*5, y: 16*5

def redrawAll(app,canvas):
    # --background
    canvas.create_image(app.curRoomCX,app.curRoomCY,image = 
                        ImageTk.PhotoImage(app.bgImage))
    # temporary grid to check obstacle placement
    for p in range(4):
        for q in range(9):
            x0 = 70+95*q
            y0 = 80+95*p
            x1 = x0 + 95
            y1 = y0 + 95
            canvas.create_rectangle(x0,y0,x1,y1)
    for obsLoc in app.roomType.obsLocations:
        canvas.create_image((obsLoc[0]+0.5)*95+70,(obsLoc[1]+0.5)*95+80,image = ImageTk.PhotoImage(app.roomType.obsLocations[obsLoc]))
    # doors:
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    for dir in dirs:
        newRow = app.curRoom[0] + dir[0]
        newCol = app.curRoom[1] + dir[1]
        if inBounds(app.map,newRow,newCol) and app.map[newRow][newCol] != 0 and app.map[newRow][newCol]!= "secretRoom":
            if dir == (-1,0):
                canvas.create_rectangle(app.width/2-30,0,app.width/2+30,80, fill = "black")
            elif dir == (1,0):
                canvas.create_rectangle(app.width/2-30,app.height-40,app.width/2+30,app.height, fill = "black")
            elif dir == (0,-1):
                canvas.create_rectangle(0,app.height/2-30,70,app.height/2+30, fill = "black")
            elif dir == (0,1):
                canvas.create_rectangle(app.width-75,app.height/2-30,app.width,app.height/2+30, fill = "black")
    
    # items
    for bomb in app.bombs:
        canvas.create_image(bomb.cx,bomb.cy,image = ImageTk.PhotoImage(bomb.image))
    if app.holeLoc != None and app.secretFound == app.curRoom:
        if app.holeLoc == "top":
            canvas.create_image(app.width/2,30,image = ImageTk.PhotoImage(app.holeImage))
        elif app.holeLoc == "bottom":
            image = app.holeImage.transpose(Image.ROTATE_180)
            canvas.create_image(app.width/2,470,image = ImageTk.PhotoImage(image))
        elif app.holeLoc == "left":
            image = app.holeImage.transpose(Image.ROTATE_90)
            canvas.create_image(30,app.height/2,image = ImageTk.PhotoImage(image))
        elif app.holeLoc == "right":
            image = app.holeImage.transpose(Image.ROTATE_270)
            canvas.create_image(970,app.height/2,image = ImageTk.PhotoImage(image))
    for item in app.items:
        canvas.create_image(item.cx,item.cy,image = ImageTk.PhotoImage(item.image))

    # --character
    spriteImage = app.sprites[app.direction][app.charSpriteCounter]
    if app.charHP > 0:
        canvas.create_image(app.charX, app.charY, image = ImageTk.PhotoImage(spriteImage))
    for i in range(app.charHP):
        x0 = 20 + i*(app.lifeWidth + 10)
        y0 = 20
        x1 = 20 + (i+1)*(app.lifeWidth + 10)
        y1 = app.lifeHeight
        canvas.create_image((x0+x1)/2,(y0+y1)/2, image = ImageTk.PhotoImage(app.life))
    # bombs:
    canvas.create_text(40,70,anchor = W,text = f"Bombs: {app.charBombs}", fill = "white", font = "Helvetica 12")
    # draw projectiles the character has shot
    for proj in app.charProj:
        canvas.create_image(proj.cx, proj.cy, image = ImageTk.PhotoImage(app.poopImage))
    if app.daggerWield:
        daggerImage = app.daggerImage.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(app.charX+20,app.charY,image = ImageTk.PhotoImage(daggerImage))


    # --mobs
    for mob in app.mobs:
        mobSprite = mob.sprites[mob.type][mob.spriteCounter]
        canvas.create_image(mob.cx, mob.cy, image = ImageTk.PhotoImage(mobSprite))
        for proj in mob.proj:
            if isinstance(mob,Ghost):
                canvas.create_oval(proj.cx-6,proj.cy-6,proj.cx+6,proj.cy+6, fill = "white")
            else:
                image = proj.image
                if proj.reflect == True:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                canvas.create_image(proj.cx,proj.cy,image = ImageTk.PhotoImage(image))
        if isinstance(mob,Boss):
            for minion in mob.minionList:
                minionSprite = minion.sprites["walk"][minion.spriteCounter]
                canvas.create_image(minion.cx,minion.cy,image = ImageTk.PhotoImage(minionSprite))
            canvas.create_rectangle(app.width-300,25,app.width-50,50,fill ="white")
            canvas.create_rectangle(app.width-295,30,app.width-295+240*(mob.health/mob.initHealth),45,fill = "OrangeRed3")
            canvas.create_text(app.width-290,38,anchor = W,text = f"Boss HP:{mob.health}/{mob.initHealth}", fill = "black",font = "Helvetica 8")
    
    # screens
    if app.newRoom > 0:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.loadingImage))
    if app.paused == True:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.pauseImage))
    if app.win == True:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.winImage))
    '''if app.lose == True:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.loseImage))'''
    if app.start == 0:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.startImage))
    if app.help == True:
        canvas.create_image(app.curRoomCX,app.curRoomCY,image = ImageTk.PhotoImage(app.helpImage))
    


def timerFired(app):
    if app.paused == False:
        app.count += 1
        m = 0
        while m < len(app.bombs):
            bomb = app.bombs[m]
            bomb.timer += 1
            if bomb.timer >= 10:
                bomb.explode(app)
                app.bombs.pop(m)
        if app.newRoom > 0:
            app.newRoom -= 1
        if app.isMoving:
            app.charSpriteCounter = (app.charSpriteCounter + 1) % 4
            moveChar(app,15)
        i = 0
        while i < len(app.charProj):
            proj = app.charProj[i]
            proj.spriteCounter = int((proj.spriteCounter + 1) % 6)
            proj.time += 1
            proj.move(app)
            if proj.cx < 50 or proj.cx > app.width-50 or proj.cy < 50 or proj.cy > app.height-50:
                app.charProj.pop(i)
            else:
                i += 1
        for mob in app.mobs:
            mob.spriteCounter = int((mob.spriteCounter + 1) % mob.totalSprites)
            if not isinstance(mob,Boss):
                mob.move(app,5)
                # slows down mob atks
                if app.count % 20 == 0:
                    mob.atk(app,10)
                    # the mob is attacking the player - melee
                    if ((mob.cx) >= (app.charX - app.charWidth/2) and
                        (mob.cx) <= (app.charX + app.charWidth/2) and
                        (mob.cy) >= (app.charY - app.charHeight/2) and
                        (mob.cy) >= (app.charY + app.charHeight/2)):
                        app.charHP -= 1
                        if app.charHP <= 0:
                            app.lose = True
                            app.paused = True
            k = 0
            while k < len(mob.proj):
                proj = mob.proj[k]
                oldX = proj.cx
                proj.move()
                if oldX > proj.cx:
                    proj.reflect = True
                # the projectiles hit the character
                if ((proj.cx + 5) >= (app.charX - app.charWidth/2) and 
                    (proj.cx + 5) <= (app.charX + app.charWidth/2) and
                    (proj.cy + 5) >= (app.charY - app.charHeight/2) and
                    (proj.cy + 5) <= (app.charY + app.charHeight/2)):
                    mob.proj.pop(k)
                    app.charHP -= 1
                    if app.charHP <= 0:
                        app.lose = True
                        app.paused = True
                else:
                    k += 1
            else:
                # similar for boss minions
                for minion in mob.minionList:
                    minion.move(app,5)
                    # slows down mob atks
                    if app.count % 20 == 0:
                        minion.atk(app,10)
                        # the mob is attacking the player - melee
                        if ((minion.cx) >= (app.charX - app.charWidth/2) and
                            (minion.cx) <= (app.charX + app.charWidth/2) and
                            (minion.cy) >= (app.charY - app.charHeight/2) and
                            (minion.cy) >= (app.charY + app.charHeight/2)):
                            app.charHP -= 1
                            if app.charHP <= 0:
                                app.lose = True
                                app.paused = True
                    j = 0
                    while j < len(app.charProj):
                        proj = app.charProj[j]
                        if ((proj.cx + app.poopRad) >= (minion.cx - minion.width/2) and 
                            (proj.cx + app.poopRad) <= (minion.cx + minion.width/2) and
                            (proj.cy + app.poopRad) >= (minion.cy - minion.height/2) and
                            (proj.cy + app.poopRad) <= (minion.cy + minion.height/2)):
                            minion.gotHit(proj.strength*25,app)
                            app.charProj.pop(j)
                        else:
                            j += 1
                h = 0
                while h < len(mob.minionList):
                    if mob.minionList[h].health <= 0:
                        mob.minionList.pop(h)
                    else:
                        h += 1
            j = 0
            while j < len(app.charProj):
                proj = app.charProj[j]
                if ((proj.cx + app.poopRad) >= (mob.cx - mob.width/2) and 
                    (proj.cx + app.poopRad) <= (mob.cx + mob.width/2) and
                    (proj.cy + app.poopRad) >= (mob.cy - mob.height/2) and
                    (proj.cy + app.poopRad) <= (mob.cy + mob.height/2)):
                    mob.gotHit(proj.strength*app.charStrength,app)
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
        for mob in app.mobs:
            if isinstance(mob,Boss):
                mob.stateMachine.run(app)
                print(mob.stateMachine.curState)
        n = 0
        while n < len(app.items):
            item = app.items[n]
            if distance(app.charX,app.charY,item.cx,item.cy) < 25:
                app.items.pop(n)
                item.pickUp(app)
                print(f"collected: {item}")
            else:
                n += 1

def convertToGrid(x,y):
    row = (y-80)//95
    col = (x-70)//95
    return (int(row),int(col))

def moveChar(app,amount):
    leftWall = 75
    rightWall = app.width - 75
    topWall = 80
    botWall = app.height - 50
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
        gridRow, gridCol = convertToGrid(newX,newY)
        if gridRow < 4 and gridRow >=0 and gridCol < 9 and gridCol >= 0:
            if app.roomType.map[gridRow][gridCol] != 1:
                app.charX = newX
                app.charY = newY
    else:
        if newX > rightWall:
            if app.charY > app.height/2-30 and app.charY < app.height/2+30:
                newCol =  app.curRoom[1] + 1
                newRow = app.curRoom[0]
                if inBounds(app.map,newRow,newCol):
                    newRoom = app.map[newRow][newCol]
                else:
                    return
                if newRoom != 0 and newRoom != "secretRoom" and newRoom != "superSecretRoom":
                    app.charX = 85
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
                if (newRoom == "secretRoom" or newRoom == "superSecretRoom") and app.secretFound == app.curRoom:
                    app.charX = 85
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
        elif newX < leftWall:
            if app.charY > app.height/2-30 and app.charY < app.height/2+30:
                newCol =  app.curRoom[1] - 1
                newRow = app.curRoom[0]
                if inBounds(app.map,newRow,newCol):
                    newRoom = app.map[newRow][newCol]
                else:
                    return
                if newRoom != 0 and newRoom != "secretRoom" and newRoom != "superSecretRoom":
                    app.charX = app.width - 80
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
                if (newRoom == "secretRoom" or newRoom == "superSecretRoom") and app.secretFound == app.curRoom:
                    app.charX = app.width - 80
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True 
        elif newY < topWall:
            if app.charX > app.width/2-30 and app.charX < app.width/2+30:
                newCol =  app.curRoom[1]
                newRow = app.curRoom[0] - 1
                if inBounds(app.map,newRow,newCol):
                    newRoom = app.map[newRow][newCol]
                else:
                    return
                if newRoom != 0 and newRoom != "secretRoom" and newRoom != "superSecretRoom":
                    app.charY = app.height - 60
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
                if (newRoom == "secretRoom" or newRoom == "superSecretRoom") and app.secretFound == app.curRoom:
                    app.charY = app.height - 60
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
        elif newY > botWall:
            if app.charX > app.width/2-30 and app.charX < app.width/2+30:
                newCol =  app.curRoom[1]
                newRow = app.curRoom[0] + 1
                if inBounds(app.map,newRow,newCol):
                    newRoom = app.map[newRow][newCol]
                else:
                    return
                if newRoom != 0 and newRoom != "secretRoom" and newRoom != "superSecretRoom":
                    app.charY = 85
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
                if (newRoom == "secretRoom" or newRoom == "superSecretRoom") and app.secretFound == app.curRoom:
                    app.charY = 85
                    app.curRoom = (newRow,newCol) 
                    app.changeRoom = True
        else:
            return
        if app.changeRoom == True:
            app.changeRoom = False
            app.newRoom = 5
            app.isMoving = False
            app.roomType = app.map[app.curRoom[0]][app.curRoom[1]]
            app.items = app.roomType.items  
            app.mobs = app.roomType.mobs
            for mob in app.mobs:
                mob.imageInit(app)
                mob.respawn(app)
            for item in app.items:
                item.initImages(app)
            print(app.curRoom)


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
    elif event.key == "t":
        app.charHP = 5
    elif event.key == "r" and app.dagger == True:
        app.daggerWield = not app.daggerWield
        for mob in app.mobs:
            if distance(app.charX,app.charY,mob.cx,mob.cy) < 40:
                mob.gotHit(5*app.charStrength,app)
            if isinstance(mob,Boss):
                for minion in mob.minionList:
                    if distance(app.charX,app.charY,minion.cx,minion.cy) < 40:
                        minion.gotHit(app.charStrength,app)
            h = 0
            while h < len(app.mobs):
                if app.mobs[h].health <= 0:
                    app.mobs.pop(h)
                else:
                    h += 1
    elif event.key == "e" and app.charBombs > 0:
        app.charBombs -= 1
        newBomb = Bomb(app.charX,app.charY)
        app.bombs.append(newBomb)
        newBomb.initImages(app)
        newBomb.placed(app)
    elif event.key == "p":
        app.paused = not app.paused
        app.start += 1
    elif event.key == "q":
        if app.help == True:
            app.help = False
        else:
            app.start = 0
            app.paused = True
    elif app.paused and event.key == "o":
        app.help = True
    # shortcuts
    elif event.key == "0":
        bossLoc = None
        for i in range(7):
            for j in range(7):
                if app.map[i][j] == "bossRoom":
                    bossLoc = (i,j)
        app.curRoom = bossLoc
        app.newRoom = 5
        app.isMoving = False
        app.roomType = app.map[app.curRoom[0]][app.curRoom[1]]  
        app.mobs = [Reaper()]
        for mob in app.mobs:
            mob.respawn(app)
            mob.imageInit(app)
        app.items = app.roomType.items
        print(app.curRoom)
        app.charX = 500
        app.charY = 350
    elif event.key == "9":
        bossLoc = None
        for i in range(7):
            for j in range(7):
                if app.map[i][j] == "bossRoom":
                    bossLoc = (i,j)
        app.curRoom = bossLoc
        app.newRoom = 5
        app.isMoving = False
        app.roomType = app.map[app.curRoom[0]][app.curRoom[1]]  
        app.mobs = [Golem()]
        for mob in app.mobs:
            mob.respawn(app)
            mob.imageInit(app)
        app.items = app.roomType.items
        print(app.curRoom)
        app.charX = 500
        app.charY = 350
    elif event.key == "8":
        secretLoc = None
        for i in range(7):
            for j in range(7):
                if app.map[i][j] == "secretRoom" or app.map[i][j] == "superSecretRoom":
                    secretLoc = (i,j)
        app.curRoom = secretLoc
        app.newRoom = 5
        app.isMoving = False
        app.roomType = app.map[app.curRoom[0]][app.curRoom[1]]  
        for mob in app.mobs:
            mob.respawn(app)
            mob.imageInit(app)
        app.items = app.roomType.items
        app.charX = 500
        app.charY = 350
    elif event.key == "Space":
        locKey = None
        for key in app.roomType.obsLocations:
            if app.roomType.obsLocations[key] == app.closedChest:
                app.roomType.obsLocations[key] = app.openChest
                locKey = key
        if locKey != None:
            num = random.randint(0,2)
            row,col = locKey
            x = row*95 + random.randint(-15,15)
            y = col*95 + random.randint(-15,15)
            if num == 0:
                item = Bomb(x,y)
            elif num == 1:
                item = Milk(x,y)
            elif num == 2:
                item = Dagger(x,y)
            item.initImages(app)
            app.items.append(item)
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
    newProj.vx = 12*newProj.strength*math.cos(newProj.angle)
    newProj.vy = 8*newProj.strength*math.sin(newProj.angle)

runApp(width = 1000, height = 500)
