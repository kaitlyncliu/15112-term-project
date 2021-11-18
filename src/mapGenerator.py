import random
import copy
from graphics import *

# 1 represents open door, 0 represents closed door
# room templates will be represented by (north, east, south, west)
# will make rooms into a class later
#  1
# 1 0
#  0
room1 = (1, 0, 0, 1)
#  1
# 1 1
#  1
room2 = (1, 1, 1, 1)
#  0
# 1 1
#  1
room3 = (0, 1, 1, 1)
#  1
# 0 0
#  0
room4 = (1, 0, 0, 0)
#  0
# 1 0
#  1
room5 = (0, 0, 1, 1)
#  0
# 1 1
#  0
room6 = (0, 1, 0, 1)
#  0
# 0 1
#  1
room7 = (0, 1, 1, 0)
#  1
# 0 1
#  0
room8 = (1, 1, 0, 0)

roomList = [room1,room2,room3,room4,room5,room6,room7,room8]

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

defaultMap1 = [[leftBossRoom, None, None,       None, shopRoom2],
              [None,          None, None,       None, None],
              [None,          None, potionRoom, None, None],
              [None,          None, None,       None, None],
              [None,          None, None,       None, None],
              [None,          None, spawnRoom,  None, None]]


defaultMap2 = [ [shopRoom2,  None, None,       None, rightBossRoom],
                [None,       None, None,       None, None],
                [None,       None, potionRoom, None, None],
                [None,       None, None,       None, None],
                [None,       None, None,       None, None],
                [None,       None, spawnRoom,  None, None]    ]

mapsList = [defaultMap1,defaultMap2]

# this is incomplete but will keep placing rooms until the map is walkable and 
# the board is at least 75% full 
def makeFloor(map):
    map = copy.deepcopy(mapsList[random.randint(0,len(mapsList)-1)])
    # can successfully make it from the boss room to the spawn room
    # may or may not be possible to make it to potion room on each floor
    if map == defaultMap1:
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
                    map[i][j] == randomRoom

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
            if (newRow < len(map) and newRow >= 0 and newCol < len(map[0])
                and newCol >=0 and map[newRow][newCol] != None):
                result = walkable(map,newRow,newCol,tgt)
                if result != False:
                    return True
        return False

###############################################
# Test Functions

def testCheckValidRoom():
    print("Testing checkValidRoom...", end=" ")
    testMap = [[room7,room5,room7,room4],
               [room8,None,None,None],
               [None,None,None,None],
               [None,None,None,None]]

    assert(checkValidRoom(testMap, 0, 2, room3) == False)
    assert(checkValidRoom(testMap, 1, 1, room1) == True)
    assert(checkValidRoom(testMap, 0, 0, room1) == False)
    print("Passed!")

#################################################
testCheckValidRoom()