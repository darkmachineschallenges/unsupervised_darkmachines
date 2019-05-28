# created by M. van Beekveld
# mcbeekveld@gmail.com
# usage: python susycommands.py "stop OR gluino_to_top" "stop OR gluino mass" "neutralino mass" "simplified OR real (only gluino)"
# e.g. python susycommands.py stop 800 100 

import os
import sys
# General settings
nevents=1000000
seed=0
beamenergy = 13000.

# Merging settings
ickkw=1
nJetMax=4
xqcut=-1

# input parameters
event_number = str(sys.argv[1])
gluino_mass = int(sys.argv[2])
neutralino_mass = int(sys.argv[3])
sim_real = str(sys.argv[4])
name = event_number
segfault = 0

if event_number == "ew_final_states":
    mgproc="""generate p p > ew ew @0
add process p p > ew ew j@1
add process p p > ew ew j j@2
"""
    name=event_number
    nJetMax=2


if event_number == "gluino_to_top":
    mgproc="""generate p p > go go @0
add process p p > go go j@1
add process p p > go go j j@2
"""
    name=event_number
    pythiaprocess='pp>gogo'
    nJetMax=2


if event_number == "stop":
    mgproc="""generate p p > t1 t1~ @0
add process p p > t1 t1~ j@1
add process p p > t1 t1~ j j@2
"""
    name=event_number
    pythiaprocess='pp>tt'
    nJetMax=2

namefile = ""
if event_number == "stop":
	namefile = "stop"+str(gluino_mass)+"_neutralino"+str(neutralino_mass)+"_converted.dat"
elif event_number == "ew_final_states":
	namefile = "EWMSSM_benchmark_"+str(gluino_mass)+"_converted.dat"
else:
	namefile = str(sim_real)+"_gluino"+str(gluino_mass)+"_neu"+str(neutralino_mass)+"_converted.dat"

print namefile
fcard = open('generate_'+event_number+'.dat','w')
fcard.write("""n
define eall = e+ e-
define veall = ve ve~
define muall = mu+ mu-
define vmall = vm vm~
define taall = ta+ ta-
define vtall = vt vt~
define w = w+ w-
define tall = t t~
define ball = b b~
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
import model MSSM_SLHA2
define ew = n1 n2 n3 n4 x1+ x2+
"""+mgproc+"""
output """+name)
fcard.close()
fcard = open('launch_'+event_number+'.dat','w')
fcard.write("""launch """+name+"""
shower=Pythia8
detector=Delphes
analysis=off
0
"""+str(namefile)+"""
run_card_modified_"""+event_number+""".dat
pythia8_card_"""+event_number+""".dat
delphes_card_ATLAS.dat

""")
fcard.close()
if(segfault == True):
	ickkw = 0
fcard1 = open('run_card_modified.dat')
fcard = open('run_card_modified_'+event_number+'.dat','w')
for line in fcard1:
	if "nevents ! Number of unweighted" in line:
		fcard.write("  "+str(nevents)+" = nevents ! Number of unweighted events requested \n")
	elif "iseed   ! rnd seed (0=assigned automatically=default))" in line:
		fcard.write("  "+str(seed)+"   = iseed   ! rnd seed (0=assigned automatically=default)) \n")
	elif "ebeam1  ! beam 1 total energy in GeV" in line:
		fcard.write("     "+str(beamenergy/2.)+"     = ebeam1  ! beam 1 total energy in GeV \n")
	elif "ebeam2  ! beam 2 total energy in GeV" in line:
		fcard.write("     "+str(beamenergy/2.)+"     = ebeam2  ! beam 2 total energy in GeV \n")
	elif "ickkw            ! 0 no matching, 1 MLM" in line:
		fcard.write(" "+str(ickkw)+" = ickkw            ! 0 no matching, 1 MLM \n")
	elif "xqcut   ! minimum kt jet measure between partons" in line:
		fcard.write(" "+str(xqcut)+"   = xqcut   ! minimum kt jet measure between partons\n")
	else:
		fcard.write(line)
fcard.close()
fcard1.close()

fcard1 = open('pythia8_card.dat')
fcard = open('pythia8_card_'+event_number+'.dat','w')
for line in fcard1:
	if "Main:numberOfEvents" in line:
		fcard.write("Main:numberOfEvents      = "+str(nevents)+"\n")	
	elif "JetMatching:nJetMax" in line:
		fcard.write("JetMatching:nJetMax  		 = "+str(nJetMax)+"\n")
	elif "partonlevel:mpi = off" in line:
		fcard.write("partonlevel:mpi = off\n")
	else:
		fcard.write(line)
fcard.close()
fcard1.close()

# check if the directory already exists
if (os.path.isdir(event_number)==False):
	os.system("./mg5_aMC < generate_"+event_number+".dat")
# launch madgraph, do showering, do detector simulation
os.system("./mg5_aMC < launch_"+event_number+".dat")
