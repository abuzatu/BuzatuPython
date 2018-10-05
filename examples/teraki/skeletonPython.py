#!/usr/bin/python
from HelperPyRoot import *
ROOT.gROOT.SetBatch(True)

total = len(sys.argv)
# number of arguments plus 1
if total!=1:
    print "You need some arguments, will ABORT!"
    print "Ex: ",sys.argv[0]," "
    assert(False)
# done if

#################################################################
################### Configurations ##############################
#################################################################

debug=True
list_option="A".split(",")

#################################################################
################### Functions ###################################
#################################################################

def doItOne(option):
    if debug:
        print "doItOne() with option",option
    

    None
# done function

def doItAll():
    for option in list_option:
        if debug:
            print "option",option
        doItOne(option)
    None  
# done function

#################################################################
################### Run #########################################
#################################################################

doItAll()

#################################################################
################### Finished ####################################
#################################################################

print ""
print ""
print "Finished all in",sys.argv[0]
