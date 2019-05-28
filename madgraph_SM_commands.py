#created by M. van Beekveld
#mcbeekveld@gmail.com
#usage: python possibilities
#where possibilies is one of the options in the array possibilities
#feel free to add more possibilities if necessary
#place this in the ./bin dir of madgraph, make sure that pythia and delphes are installed
#also place the files delphes_card_ATLAS.dat, pythia8_card.dat and run_card_modified.dat
# in the same directory
import random
import os
import sys
# General settings
nevents=1000000
seed=random.randint(1,100000) #note that banner.py in madgraph/various needs to be modified to be able to handle this.
beamenergy = 13000.
# note that in the run_card_modified file this is all preset. Also we don't use systematics,
# this creates an array of weights, which cannot be used in delphes
# Merging settings, we use MLM
ickkw=1
nJetMax=4
# some processes cannot be matched. Madgraph developers know this and are working to solve the problem
# for now, just use LO without extra jet matrix element
segfault = False
# default/average value
xqcut=20
# pythiaprocess only necessary for CKKW matching, we don't use that now. 
pythiaprocess = ""
#metmin
metmin=0.
possibilities=["2jets","3jets","4jets","njets","z_jets","znuall_jets","w_jets","Wene_jets","Wmune_jets","Wtaune_jets", "Zee_jets","Zmumu_jets","Ztautau_jets","gam_jets","4top","ttbarHiggs",
"ttbarGam","ttbarZ","ttbarW","ttbarWW","ttbar_jets","single_top","single_topbar","wtop","wtopbar",
"ztop","ztopbar","atop","atopbar","zz_jets","zw_jets","ww_jets"]
event_number = str(sys.argv[1])


if event_number not in possibilities:
	print "Wrong event indicated!:"+event_number
	print "choose one from: "
	print possibilities
	print "for SUSY processes, use susycommands.py"
	exit()
	
# QCD DOES NOT WORK
if event_number == "njets":
    mgproc="""generate p p > j j @0
add process p p > j j j @1
add process p p > j j j j @2
"""
    name='njets'
    nJetMax=2
# z > nubar nu + jets
if event_number == "znuall_jets":
    mgproc="""generate p p > nuall nuall @0
add process p p > nuall nuall j @1
add process p p > nuall nuall j j @2
"""
    name='znuall_jets'
    nJetMax=2
    xqcut = 10

# z + jets
if event_number == "z_jets":
    mgproc="""generate p p > z @0
add process p p > z j @1
add process p p > z j j @2
"""
    name='z_jets'
    nJetMax=2
    xqcut = 10


if event_number == "w_jets":
    mgproc="""generate p p > w @0
add process p p > w j @1
add process p p > w j j @2
"""
    name='w_jets'
    nJetMax=2
    xqcut = 10
        
    
if event_number == "Wene_jets":
    mgproc="""generate p p > eall veall @0
add process p p > eall veall j @1
add process p p > eall veall j j @2
"""
    name='Wene_jets'
    pythiaprocess='pp>LEPTONS,NEUTRINOS'
    nJetMax=2
    xqcut = 10

# W > mu nu + jets    
if event_number == "Wmune_jets":
    mgproc="""
generate p p > muall vmall @0
add process p p > muall vmall j @1
add process p p > muall vmall j j @2
"""
    name='Wmune_jets'
    pythiaprocess='pp>LEPTONS,NEUTRINOS'
    nJetMax=2
    xqcut = 10
    
# W > tau nu + jets
if event_number == "Wtaune_jets":
    mgproc="""
generate p p > taall vtall @0
add process p p > taall vtall j @1
add process p p > taall vtall j j @2
"""
    name='Wtaune_jets'
    pythiaprocess='pp>LEPTONS,NEUTRINOS'
    nJetMax=2
    xqcut = 10
#Z / gam -> ee + jets
if event_number == "Zee_jets":
    mgproc="""generate p p > e+ e- @0
add process p p > e+ e- j @1
add process p p > e+ e- j j @2
"""
    name=event_number 
    pythiaprocess='pp>e+e-'
    nJetMax=2
    xqcut = 10
#Z / gam -> mu + jets
if event_number == "Zmumu_jets":
    mgproc="""generate p p > mu+ mu- @0
add process p p > mu+ mu- j @1
add process p p > mu+ mu- j j @2
"""
    name=event_number 
    pythiaprocess='pp>mu+mu-'
    nJetMax=2
    xqcut = 10
#Z / gam -> tautau + jets
if event_number == "Ztautau_jets":
    mgproc="""generate p p > ta+ ta- @0
add process p p > ta+ ta- j @1
add process p p > ta+ ta- j j @2
"""
    name=event_number 
    
    pythiaprocess='pp>ta+ta-'
    nJetMax=2
    xqcut = 10
    
#gam + jets
if event_number == "gam_jets":
    mgproc="""generate p p > a j @0
add process p p > a j j @1
"""
    name=event_number 
    
    pythiaprocess='pp>aj'
    nJetMax=2

# ww
if event_number == "ww_jets":
    mgproc="""generate p p > w- w+ @0
add process p p > w- w+ j @1
add process p p > w- w+ j j @2
"""
    name=event_number 
    pythiaprocess='pp>w+w-'
    nJetMax=2


# wz
if event_number == "zw_jets":
    mgproc="""generate p p > w z @0
add process p p > w z j @1
add process p p > w z j j @2
"""
    name=event_number 
    
    pythiaprocess='pp>wz'
    nJetMax=2

