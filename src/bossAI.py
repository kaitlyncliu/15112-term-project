from mobAI import Mob
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
    
class GotHit(State):
    def run(self,app):
        self.stateMachine.boss.type = "idle"
        self.stateMachine.boss.totalSprites = 8
        self.stateMachine.curState = Enraged(self.stateMachine)
        self.stateMachine.changeState = True

class Move(State):
    def run(self,app):
        b = self.stateMachine.boss
        b.type = "idle"
        b.totalSprites = 8
        b.move(app,10)
        if distance(app.charX,app.charY,b.cx,b.cy) <= 50:
            self.stateMachine.curState = Enraged(self.stateMachine)
            self.stateMachine.changeState = True
        if self.timer > 16 and b.stage > 1:
            self.stateMachine.curState = SpawnMinion(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1

class Attack(State): 
    def run(self,app):
        b = self.stateMachine.boss
        b.type = "attack"
        b.totalSprites = 12
        if distance(app.charX,app.charY,b.cx,b.cy) <= 30 and self.timer > 11:
            app.charHP -= 1
        if self.timer > 12:
            self.stateMachine.curState = Move(self.stateMachine)
            self.stateMachine.changeState = True
        self.timer += 1
        

class Enraged(State): 
    def run(self,app):
        self.stateMachine.boss.type = "enraged"
        self.stateMachine.boss.totalSprites = 8
        if self.timer > 5:
            nextMoves = [Attack(self.stateMachine),Skill(self.stateMachine)]
            self.stateMachine.curState = nextMoves[random.randint(0,1)]
            self.stateMachine.changeState = True
        self.timer += 1


class Skill(State): 
    def run(self,app):
        b = self.stateMachine.boss
        b.type = "skill"
        b.totalSprites = 12
        if distance(app.charX,app.charY,b.boss.cx,b.boss.cy) <= 30 and self.timer > 11:
            app.charHP -= 1
        if self.timer > 12:
            b.curState = Move(self.boss)
            b.changeState = True
        self.timer += 1

class SpawnMinion(State): 
    def run(self,app):
        self.stateMachine.boss.type = "idle"
        for i in range(random.randint(1,2*self.stage-2)):
            minion = Minion(self.stage)
            minion.imageInit(app)
            self.stateMachine.boss.minionList.append(minion)
        self.timer += 1
        self.stateMachine.curState = Move(self)
        self.stateMachine.changeState = True
        

class Death(State):
    def run(self,app):
        self.stateMachine.boss.type = "death"
        self.stateMachine.boss.totalSprites = 10
        app.win = True
        app.paused = True


class Minion(Mob):
    def __init__(self,stage):
        super().__init__(stage*100,random.randint(300,700),random.randint(200,300))
        self.totalSprites = 4

    def imageInit(self,app):
        self.sprite = app.loadImage("minion.png")
        self.sprite = app.scaleImage(self.sprite,3)
        self.spriteWidth, self.spriteHeight = self.sprite.size
        self.sprites = []
        for row in range(2):
            for col in range(3):
                topLeftX = self.spriteWidth*col/4
                botRightX = self.spriteWidth*(col+1)/4
                topLeftY = self.spriteHeight*row/2
                botRightY = self.spriteHeight*(row+1)/2
                sprite = self.sprite.crop((topLeftX,topLeftY,botRightX,botRightY))
                self.sprites.append(sprite)


class BossStateMachine(object):
    def __init__(self,boss):
        self.boss = boss
        self.curState = Move(self)
        self.changeState = False

    def run(self,app):
        if self.changeState:
            self.changeState = False
            self.curState.start()
        self.curState.run(app)


class Boss(Mob):
    def __init__(self):
        self.name = "boss"
        self.initHealth = 1000
        self.health = 1000
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 500 
        self.cy = 250 
        self.type = "idle"
        self.state = "idle"
        self.stateTimer = 0
        self.proj = []
        self.next = "idle"
        self.minionList = []
        self.stage = 1
        self.stateMachine = BossStateMachine(self)

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
        states2 = ["idle", "enraged"]
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
        self.stateMachine.curState = GotHit(app)