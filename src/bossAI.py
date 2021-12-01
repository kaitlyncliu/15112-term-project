from mobAI import Mob,Projectile
import math
import random

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

class State(object):
    def __init__(self,mac):
        self.timer = 0
        self.stateMachine = mac

    def start(self):
        self.timer = 0

#Reaper States:
class GotHitR(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 8
        b.type = "idle"
        print(b.health)
        if b.health < .5*b.initHealth:
            b.stage = 3
            b.dis = 200
            print("im")
            self.stateMachine.boss.imageInit(app)
        elif b.health<.75*b.initHealth:
            b.stage = 2
        if b.health <= 0:
            self.stateMachine.curState = DeathR(self.stateMachine)
            self.stateMachine.changeState = True
        else:
            self.stateMachine.curState = EnragedR(self.stateMachine)
            self.stateMachine.changeState = True

class MoveR(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 8
        b.type = "idle"
        b.move(app,10)
        if distance(app.charX,app.charY,b.cx,b.cy) <= b.dis:
            self.stateMachine.curState = EnragedR(self.stateMachine)
            self.stateMachine.changeState = True
        if self.timer > 16 and b.stage > 1:
            self.stateMachine.curState = SpawnPrepR(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class AttackR(State): 
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 12
        b.type = "attack"
        if distance(app.charX,app.charY,b.cx,b.cy) <= b.dis and self.timer == 11:
            app.charHP -= 1
        if self.timer > 12:
            self.stateMachine.curState = MoveR(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class EnragedR(State): 
    def run(self,app):
        self.stateMachine.boss.totalSprites = 8
        self.stateMachine.boss.type = "enraged"
        if self.timer > 5:
            nextMoves = [AttackR(self.stateMachine),SkillR(self.stateMachine)]
            self.stateMachine.curState = nextMoves[random.randint(0,1)]
            self.stateMachine.changeState = True
        self.timer += 1

class SkillR(State): 
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 12
        b.type = "skill"
        if distance(app.charX,app.charY,b.cx,b.cy) <= (b.dis + 20) and self.timer == 11:
            app.charHP -= 1
        if self.timer > 12:
            self.stateMachine.curState = MoveR(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class SpawnPrepR(State):
    def run(self,app):
        self.stateMachine.boss.totalSprites = 8
        self.stateMachine.boss.type = "spawnPrep"
        if self.timer > 5:
            self.stateMachine.curState = SpawnMinionR(self.stateMachine)
            self.changeState = True
        self.timer += 1

class SpawnMinionR(State): 
    def run(self,app):
        self.stateMachine.boss.totalSprites = 8
        self.stateMachine.boss.type = "idle"
        for i in range(random.randint(1,2*self.stateMachine.boss.stage-2)):
            if self.timer % 3 == 0:
                minion = Minion(self.stateMachine.boss.stage)
                minion.imageInit(app)
                self.stateMachine.boss.minionList.append(minion)
        self.timer += 1
        self.stateMachine.curState = MoveR(self.stateMachine)
        self.stateMachine.changeState = True

class DeathR(State):
    def run(self,app):
        self.stateMachine.boss.totalSprites = 10
        self.stateMachine.boss.type = "death"
        if self.timer > 10:
            app.win = True
            app.paused = True
        self.timer += 1

# Golem States:

class DefendG(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 8
        b.type = "defend"
        print(b.health)
        if b.health < .5*b.initHealth:
            b.stage = 3
            b.dis = 200
            self.stateMachine.boss.imageInit(app)
        elif b.health<.75*b.initHealth:
            b.stage = 2
        if b.health <= 0:
            self.stateMachine.curState = DeathG(self.stateMachine)
            self.stateMachine.changeState = True
        else:
            self.stateMachine.curState = EnragedG(self.stateMachine)
            self.stateMachine.changeState = True

class SpawnG(State):
    def run(self,app):
        self.stateMachine.boss.totalSprites = 14
        self.stateMachine.boss.type = "spawn"
        if self.timer > 14:
            self.stateMachine.curState = IdleG(self.stateMachine)
        self.timer += 1

class IdleG(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.totalSprites = 4
        b.type = "idle"
        b.move(app,10)
        if self.timer > 16 and b.stage > 1:
            self.stateMachine.curState = EnragedG(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class EnragedG(State): 
    def run(self,app):
        b = self.stateMachine.boss
        self.stateMachine.boss.totalSprites = 8
        self.stateMachine.boss.type = "enraged"
        if self.timer > 8:
            if distance(app.charX,app.charY,b.cx,b.cy) <= b.dis:
                self.stateMachine.curState = MeleeG(self.stateMachine)
                self.stateMachine.changeState = True
            else:
                if b.stage < 2:
                    self.stateMachine.curState = AttackG(self.stateMachine)
                    self.stateMachine.changeState = True
                '''else:
                    if random.randint(0,1) == 1:
                        self.stateMachine.curState = LaserG(self.stateMachine)
                        self.stateMachine.changeState = True
                    else:
                        self.stateMachine.curState = AttackG(self.stateMachine)
                        self.stateMachine.changeState = True'''
        self.timer += 1

class MeleeG(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.type = "melee"
        self.stateMachine.boss.totalSprites = 7
        if distance(app.charX,app.charY,b.cx,b.cy) <= b.dis and self.timer == 11:
            app.charHP -= 1 
        if self.timer > 7:
            self.stateMachine.curState = IdleG(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class AttackG(State):
    def run(self,app):
        charX, charY = app.charX, app.charY
        b = self.stateMachine.boss
        b.type = "atk"
        b.totalSprites = 9
        difX = b.cx - charX
        difY = b.cy - charY
        angle = math.atan2(difY,difX)
        b.proj.append(GolemArm(10,b.cx,b.cy))
        b.proj[-1].angle = angle
        if self.timer > 9:
            self.stateMachine.curState = IdleG(self.stateMachine)
            self.stateMachine.changeState = True
        self.time += 1

class DeathG(State):
    def run(self,app):
        self.stateMachine.boss.totalSprites = 14
        self.stateMachine.boss.type = "death"
        if self.timer > 10:
            app.win = True
            app.paused = True
        self.timer += 1

class GolemArm(Projectile):
    def imageInit(self,app):
        self.image = app.load("arm.png")
        imageWidth,imageHeight = self.image.size
        self.image = self.image.crop((0,0,imageWidth,imageHeight*2/3))
        self.sprites = []
        for i in range(2):
            for j in range(3):
                topLeftX = self.spriteWidth*j/3
                botRightX = self.spriteWidth*(j+1)/3
                topLeftY = self.spriteHeight*i/2
                botRightY = self.spriteHeight*(i+1)/2
                sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
                self.sprites.append(sprite)   

    def move(self):
        self.cx -= 35 * math.cos(self.angle)
        self.cy -= 35 * math.sin(self.angle)

class Minion(Mob):
    def __init__(self,stage):
        super().__init__(stage*50,random.randint(300,700),random.randint(200,300))
        self.totalSprites = 4

    def imageInit(self,app):
        self.sprite = app.loadImage("minion.png")
        self.sprite = app.scaleImage(self.sprite,5)
        self.spriteWidth, self.spriteHeight = self.sprite.size
        self.sprites = dict()
        tempSprite = []
        for row in range(2):
            for col in range(3):
                topLeftX = self.spriteWidth*col/4
                botRightX = self.spriteWidth*(col+1)/4
                topLeftY = self.spriteHeight*row/2
                botRightY = self.spriteHeight*(row+1)/2
                sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
                tempSprite.append(sprite)
        self.sprites["walk"] = tempSprite
        self.width,self.height = self.sprites["walk"][0].size


class ReaperStateMachine(object):
    def __init__(self,boss):
        self.boss = boss
        self.curState = MoveR(self)
        self.changeState = False

    def run(self,app):
        if self.changeState:
            self.changeState = False
            self.boss.spriteCounter = 0
            self.curState.start()
        self.curState.run(app)


class GolemStateMachine(object):
    def __init__(self,boss):
        self.boss = boss
        self.curState = SpawnG(self)
        self.changeState = False

    def run(self,app):
        if self.changeState:
            self.changeState = False
            self.boss.spriteCounter = 0
            self.curState.start()
        self.curState.run(app)

class Boss(Mob):
    pass

class Reaper(Boss):
    def __init__(self):
        self.name = "Reaper"
        self.initHealth = 1000
        self.health = 1000
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 500 
        self.cy = 250 
        self.type = "idle"
        self.stateTimer = 0
        self.proj = []
        self.minionList = []
        self.stage = 1
        self.dis = 125
        self.stateMachine = ReaperStateMachine(self)

    # IMAGE CITATION: https://darkpixel-kronovi.itch.io/undead-executioner
    def imageInit(self,app):
        self.sprites = dict()
        states = ["attack","skill"]
        for i in range(len(states)):
            self.sprite = app.loadImage(f'{states[i]}.png')
            if self.stage == 3:
                self.sprite = app.scaleImage(self.sprite,6)
            else:
                self.sprite = app.scaleImage(self.sprite,4)
            self.spriteWidth, self.spriteHeight = self.sprite.size
            tempSprites = []
            for j in range(2):
                for k in range(6):
                    topLeftX = self.spriteWidth*k/6
                    botRightX = self.spriteWidth*(k+1)/6
                    topLeftY = self.spriteHeight*j/2
                    botRightY = self.spriteHeight*(j+1)/2
                    sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
                    tempSprites.append(sprite)
            self.sprites[states[i]] = tempSprites
        self.width,self.height = self.sprites["attack"][0].size
        states2 = ["idle", "enraged","spawnPrep"]
        for i in range(len(states2)):
            self.sprite = app.loadImage(f'{states2[i]}.png')
            if self.stage == 3:
                self.sprite = app.scaleImage(self.sprite,6)
            else:
                self.sprite = app.scaleImage(self.sprite,4)
            self.spriteWidth, self.spriteHeight = self.sprite.size
            tempSprite = []
            for row in range(2):
                for col in range(4):
                    topLeftX = self.spriteWidth*col/4
                    botRightX = self.spriteWidth*(col+1)/4
                    topLeftY = self.spriteHeight*row/2
                    botRightY = self.spriteHeight*(row+1)/2
                    sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
                    tempSprite.append(sprite)
            self.sprites[states2[i]] = tempSprite
        self.sprite = app.loadImage("death.png")
        self.sprite = app.scaleImage(self.sprite,6)
        self.spriteWidth, self.spriteHeight = self.sprite.size
        tempSprite = []
        for i in range(10):
            topLeftX = self.spriteWidth*i/10
            botRightX = self.spriteWidth*(i+1)/10
            topLeftY = 0
            botRightY = self.spriteHeight
            sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
            tempSprite.append(sprite)
        self.sprites["death"] = tempSprite

    def gotHit(self,dmg,app):
        self.health -= dmg
        self.stateMachine.curState = GotHitR(self.stateMachine)
        self.stateMachine.changeState = True

class Golem(Boss):
    def __init__(self):
        self.name = "Golem"
        self.initHealth = 1000
        self.health = 1000
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 500 
        self.cy = 250 
        self.type = "idle"
        self.stateTimer = 0
        self.proj = []
        self.minionList = []
        self.stage = 1
        self.dis = 125
        self.stateMachine = GolemStateMachine(self)

    
    # IMAGE CITATION: https://darkpixel-kronovi.itch.io/mecha-golem-free
    def imageInit(self,app):
        self.sprites = dict()
        states = {"idle0":4,"enraged1":8,"atk2":9,"defend3":8,"melee4":7,"laser5":7,"buffUp6":10,"death7":10}
        self.spriteSheet = app.loadImage("Golem.png")
        self.spriteSheet = app.scaleImage(self.spriteSheet,4)
        self.spriteWidth, self.spriteHeight = self.spriteSheet.size
        uncropped = []
        for i in range(9):
            topLeftX = 0
            topLeftY = self.spriteHeight*i/10
            botRightX = self.spriteWidth
            botRightY = self.spriteHeight*(i+1)/10
            uncrop = self.spriteSheet.crop((topLeftX,topLeftY,botRightX,botRightY))
            uncropped.append(uncrop)
        
        spriteWidth,spriteHeight = uncropped[0].size
        for state in states:
            tempSprite = []
            num = int(state[-1])
            name = state[:-1]
            for i in range(states[state]):
                topLeftX = spriteWidth*i/10
                botRightX = spriteWidth*(i+1)/10
                topLeftY = 0
                botRightY = spriteHeight
                new = uncropped[num].crop((topLeftX,topLeftY,botRightX,botRightY))
                tempSprite.append(new)
            self.sprites[name] = tempSprite
        tempSprite = []
        for i in range(4):
            topLeftX = spriteWidth*i/10
            botRightX = spriteWidth*(i+1)/10
            topLeftY = 0
            botRightY = spriteHeight
            new = uncropped[8].crop((topLeftX,topLeftY,botRightX,botRightY))
            self.sprites["death"].append(new)
        self.sprites["spawn"] = self.sprites["death"][::-1]
        
    def gotHit(self,dmg,app):
        self.health -= dmg
        self.stateMachine.curState = DefendG(self.stateMachine)
        self.stateMachine.changeState = True