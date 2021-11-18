import random

class Mob(object):
    def __init__(self,name,health):
        self.name = name
        self.health = health
        self.spriteCounter = 0
        self.cx = random.randint(0,1000)
        self.cy = random.randint(0,500)
        self.type = "idle"

    def gotHit(self,dmg):
        self.health -= dmg
        if self.health > 0:
            self.type = "hurt"
        else:
            self.type = "death"
    
    def move(self,app):
        charX, charY = app.charCX, app.charCY


