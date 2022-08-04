#!/usr/bin/env python3

def TestPrime(number):
	i = 2;
	max = number / 2
	while i < max:
		remain = number % i
		if remain == 0:
			return False
		i += 1
	return True

def CheckPrime(start, stop):
	if start < 2:
		start = 2
	for i in range(start, stop+1):
		if TestPrime(i):
			print("%d is prime" % (i))

def main():
	CheckPrime(1, 100)

if __name__ == "__main__":
	main()
