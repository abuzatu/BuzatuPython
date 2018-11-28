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
verbose=True

factor_charged_to_charged=1/math.e
factor_charged_to_neutral=1-factor_charged_to_charged
factor_neutral_to_charged=0.5

dict_name_tuple_tuple_name_factor={
    "electron":(("positron",factor_charged_to_charged),("photon",factor_charged_to_neutral)),
    "positron":(("electron",factor_charged_to_charged),("photon",factor_charged_to_neutral)),
    "photon":(("electron",factor_neutral_to_charged),("positron",factor_neutral_to_charged)),
}

# energy unit in MeV
energy_cutOff_charged=7.6
energy_cutOff_neutral=1.0

dict_name_energy_cutOff={
    "electron":"energy_cutOff_charged",
    "positron":"energy_cutOff_charged",
    "photon":"energy_cutOff_neutral",
}

#######################################################
#### Class Analysis                                 ###
#######################################################

class Particle:
    """Particle class, to add the mostly common function"""
    """To not have to write them any time we do a new analysis"""

    ### init 
    def __init__(self,name,energy):
        self.name=name
        self.energy=name
    # done function

    ### setters


#################################################################
################### Functions ###################################
#################################################################

def doItAll():
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
