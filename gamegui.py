#!/usr/bin/env python3
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# ASCII tile map of our level
game_map = [
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

warpx = 0
warpy = 0

map_width = 50
map_height = 18

playerx = 0
playery = 0

lastaction = ""
total_moves = 0
inventory = []

# -----------------------------------------------------------------------------
# retrive the specified byte value at (x,y) in game map
def GetTile(x, y):
	return game_map[x + y * map_width]

def SetTile(tile, x, y):
	game_map[x + y * map_width] = tile

def AddRoom(x1, y1, w, h):
	x = 0
	y = 0
	x2 = x1 + w
	y2 = y1 + h
	for tile in game_map:
		if x >= x1 and x <= x2 and y >= y1 and y <= y2:
			game_map[x + y * map_width] = ' '
		x += 1
		if x == map_width:
			x = 0
			y += 1

def AddHHall(x1, y1, w):
	AddRoom(x1, y1, w, 0)

def AddVHall(x1, y1, h):
	AddRoom(x1, y1, 0, h)

def PrintTile(tile, x, y):
	if x == playerx and y == playery:
		print("\u2660", end="")
	elif tile == 0:
		print("\u2592", end="")
	else:
		print(tile, end="")

def PrintGameMap():
	x = 0
	y = 0
	for tile in game_map:
		PrintTile(tile, x, y)
		x += 1
		if x == map_width:
			x = 0
			y += 1
			print("")

# -----------------------------------------------------------------------------
def AddInventory(item_name, x, y):
	inventory.append(item_name)
	SetTile(' ', x, y)

def RemoveInventory(item_name):
	inventory.remove(item_name)

# -----------------------------------------------------------------------------
def MovePlayer(deltax, deltay):
	global playerx, playery, total_moves
	tempx = playerx + deltax
	tempy = playery + deltay
	if tempx < 0 or tempx >= map_width:
		return
	if tempy < 0 or tempy >= map_height:
		return
	# player can't be on solid space
	if GetTile(tempx, tempy) == 0:
		return
	total_moves += 1
	playerx += deltax
	playery += deltay
	# player tries to open door
	if GetTile(tempx, tempy) == 'D':
		CheckDoor(tempx, tempy)
	# player gets a key
	if GetTile(tempx, tempy) == 'K':
		AddInventory("key", tempx, tempy)
	# player warps
	if GetTile(tempx, tempy) == 'W':
		playerx = warpx
		playery = warpy
		SetTile('K', 12, 12)

# slightly annoying movement since we must press enter
# for this reason, store last move
def DoLastMove():
	if lastaction == "w":
		MovePlayer(0, -1)
	elif lastaction == "s":
		MovePlayer(0, +1)
	elif lastaction == "a":
		MovePlayer(-1, 0)
	elif lastaction == "d":
		MovePlayer(+1, 0)

def DecideMove():
	global lastaction
	action = input("Move: (w/a/s/d): ")
	if action == "w":
		MovePlayer(0, -1)
		lastaction = action
	elif action == "s":
		MovePlayer(0, +1)
		lastaction = action
	elif action == "a":
		MovePlayer(-1, 0)
		lastaction = action
	elif action == "d":
		MovePlayer(+1, 0)
		lastaction = action
	elif action == "":
		DoLastMove()

# -----------------------------------------------------------------------------
def GenerateHouse(startx, starty):
	global playerx, playery
	playerx = startx
	playery = starty
	AddRoom(5, 1, 12, 5) # main room
	AddRoom(25, 1, 8, 5) # kitchen
	AddRoom(5, 10, 8, 5) # bedroom
	AddHHall(18, 3, 8) # main room -> kitchen
	AddVHall(9, 7, 3) # main room -> bedroom
	SetTile('K', 12, 12) # add key
	SetTile('D', 34, 1) # door to garage
	SetTile('D', 14, 13) # door to garage

def OpenGarage():
	global warpx, warpy
	AddRoom(37, 1, 5, 7) # garage
	AddHHall(35, 1, 1) # kitchen -> garage
	SetTile('W', 40, 4)
	SetTile('K', 42, 8)
	warpx = 9
	warpy = 14

def OpenPatio():
	AddRoom(16, 11, 10, 3) # patio
	AddHHall(15, 13, 3) # bedroom -> patio
	SetTile('K', 22, 12)
	SetTile('D', 27, 14)

def OpenOutside():
	AddRoom(30, 14, 10, 2) # outside
	AddHHall(28, 14, 1) # patio -> outside
	SetTile('D', 37, 17)

def CheckDoor(x, y):
	if x == 34 and y == 1:
		if "key" in inventory:
			RemoveInventory("key")
			OpenGarage()
	if x == 14 and y == 13:
		if "key" in inventory:
			RemoveInventory("key")
			OpenPatio()
	if x == 27 and y == 14:
		if "key" in inventory:
			RemoveInventory("key")
			OpenOutside()
	if x == 37 and y == 17:
		if "key" in inventory:
			RemoveInventory("key")
			cls()
			input("Congrats you won! Press any key to exit")
			exit()

# -----------------------------------------------------------------------------
def RunGameLoop():
	cls()
	PrintGameMap()
	print("(%d,%d) - Moves: %d" % (playerx, playery, total_moves))
	print("Inventory: ", end="")
	for item in inventory:
		print("\"" + item + "\" ", end="")
	print("")
	DecideMove()

def main():
	GenerateHouse(8, 5)
	while 1:
		RunGameLoop()

if __name__ == "__main__":
	main()
