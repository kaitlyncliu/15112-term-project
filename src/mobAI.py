import random
import math

class Mob(object):
    def __init__(self,name,health):
        self.name = name
        self.health = health
        self.spriteCounter = 0
        self.cx = random.randint(100,900)
        self.cy = random.randint(50,450)
        self.type = "idle"
        self.proj = []

    def gotHit(self,dmg):
        self.health -= dmg
        if self.health > 0:
            self.type = "hurt"
        else:
            self.type = "death"
        print(self.health)
    
    def move(self,app,amt):
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
        charX, charY = app.charX, app.charY
        difX = self.cx - charX
        difY = self.cy - charY
        angle = math.atan2(difY,difX)
        self.cx -= .2 * amt * math.cos(angle)
        self.cy -= .2 * amt * math.sin(angle)
    
    def atk(self,app,dmg):
        charX, charY = app.charX, app.charY
        difX = self.cx - charX
        difY = self.cy - charY
        angle = math.atan2(difY,difX)
        self.proj.append(GhostTear(10,self.cx,self.cy))
        self.proj[-1].angle = angle
       


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
    def move(self,app):
        self.cx -= 50 * math.cos(self.angle)
        self.cy -= 50 * math.sin(self.angle)