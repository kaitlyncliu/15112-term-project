import random
import copy
import math

# Map Generator

# REFERENCE (for guidelines not code):
# following a similar set of guidelines for map gen as those in Binding of Isaac, as stated here:
# https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/
# code is all mine though

'''
For each cell in the queue, it loops over the 4 cardinal directions and does the following:

Determine the neighbour cell by adding +10/-10/+1/-1 to the currency cell.
If the neighbour cell is already occupied, give up
If the neighbour cell itself has more than one filled neighbour, give up.
If we already have enough rooms, give up
Random 50% chance, give up
Otherwise, mark the neighbour cell as having a room in it, and add it to the queue.
'''


def distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)

def getTargetRooms(level):
    rooms = int(level*1.4 + 8 + random.randint(0,4))
    return rooms

# wrapper function for makeRooms
def startMakeRooms(targetRooms):
    defaultMap =  [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]]
    endRooms = []
    queue = [(3,3)]
    resultMap, endRooms = makeRooms(defaultMap,queue,endRooms,targetRooms,0)
    # making special rooms:
    finalMap = makeSpecialRooms(resultMap,endRooms)
    return finalMap

def makeSpecialRooms(map, endRooms):
    if (3,3) in endRooms:
        endRooms.remove((3,3))
    for i in range(len(endRooms)):
        tempRoom = endRooms[-i]
        d = distance(tempRoom[0],tempRoom[1],3,3)
        print(d,tempRoom)
        if d > 1.5:
            print(endRooms)
            bossLocation = endRooms[-i]
            map[bossLocation[0]][bossLocation[1]] = "bossRoom"
            endRooms.pop(-i)
            break
    if len(endRooms) > 0:
        treasureLocation = endRooms[-1]
        map[treasureLocation[0]][treasureLocation[1]] = "treasureRoom"
        endRooms.pop()
    if len(endRooms) > 0:
        shopLocation = endRooms[-1]
        map[shopLocation[0]][shopLocation[1]] = "shopRoom"
        endRooms.pop()
    rows = len(map)
    cols = len(map[0])
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    random.shuffle(dirs)
    secretRoomPlaced = False
    minRoomsNear = 3
    while secretRoomPlaced == False:
        for row in range(rows):
            for col in range(cols):
                # if there already is a secret room, breaks the loop
                if secretRoomPlaced == True:
                    break
                # only tries to put secret room if cell is empty
                if map[row][col] != 0:
                    continue
                neighbors = 0
                for dir in dirs:
                    newRow = dir[0] + row
                    newCol = dir[1] + col
                    if not inBounds(map,newRow,newCol):
                        continue
                    elif map[newRow][newCol] == 1:
                        neighbors += 1
                # tries to put secret rooms next to a lot of rooms
                if neighbors > minRoomsNear:
                    if minRoomsNear < 2:
                        map[row][col] = "superSecretRoom"
                    else:    
                        map[row][col] = "secretRoom"
                    secretRoomPlaced = True
        # loosens constraints if a room can't be placed
        if secretRoomPlaced == False:
            minRoomsNear -= 1
    return map
        

# checks that a coordinate is in bounds
def inBounds(map,row,col):
    if row < len(map) and row >= 0 and col < len(map[0]) and col >= 0:
        return True
    else:
        return False

# directly changes the default map and fills it with rooms until a targetRooms number of rooms is created
def makeRooms(map, queue, endRooms, targetRooms, currRooms):
    startRoom = (len(map)//2, len(map[0])//2)
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    random.shuffle(dirs)
    if targetRooms <= currRooms:
        return map, endRooms
    else:
        for room in queue:
            addedRoom = False
            for dir in dirs:
                newRow = room[0] + dir[0]
                newCol = room[1] + dir[1]
                # if the neighbour cell is already occupied, give up
                if (not inBounds(map,newRow,newCol)) or map[newRow][newCol] != 0:
                    continue
                filledNeighbors = 0
                for dir2 in dirs:
                    if (inBounds(map, newRow + dir2[0], newCol + dir2[1]) and
                        map[newRow+dir2[0]][newCol+dir2[1]] != 0):
                        filledNeighbors += 1
                # if neighbor has more than 2 neighbors, give up
                if filledNeighbors >= 2:
                    continue
                # 50% chance to give up - adds some randomness to the map
                val = random.randint(0,1)
                if val != 0:
                    continue
                else:
                    # make the neighbor a new filled room
                    map[newRow][newCol] = 1
                    queue.append((newRow,newCol))
                    addedRoom = True
                    currRooms += 1
            # did not add any rooms, so the current room is an edge room
            if addedRoom == False and inBounds(map,newRow,newCol):
                endRooms.append((newRow,newCol))
        # randomly seed the start room back into the queue to keep making rooms
        if targetRooms >= 16 and random.randint(0,4) == 1:
            queue.append((startRoom))
        return makeRooms(map, queue, endRooms, targetRooms, currRooms)

################################################################################
# Room Contents:

# Things to include in rooms:   rocks, miniboss, fire, chest, bombs, cobwebs, grass, vines
def initObstacles(app):
    # rock -- IMAGE CITATION: http://pixelartmaker.com/art/f5fdad653370140
    app.rockImage = app.loadImage("rockObs.png")
    app.rockImage = app.rockImage.resize((95,95))
    # fire -- 
    app.fireImage = None
    # chest -- IMAGE CITATION: http://pixelartmaker.com/art/ea5b0b790e16511
    # open chest: http://pixelartmaker.com/art/f9fc8af2cb6d5ff
    app.openChest = app.loadImage("openChest.png")
    app.openChest = app.openChest.resize((95,95))
    app.closedChest = app.loadImage("closedChest.png")
    app.closedChest = app.closedChest.resize((95,95))


class DungeonRoom(object):
    def __init__(self,name):
        self.name = name
        self.mobs = []
        self.liveMobs = []
        self.background = None
        self.obsLocations = {}
        self.map = [[1,0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,1],]

    def __repr__(self):
        return self.name