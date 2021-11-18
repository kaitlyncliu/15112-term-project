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


