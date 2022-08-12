import os

try:
	os.chdir("diabdat")
except:
	print("No such directory")
	quit()

# filelist = []
# for f in os.listdir("./"):
	# filelist.append(f)

filelist = []
for root, dirs, files in os.walk("."):
	for filename in files:
		filelist.append(os.path.join(root, filename))
	for dirname in dirs:
		filelist.append(os.path.join(root, dirname))

# filelist.sort()

# for f in filelist:
	# print(f)

# for root, dirs, files in os.walk("."):
	# print(dirs)
	# for f in files:
		# print(root, dirs, f, "\n")

filelist.sort()

outfile = open("filenames.txt", "w")

for f in filelist:
	outfile.write(f + "\n")

outfile.close()