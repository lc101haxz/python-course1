#!/usr/bin/env python3

# import urllib.request
# import json
import requests

SPACESITE = "http://api.open-notify.org/astros.json"

def main():
	# groundctrl = urllib.request.urlopen(SPACESITE)
	# helmet = groundctrl.read()
	# helmetson = json.loads(helmet.decode("utf-8"))

	groundctrl = requests.get(SPACESITE)
	helmetson = groundctrl.json()
	count = helmetson["number"]
	print("People in space: %d" % (count))
	for person in helmetson["people"]:
		print("%s on the %s" % (person["name"], person["craft"]))

if __name__ == "__main__":
	main()
