# created by M. van Beekveld
# mcbeekveld@gmail.com
# usage: python fixed_length.py input_csv output_csv
# output is a file with fixed entries in fixed order:
# MET, METphi, jets, bjets, elec, positrons, muons-, muons+, photons
# note that now 1 quantity for MET, 1 for METphi is assumed and 3 for other objects
# if instead the convert_csv.cc script is modfied, one needs to modify the lenghts = array correspondingly!

import sys
input_csv = sys.argv[1]
output_csv = sys.argv[2]


# modify these if you want a max number of objects
maxmet = -1
maxmetphi = -1
maxjet = -1
maxbjet = -1
maxelec = -1
maxpos = -1
maxmumin = -1
maxmuplus = -1
maxgam = -1
lengths = [maxmet, maxmetphi,maxjet*3,maxbjet*3,maxelec*3,maxpos*3,maxmumin*3,maxmuplus*3,maxgam*3]
objects = [[],[],[],[],[],[],[],[],[]]
m  = 0
txt = open(input_csv)
for line in txt:
	obhold = [[],[],[],[],[],[],[],[],[]]
	if ";" in line:
		split = line.split(";")
		obhold[0].append(split[1])
		obhold[1].append(split[2])
		for k in range(3, len(split)):
			new=split[k].split(",")
			#print new[0]
			if new[0] == "j":
				for l in range(1,len(new)):
					obhold[2].append(new[l])
			elif new[0] == "b":
				for l in range(1,len(new)):
					obhold[3].append(new[l])
			elif new[0] == "e+":
				for l in range(1,len(new)):
					obhold[4].append(new[l])
			elif new[0] == "e-":
				for l in range(1,len(new)):
					obhold[5].append(new[l])
			elif new[0] == "m+":
				for l in range(1,len(new)):
					obhold[6].append(new[l])
			elif new[0] == "m-":
				for l in range(1,len(new)):
					obhold[7].append(new[l])
			elif new[0] == "a":
				for l in range(1,len(new)):
					obhold[8].append(new[l])
	for k in range(0,9):
		objects[k].append(obhold[k])
	m = m + 1
txt.close()	
txt = open(output_csv,"w")
for i in range(0,9):
	if lengths[i] < 0:
		txt.write(str(max([len(k) for k in objects[i]]))+" ")
		lengths[i] = int(max([len(k) for k in objects[i]]))
	else:
		txt.write(str(lengths[i])+" ")
txt.write("\n")
for k in range(0,m):
	linewrite = ""
	for i in range(0,9):
		for l in range(0,lengths[i]):
			if l+1 > lengths[i] and lengths[i]>=0:
				continue
			if l+1 > len(objects[i][k]):
				linewrite = linewrite+"0"+","
			else:
				linewrite=linewrite+str(objects[i][k][l])+","
	txt.write(linewrite[:-1]+"\n")
txt.close()
