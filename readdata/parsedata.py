#!/usr/bin/env python3

# import urllib.request
# import json
import csv
import gameutils

DATAFILE = "items.tsv"

class DiabloItem():
	def __init__(self):
		self.Name = ""
		self.Class = ""
		self.MinDam = 0
		self.MaxDam = 0
		self.MinAC = 0
		self.MaxAC = 0
		self.Durability = 0
		self.MinStr = 0
		self.MinMag = 0
		self.MinDex = 0
		self.MaxValue = 0

	def AvgDamage(self):
		return (self.MinDam + self.MaxDam) / 2

def SetupItem(item_name):
	new_item = DiabloItem()
	new_item.Name = item_name["Name"]
	new_item.Class = item_name["Class"]
	new_item.MinDam = int(item_name["MinDam"])
	new_item.MaxDam = int(item_name["MaxDam"])
	new_item.MinAC = int(item_name["MinAC"])
	new_item.MaxAC = int(item_name["MaxAC"])
	new_item.Durability = int(item_name["Durability"])
	new_item.MinStr = int(item_name["MinStr"])
	new_item.MinMag = int(item_name["MinMag"])
	new_item.MinDex = int(item_name["MinDex"])
	new_item.MaxValue = int(item_name["MaxValue"])
	return new_item

def PrintItemStats(new_item):
	print(new_item.Name)
	print("Class: ", new_item.Class)
	if new_item.Class == "weap":
		print("Damage: %d to %d" % (new_item.MinDam, new_item.MaxDam))
	if new_item.Class == "armor":
		print("Armor: %d to %d" % (new_item.MinAC, new_item.MaxAC))
	print("Durability: %d" % (new_item.Durability))
	if new_item.MinStr != 0:
		print("Required Strength: %d" % (new_item.MinStr))
	if new_item.MinMag != 0:
		print("Required Magic: %d" % (new_item.MinMag))
	if new_item.MinDex != 0:
		print("Required Dexterity: %d" % (new_item.MinDex))
	print("Value:", new_item.MaxValue, "gold")

def PrintDamage(listItems):
	highest_val = 0
	for item in listItems:
		new_item = SetupItem(item)
		dmg_avg = new_item.AvgDamage()
		if dmg_avg > highest_val:
			highest_val = dmg_avg
			itemx = new_item
	PrintItemStats(itemx)
	print("\n*** %s does the most average damage at %d per hit ***" % (itemx.Name, highest_val))

def PrintArmor(listItems):
	highest_val = 0
	item_name = []
	for item in listItems:
		if int(item["MaxAC"]) > highest_val:
			highest_val = int(item["MaxAC"])
			item_name = item
	new_item = SetupItem(item_name)
	PrintItemStats(new_item)
	print("\n*** %s has the highest defense at %d ***" % (item_name["Name"], highest_val))

def PrintValue(listItems):
	highest_val = 0
	item_name = []
	for item in listItems:
		if int(item["MaxValue"]) > highest_val:
			highest_val = int(item["MaxValue"])
			item_name = item
	new_item = SetupItem(item_name)
	PrintItemStats(new_item)
	print("\n*** %s is the most expensive item at %d gold pieces ***" % (item_name["Name"], highest_val))

def PrintUsable(listItems):
	count = 0
	for item in listItems:
		if int(item["Usable"]) == 1:
			count += 1
			print(item["Name"])
	print("\n*** There are %d usable items in the game ***" % (count))

def PrintQuest(listItems):
	count = 0
	for item in listItems:
		if item["Class"] == "special":
			count += 1
			print(item["Name"])
	print("\n*** There are %d quest items in the game ***" % (count))

def PrintSpell(listItems):
	count = 0
	for item in listItems:
		if not item["Spell"].isdigit():
			count += 1
			print(item["Name"], "has spell", item["Spell"])
	print("\n*** There are %d items with spells in the game ***" % (count))

def main():
	# get option for what we want to print
	intOption = 0
	while True:
		gameutils.cls()
		print("1 - Show highest damage weapons")
		print("2 - Show highest defense armor")
		print("3 - Show most expensive items")
		print("4 - Show all useable items")
		print("5 - Show all quest items")
		print("6 - Show items with spells")

		strOption = input("Enter option:\n>")
		if not strOption.isdigit():
			continue
		intOption = int(strOption)
		if intOption >= 1 and intOption <= 6:
			break

	# read the TSV file using the CSV library
	listItems = []
	with open(DATAFILE) as csvfile:
		spamreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
		for row in spamreader:
			listItems.append(row)

	# print based on the option we chose
	gameutils.cls()
	if intOption == 1:
		PrintDamage(listItems)
	if intOption == 2:
		PrintArmor(listItems)
	if intOption == 3:
		PrintValue(listItems)
	if intOption == 4:
		PrintUsable(listItems)
	if intOption == 5:
		PrintQuest(listItems)
	if intOption == 6:
		PrintSpell(listItems)

	# wait for abort
	input("\n\nPress any key to continue...")

if __name__ == "__main__":
	main()
