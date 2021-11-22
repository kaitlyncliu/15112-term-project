import random
import copy

# 1 represents open door, 0 represents closed door
# room templates will be represented by (north, east, south, west)
#  1
# 1 1
#  1
startRoom = (1, 1, 1, 1) 
#  0
# 0 0
#  1
sRoom = (0, 0, 1, 0)
#  0
# 1 0
#  0
wRoom = (0, 0, 0, 1)
#  1
# 0 0
#  0
nRoom = (1, 0, 0, 0)
#  0
# 0 1
#  0
eRoom = (0, 1, 0, 0)
#  0
# 1 1
#  0
ewRoom = (0, 1, 0, 1)
#  0
# 0 1
#  1
esRoom = (0, 1, 1, 0)
#  1
# 0 1
#  0
neRoom = (1, 1, 0, 0)
#  1
# 0 0
#  1
nsRoom = (1, 0, 1, 0)
#  1
# 1 0
#  0
nwRoom = (1, 0, 0, 1)
#  1
# 1 1
#  0
newRoom = (1, 1, 0, 1)
#  1
# 0 1
#  1
nesRoom = (1, 1, 1, 0)
#  1
# 1 0
#  1
nswRoom = (1, 0, 1, 1)
#  0
# 1 1
#  1
eswRoom = (0, 1, 1, 1)


roomList = [startRoom, nRoom, eRoom, sRoom, wRoom, neRoom, nwRoom, ewRoom, esRoom, nsRoom, nesRoom, newRoom, nswRoom, eswRoom]

# checks to see if a new room is valid based on current dungeon map
def checkValidRoom(map, row, col, room):
    # there is already a room at the location or the room is out of bounds
    if (row >= len(map) or row < 0 or col >= len(map[0]) or col < 0
        or map[row][col] != None):
        return False
    dirs = [(-1,0),(0,1),(1,0),(0,-1)]
    # s of room above must be open if north of current room is open
    # w of room to the right open if e of current room is open
    # n of room below must be open if s current room open
    # e of room to the left open if w of current room is open
    # index + 2 to get the room that should be open
    for i in range(len(room)):
        connectingRoom = map[row+dirs[i][0]][col+dirs[i][1]]
        # room is empty, do nothing
        if connectingRoom == None:
            continue
        connectingRoomSide = connectingRoom[(i+2)%len(room)]
        if connectingRoomSide != room[i]:
            return False
    return True



# following a similar set of guidelines for map gen as those in Binding of Isaac, as stated here:
# https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/
# code is all by me though

'''
For each cell in the queue, it loops over the 4 cardinal directions and does the following:

Determine the neighbour cell by adding +10/-10/+1/-1 to the currency cell.
If the neighbour cell is already occupied, give up
If the neighbour cell itself has more than one filled neighbour, give up.
If we already have enough rooms, give up
Random 50% chance, give up
Otherwise, mark the neighbour cell as having a room in it, and add it to the queue.
'''

def getTargetRooms(level):
    rooms = int(level*1.4 + 8 + random.randint(4))
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
    makeSpecialRooms(resultMap,endRooms)

def makeSpecialRooms(map, endRooms):
    bossLocation = endRooms[-1]
    map[bossLocation[0]][bossLocation[1]] = "bossRoom"
    treasureLocation = endRooms[-2]
    map[treasureLocation[0]][treasureLocation[1]] = "treasureRoom"
    rows = len(map)
    cols = len(map[0])
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    secretRoomPlaced = False
    minRoomsNear = 3
    while minRoomsNear > 0:
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
                if neighbors < minRoomsNear:
                    map[row][col] = "secretRoom"
                    secretRoomPlaced = True
        # loosens constraints if a room can't be placed
        if secretRoomPlaced == False:
            minRoomsNear -= 1
        

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
    if targetRooms <= currRooms:
        return map, endRooms
    else:
        for room in queue:
            addedRoom = False
            for dir in dirs:
                newRow = room[0] + dir[0]
                newCol = room[1] + dir[1]
                # if the neighbour cell is already occupied, give up
                print(newRow,newCol,inBounds(map,newRow,newCol))
                if not inBounds(map,newRow,newCol) or map[newRow][newCol] != 0:
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
            if addedRoom == False:
                endRooms.append((newRow,newCol))
        # randomly seed the start room back into the queue to keep making rooms
        if targetRooms >= 16 and random.randint(0,2) == 1:
            queue.append((startRoom))
        return makeRooms(map, queue, endRooms, targetRooms, currRooms)

# this is incomplete but will keep placing rooms until the map is walkable and 
# the board is at least 75% full 
'''
def makeFloor(map):
    map = copy.deepcopy(mapsList[random.randint(0,len(mapsList)-1)])
    # can successfully make it from the boss room to the spawn room
    # may or may not be possible to make it to potion room on each floor
    if map == defaultMap:
        startRow = 0
        startCol = 0
    else:
        startRow = 0
        startCol = 4
    if walkable(map,startRow,startCol,(5,2)):
        return map
    else:
        for i in range(len(map)):
            for j in range(len(map[0])):
                randomRoom = roomList[random.randint(0,len(roomList)-1)]
                if checkValidRoom(map,i,j,randomRoom):
                    map[i][j] == randomRoom'''

# backtracker that checks if a path from the boss room to the spawn 
# exists on the map
def walkable(map, row, col, tgt):
    if (row,col) == tgt:
        return True
    else:
        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        for i in range(dirs):
            dir = dirs[i]
            newRow = row + dir[0]
            newCol = col + dir[1]
            if inBounds(map,newRow,newCol) and map[newRow][newCol] != None:
                result = walkable(map,newRow,newCol,tgt)
                if result != False:
                    return True
        return False


###############################################
# Test Functions
'''
def testCheckValidRoom():
    print("Testing checkValidRoom...", end=" ")
    testMap = [[room7,room5,room7,room4],
               [room8,None,None,None],
               [None,None,None,None],
               [None,None,None,None]]

    assert(checkValidRoom(testMap, 0, 2, room3) == False)
    assert(checkValidRoom(testMap, 1, 1, room1) == True)
    assert(checkValidRoom(testMap, 0, 0, room1) == False)
    print("Passed!")'''

def testWalkable():
    print("Testing walkable...", end=" ")
    testMap = [[]]

#################################################
#testCheckValidRoom()