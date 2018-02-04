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
####                                                ###
#######################################################



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

    def set_do_evaluate_list_processInitial(self,do_evaluate_list_processInitial):
        self.do_evaluate_list_processInitial=do_evaluate_list_processInitial

    def set_list_processInitial(self,list_processInitial):
        self.list_processInitial=list_processInitial

    def set_do_hadd_processInitial(self,do_hadd_processInitial):
        self.do_hadd_processInitial=do_hadd_processInitial  

    def add_category(self,category):
        self.list_category.append(category)

    def set_list_processInitial(self,list_processInitial):
        self.list_processInitial=list_processInitial

    def set_list_category(self,list_category):
        self.list_category=list_category

    def set_list_variable(self,list_variable):
        self.list_variable=list_variable

    def set_list_process(self,list_process):
        self.list_process=list_process

    def set_do_evaluate_content_of_all_processInitial(self,do_evaluate_content_of_all_processInitial):
        self.do_evaluate_content_of_all_processInitial=do_evaluate_content_of_all_processInitial
 
    ### actions

    def create_folderProcessInitial(self):
        self.folderProcessInitial=self.folderOutput+"/processInitial"
        os.system("mkdir -p "+self.folderProcessInitial)
    # done function

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
        list_processInitial=sorted(set_processInitial)
        if self.debug:
            print "list_processInitial",list_processInitial
            for processInitial in list_processInitial:
                print "processInitial",processInitial
                # create the python file with the lists
        outputFile=open(self.folderProcessInitial+"/list_processInitial.txt","w")
        for processInitial in list_processInitial:
            outputFile.write(processInitial+"\n")
    # done function

    def set_list_processInitial(self,list_processInitial):
        self.list_processInitial=list_processInitial
        if self.debug:
            print "list_processInitial",self.list_processInitial
            for processInitial in self.list_processInitial:
                print "processInitial",processInitial
    # done function

    def set_evaluated_list_processInitial(self):
        fileName=self.folderProcessInitial+"/list_processInitial.txt"
        self.list_processInitial=get_list_from_file(fileName,self.debug)
    # done function

    def hadd_each_processInitial(self):
        for processInitial in self.list_processInitial:
            output=self.folderProcessInitial+"/"+processInitial+".root"
            inputs=self.folderInput+"/hist-"+processInitial+"-*.root"
            command="hadd -f "+output+" "+inputs
            if self.debug:
                print "command",command
            os.system(command)
    # done function

    def evaluate_content_of_one_processInitial(self,processInitial,debug):
        fileName=self.folderProcessInitial+"/"+processInitial+".root"
        directoryPath=""
        searchClass="TH1F"
        list_searchName=["",""]
        doOption="C"
        doShowIntegral=False
        outputFileName=self.folderProcessInitial+"/"+processInitial+"_content.txt"
        list_objectName=listObjects(fileName,directoryPath,searchClass,list_searchName,doOption,doShowIntegral,outputFileName,debug=debug)
        if debug:
            for objectName in list_objectName:
                print "objectName",objectName
        return list_objectName
    # done function
        
    def evaluate_content_of_all_processInitial(self):
        set_process=Set()
        set_category=Set()
        set_variable=Set()
        for processInitial in self.list_processInitial:
            if True:
                print "processInitial",processInitial
            list_histoName=self.evaluate_content_of_one_processInitial(processInitial,False)
            for histoName in list_histoName:
                # e.g. ttbar_3ptag5pjet_150ptv_SR_yBB
                list_histoNameElement=histoName.split("_")
                process=list_histoNameElement[0] # first element e.g. ttbar
                category=list_histoNameElement[1]+"_"+list_histoNameElement[2]+"_"+list_histoNameElement[3] # next three elements, eg. 3ptag5pjet_150ptv_SR
                variable=histoName.replace(process+"_"+category+"_","") # the rest, tricky as sometimes the name has an _ in it
                if self.debug:
                    print "histoName",histoName,"list_histoNameElement",list_histoNameElement,"process",process,"category",category,"variable",variable
                set_process.add(process)
                set_category.add(category)
                set_variable.add(variable)
            # done for loop over histoName
        # done for loop over processInitial
        list_process=sorted(set_process)
        list_category=sorted(set_category)
        list_variable=sorted(set_variable)
        if self.debug:
            print "list_process",list_process
            for process in list_process:
                print "process",process
            print "list_category",list_category
            for category in list_category:
                print "category",category
            print "list_variable",list_variable
            for variable in list_variable:
                print "variable",variable
        # create the python file with the lists
        # list_process
        outputFile=open(self.folderProcessInitial+"/list_process.txt","w")
        for process in list_process:
            if "QQ2H" in process or "GG2H" in process or process=="UNKNOWN":
                continue
            outputFile.write(process+"\n")
        outputFile.close()
        # list_category
        outputFile=open(self.folderProcessInitial+"/list_category.txt","w")
        for category in list_category:
            outputFile.write(category+"\n")
        outputFile.close()
        # list_variable
        outputFile=open(self.folderProcessInitial+"/list_variable.txt","w")
        for variable in list_variable:
            outputFile.write(variable+"\n")
        outputFile.close()
    # done function
            
    def set_evaluated_list_process(self):
        fileName=self.folderProcessInitial+"/list_process.txt"
        self.list_process=get_list_from_file(fileName,self.debug)
    # done function 

    def set_evaluated_list_category(self):
        fileName=self.folderProcessInitial+"/list_category.txt"
        self.list_category=get_list_from_file(fileName,self.debug)
    # done function 

    def set_evaluated_list_variable(self):
        fileName=self.folderProcessInitial+"/list_variable.txt"
        self.list_variable=get_list_from_file(fileName,self.debug)
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
        self.create_folderProcessInitial()
        if self.do_evaluate_list_processInitial:
            self.evaluate_list_processInitial()
        self.set_evaluated_list_processInitial()
        if self.do_hadd_processInitial:
            self.hadd_each_processInitial()
        if self.do_evaluate_content_of_all_processInitial:
            self.evaluate_content_of_all_processInitial()
        self.set_evaluated_list_process()
        self.set_evaluated_list_category()
        self.set_evaluated_list_variable()
        if self.debug:
            print "\n list_processInitial",self.list_processInitial
            print "\n list_process",self.list_process
            print "\n list_category",self.list_category
            print "\n list_variable",self.list_variable
        self.set_list_category("2tag2jet_150ptv_SR")
        self.set_list_variable("pTB1")

        #self.set_list_processInitial(["WHlv125J_MINLO"])
        #self.set_list_processInitial(["ZeeL_v221"])
        #self.evaluate_content_of_one_processInitial("WHlv125J_MINLO","False")
        #self.print_all()

    ### done methods

# done class