# zz
if event_number == "zz_jets":
    mgproc="""generate p p > z z @0
add process p p > z z j @1
add process p p > z z j j @2
"""
    name=event_number 
    
    pythiaprocess='pp>zz'
    nJetMax=2

# wtops_tchan
if event_number == "single_top":
    mgproc="""import model sm-ckm
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
generate p p > t j @0
add process p p > t j j@1
add process p p > t j j j @2
"""
    name=event_number 
    pythiaprocess='pp>tj'
    nJetMax=3

if event_number == "single_topbar":
    mgproc="""import model sm-ckm
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
generate p p > t~ j @0
add process p p > t~ j j@1
add process p p > t~ j j j @2
"""
    name=event_number 
    pythiaprocess='pp>t~j'
    nJetMax=3

# wtops
if event_number == "wtop":
    mgproc="""import model sm-ckm
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
generate p p > t w @0
add process p p > t w j@1
add process p p > t w j j@2
"""
    name=event_number  
    pythiaprocess='pp>tW'
    nJetMax=2  
    
if event_number == "wtopbar":
    mgproc="""import model sm-ckm
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
generate p p > t~ w @0
add process p p > t~ w j@1
add process p p > t~ w j j@2
"""
    name=event_number  
    pythiaprocess='pp>t~W' 
    nJetMax=2  

# ztops
if event_number == "ztop":
    mgproc="""generate p p > t z @0
add process p p > t z j@1
add process p p > t z j j@2
"""
    name=event_number 
    pythiaprocess='pp>tz'
    nJetMax=2


if event_number == "ztopbar":
    mgproc="""generate p p > t~ z @0
add process p p > t~ z j@1
add process p p > t~ z j j@2
"""
    name=event_number 
    pythiaprocess='pp>t~z' 
    nJetMax=2
 

if event_number == "atop":
    mgproc="""generate p p > t a @0
add process p p > t a j@1
add process p p > t a j j@2
"""
    name=event_number 
    pythiaprocess='pp>ta' 
    nJetMax=2


if event_number == "atopbar":
    mgproc="""generate p p > t~ a @0
add process p p > t~ a j@1
add process p p > t~ a j j@2
"""
    name=event_number 
    pythiaprocess='pp>t~a'
    nJetMax=2 
# ttbar
if event_number == "ttbar_jets":
    mgproc="""generate p p > t t~ @0
add process p p > t t~ j @1
add process p p > t t~ j j @2
"""
    name=event_number 
    
    pythiaprocess='pp>tt~'
    nJetMax=2


# ttbarW
if event_number == "ttbarW":
    mgproc="""generate p p > t t~ w @0
"""
    name=event_number 
    segfault = True

# ttbarWW
if event_number == "ttbarWW":
    mgproc="""generate p p > t t~ w w @0
"""
    name=event_number 
    pythiaprocess='pp>tt~WW'
    segfault = True

# ttbarZ
if event_number == "ttbarZ":
    mgproc="""generate p p > t t~ z @0
"""
    name=event_number 
    segfault = True


# ttbarGam
if event_number == "ttbarGam":
    mgproc="""generate p p > t t~ a @0
add process p p > t t~ a j @1
"""
    name=event_number 
    pythiaprocess='pp>tt~a'
    nJetMax=1



# ttbarHiggs
if event_number == "ttbarHiggs":
    mgproc="""generate p p > t t~ h @0
add process p p > t t~ h j @1
"""
    name=event_number
    pythiaprocess='pp>tt~h'
    nJetMax=1
      
# 4top
if event_number == "4top":
    mgproc="""generate p p > t t~ t t~@0
"""
    name=event_number 
    pythiaprocess='pp>tt~tt~'
    segfault = True

fcard = open('generate_'+event_number+'.dat','w')
fcard.write("""define eall = e+ e-
define veall = ve ve~
define muall = mu+ mu-
define vmall = vm vm~
define taall = ta+ ta-
define vtall = vt vt~
define nuall = ve ve~ vm vm~ vt vt~
define w = w+ w-
define tall = t t~
define ball = b b~
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
"""+mgproc+"""
output """+name)
fcard.close()
fcard = open('launch_'+event_number+'.dat','w')
fcard.write("""launch """+name+"""
shower=Pythia8
detector=Delphes
analysis=off
0
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
	elif "! minimum missing Et (sum of neutrino's momenta)" in line:
		fcard.write(" "+str(metmin)+"  = misset    ! minimum missing Et (sum of neutrino's momenta)\n")
	else:
		fcard.write(line)
fcard.close()
fcard1.close()

fcard1 = open('pythia8_card.dat')
fcard = open('pythia8_card_'+event_number+'.dat','w')
for line in fcard1:
	if "Main:numberOfEvents" in line:
		fcard.write("Main:numberOfEvents      = "+str(nevents)+"\n")	
	elif "JetMatching:nJetMax" in line: #needed for the matching, safe to set it
		fcard.write("JetMatching:nJetMax  		 = "+str(nJetMax)+"\n")
	elif "partonlevel:mpi = off" in line: #MPI
		fcard.write("!partonlevel:mpi = off\n")
	else:
		fcard.write(line)
fcard.close()
fcard1.close()

# check if the directory already exists
if (os.path.isdir(event_number)==False):
	os.system("./mg5_aMC < generate_"+event_number+".dat")
# launch madgraph, do showering, do detector simulation
os.system("./mg5_aMC < launch_"+event_number+".dat")
