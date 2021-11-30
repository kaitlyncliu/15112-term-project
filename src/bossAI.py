from mobAI import Mob
import math
import random

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

class State(object):
    def __init__(self,boss):
        self.timer = 0
        self.boss = boss
        self.stateMachine = boss.stateMachine

    def start(self):
        self.timer = 0
    
class GotHit(State):
    def run(self,app):
        self.boss.type = "idle"
        self.boss.totalSprites = 8
        self.boss.curState = Enraged(app)
        self.boss.changeState = True

class Move(State):
    def run(self,app):
        self.boss.type = "idle"
        self.boss.totalSprites = 8
        self.boss.move(app,10)
        if distance(app.charX,app.charY,self.boss.cx,self.boss.cy) <= 50:
            self.stateMachine.curState = Enraged(app)
            self.stateMachine.changeState = True
        if self.timer > 16 and self.boss.stage > 1:
            self.stateMachine.curState = SpawnMinion(app)
            self.stateMachine.changeState = True

class Attack(State): 
    def run(self,app):
        self.boss.type = "attack"
        self.boss.totalSprites = 12
        if distance(app.charX,app.charY,self.boss.cx,self.boss.cy) <= 30 and self.timer > 11:
            app.charHP -= 1
        if self.timer > 12:
            self.stateMachine.curState = Move(app)
            self.stateMachine.changeState = True
        

class Enraged(State): 
    def run(self,app):
        self.boss.type = "enraged"
        self.boss.totalSprites = 8
        if self.timer > 5:
            nextMoves = [Attack(app),Skill(app)]
            self.stateMachine.curState = nextMoves[random.randint(0,1)]
            self.stateMachine.changeState = True
        self.timer += 1


class Skill(State): 
    def run(self,app):
        self.boss.type = "skill"
        self.boss.totalSprites = 12
        if distance(app.charX,app.charY,self.cx,self.cy) <= 30 and self.timer > 11:
            app.charHP -= 1
        if self.timer > 12:
            self.stateMachine.curState = Move(app)
            self.stateMachine.changeState = True
        self.timer += 1

class SpawnMinion(State): 
    def run(self,app):
        self.boss.type = "idle"
        for i in range(random.randint(1,2*self.stage-2)):
            self.minion = Minion(self.stage)
            self.minion.imageInit(app)
            self.minionList.append(self.minion)
        self.timer += 1
        

class Death(State):
    def run(self,app):
        self.boss.type = "death"
        self.boss.totalSprites = 10
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
        self.curState = Move(boss)
        self.changeState = False

    def run(self):
        if self.changeState:
            self.changeState = False
            self.curState.start()
        self.curState.run()


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
        self.stateMachine = None

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
        
    def machineInit(self,mac):
        self.stateMachine = mac

    def gotHit(self,dmg,app):
        self.health -= dmg
        self.stateMachine.curState = GotHit(app)