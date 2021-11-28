import random
import math
from mapGenerator import *

## mob ideas: chest mimic, the mobs in sprite pack downloaded
# animals that eat frogs: ducks and lots of birds, snakes, final boss: frog mimic that can eat you up

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

def inMapBounds(app,x,y):
    leftWall = 75
    rightWall = app.width - 70
    topWall = 75
    botWall = app.height - 50
    if x > leftWall and x < rightWall and y > topWall and y < botWall:
        return True
    return False

class Mob(object):
    def __init__(self,name,health):
        self.name = name
        self.initHealth = health
        self.health = health
        self.spriteCounter = 0
        self.totalSprites = 8
        row = random.randint(0,3)
        col = random.randint(0,8)

        self.cx = random.randint(100,850)
        self.cy = random.randint(200,400)
        self.initx = self.cx
        self.inity = self.cy
        self.type = "walk"
        self.proj = []
        self.minionList = []

    def gotHit(self,dmg,app):
        self.health -= dmg
        if self.health > 0:
            self.type = "hurt"
        else:
            self.type = "death"
        print(self.health)
    
    def move(self,app,amt):
        self.cx += 10
        self.cy += 20
        dFromProj = []
        charRow, charCol = convertToGrid(app.charX,app.charY)
        charLoc = (charRow,charCol)
        selfRow, selfCol = convertToGrid(self.cx,self.cy)
        selfLoc = (selfRow,selfCol)
        for proj in app.charProj:
            d = distance(self.cx,self.cy,proj.cx,proj.cy)
            dFromProj.append(d)
        if app.charProj != []:
            dFromClosest = min(dFromProj)
            closestProj = dFromProj.index(dFromClosest)
        # dodges character projectiles that are close by
        if app.charProj != [] and dFromClosest <= 80:
            self.type = "idle"
            difX = self.cx - app.charProj[closestProj].cx
            difY = self.cy - app.charProj[closestProj].cy
            angle = math.atan2(difY,difX)
            newX = self.cx + amt*3 * math.cos(angle)
            newY = self.cy + amt*3 * math.sin(angle)
            if inMapBounds(app,newX,newY):
                self.cx = newX
                self.cy = newY
        else:
            path = aStar(app.roomType.map,(charLoc),(selfLoc))
            print(path,selfLoc,charLoc)
            if path != None and len(path) > 0:
                nextRow = path[1][0]
                nextCol = path[1][1]
                tempX = self.cx
                tempY = self.cy
                print(nextRow,selfRow,nextCol,selfCol)
                if nextRow < selfRow and inMapBounds(app,self.cx,self.cy-amt):
                    self.cy -= amt*2
                elif nextRow > selfRow and inMapBounds(app,self.cx,self.cy+amt):
                    self.cy += amt*2
                if nextCol <  selfCol and inMapBounds(app,self.cx-amt,self.cy):
                    self.cx -= amt*2
                elif nextCol > selfCol and inMapBounds(app,self.cx-amt,self.cy):
                    self.cx += amt*2
                if inMapBounds(app,self.cx,self.cy) == False:
                    self.cx, self.cy = tempX, tempY
        self.cx -= 10
        self.cy -= 20

    def atk(self,app,dmg):
        pass

    
    def respawn(self,app):
        self.cx = self.initx
        self.cy = self.inity
        self.health = self.initHealth




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

#####################################################

# Pathfinding Algorithm - (A*)

class Node(object):
    def __init__(self,parent,row,col,end):
        
        self.row = row
        self.col = col
        self.parent = parent
        
        self.g = 0
        self.h = abs(end[0]-row) + abs(end[1]-col)
        self.f = self.g + self.h
    
    def __eq__(self,other):
        if self.row == other.row and self.col == other.col:
            return True
        else:
            return False

def inBounds(map,row,col):
    if row < len(map) and row >= 0 and col < len(map[0]) and col >= 0:
        return True
    else:
        return False


def convertToGrid(x,y):
    row = (y-80)//95
    col = (x-70)//95
    return (int(row),int(col))


# CITATION: Used this tutorial: https://brilliant.org/wiki/a-star-search/
def aStar(roomMap,start,end):
    startRow, startCol = start
    startNode = Node(None,startRow,startCol,end)
    dummyNode = Node(None,9999,9999,end)
    open = [startNode]
    closed = []
    curNode = startNode
    dirs = [(0,+1),(0,-1),(+1,0),(-1,0)]
    while (curNode.row,curNode.col) != end:
        bestFNode = dummyNode
        for node in open:
            if node.f < bestFNode.f:
                bestFNode = node
        if (bestFNode.row,bestFNode.col) == end:
            return getPath(bestFNode)
        else:
            curNode = bestFNode
            closed.append(bestFNode)
            if open == []:
                return None
            open.remove(bestFNode)
            childNodes = []
            for i in range(len(dirs)):
                newNodeRow = curNode.row+dirs[i][0]
                newNodeCol = curNode.col+dirs[i][1]
                if inBounds(roomMap,newNodeRow,newNodeCol) and roomMap[newNodeRow][newNodeCol] != 1:
                    newNode = Node(curNode,newNodeRow,newNodeCol,end)
                    newNode.g = curNode.g + 1
                    childNodes.append(newNode)
            for child in childNodes:
                if child in closed:
                    for closedNode in closed:
                        if child == closedNode and child.g < closedNode.g:
                            closedNode.g = child.g
                            closedNode.parent = curNode
                elif child in open:
                    for openNode in open:
                        if child == openNode and child.g < openNode.g:
                            openNode.g = child.g
                            openNode.parent = curNode
                else:
                    open.append(child)

# CITATION: https://www.educative.io/edpresso/what-is-the-a-star-algorithm
def getPath(endNode):
    path = []
    curNode = endNode
    while curNode is not None:
        path.append((curNode.row,curNode.col))
        curNode = curNode.parent
    return path
