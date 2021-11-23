import random
import math


## mob ideas: chest mimic, the mobs in sprite pack downloaded
# animals that eat frogs: ducks and lots of birds, snakes, final boss: frog mimic that can eat you up

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Mob(object):
    def __init__(self,name,health):
        self.name = name
        self.health = health
        self.spriteCounter = 0
        self.cx = random.randint(100,900)
        self.cy = random.randint(50,450)
        self.type = "walk"
        self.proj = []

    def gotHit(self,dmg):
        self.health -= dmg
        if self.health > 0:
            self.type = "hurt"
        else:
            self.type = "death"
        print(self.health)
    
    def move(self,app,amt):
        dFromProj = []
        for proj in app.charProj:
            d = distance(self.cx,self.cy,proj.cx,proj.cy)
            dFromProj.append(d)
        if app.charProj != []:
            dFromClosest = min(dFromProj)
            closestProj = dFromProj.index(dFromClosest)
        # dodges character projectiles that are close by
        if app.charProj != [] and dFromClosest <= 80:
            self.type = "run"
            difX = self.cx - app.charProj[closestProj].cx
            difY = self.cy - app.charProj[closestProj].cy
            angle = math.atan2(difY,difX)
            self.cx += amt*3 * math.cos(angle)
            self.cy += amt*3 * math.sin(angle)
        else:
            charX, charY = app.charX, app.charY
            difX = self.cx - charX
            difY = self.cy - charY
            angle = math.atan2(difY,difX)
            self.cx -= amt * math.cos(angle)
            self.cy -= amt * math.sin(angle)

    def atk(self,app,dmg):
        pass


class Ghost(Mob):
    def move(self,app,amt):
        self.type = "idle"
        dFromProj = []
        for proj in app.charProj:
            d = distance(self.cx,self.cy,proj.cx,proj.cy)
            dFromProj.append(d)
        if app.charProj != []:
            dFromClosest = min(dFromProj)
            closestProj = dFromProj.index(dFromClosest)
        # dodges character projectiles that are close by
        if app.charProj != [] and dFromClosest <= 80:
            difX = self.cx - app.charProj[closestProj].cx
            difY = self.cy - app.charProj[closestProj].cy
            angle = math.atan2(difY,difX)
            self.cx += amt*3 * math.cos(angle)
            self.cy += amt*3 * math.sin(angle)
    
    def atk(self,app,dmg):
        charX, charY = app.charX, app.charY
        difX = self.cx - charX
        difY = self.cy - charY
        angle = math.atan2(difY,difX)
        self.proj.append(GhostTear(10,self.cx,self.cy))
        self.proj[-1].angle = angle
       
# basic projectiles for both the player and mobs
class Projectile(object):
    def __init__(self,strength,x,y):
        self.time = 0
        self.strength = strength
        self.initY = y
        self.initX = x
        self.cx = x
        self.cy = y
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.image = None
    
    def move(self,app):
        self.cx = self.initX + self.vx*self.time
        self.cy = self.initY + (self.vy*self.time - 0.5*(-3)*self.time**2)
        
    
class GhostTear(Projectile):
    def move(self):
        self.cx -= 30 * math.cos(self.angle)
        self.cy -= 30 * math.sin(self.angle)


# Pathfinding Algorithm - (A*)
