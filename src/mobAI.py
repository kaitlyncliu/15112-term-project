import random
import math
from mapGenerator import *

## mob ideas: chest mimic, the mobs in sprite pack downloaded
# animals that eat frogs: ducks and lots of birds, snakes, final boss: frog mimic that can eat you up

def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Mob(object):
    def __init__(self,name,health):
        self.name = name
        self.initHealth = health
        self.health = health
        self.spriteCounter = 0
        self.totalSprites = 8
        self.initx = 300
        self.inity = 200
        self.cx = 300 #random.randint(100,900)
        self.cy = 200 #random.randint(50,450)
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
            self.type = "idle"
            difX = self.cx - app.charProj[closestProj].cx
            difY = self.cy - app.charProj[closestProj].cy
            angle = math.atan2(difY,difX)
            self.cx += amt*3 * math.cos(angle)
            self.cy += amt*3 * math.sin(angle)
        else:
            #charX, charY = convertToGrid(app.charY,app.charX)
            #selfX, selfY = convertToGrid(self.cy,self.cx)
            charX, charY = app.charX, app.charY
            difX = self.cx - charX
            difY = self.cy - charY
            angle = math.atan2(difY,difX)
            newX = self.cx - amt * math.cos(angle)
            newY = self.cy - amt * math.sin(angle)
            gridRow, gridCol = convertToGrid(newX,newY)
            if app.roomType.map[gridRow][gridCol] != 1:
                self.cx = newX
                self.cy = newY
            '''path = aStar(app.roomType.map,(selfX,selfY),(charX,charY))
            if path != None:
                print(path[0][1],path[0][0])
                difX = abs(self.cx - path[0][0]*19)
                difY = abs(self.cy - path[0][1]*19)
                angle = math.atan2(difY,difX)
                self.cx += amt * math.cos(angle)
                self.cy += amt * math.sin(angle)'''

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
    def __init__(self,parent,x,y,end):
        
        self.x = x
        self.y = y
        self.parent = parent
        
        self.g = 0
        self.h = abs(end[0]-x) + abs(end[1]-y)
        self.f = self.g + self.h
    
    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
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
    startx, starty = start
    startNode = Node(None,startx,starty,end)
    dummyNode = Node(None,9999,9999,end)
    open = [startNode]
    closed = []
    curNode = startNode
    dirs = [(0,+1),(0,-1),(+1,0),(-1,0)]
    while (curNode.x,curNode.y) != end:
        bestFNode = dummyNode
        for node in open:
            if node.f < bestFNode.f:
                bestFNode = node
        if (bestFNode.x,bestFNode.y) == end:
            return getPath(bestFNode)
        else:
            curNode = bestFNode
            closed.append(bestFNode)
            if open == []:
                return None
            open.remove(bestFNode)
            childNodes = []
            for i in range(len(dirs)):
                newNodeX = curNode.x+dirs[i][0]
                newNodeY = curNode.y+dirs[i][1]
                if inBounds(roomMap,newNodeX,newNodeY) and roomMap[newNodeX][newNodeY] != 1:
                    newNode = Node(curNode,newNodeX,newNodeY,end)
                    if i <= 3: # straight movement
                        newNode.g = curNode.g + 1
                    '''else: # diagonal movement
                        newNode.g = curNode.g + 1.4'''
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
        path.append((curNode.x,curNode.y))
        print(path)
        curNode = curNode.parent
    return path[::-1]

"""
room2 = [[0,0,0,0,0,1,0,1,0],
        [0,1,0,1,0,1,0,0,0],
        [1,0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0],]

print(aStar(room2,(2,1),(2,6)))
"""