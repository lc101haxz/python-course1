#!/usr/bin/env python3
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

seed = 3824294
hpmin = 50
hpmax = 50
cstrength = 30
cag = 20
cint = 15

witch1 = {
	"start": "A witch confronts you and asks to show you something, do you accept?",
	"yes": "The witch leads you inside showing you a sword, she gives it to you for your quest",
	"no": "See it yourself! The witch says angerly. You proceed down the path",
	"life": 0
}

witch2 = {
	"start": "A witch confronts you and asks to teach you a spell for 30 gold pieces, do you accept?",
	"yes": "The witch teaches you the spell of ice crush. You may now use it on your foe!",
	"no": "You don't want my wisdom for your journey! The witch storms off",
	"life": 0
}

orc_confront = {
	"start": "An orc confronts you: You vikings, this is our territory! You have to fight me for it! Will you fight?",
	"yes": "So be it to the death!",
	"no": "I though so coward! Run to your king!",
	"life": 20
}

orc_nice = {
	"start": "An orc confronts you: You vikings, we want your gold! We will only retreat for 500 pounds! Will you pay?",
	"yes": "So be it!",
	"no": "Then we shall continue fighting!",
	"life": 40
}

quest_dialogs = [
	witch1,
	witch2,
	orc_confront,
	orc_nice
]

def RandSeed():
	global seed
	tempA = seed >> 16
	tempB = seed << 16
	seed = (tempA + 1) * (tempB + 1)
	salt = 0x7FED18CD
	seed = (seed * salt) & 0xFFFFFFFF

def SaltQuest():
	global seed
	qlen = len(quest_dialogs)
	res = seed * qlen / 100
	return int(res % qlen)

def GamePrint():
	print("-------------------------------------------------------------------------------")
	print("   Hero Name: Rölfan Helgstorm")
	print("       Class: Barbarian - Race: Celtic/Swedish - Age: 25")
	print("        Life: %d / %d" % (hpmin, hpmax))
	print("    Strength: %d" % (cstrength))
	print("     Agility: %d" % (cag))
	print("Intelligence: %d - Special Abilities: Might, Scavenging, Bargaining" % (cint))
	print("-------------------------------------------------------------------------------")
	RandSeed()
	print("Random Seed: 0x%08X\n" % (seed))

def CheckLife():
	global hpmin
	if hpmin > 0:
		return
	cls()
	print("-------------------------------------------------------------------------------")
	print("Game over! You have died!")
	input("Press any key to exit...")
	quit()

def RunQuest():
	global hpmin
	cls()
	GamePrint()
	q = SaltQuest()
	print(quest_dialogs[q]["start"])
	action = input("Action: (yes/no): ")

	# salt the seed twice for yes, once for no
	# this gives us pseudo-randomness from the users' action
	if action == "yes":
		RandSeed()
		RandSeed()
	elif action == "no":
		RandSeed()

	print(quest_dialogs[q][action])
	val = int(quest_dialogs[q]["life"])
	if val != 0:
		hpmin -= quest_dialogs[q]["life"]
		print("You take %d damage!" % (val))
		CheckLife()

	input("\nPress any key to continue...")

def main():
	cls()
	GamePrint()
	print("You leave your home in Stockholm Sweden and set out for quest")
	print("The king has summoned you to fight Orcs invading south of the village")
	print("You begin traveling down to Skåne but arrive at a mysterious house")
	input("\nPress any key to continue...")
	while 1:
		RunQuest()

if __name__ == "__main__":
	main()
