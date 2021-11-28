from mobAI import Mob
import math
import random

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Boss(Mob):
    def __init__(self,name,health):
        self.name = name
        self.initHealth = health
        self.health = health
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 500 
        self.cy = 250 
        self.type = "idle"
        self.state = "idle"
        self.proj = []
        self.next = "idle"
        self.minionList = []

    def gotHit(self,dmg,app):
        self.health -= dmg
        if self.health <= 0:
            app.win = True
            app.paused = True
        print(self.health)
        self.next = "idle"

    def idle(self):
        self.type = "idle"
        self.next = "prepATK"
    
    def attack(self,app):
        self.type = "attack"
        self.move(app,10)
        if distance(app.charX,app.charY,self.cx,self.cy) <= 30:
            app.charHP -=1
        self.next = "skill"
    
    def prepATK(self):
        self.next = "attack"
    
    def skill(self,app):
        self.type = "skill"
        if distance(app.charX,app.charY,self.cx,self.cy) <= 30:
            app.charHP -= 1
    
    def spawn(self,app):
        self.type = "idle"
        for i in range(random.randint(0,3)):
            self.minion = Mob(f"minion{i}", 50)
            self.minionList.append(self.minion)
        
        

class StateMachine(object):
    def setState(self,enemy,app):
        if enemy.next == "attack":
            enemy.state = "attack"
            enemy.attack(app)
        elif enemy.next == "idle":
            enemy.state = "idle"
            enemy.idle()
        elif enemy.next == "prepATK":
            enemy.state = "prepATK"
            enemy.prepATK()
        elif enemy.next == "skill":
            enemy.state = "skill"
            enemy.skill(app)

bossStateMac = StateMachine()