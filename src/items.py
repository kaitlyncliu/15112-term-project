import random

class Item(object):
    def __init__(self,x,y):
        self.image = None
        self.cx = 0
        self.cy = 0
    
    def used(self):
        pass
    
def inBounds(map,row,col):
    if row < len(map) and row >= 0 and col < len(map[0]) and col >= 0:
        return True
    else:
        return False

class Bomb(Item):
    def initImages(self,app):
        self.unlit = app.loadImage("BombUnlit.png")
        self.unlit = app.scaleImage(self.unlit,0.25)
        self.lit = app.loadImage("BombLit.png")
        self.lit = app.scaleImage(self.lit,0.25)
        self.image = self.unlit
        self.timer = 0
        self.cx = 0
        self.cy = 0
        
    def explode(self,app):
        # top door
        if (self.cx > app.width/2 - 40) and (self.cx < app.width/2 + 40) and self.cy < 120:
            row = app.curRoom[0] - 1
            col = app.curRoom[1]
            if inBounds(app.map,row,col) and (app.map[row][col] == "secretRoom" or app.map[row][col] == "superSecretRoom"):
                app.secretFound = app.curRoom
                app.holeLoc = "top"
        # bottom door
        elif (self.cx > app.width/2 - 40) and (self.cx < app.width/2 + 40) and self.cy > 400:
            row = app.curRoom[0] + 1
            col = app.curRoom[1]
            if inBounds(app.map,row,col) and (app.map[row][col] == "secretRoom" or app.map[row][col] == "superSecretRoom"):
                app.secretFound = app.curRoom
                app.holeLoc = "bottom"
        # left door
        elif (self.cy > app.height/2 - 40) and (self.cy < app.height/2 + 40) and self.cx < 150:
            row = app.curRoom[0]
            col = app.curRoom[1] - 1
            if inBounds(app.map,row,col) and (app.map[row][col] == "secretRoom" or app.map[row][col] == "superSecretRoom"):
                app.secretFound = app.curRoom
                app.holeLoc = "left"
        # right door
        elif (self.cy > app.height/2 - 40) and (self.cy < app.height/2 + 40) and self.cx > 875:
            row = app.curRoom[0]
            col = app.curRoom[1] + 1
            if inBounds(app.map,row,col) and (app.map[row][col] == "secretRoom" or app.map[row][col] == "superSecretRoom"):
                app.secretFound = app.curRoom
                app.holeLoc = "right"
    
    def placed(self,app):
        self.image = self.lit
        self.timer = 0
        self.cx = app.charX
        self.cy = app.charY

# take less damage, greater attack
class Egg(Item):
    pass

# bigger, stronger poops
class Milk(Item):
    pass

# New attack mode - melee with left click
class Dagger(Item):
    pass

# Makes character run faster
class Soda(Item):
    pass

# heals health
class Heart(Item):
    pass

# Every time you kill an enemy (not a minion) you gain a heart
class Bat(Item):
    pass
