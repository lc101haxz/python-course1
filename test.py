#!/usr/bin/env python3

def myprint(xyz):
	for i in range(1, xyz+1):
		if i % 3 == 0 and i % 5 == 0:
			print("0x%X FizzBuzz" % (i))
		elif i % 3 == 0:
			print("0x%X Fizz" % (i))
		elif i % 5 == 0:
			print("0x%X Buzz" % (i))

	i = 1
	while i < 30:
		print("%d" % (i))
		i += 1

def main():
	myprint(100)

if __name__ == "__main__":
	main()
