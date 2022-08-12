#!/usr/bin/env python3

def main():
	vcount = 0
	with open("dracula.txt", "r", encoding="utf-8") as bookfile:
		with open("vampytimes.txt", "w", encoding="utf-8") as outfile:
			for currline in bookfile:
				if "vampire" in currline.lower():
					vcount += 1
					print(currline)
					outfile.write(currline)

	print("Vampire occurs %d times" % (vcount))

main()