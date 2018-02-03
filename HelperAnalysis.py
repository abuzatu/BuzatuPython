# !/usr/bin/python
# Adrian Buzatu (adrian.buzatu@cern.ch)
# 03 Feb 2017, Python classes to summarise most common steps 
# when doing a data analysis, like looping about categories, variables,
# summing up the singals and the backgrounds and data
# to stacked plots
# do sensitivies and yiels, in each category and combined
# to easily to optimisation studies
# comparison of a given process from different DSID, etc

from HelperPyRoot import *
import subprocess
from sets import Set

#######################################################
#### Dummy                                          ###
#######################################################

class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        print 'hello world'
# done class

#######################################################
#### Class Analysis                                 ###
#######################################################

class Analysis:
    """Analysis class, to add the mostly common function"""
    """To not have to write them any time we do a new analysis"""

    ### init 
    def __init__(self,name):
        self.name=name
        self.list_category=[] # empty list to store the categories
    # done function

    ### setters

    def set_debug(self,debug):
        self.debug=debug
    
    def set_folderInput(self,folderInput):
        self.folderInput=folderInput

    def set_folderOutput(self,folderOutput):
        self.folderOutput=folderOutput
        os.system("mkdir -p "+ self.folderOutput)

    def set_doHaddProcessInitial(self,doHaddProcessInitial):
        self.doHaddProcessInitial=doHaddProcessInitial  

    def add_category(self,category):
        self.list_category.append(category)

    def set_list_category(self,list_category):
        self.list_category=list_category
 
    ### actions

    def evaluate_list_processInitial(self):
        p = subprocess.Popen(
            ['ls', '/Users/abuzatu/data/Reader/Jan30/mc16c_MVA_PRWApplied'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
            )
        result=p.communicate()
        output=result[0]
        error=result[1]
        # 
        set_processInitial=Set()
        for fileName in output.split():
            if self.debug:
                print "fileName",fileName
            # e.g. hist-data17-3.root
            list_fileNameElement=fileName.split("-")
            processInitial=list_fileNameElement[1]
            if self.debug:
                print "processInitial",processInitial
            set_processInitial.add(processInitial)
        # done for loop
        # sort alphabetically the set, it returns a list
        self.list_processInitial=sorted(set_processInitial)
        if self.debug:
            print "list_processInitial",self.list_processInitial
            for processInitial in self.list_processInitial:
                print "processInitial",processInitial
    # done function

    def hadd_each_processInitial(self):
        self.folderProcessInitial=self.folderOutput+"/processInitial"
        os.system("mkdir -p "+self.folderProcessInitial)
        for processInitial in self.list_processInitial:
            output=self.folderProcessInitial+"/"+processInitial+".root"
            inputs=self.folderInput+"/hist-"+processInitial+"-*.root"
            command="hadd -f "+output+" "+inputs
            if self.debug:
                print "command",command
            os.system(command)
    # done function
        
  ### print

    def print_list_category(self):
        print "list_category",self.list_category

    def print_all(self):
        print ""
        print "Printing all for Analysis",self.name,":"
        self.print_list_category()
        print "debug",self.debug
        print "folderInput",self.folderInput
        print "folderOutput",self.folderOutput
        print "list_processInitial",self.list_processInitial
       
    ### summary

    def do_all(self):
        self.evaluate_list_processInitial()
        if self.doHaddProcessInitial:
            self.hadd_each_processInitial()
        self.print_all()

    ### done methods

# done class

