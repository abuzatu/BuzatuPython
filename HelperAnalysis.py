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

    def set_stem(self,stem):
        self.stem=stem
        # e.g. 0L_31-15_a_MVA_TD
        (self.channel,self.vtag,self.period,self.analysis,self.btag)=stem.split("_")
        if True:
            print "stem",stem,"(channel,vtag,period,analysis,btag)",(self.channel,self.vtag,self.period,self.analysis,self.btag)
        
    def set_debug(self,debug):
        self.debug=debug

    def set_verbose(self,verbose):
        self.verbose=verbose
    
    def set_folderInput(self,folderInput):
        self.folderInput=folderInput

    def set_folderOutput(self,folderOutput):
        self.folderOutput=folderOutput
        os.system("mkdir -p "+ self.folderOutput)
    
    def set_doFirst(self,doFirst):
        self.doFirst=doFirst

    def set_do_evaluate_list_processInitial(self,do_evaluate_list_processInitial):
        self.do_evaluate_list_processInitial=do_evaluate_list_processInitial

    def set_do_hadd_all_processInitial_to_produce_fit_inputs(self,do_hadd_all_processInitial_to_produce_fit_inputs):
        self.do_hadd_all_processInitial_to_produce_fit_inputs=do_hadd_all_processInitial_to_produce_fit_inputs

    def set_list_processInitial(self,list_processInitial):
        self.list_processInitial=list_processInitial

    def set_do_hadd_processInitial(self,do_hadd_processInitial):
        self.do_hadd_processInitial=do_hadd_processInitial  

    def add_category(self,category):
        self.list_category.append(category)

    def set_list_category(self,list_category):
        self.list_category=list_category

    def set_list_variable(self,list_variable):
        self.list_variable=list_variable

    def set_list_process(self,list_process):
        self.list_process=list_process

    def set_do_evaluate_content_of_all_processInitial(self,do_evaluate_content_of_all_processInitial):
        self.do_evaluate_content_of_all_processInitial=do_evaluate_content_of_all_processInitial

    def set_do_overlay_histosRaw_by_processInitial(self,do_overlay_histosRaw_by_processInitial):
        self.do_overlay_histosRaw_by_processInitial=do_overlay_histosRaw_by_processInitial

    def set_do_later(self,do_later):
        self.do_later=do_later

    def set_do_create_histosRaw(self,do_create_histosRaw):
        self.do_create_histosRaw=do_create_histosRaw

    def set_do_create_histosProcess(self,do_create_histosProcess):
        self.do_create_histosProcess=do_create_histosProcess

    def set_do_create_histosProcessMerged(self,do_create_histosProcessMerged):
        self.do_create_histosProcessMerged=do_create_histosProcessMerged

    def set_do_create_results(self,do_create_results):
        self.do_create_results=do_create_results

    def set_do_create_latex_table(self,do_create_latex_table):
        self.do_create_latex_table=do_create_latex_table

    def set_do_create_stacked_plots(self,do_create_stacked_plots):
        self.do_create_stacked_plots=do_create_stacked_plots

    ### actions

    def create_folderProcessInitial(self):
        self.folderProcessInitial=self.folderOutput+"/processInitial"
        command="mkdir -p "+self.folderProcessInitial
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def do_hadd_all(self):
        self.create_folderProcessInitial()
        former_folderProcessInitial=self.folderProcessInitial
        self.folderOutput=self.folderOutput.replace("_1","_2")
        self.create_folderProcessInitial()
        command="hadd -f "+self.folderProcessInitial+"/all.root "+former_folderProcessInitial+"/*.root"
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def create_folderFitInput(self):
        self.folderFitInput=self.folderOutput+"/fitInput"
        command="mkdir -p "+self.folderFitInput
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def evaluate_list_processInitial(self,option="ReaderBatch"):
        if self.debug:
            print "Start evaluate_list_processInitial()"
        if option=="ReaderBatch":
            inputFolder=self.folderInput
        elif option=="processInitial":
            inputFolder=self.folderProcessInitial
        else:
            print "Option",option,"not known. Will ABORTT!!"
            assert(False)
        # done if
        if self.debug:
            print "inputFolder",inputFolder
        p = subprocess.Popen(
            ['ls', inputFolder],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
            )
        result=p.communicate()
        output=result[0]
        error=result[1]
        if self.debug:
            print "result",result
        # 
        set_processInitial=Set()
        for fileName in output.split():
            if self.debug:
                print "fileName",fileName
            if ".root" not in fileName:
                print "skipping non *.root file fileName",fileName
                continue
            if option=="ReaderBatch":
                # e.g. hist-data17-3.root
                list_fileNameElement=fileName.split("-")
                processInitial=list_fileNameElement[1]
            elif option=="processInitial":
                # e.g. data17.root
                list_fileNameElement=fileName.split(".")
                processInitial=list_fileNameElement[0]
            else:
                print "Option",option,"not known. Will ABORTT!!"
                assert(False)
            # done if
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

    def hadd_tagFinal(self):
        for processInitial in self.list_processInitial:
            output=self.folderProcessInitial+"/"+processInitial+".root"
            inputs=self.folderInput+"/hist-"+processInitial+"-*.root"
            command="hadd -f "+output+" "+inputs
            if self.debug:
                print "command",command
            os.system(command)
    # done function  

    def evaluate_content_of_one_processInitial(self,processInitial,debug):
        if self.debug:
            print "Start evaluate_content_of_one_processInitial()"
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
        if self.debug:
            print "Start evaluate_content_of_all_processInitial()"
        set_processInitial=Set()
        set_process=Set()
        set_category=Set()
        set_variable=Set()
        set_all=Set()
        for processInitial in self.list_processInitial:
            if True:
                print "processInitial",processInitial
            list_histoName=self.evaluate_content_of_one_processInitial(processInitial,False)
            for histoName in list_histoName:
                if self.debug:
                    print "histoName",histoName
                # e.g. ttbar_3ptag5pjet_150ptv_SR_yBB
                list_histoNameElement=histoName.split("_")
                if self.debug:
                    print "list_histoNameElement",list_histoNameElement

                #if "ttbar_dilep" in histoName or "stopWt_dilep" in histoName or "ggH125_bb" in histoName or "ggH125_inc" in histoName or "VBFH125_inc" in histoName or "ttbar_spin" in histoName:
                #    process=list_histoNameElement[0]+"_"+list_histoNameElement[1] # e.g. "ttbar_dilep or stopWt_dilep
                #    category=list_histoNameElement[2]+"_"+list_histoNameElement[3]+"_"+list_histoNameElement[4] # next three elements, eg. 3ptag5pjet_150ptv_SR
                #else:
                # only one word to define the process, e.g. ttbar or ttbarDilep
                process=list_histoNameElement[0] # first element e.g. ttbar
                index=None
                for i,s in enumerate(list_histoNameElement):
                    if self.debug:
                        print "i,s",i,s
                    if "ptv" in s:
                        index=i
                if self.debug:
                    print "index of element that contains ptv",index
                if index==None:
                    print "list_histoNameElement",list_histoNameElement
                if "jet" in list_histoNameElement[index-1]:
                    category=list_histoNameElement[1]+"_"+list_histoNameElement[2]+"_"+list_histoNameElement[3] # next three elements, eg. 3ptag5pjet_150ptv_SR or 3ptag5pjet_200ptv_SR
                else:
                    category=list_histoNameElement[1]+"_"+list_histoNameElement[2]+"_"+list_histoNameElement[3]+"_"+list_histoNameElement[4] # next three elements, eg. 3ptag5pjet_150_200ptv_SR
                # done if
                variable=histoName.replace(process+"_"+category+"_","") # the rest, tricky as sometimes the name has an _ in it
                if self.debug:
                    print "histoName",histoName,"list_histoNameElement",list_histoNameElement,"process",process,"category",category,"variable",variable
                set_processInitial.add(processInitial)
                set_process.add(process)
                set_category.add(category)
                set_variable.add(variable)
                set_all.add(variable+","+category+","+process+","+processInitial)
            # done for loop over histoName
        # done for loop over processInitial
        list_processInitial=sorted(set_processInitial)
        list_process=sorted(set_process)
        list_category=sorted(set_category)
        list_variable=sorted(set_variable)
        list_all=sorted(set_all)
        if self.debug:
            print "list_process",list_process
            for processInitial in list_processInitial:
                print "processInitial",processInitial
            print "list_process",list_process
            for process in list_process:
                print "process",process
            print "list_category",list_category
            for category in list_category:
                print "category",category
            print "list_variable",list_variable
            for variable in list_variable:
                print "variable",variable
            print "list_all",list_all
            for all in list_all:
                print "all",all
        # create the python file with the lists
        # list_processInitial
        outputFileName=self.folderProcessInitial+"/list_processInitial.txt"
        os.system("rm -f "+outputFileName)
        outputFile=open(outputFileName,"w")
        for processInitial in list_processInitial:
            outputFile.write(processInitial+"\n")
        outputFile.close()
        # list_process
        outputFileName=self.folderProcessInitial+"/list_process.txt"
        os.system("rm -f "+outputFileName)
        outputFile=open(outputFileName,"w")
        for process in list_process:
            if "QQ2H" in process or "GG2H" in process or process=="UNKNOWN":
                continue
            outputFile.write(process+"\n")
        outputFile.close()
        # list_category
        outputFileName=self.folderProcessInitial+"/list_category.txt"
        os.system("rm -f "+outputFileName)
        outputFile=open(outputFileName,"w")
        for category in list_category:
            outputFile.write(category+"\n")
        outputFile.close()
        # list_variable
        outputFileName=self.folderProcessInitial+"/list_variable.txt"
        os.system("rm -f "+outputFileName)
        outputFile=open(outputFileName,"w")
        for variable in list_variable:
            outputFile.write(variable+"\n")
        outputFile.close()
        # list_all
        outputFileName=self.folderProcessInitial+"/list_all.txt"
        os.system("rm -f "+outputFileName)
        outputFile=open(outputFileName,"w")
        for all in list_all:
            outputFile.write(all+"\n")
        outputFile.close()
    # done function

    def hadd_all_processInitial_to_produce_fit_inputs(self):
        output=self.folderFitInput+"/LimitHistograms.VH.vvbb.13TeV.mc16a.AcademiaSinica.v02.root"
        inputs=""
        for processInitial in self.list_processInitial:
            inputs+=" "+self.folderProcessInitial+"/hist-"+processInitial+"-*.root"
        # done if
        command="hadd -f "+output+" "+inputs
        if self.debug:
            print "command",command
        # os.system(command)
    # done function
            
    def set_evaluated_list_process(self):
        if self.debug:
            print "Start set_evaluated_list_process()"
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

    def set_evaluated_list_all(self):
        fileName=self.folderProcessInitial+"/list_all.txt"
        self.list_all=get_list_from_file(fileName,self.debug)
    # done function 

    def create_folderHistos(self):
        self.folderHistos=self.folderOutput+"/histos"
        os.system("mkdir -p "+self.folderHistos)
    # done function

    def get_histoNameInitial(self,process,category,variable):
        histoNameInitial=process+"_"+category+"_"+variable
        if self.debug:
            print "histoNameInitial",histoNameInitial
        return histoNameInitial
    # done function

    def get_histoNameProcess(self,variable,category,process):
        histoNameInitial=variable+"_"+category+"_"+process
        if self.debug:
            print "histoNameInitial",histoNameInitial
        return histoNameInitial
    # done function

    def get_histoNameProcess_new(self,variable,category,process):
        histoNameInitial=process+"_"+category+"_"+variable
        if self.debug:
            print "histoNameInitial_new",histoNameInitial
        return histoNameInitial
    # done function

    def get_histoNameRaw(self,process,category,variable,processInitial):
        if self.debug:
            print "Start get_histoNameRaw()"
        histoNameRaw=variable+"_"+category+"_"+process+"_"+processInitial
        if self.debug:
            print "histoNameRaw",histoNameRaw
        return histoNameRaw
    # done function

    def set_fileNameHistosInput(self):
        self.fileNameHistosInput=self.folderHistos+"/histosInput.root"
    # done function  

    def set_fileNameHistosRaw(self):
        # suffix=""
        suffix="_"+self.list_category[0]+"_"+self.list_variable[0]
        self.fileNameHistosRaw=self.folderHistos+"/histosRaw"+suffix+".root"
    # done function

    def create_histosRaw(self,option):
        if self.debug or self.verbose:
            print "Start create_histosRaw()"
        # stores those histograms that exist, and puts them in the same folder
        outputFile=TFile(self.fileNameHistosRaw,"RECREATE")
        outputFile.Close()
        for infoall in self.list_all:
            list_infoall=infoall.split(",")
            variable=list_infoall[0]
            category=list_infoall[1]
            process=list_infoall[2]
            processInitial=list_infoall[3]
            if option=="reduced":
                if variable not in self.list_variable or category not in self.list_category or process not in self.list_process:
                    continue
            if self.debug:
                print "%-10s %-10s %-10s %-10s" % (variable,category,process,processInitial)
            inputFileName=self.folderProcessInitial+"/"+processInitial+".root"
            histoNameInitial=self.get_histoNameInitial(process,category,variable)
            histoNameRaw    =self.get_histoNameRaw    (process,category,variable,processInitial)
            histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameInitial,name=histoNameRaw,returnDummyIfNotFound=True,debug=self.debug)
            if histo=="dummy":
                continue
            outputFile=TFile(self.fileNameHistosRaw,"UPDATE")
            histo.SetDirectory(outputFile)
            histo.Write()
            outputFile.Close()
        # done for loop over all
    # done function

    def set_folderPlotsHistosRawByProcessInitial(self):
        self.folderPlotsHistosRawByProcessInitial=self.folderOutput+"/plots_histosRaw_by_processInital"
        os.system("mkdir -p "+self.folderPlotsHistosRawByProcessInitial)
    # done function

    def set_dict_variable_info(self):
        if self.debug:
            print "Start set_dict_variable_info()"
        debug_binRange=False

        # mBB
        binRange_mBB=get_binRange(0,30,30,debug_binRange)+","+get_binRange(30,160,10,debug_binRange)+","+get_binRange(160,300,20,debug_binRange)+","+get_binRange(300,500,40,debug_binRange)
        # mva EPS 2017 https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/SMVHbbPublication2017BkgModelling#BDT_Binning
        self.binRange_mva2J="-1,-0.91,-0.77,-0.542,-0.268,-0.05,0.094,0.194,0.278,0.358,0.424,0.48,0.53,0.584,0.656,1.0"
        self.binRange_mva3J="-1,-0.848,-0.676,-0.492,-0.3,-0.126,0.03,0.158,0.272,0.362,0.44,0.51,0.576,0.644,0.722,1.0"
        self.binRange_mBB=binRange_mBB
        # self.binRange_pTB1=[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)

        self.dict_variable_info={
            "EtaB1":[get_binRange(-2.5,2.5,0.2,debug_binRange)],
            "EtaB2":[get_binRange(-2.5,2.5,0.2,debug_binRange)],
            "EtaJ3":[get_binRange(-4.5,-2.5,0.5,debug_binRange)+","+get_binRange(-2.5,2.5,0.2,debug_binRange)+","+get_binRange(2.5,4.5,0.5,debug_binRange)],
            "PhiB1":[get_binRange(-3.15,3.15,0.0315*10,debug_binRange)],
            "PhiB2":[get_binRange(-3.15,3.15,0.0315*10,debug_binRange)],
            "PhiJ3":[get_binRange(-3.15,3.15,0.0315*10,debug_binRange)],
            "EtaFwdJets":[get_binRange(-4.5,4.5,0.1,debug_binRange)],
            "EtaSigJets":[get_binRange(-2.5,2.5,0.1,debug_binRange)],
            # "MET":[get_binRange(150,400,10,debug_binRange)+","+get_binRange(400,700,100,debug_binRange)],
            "MET":[get_binRange(150,400,10,debug_binRange)],
            "MET_Track":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,100,debug_binRange)],
            "MEff":[get_binRange(280,500,10,debug_binRange)+","+get_binRange(500,1000,20,debug_binRange)],
            "MEff3":[get_binRange(280,500,10,debug_binRange)+","+get_binRange(500,1000,20,debug_binRange)],
            "METDirectional":[""],
            "MV2c10_B":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2c10_C":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2c10_L":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2c10_Data":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2cB1":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2cB2":[get_binRange(0.8,1,0.02,debug_binRange)],
            "MV2c10_B":[get_binRange(0.8,1,0.02,debug_binRange)],
            "btag_weight_B":[get_binRange(0.0,1,0.05,debug_binRange)],
            "btag_weight_C":[get_binRange(0.0,1,0.05,debug_binRange)],
            "btag_weight_L":[get_binRange(0.0,1,0.05,debug_binRange)],
            "btag_weight_Data":[get_binRange(0.0,1,0.05,debug_binRange)],
            "eff_B":[get_binRange(0.0,1,0.05,debug_binRange)],
            "eff_C":[get_binRange(0.0,1,0.05,debug_binRange)],
            "eff_L":[get_binRange(0.0,1,0.05,debug_binRange)],
            "eff_Data":[get_binRange(0.0,1,0.05,debug_binRange)],
            "MindPhiMETJet":[get_binRange(0.0315*0,3.15,0.0315*2,debug_binRange)],
            "NTags":[""],
            "Njets":[get_binRange(2,10,1,debug_binRange)],
            "njets":[get_binRange(2,10,1,debug_binRange)],
            "NFwdJets":[get_binRange(2,10,1,debug_binRange)],
            "NSigJets":[get_binRange(2,10,1,debug_binRange)],
            "SumPtJet":[get_binRange(120,400,10,debug_binRange)+","+get_binRange(400,600,50,debug_binRange)],
            "HT":[get_binRange(240,560,20,debug_binRange)+","+get_binRange(560,600,20,debug_binRange)+","+get_binRange(600,1000,50,debug_binRange)],
            "costheta":[get_binRange(0,1,0.05,debug_binRange)],
            "dEtaBB":[get_binRange(0,1.5,0.1,debug_binRange)+","+get_binRange(1.5,2.5,0.2,debug_binRange)+","+get_binRange(2.5,4.5,1,debug_binRange)],
            "dPhiBB":[get_binRange(0,3.2,5*0.032,debug_binRange)],
            "dPhiMETMPT":[get_binRange(0,3.15-0.0315*48,0.0315,debug_binRange)],
            "dPhiVBB":[get_binRange(3.2-35*0.032,3.2-20*0.032,5*0.032,debug_binRange)+","+get_binRange(3.2-20*0.032,3.2-10*0.032,2*0.032,debug_binRange)+","+get_binRange(3.2-10*0.032,3.2-0*0.032,1*0.032,debug_binRange)],
            "dRB1J3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "dRB2J3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "dRBB":[get_binRange(0.4,0.7,0.1,debug_binRange)+","+get_binRange(0.7,1.0,0.1,debug_binRange)+","+get_binRange(1.0,3.0,0.2,debug_binRange)+","+get_binRange(3.0,4.0,0.5,debug_binRange)+","+get_binRange(4.0,5.0,1.0,debug_binRange)],
            "mBB":[binRange_mBB],
            "mBBMVA":[binRange_mBB],
            "mBBNominal":[binRange_mBB],
            "mBBOneMu":[binRange_mBB],
            "mBBOneMu4GeV":[binRange_mBB],
            "mBBOneMu5GeV":[binRange_mBB],
            "mBBOneMu6GeV":[binRange_mBB],
            "mBBOneMu7GeV":[binRange_mBB],
            "mBBOneMu10GeV":[binRange_mBB],
            "mBBOneMu12GeV":[binRange_mBB],
            "mBBOneMu15GeV":[binRange_mBB],
            "mBBOneMu20GeV":[binRange_mBB],
            "mBBAllMu":[binRange_mBB],
            "mBBOneMu2":[binRange_mBB],
            "mBBAllMu2":[binRange_mBB],
            "mBBAllMu2MuR":[binRange_mBB],
            "mBBAllMu2MuRElR":[binRange_mBB],
            "mBBPtReco":[binRange_mBB],
            "nrMuonInJetB1":[get_binRange(0,3,1,debug_binRange)],  
            "nrMuonInJetB2":[get_binRange(0,3,1,debug_binRange)],  
            "nrMuonInJetJ3":[get_binRange(0,3,1,debug_binRange)],  
            "nrElectronInJetB1":[get_binRange(0,3,1,debug_binRange)],  
            "nrElectronInJetB2":[get_binRange(0,3,1,debug_binRange)],  
            "nrElectronInJetJ3":[get_binRange(0,3,1,debug_binRange)],  
            #"ptMuonInJetB1":["0,2,4,5,6,7,10,12,15,20,30,50,100"],  
            #"ptMuonInJetB2":["0,2,4,5,6,7,10,12,15,20,30,50,100"],  
            #"ptMuonInJetJ3":["0,2,4,5,6,7,10,12,15,20,30,50,100"],  
            "ptOneMuInJetB1":["1,2,3,4,7,10,12,15,20,30"],
            "ptOneMuInJetB2":["1,2,3,4,7,10,12,15,20,30"],
            "ptOneMuInJetJ3":["1,2,3,4,7,10,12,15,20,30"],
            "dRMuonInJetB1":[get_binRange(0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.4,0.05,debug_binRange)],  
            "dRMuonInJetB2":[get_binRange(0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.4,0.05,debug_binRange)],  
            "dRMuonInJetJ3":[get_binRange(0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.4,0.05,debug_binRange)],
            "PtRatioOneElectronInJetB1":[get_binRange(0.0,0.1,0.01,debug_binRange)],
            "PtRatioOneElectronInJetB2":[get_binRange(0.0,0.1,0.01,debug_binRange)],
            "PtRatioOneElectronInJetJ3":[get_binRange(0.0,0.1,0.01,debug_binRange)],
            "PtRatioOneMuonInJetB1":[get_binRange(0.0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.2,0.02,debug_binRange)+","+get_binRange(0.2,1.0,0.05,debug_binRange)],
            "PtRatioOneMuonInJetB2":[get_binRange(0.0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.2,0.02,debug_binRange)+","+get_binRange(0.2,1.0,0.05,debug_binRange)],
            "PtRatioOneMuonInJetJ3":[get_binRange(0.0,0.1,0.01,debug_binRange)+","+get_binRange(0.1,0.2,0.02,debug_binRange)+","+get_binRange(0.2,1.0,0.05,debug_binRange)],
            "mBBJ":[get_binRange(40,80,20,debug_binRange)+","+get_binRange(80,160,10,debug_binRange)+","+get_binRange(160,300,20,debug_binRange)+","+get_binRange(300,500,40,debug_binRange)+","+get_binRange(500,700,50,debug_binRange)+","+get_binRange(700,1000,100,debug_binRange)],
            "maxdRBJ3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "mindRBJ3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "AverageMu":[get_binRange(0,100,2,debug_binRange)],
            "AverageMuScaled":[get_binRange(0,100,2,debug_binRange)],
            "ActualMu":[get_binRange(0,100,2,debug_binRange)],
            "ActualMuScaled":[get_binRange(0,100,2,debug_binRange)],
            "PileupReweight":[""],
            "RandomRunNumber":[""],
            # "mva":[get_binRange(-1,1,0.05,debug_binRange)],
            "mva":[self.binRange_mva2J],
            "mvadiboson":[get_binRange(-1,1,0.05,debug_binRange)],
            "nTaus":[get_binRange(0,3,1,debug_binRange)],
            "pTB1":[get_binRange(0,240,10,debug_binRange)+","+get_binRange(240,300,20,debug_binRange)+","+get_binRange(300,400,50,debug_binRange)],
            "pTB2":[get_binRange(0,140,10,debug_binRange)+","+get_binRange(140,160,20,debug_binRange)],
            "PtFwdJets":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)],
            "PtSigJets":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)],
            "pTBB":[get_binRange(40,80,20,debug_binRange)+","+get_binRange(80,300,10,debug_binRange)+","+get_binRange(300,400,50,debug_binRange)],
            "pTBBMETAsym":[get_binRange(-0.6,-0.2,0.1,debug_binRange)+","+get_binRange(-0.2,-0.1,0.05,debug_binRange)+","+get_binRange(-0.1,0.1,0.02,debug_binRange)+","+get_binRange(0.1,0.2,0.05,debug_binRange)],
            "pTBBoverMET":[get_binRange(0.0,0.7,0.1,debug_binRange)+","+get_binRange(0.7,0.8,0.05,debug_binRange)+","+get_binRange(0.8,1.2,0.02,debug_binRange)+","+get_binRange(1.2,1.3,0.05,debug_binRange)+","+get_binRange(1.3,1.7,0.1,debug_binRange)],
            "METOverSqrtHT":[get_binRange(0.2,0.7,0.1,debug_binRange)+","+get_binRange(0.7,1.2,0.02,debug_binRange)+","+get_binRange(1.2,1.6,0.1,debug_binRange)],
            "METOverSqrtSumET":[get_binRange(0.2,0.7,0.1,debug_binRange)+","+get_binRange(0.7,1.2,0.02,debug_binRange)+","+get_binRange(1.2,1.6,0.1,debug_binRange)],
            "METRho":[""],
            "METSig":[""],
            "METSig_hard":[""],
            "METSig_soft":[""],
            "METVarL":[""],
            "METVarL_hard":[""],
            "METVarL_soft":[""],
            "METVarT":[""],
            "pTJ3":[get_binRange(0,120,10,debug_binRange)+","+get_binRange(120,200,40,debug_binRange)],
            "yBB":[get_binRange(0,2.5,0.1,debug_binRange)],
            }
    # done function

    def get_dict_variable_info(self):
        return self.dict_variable_info
    # done function

    def overlay_histosRaw_by_processInitial(self):
        if self.debug:
            print "Start overlay_histosRaw_by_processInitial()"
        for variable in self.list_variable:
            info=self.dict_variable_info[variable]
            binRange=info[0]
            for category in self.list_category:
                for process in self.list_process:
                    list_tuple_h1D=[]
                    for i,processInitial in enumerate(self.list_processInitial):
                        if self.debug:
                            print "%-10s %-10s %-10s %-10s" % (variable,category,process,processInitial)
                        inputFileName=self.fileNameHistosRaw
                        histoNameRaw=self.get_histoNameRaw(process,category,variable,processInitial)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameRaw,name="",returnDummyIfNotFound=True,debug=self.debug)
                        if histo=="dummy":
                            continue
                        histo=get_histo_generic_binRange(histo,binRange=binRange,option="average",debug=False)
                        histo.SetLineColor(list_color[i])
                        # normalise to unit area
                        histo=get_histo_normalised(histo)
                        list_tuple_h1D.append((histo,processInitial))
                    # done for loop over processInitial
                    if self.debug:
                        print "len(list_tuple_h1D)",len(list_tuple_h1D)
                    if len(list_tuple_h1D)==0:
                        continue
                    outputFileName=self.folderPlotsHistosRawByProcessInitial+"/overlay_"+variable+"_"+category+"_"+process
                    overlayHistograms(list_tuple_h1D,fileName=outputFileName,extensions="pdf",option="histo",doValidationPlot=False,canvasname="canvasname",addHistogramInterpolate=False,addfitinfo=False,addMedianInFitInfo=False,significantDigits=("3","3","3","3"),min_value=-1,max_value=-1,YTitleOffset=0.45,doRatioPad=True,min_value_ratio=0.8,max_value_ratio=1.2,statTitle="MC. stat uncertainty",statColor=6,ratioTitle="Ratio to one on top",plot_option="HIST E",plot_option_ratio="HIST",text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; VHbb 0L MVA selection}?#bf{Var "+variable+" Cat "+category+"}?#bf{Process "+process+"}",0.04,13,0.15,0.88,0.05),legend_info=[0.55,0.70,0.88,0.88,72,0.037,0],line_option=([0,0.5,0,0.5],2),debug=False) 
                # done for loop over process
            # done for loop over category
        # done for loop over variable
    # done function

    def set_fileNameHistosProcess(self):
        # suffix=""
        suffix="_"+self.list_category[0]+"_"+self.list_variable[0]
        self.fileNameHistosProcess=self.folderHistos+"/histosProcess"+suffix+".root"
    # done function

    def create_histosProcess(self):
        if self.debug or self.verbose:
            print "Start create_histosProcess()"
        # now we want to sum over processInitial for a given process
        outputFile=TFile(self.fileNameHistosProcess,"RECREATE")
        outputFile.Close()
        for variable in self.list_variable:
            counter_variable=0
            for category in self.list_category:
                for processRenamed in self.list_process:
                    if self.debug:
                        print "processRenamed",processRenamed
                    counter=0
                    if self.debug:
                        print " %-10s %-10s %-10s" % (variable,category,processRenamed)
                    list_processInfo=self.dict_process_info[processRenamed]
                    if self.debug:
                        print "list_processInfo",list_processInfo
                    list_processInfoToAdd=list_processInfo[0]
                    dict_jet_SF=list_processInfo[1]
                    for processInfo in list_processInfoToAdd:
                        process=processInfo[0]
                        processInitial=processInfo[1]
                        if self.debug:
                            print "%-10s %-10s %-10s %-10s" % (variable,category,process,processInitial)
                        inputFileName=self.fileNameHistosRaw
                        histoNameRaw    =self.get_histoNameRaw    (process,category,variable,processInitial)
                        histoNameProcess=self.get_histoNameProcess(variable,category,processRenamed)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameRaw,name=histoNameProcess,returnDummyIfNotFound=True,debug=self.debug)
                        if histo=="dummy":
                            continue
                        if counter_variable==0:
                            if self.debug:
                                print "counter_variable=0"
                                print "type(histo)",type(histo)
                            histoReset=histo.Clone()
                            if self.debug:
                                print "type(histoReset)",type(histoReset)
                            histoReset.Reset()
                        counter_variable+=1
                        if counter==0:
                            histoProcess=histo
                        else:
                            histoProcess.Add(histo)
                        counter+=1
                    # done for loop over processInitial
                    if self.debug:
                        print "counter final",counter
                    if counter==0:
                        histoNameRaw    =self.get_histoNameRaw    ("ttbar",category,variable,"ttbar_nonallhad_PwPy8")
                        histoReset=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameRaw,name=histoNameProcess,returnDummyIfNotFound=True,debug=self.debug)
                        histoReset.Reset()
                        histoProcess=histoReset
                        histoNameProcess=self.get_histoNameProcess(variable,category,processRenamed)
                        histoProcess.SetName(histoNameProcess)
                        histoProcess.SetTitle(histoNameProcess)
                        if self.debug:
                            print "counter",counter,"for process",process,"which was not found for category",category,"in list of processInitial",self.list_processInitial
                    outputFile=TFile(self.fileNameHistosProcess,"UPDATE")
                    histoProcess.SetDirectory(outputFile)
                    histoProcess.Write()
                    outputFile.Close()
                # done for loop over process
            # done for loop over category
        # done for loop over variable
    # done function

    def set_list_process_info(self):
        self.list_process=[
            "qqZvvHbb",
            "qqWlvHbb",
            "ggZvvHbb",
            "qqZllHbb",
            "ggZllHbb",
            "qqZvvHcc",
            "qqWlvHcc",
            "ggZvvHcc",
            "qqZllHcc",
            "ggZllHcc",
            "qqZincH4l",
            "qqWincH4l",
            "ggH",
            "ggHbb",
            "bbH",
            "VBF",
            "ttH",
            "WW",
            "WZ",
            "ZZ",
            "ggZZ",
            "ggWW",
            "ZllZbb",
            "ZvvZbb",
            "WlvZbb",
            "ZllZvv",
            "Wbb",
            "Wbc",
            "Wbl",
            "Wcc",
            "Wcl",
            "Wl",
            "Zbb",
            "Zbc",
            "Zbl",
            "Zcc",
            "Zcl",
            "Zl",
            "ttbar",
            "ttbarOld",
            "ttbarDilep",
            "ttbarDilepOld",
            "ttbarSpin",
            "stops",
            "stopt",
            "stopWt",
            "stoptZq",
            "ttV",
            "ttVV",
            "ttt",
            "tttt",
            "data",
            #"dataB",
            #"dijet",
            # "",
            ]
        
        dict_one_SF={"2":1.00,"3":1.00,"4":1.0,"5p":1.0}
        # EPS 2017 with systematics fit
        dict_Whf_SF={"2":1.27,"3":1.27,"4":1.0,"5p":1.0}
        dict_Zhf_SF={"2":1.42,"3":1.31,"4":1.0,"5p":1.0}
        dict_ttbar_SF={"2":0.97,"3":1.00,"4":1.0,"5p":1.0}

        self.dict_process_info={
            # example
            # "processMine":[[["process","processInitial"],["process2","processInitial2"]],{"2":SF2jet,"3":SF3jet,"4":SF4jet,"5p":SF5pjet}],
            # VHbb
            "qqZvvHbb":[[["qqZvvH125","qqZvvHbbJ_PwPy8MINLO"]],dict_one_SF,],
            "qqWlvHbb":[[["qqWlvH125","qqWlvHbbJ_PwPy8MINLO"]],dict_one_SF,],
            "ggZvvHbb":[[["ggZvvH125","ggZvvHbb_PwPy8"]],dict_one_SF,],
            "qqZllHbb":[[["qqZllH125","qqZllHbbJ_PwPy8MINLO"]],dict_one_SF,],
            "ggZllHbb":[[["ggZllH125","ggZllHbb_PwPy8"]],dict_one_SF,],
            # VHcc
            "qqZvvHcc":[[["qqZvvH125cc","qqZvvHccJ_PwPy8MINLO"]],dict_one_SF,],
            "qqWlvHcc":[[["qqWlvH125cc","qqWlvHccJ_PwPy8MINLO"]],dict_one_SF,],
            "ggZvvHcc":[[["ggZvvH125cc","ggZvvHcc_PwPy8"]],dict_one_SF,],
            "qqZllHcc":[[["qqZllH125cc","qqZllHccJ_PwPy8MINLO"]],dict_one_SF,],
            "ggZllHcc":[[["ggZllH125cc","ggZllHcc_PwPy8"]],dict_one_SF,],
            # other ZH
            "qqZincH4l":[[["qqZincH4l","ZincHJZZ4l_PwPy8MINLO"]],dict_one_SF,],
            "qqWincH4l":[[["qqWmincH4l","WincHJZZ4l_PwPy8MINLO"],["qqWpincH4l","WincHJZZ4l_PwPy8MINLO"]],dict_one_SF,],
            # non ZH signals
            "VBF":[[["VBFH125Inc","VBFHinc_PwPy8"]],dict_one_SF,],
            "ggHbb":[[["ggH125bb","ggHbb_PwPy8NNLOPS"]],dict_one_SF,],
            "ggH":[[["ggH125Inc","ggHinc_PwPy8"]],dict_one_SF,],
            "bbH":[[["bbH125","bbHinc_aMCatNLOPy8"]],dict_one_SF,],
            "ttH":[[["ttH","ttHinc_aMCatNLOPy8"]],dict_one_SF,],
            # dijet
            "dijet":[[["dijetJZW","MJ_Py8"]],dict_one_SF,],
            # dibosons
            "WW":[[["WW","WqqWlv_Sh221"]],dict_one_SF,],
            "ggWW":[[["ggWW","ggWqqWlv_Sh222"]],dict_one_SF,],
            "WZ":[[["WZ","WqqZvv_Sh221"],["WZ","WqqZll_Sh221"],["WZ","WlvZqq_Sh221"]],dict_one_SF,],
            "ZZ":[[["ZZ","ZqqZvv_Sh221"],["ZZ","ZqqZll_Sh221"]],dict_one_SF,],
            "ggZZ":[[["ggZZ","ggZqqZvv_Sh222"],["ggZZ","ggZqqZll_Sh222"]],dict_one_SF,],
            "ZllZbb":[[["ZllZbb","ZZ_bb_Sh221"]],dict_one_SF,],
            "ZvvZbb":[[["ZvvZbb","ZZ_bb_Sh221"]],dict_one_SF,],
            "WlvZbb":[[["WlvZbb","WZ_bb_Sh221"]],dict_one_SF,],
            "ZllZvv":[[["llvv","VV_fulllep_Sh222"]],dict_one_SF,],
            # W+jets
            "Wbb":[
                [
                    ["Wbb","WenuB_Sh221"],
                    ["Wbb","WenuC_Sh221"],
                    ["Wbb","WenuL_Sh221"],
                    ["Wbb","Wenu_Sh221"],
                    ["Wbb","WmunuB_Sh221"],
                    ["Wbb","WmunuC_Sh221"],
                    ["Wbb","WmunuL_Sh221"],
                    ["Wbb","Wmunu_Sh221"],
                    ["Wbb","WtaunuB_Sh221"],
                    ["Wbb","WtaunuC_Sh221"],
                    ["Wbb","WtaunuL_Sh221"],
                    ["Wbb","Wtaunu_Sh221"],
                    ],
                dict_Whf_SF,
                ],
            "Wbc":[
                [
                    ["Wbc","WenuB_Sh221"],
                    ["Wbc","WenuC_Sh221"],
                    ["Wbc","WenuL_Sh221"],
                    ["Wbc","Wenu_Sh221"],
                    ["Wbc","WmunuB_Sh221"],
                    ["Wbc","WmunuC_Sh221"],
                    ["Wbc","WmunuL_Sh221"],
                    ["Wbc","Wmunu_Sh221"],
                    ["Wbc","WtaunuB_Sh221"],
                    ["Wbc","WtaunuC_Sh221"],
                    ["Wbc","WtaunuL_Sh221"],
                    ["Wbc","Wtaunu_Sh221"],
                    ],
                dict_Whf_SF,
                ],
            "Wbl":[
                [
                    ["Wbl","WenuB_Sh221"],
                    ["Wbl","WenuC_Sh221"],
                    ["Wbl","WenuL_Sh221"],
                    ["Wbl","Wenu_Sh221"],
                    ["Wbl","WmunuB_Sh221"],
                    ["Wbl","WmunuC_Sh221"],
                    ["Wbl","WmunuL_Sh221"],
                    ["Wbl","Wmunu_Sh221"],
                    ["Wbl","WtaunuB_Sh221"],
                    ["Wbl","WtaunuC_Sh221"],
                    ["Wbl","WtaunuL_Sh221"],
                    ["Wbl","Wtaunu_Sh221"],
                    ],
                dict_Whf_SF,
                ],
            "Wcc":[
                [
                    ["Wcc","WenuB_Sh221"],
                    ["Wcc","WenuC_Sh221"],
                    ["Wcc","WenuL_Sh221"],
                    ["Wcc","Wenu_Sh221"],
                    ["Wcc","WmunuB_Sh221"],
                    ["Wcc","WmunuC_Sh221"],
                    ["Wcc","WmunuL_Sh221"],
                    ["Wcc","Wmunu_Sh221"],
                    ["Wcc","WtaunuB_Sh221"],
                    ["Wcc","WtaunuC_Sh221"],
                    ["Wcc","WtaunuL_Sh221"],
                    ["Wcc","Wtaunu_Sh221"],
                    ],
                dict_Whf_SF,
                ],
            "Wcl":[
                [
                    ["Wcl","WenuB_Sh221"],
                    ["Wcl","WenuC_Sh221"],
                    ["Wcl","WenuL_Sh221"],
                    ["Wcl","Wenu_Sh221"],
                    ["Wcl","WmunuB_Sh221"],
                    ["Wcl","WmunuC_Sh221"],
                    ["Wcl","WmunuL_Sh221"],
                    ["Wcl","Wmunu_Sh221"],
                    ["Wcl","WtaunuB_Sh221"],
                    ["Wcl","WtaunuC_Sh221"],
                    ["Wcl","WtaunuL_Sh221"],
                    ["Wcl","Wtaunu_Sh221"],
                    ],
                dict_one_SF,
                ],
            "Wl": [
                [
                    ["Wl" ,"WenuB_Sh221"],
                    ["Wl" ,"WenuC_Sh221"],
                    ["Wl" ,"WenuL_Sh221"],
                    ["Wl" ,"Wenu_Sh221"],
                    ["Wl" ,"WmunuB_Sh221"],
                    ["Wl" ,"WmunuC_Sh221"],
                    ["Wl" ,"WmunuL_Sh221"],
                    ["Wl" ,"Wmunu_Sh221",],
                    ["Wl" ,"WtaunuB_Sh221"],
                    ["Wl" ,"WtaunuC_Sh221"],
                    ["Wl" ,"WtaunuL_Sh221"],
                    ["Wl" ,"Wtaunu_Sh221"],
                    ],
                dict_one_SF,
                ],
            "Zbb":[
                [
                    ["Zbb","ZnunuB_Sh221"],
                    ["Zbb","ZnunuC_Sh221"],
                    ["Zbb","ZnunuL_Sh221"],
                    ["Zbb","Znunu_Sh221"],
                    ["Zbb","ZeeB_Sh221"],
                    ["Zbb","ZeeC_Sh221"],
                    ["Zbb","ZeeL_Sh221"],
                    ["Zbb","Zee_Sh221"],
                    ["Zbb","ZmumuB_Sh221"],
                    ["Zbb","ZmumuC_Sh221"],
                    ["Zbb","ZmumuL_Sh221"],
                    ["Zbb","Zmumu_Sh221"],
                    ["Zbb","ZtautauB_Sh221"],
                    ["Zbb","ZtautauC_Sh221"],
                    ["Zbb","ZtautauL_Sh221"],
                    ["Zbb","Ztautau_Sh221"],
                    ],
                dict_Zhf_SF
                ],
            "Zbc":[
                [
                    ["Zbc","ZnunuB_Sh221"],
                    ["Zbc","ZnunuC_Sh221"],
                    ["Zbc","ZnunuL_Sh221"],
                    ["Zbc","Znunu_Sh221"],
                    ["Zbc","ZeeB_Sh221"],
                    ["Zbc","ZeeC_Sh221"],
                    ["Zbc","ZeeL_Sh221"],
                    ["Zbc","Zee_Sh221"],
                    ["Zbc","ZmumuB_Sh221"],
                    ["Zbc","ZmumuC_Sh221"],
                    ["Zbc","ZmumuL_Sh221"],
                    ["Zbc","Zmumu_Sh221"],
                    ["Zbc","ZtautauB_Sh221"],
                    ["Zbc","ZtautauC_Sh221"],
                    ["Zbc","ZtautauL_Sh221"],
                    ["Zbc","Ztautau_Sh221"],
                    ],
                dict_Zhf_SF,
                ],
            "Zbl":[
                [
                    ["Zbl","ZnunuB_Sh221"],
                    ["Zbl","ZnunuC_Sh221"],
                    ["Zbl","ZnunuL_Sh221"],
                    ["Zbl","Znunu_Sh221"],
                    ["Zbl","ZeeB_Sh221"],
                    ["Zbl","ZeeC_Sh221"],
                    ["Zbl","ZeeL_Sh221"],
                    ["Zbl","Zee_Sh221"],
                    ["Zbl","ZmumuB_Sh221"],
                    ["Zbl","ZmumuC_Sh221"],
                    ["Zbl","ZmumuL_Sh221"],
                    ["Zbl","Zmumu_Sh221"],
                    ["Zbl","ZtautauB_Sh221"],
                    ["Zbl","ZtautauC_Sh221"],
                    ["Zbl","ZtautauL_Sh221"],
                    ["Zbl","Ztautau_Sh221"],
                    ],
                dict_Zhf_SF,
                ],
            "Zcc":[
                [
                    ["Zcc","ZnunuB_Sh221"],
                    ["Zcc","ZnunuC_Sh221"],
                    ["Zcc","ZnunuL_Sh221"],
                    ["Zcc","Znunu_Sh221"],
                    ["Zcc","ZeeB_Sh221"],
                    ["Zcc","ZeeC_Sh221"],
                    ["Zcc","ZeeL_Sh221"],
                    ["Zcc","Zee_Sh221"],
                    ["Zcc","ZmumuB_Sh221"],
                    ["Zcc","ZmumuC_Sh221"],
                    ["Zcc","ZmumuL_Sh221"],
                    ["Zcc","Zmumu_Sh221"],
                    ["Zcc","ZtautauB_Sh221"],
                    ["Zcc","ZtautauC_Sh221"],
                    ["Zcc","ZtautauL_Sh221"],
                    ["Zcc","Ztautau_Sh221"],
                    ],
                dict_Zhf_SF,
                ],
            "Zcl":[
                [
                    ["Zcl","ZnunuB_Sh221"],
                    ["Zcl","ZnunuC_Sh221"],
                    ["Zcl","ZnunuL_Sh221"],
                    ["Zcl","Znunu_Sh221"],
                    ["Zcl","ZeeB_Sh221"],
                    ["Zcl","ZeeC_Sh221"],
                    ["Zcl","ZeeL_Sh221"],
                    ["Zcl","Zee_Sh221"],
                    ["Zcl","ZmumuB_Sh221"],
                    ["Zcl","ZmumuC_Sh221"],
                    ["Zcl","ZmumuL_Sh221"],
                    ["Zcl","Zmumu_Sh221"],
                    ["Zcl","ZtautauB_Sh221"],
                    ["Zcl","ZtautauC_Sh221"],
                    ["Zcl","ZtautauL_Sh221"],
                    ["Zcl","Ztautau_Sh221"],
                    ],
                dict_one_SF,
                ],
            "Zl" :[
                [
                    ["Zl" ,"ZnunuB_Sh221"],
                    ["Zl" ,"ZnunuC_Sh221"],
                    ["Zl" ,"ZnunuL_Sh221"],
                    ["Zl" ,"Znunu_Sh221"],
                    ["Zl" ,"ZeeB_Sh221"],
                    ["Zl" ,"ZeeC_Sh221"],
                    ["Zl" ,"ZeeL_Sh221"],
                    ["Zl" ,"Zee_Sh221"],
                    ["Zl" ,"ZmumuB_Sh221"],
                    ["Zl" ,"ZmumuC_Sh221"],
                    ["Zl" ,"ZmumuL_Sh221"],
                    ["Zl" ,"Zmumu_Sh221"],
                    ["Zl" ,"ZtautauB_Sh221"],
                    ["Zl" ,"ZtautauC_Sh221"],
                    ["Zl" ,"ZtautauL_Sh221"],
                    ["Zl" ,"Ztautau_Sh221"],
                    ],
                dict_one_SF,
                ],
            "ttbar" :[[["ttbar","ttbar_nonallhad_PwPy8"]],dict_ttbar_SF,],
            "ttbarOld" :[[["ttbar","ttbar_nonallhad_PwPy8_old"]],dict_one_SF],
            "ttbarDilep" :[[["ttbar","ttbar_dil_PwPy8"]],dict_one_SF],
            "ttbarDilepOld" :[[["ttbarDilep","ttbar_dil_PwPy8_old"]],dict_one_SF],
            "ttbarSpin" :[[["ttbarSpin","ttbar_PwPy8_MadSpin"]],dict_one_SF],
            "stops" :[[["stops","stops_PwPy8"]],dict_one_SF],
            "stopt" :[[["stopt","stopt_PwPy8"]],dict_one_SF],
            "stopWt":[[["stopWt","stopWt_PwPy8"]],dict_one_SF],
            "stopWtMETFilt":[[["stopWt","stopWt_PwPy_METfilt"]],dict_one_SF],
            "stoptZq":[[["tZq","stoptZ_MGPy8"]],dict_one_SF],
            "ttV"   :[[["ttV","ttV_aMCatNLOPy8"]],dict_one_SF],
            "ttVV"  :[[["ttbarWW","ttVV_MGPy8"]],dict_one_SF],
            "ttt"   :[[["ttt","ttt_MGPy8"]],dict_one_SF],
            "tttt"  :[[["4topSM","tttt_MGPy8"]],dict_one_SF],
            "data"  :[
                [
                    ["data","data15"],
                    ["data","data16"],
                    ["data","data17"],
                    ],
                dict_one_SF,
                ],
            "dataB"  :[
                [
                    ["data","data15B"],
                    ["data","data16B"],
                    ["data","data17"],
                    ],
                dict_one_SF,
                ],
            }
        # Done
    # done function

    def set_dict_processMerged_stackInfo(self):
        # stackInfo: processType (S,B,D), color, SF, if overlay what is the scale (0 means no overlay), 
        self.dict_processMerged_stackInfo={
            "Zl"        :["B",ROOT.kAzure-9,1.0,0],
            "Zcl"       :["B",ROOT.kAzure-8,1.0,0],
            "Zhf"       :["B",ROOT.kAzure+2,1.0,0],
            "Wl"        :["B",ROOT.kGreen-9,1.0,0],
            "Wcl"       :["B",ROOT.kGreen-6,1.0,0],
            "Whf"       :["B",ROOT.kGreen+3,1.0,0],
            "stop"      :["B",ROOT.kOrange-1,1.0,0],
            "ttX"       :["B",ROOT.kOrange-7,1.0,0],
            "ttbar"     :["B",ROOT.kOrange,1.0,0],
            "otherHiggs":["B",ROOT.kGray+1,1.0,0],
            "diboson"   :["B",ROOT.kGray,1.0,3],
            "VHbb"      :["S",ROOT.kRed,1.0,3],
            "data"      :["D",ROOT.kBlack,1.0,1],
            }
        #
        self.list_processStack=["Zl","Zcl","Zhf","Wl","Wcl","Whf","stop","ttX","ttbar","diboson","otherHiggs","VHbb","data"]
    # done function


    def set_list_processMerged(self):
        if self.debug:
            print "Start set_list_processMerged()"

        # those stored in .root
        self.list_processMerged=self.list_process+[
            "VHbb",
            # "VHcc",
            "otherHiggs",
            "diboson",
            "Whf",
            "Zhf",
            "stop",
            "ttX",
            "S",
            "B",
            "D",
            # "BplusS",
            ]

        self.dict_processMerged_info={
            "VHbb"     :[["qqZvvHbb","qqWlvHbb","ggZvvHbb","qqZllHbb","ggZllHbb"]],
            "VHcc"     :[["qqZvvHcc","qqWlvHcc","ggZvvHcc","qqZllHcc","ggZllHcc"]],
            "otherHiggs" :[["qqZvvHcc","qqWlvHcc","ggZvvHcc","qqZllHcc","ggZllHcc","qqWincH4l","qqZincH4l","ggH","bbH","VBF","ttH"]],
            "diboson"  :[["WW","WZ","ZZ","ggWW","ggZZ"]],
            "Whf"      :[["Wbb","Wbc","Wbl","Wcc"]],
            "Zhf"      :[["Zbb","Zbc","Zbl","Zcc"]],
            "stop"     :[["stops","stopt","stopWt","stoptZq"]],
            "ttX"     :[["ttV","ttVV","ttt","tttt"]],
            "S"        :[["qqZvvHbb","qqZllHbb","ggZvvHbb","ggZllHbb","qqWlvHbb"]],
            "B"        :[["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","ttV","ttVV","ttt","tttt","stops","stopt","stopWt","stoptZq","WW","WZ","ZZ","ggWW","ggZZ","qqZvvHcc","qqZllHcc","ggZvvHcc","ggZllHcc","qqWlvHcc","qqWincH4l","qqZincH4l","ggH","bbH","VBF","ttH"]],
            "BplusS"      :[["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","ttV","ttVV","ttt","tttt","stops","stopt","stopWt","stoptZq","WW","WZ","ZZ","ggWW","ggZZ","qqZvvHcc","qqZllHcc","ggZvvHcc","ggZllHcc","qqWlvHcc","qqWincH4l","qqZincH4l","ggH","bbH","VBF","ttH","qqZvvHbb","qqZllHbb","ggZvvHbb","ggZllHbb","qqWlvHbb"]],
            "D"        :[["data"]],
            }

    def set_list_processMerged_new(self):
        if self.debug:
            print "Start set_list_processMerged()"

        self.list_process.remove('W')
        self.list_process.remove('Z')

        # those stored in .root
        self.list_processMerged=self.list_process+[
            "VHbb",
            # "VHcc",
            "otherHiggs",
            "diboson",
            "Whf",
            "Zhf",
            "stop",
            "ttX",
            "S",
            "B",
            "D",
            # "BplusS",
            ]

        self.dict_processMerged_info={
            "VHbb"     :[["qqZvvH125","qqWlvH125","ggZvvH125","qqZllH125","ggZllH125"]],
            "VHcc"     :[["qqZvvH125cc","qqWlvH125cc","ggZvvH125cc","qqZllH125cc","ggZllH125cc"]],
            "otherHiggs" :[["qqZvvH125cc","qqWlvH125cc","ggZvvH125cc","qqZllH125cc","ggZllH125cc","qqWincH4l","qqZincH4l","ggH125Inc","VBFH125Inc","bbH125","ttH"]],
            "diboson"  :[["WW","WZ","ZZ","ggWW","ggZZ"]],
            "Whf"      :[["Wbb","Wbc","Wbl","Wcc"]],
            "Zhf"      :[["Zbb","Zbc","Zbl","Zcc"]],
            "stop"     :[["stops","stopt","stopWt","stoptZq"]],
            "ttX"     :[["ttV","ttbarWW","ttt","4topSM"]],
            "S"        :[["qqZvvH125","qqWlvH125","ggZvvH125","qqZllH125","ggZllH125"]],
            "B"        :[["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","ttV","ttbarWW","ttt","4topSM","stops","stopt","stopWt","stoptZq","WW","WZ","ZZ","ggWW","ggZZ","qqZvvH125cc","qqWlvH125cc","ggZvvH125cc","qqZllH125cc","ggZllH125cc","qqWincH4l","qqZincH4l","ggH125Inc","VBFH125Inc","bbH125","ttH"]],
            "BplusS"      :[["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","ttV","ttbarWW","ttt","4topSM","stops","stopt","stopWt","stoptZq","WW","WZ","ZZ","ggWW","ggZZ","qqZvvH125cc","qqWlvH125cc","ggZvvH125cc","qqZllH125cc","ggZllH125cc","qqWincH4l","qqZincH4l","ggH125Inc","VBFH125Inc","bbH125","ttH","qqZvvH125","qqWlvH125","ggZvvH125","qqZllH125","ggZllH125"]],
            "D"        :[["data"]],
            }

    def set_fileNameHistosProcessMerged(self):
        # suffix=""
        suffix="_"+self.list_category[0]+"_"+self.list_variable[0]
        self.fileNameHistosProcessMerged=self.folderHistos+"/histosProcessMerged"+suffix+".root"
    # done function

    def create_histosProcessMerged(self,doSF=True):
        if self.debug or self.verbose:
            print "Start create_histosProcessMerged()"
        # now we want to sum over process for a given processMerged
        outputFile=TFile(self.fileNameHistosProcessMerged,"RECREATE")
        outputFile.Close()
        for variable in self.list_variable:
            for category in self.list_category:
                if self.verbose:
                    print "variable",variable,"category",category
                if "2jet" in category:
                    cat="2"
                elif "3jet" in category:
                    cat="3"
                elif "4jet" in category:
                    cat="4"
                elif "5pjet" in category:
                    cat="5p"
                else:
                    cat="none"   
                if self.debug:
                    print "cat",cat
                for processMerged in self.list_processMerged:
                    counter=0
                    if self.debug:
                        print " %-10s %-10s %-10s" % (variable,category,processMerged)
                    if processMerged not in self.dict_processMerged_info.keys():
                        if self.debug:
                            print "processMerged",processMerged,"is not in  self.dict_processMerged_info"
                        list_process=[processMerged]
                    else:
                        if self.debug:
                            print "processMerged",processMerged,"is not in  self.dict_processMerged_info"
                        list_process=self.dict_processMerged_info[processMerged][0]
                    if self.debug:
                        print "processMerged",processMerged,"list_process",list_process
                    for process in list_process:
                        if self.debug:
                            print "%-10s %-10s %-10s %-10s" % (variable,category,processMerged,process)
                        inputFileName=self.fileNameHistosProcess
                        histoNameProcess      =self.get_histoNameProcess(variable,category,process)
                        histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcess,name=histoNameProcessMerged,returnDummyIfNotFound=False,debug=self.debug)
                        if doSF:
                            if self.debug:
                                print "process",self.dict_process_info[process][1]
                                print "cat",cat
                            SF=self.dict_process_info[process][1][cat]
                        else:
                            SF=1.0
                        if self.debug:
                            print "Scale histo with SF",SF,"type(SF)",type(SF)
                        histo.Scale(SF)
                        if histo=="dummy":
                            continue
                        if counter==0:
                            histoProcessMerged=histo
                        else:
                            histoProcessMerged.Add(histo)
                        counter+=1
                    # done for loop over process that need to be summed to get processMerged
                    if self.debug:
                        print "counter",counter
                    # store the histogram
                    outputFile=TFile(self.fileNameHistosProcessMerged,"UPDATE")
                    histoProcessMerged.SetDirectory(outputFile)
                    histoProcessMerged.Write()
                    outputFile.Close()
                # done for loop over process
            # done for loop over category
        # done for loop over variable
    # done function

    def create_histosProcessMerged_new(self,doSF=True):
        if self.debug or self.verbose:
            print "Start create_histosProcessMerged()"
        # now we want to sum over process for a given processMerged
        outputFile=TFile(self.fileNameHistosProcessMerged,"RECREATE")
        outputFile.Close()
        for variable in self.list_variable:
            for category in self.list_category:
                if self.verbose:
                    print "variable",variable,"category",category
                if "2jet" in category:
                    cat="2"
                elif "3jet" in category:
                    cat="3"
                elif "4jet" in category:
                    cat="4"
                elif "5pjet" in category:
                    cat="5p"
                else:
                    cat="none"   
                if self.debug:
                    print "cat",cat
                for processMerged in self.list_processMerged:
                    counter=0
                    if self.debug:
                        print " %-10s %-10s %-10s" % (variable,category,processMerged)
                    if processMerged not in self.dict_processMerged_info.keys():
                        if self.debug:
                            print "processMerged",processMerged,"is not in  self.dict_processMerged_info"
                        list_process=[processMerged]
                    else:
                        if self.debug:
                            print "processMerged",processMerged,"is not in  self.dict_processMerged_info"
                        list_process=self.dict_processMerged_info[processMerged][0]
                    if self.debug:
                        print "processMerged",processMerged,"list_process",list_process
                    # from ICHEP2018 we get the SF as ratio of post-fit to pre-fit 
                    # and in fit enters directly the processMerged
                    # i.e. Zhf, not Zbb, Zbc, Zbl, Zcc
                    # i.e. Whf, not Wbb, Wbc, Wbl, Wcc
                    # i.e. stop, not stops, stopt, stopWt
                    if doSF:
                        categorySF=self.dict_analysis_channel_category_categorySF[self.analysis+"_"+self.channel+"_"+category]
                        if self.debug:
                            print "categorySF",categorySF
                        if categorySF+"_"+processMerged in self.dict_categorySF_processMerged_SF:
                            SF_Tuple=self.dict_categorySF_processMerged_SF[categorySF+"_"+processMerged]
                        else:
                            SF_Tuple=(1.0,0.0)
                        # done if
                    else:
                        SF_Tuple=(1.0,0.0)
                    # done if
                    SF=SF_Tuple[0]
                    if self.debug:
                        print "Scale histo processMerged",processMerged,"with SF",SF,"type(SF)",type(SF)
                    # now we have the SF for this processMerged
                    # now we multiply this SF to each process that forms processMerged
                    # so that after the SF if you add the corresponding process you get the corresponding processMerged
                    # that gives you the freedom to use the individual process, or the total processMerged
                    # in plots, sensitivities, etc
                    for process in list_process:
                        if self.debug:
                            print "%-10s %-10s %-10s %-10s" % (variable,category,processMerged,process)
                        #inputFileName=self.fileNameHistosProcess
                        inputFileName=self.folderProcessInitial+"/all.root"
                        histoNameProcess      =self.get_histoNameProcess_new(variable,category,process)
                        histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcess,name=histoNameProcessMerged,returnDummyIfNotFound=True,debug=self.debug)
                        if histo=="dummy":
                            continue
                        counter+=1
                        if doSF:
                            histo.Scale(SF)
                        # done if doSFAtProcessLevelOldWay
                        if counter==1:
                            histoProcessMerged=histo
                        else:
                            histoProcessMerged.Add(histo)
                    # done for loop over process that need to be summed to get processMerged
                    if self.debug:
                        print "counter",counter
                    if counter==0:
                        if self.debug:
                            print "No histogram in this category, so set a dummy histogram, taken from ttbar and then reset"
                        process="ttbar"
                        histoNameProcess      =self.get_histoNameProcess_new(variable,category,process)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcess,name=histoNameProcessMerged,returnDummyIfNotFound=False,debug=self.debug)
                        histoProcessMerged=histo
                        histoProcessMerged.Reset()
                    # done if
                    # now we have the histogram histoProcesMerged done
                    # store the histogram
                    outputFile=TFile(self.fileNameHistosProcessMerged,"UPDATE")
                    histoProcessMerged.SetDirectory(outputFile)
                    histoProcessMerged.Write()
                    outputFile.Close()
                # done for loop over process
            # done for loop over category
        # done for loop over variable
    # done function

    def create_folderYields(self):
        self.folderYields=self.folderOutput+"/yields"
        command="mkdir -p "+self.folderYields
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def create_folderResults(self):
        self.folderResults=self.folderOutput+"/results"
        command="mkdir -p "+self.folderResults
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def create_folderPlots(self):
        self.folderPlots=self.folderOutput+"/plots"
        command="mkdir -p "+self.folderPlots
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def set_list_processAnalysis(self):
        self.list_processAnalysis=[
            "qqZvvHbb",
            "qqWlvHbb",
            "ggZvvHbb",
            "qqZllHbb",
            "ggZllHbb",
            "qqZvvHcc",
            "qqWlvHcc",
            "ggZvvHcc",
            "qqZllHcc",
            "ggZllHcc",
            "qqZincH4l",
            "ggH",
            #"ggHbb",
            "bbH",
            "VBF",
            "ttH",
            "WW",
            "WZ",
            "ZZ",
            "ggZZ",
            "ggWW",
            #"ZllZbb",
            #"ZvvZbb",
            #"WlvZbb",
            #"ZllZvv",
            "Wbb",
            "Wbc",
            "Wbl",
            "Wcc",
            "Wcl",
            "Wl",
            "Zbb",
            "Zbc",
            "Zbl",
            "Zcc",
            "Zcl",
            "Zl",
            "ttbar",
            #"ttbarOld",
            #"ttbarDilep",
            #"ttbarDilepOld",
            #"ttbarSpin",
            "stops",
            "stopt",
            "stopWt",
            "stoptZq",
            "ttV",
            "ttVV",
            "ttt",
            "tttt",
            #"dijet",
            "S",
            "B",
            "data",
            "dataB",
            ]
    # done functions

    def get_yieldTuple(self, histo):
        yieldTuple=get_histo_integral_error(histo,myRange=-1,option="",debug=False) # -1 to include the under/over-flow bins
        if self.debug:
            print "yieldTuple= %15.6f +/- %15.6f", yieldTuple
        return yieldTuple
    # done function

    def create_results(self):
        if self.debug or self.verbose:
            print "Start create_results()"
        # suffix=""
        suffix="_"+self.list_category[0]+"_"+self.list_variable[0]
        fileName=self.folderResults+"/results"+suffix+".txt"
        # create a new file
        f = open(fileName,'w')
        if self.debug:
            print "Results:"
        for variable in self.list_variable:
            if self.debug:
                print "variable",variable
            for category in self.list_category:
                if self.debug:
                    print "category",category
                dict_processMerged_histo={}
                for processMerged in self.list_processMerged:
                    if self.debug:
                        print "processMerged",processMerged
                    inputFileName=self.fileNameHistosProcessMerged 
                    histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                    histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcessMerged,name="",returnDummyIfNotFound=False,debug=self.debug)
                    #integralValueError=get_histo_integral_error(histo,myRange=-1,option="",debug=False) # -1 to include the under/over-flow bins
                    #text="%20s %25s %10s %15.8f %15.8f" % (variable, category, processMerged, integralValueError[0], integralValueError[1])
                    dict_processMerged_histo[processMerged]=histo
                    #if self.verbose:
                    #    print text
                    #f.write(text+'\n')
                # done loop over processMerged
                # have access to the histograms
                for processResult in self.list_processResult:
                    if self.verbose:
                        print "processResult",processResult
                    if "/" in processResult:
                        # ratio of yields
                        processResultNumer=processResult.split("/")[0]
                        processResultDenom=processResult.split("/")[1]
                        yieldTupleNumer=self.get_yieldTuple(dict_processMerged_histo[processResultNumer])
                        yieldTupleDenom=self.get_yieldTuple(dict_processMerged_histo[processResultDenom])
                        tupleResult=ratioError(yieldTupleNumer[0],yieldTupleNumer[1],yieldTupleDenom[0],yieldTupleDenom[1])
                    elif "SigY_" in processResult:
                        # significance sigma B from yields
                        processResultNumer=processResult.split("_")[1]
                        processResultDenom=processResult.split("_")[2]
                        yieldTupleNumer=self.get_yieldTuple(dict_processMerged_histo[processResultNumer])
                        yieldTupleDenom=self.get_yieldTuple(dict_processMerged_histo[processResultDenom])
                        tupleResult=significanceSigmaB(yieldTupleNumer[0],yieldTupleNumer[1],yieldTupleDenom[0],yieldTupleDenom[1])
                    elif "SigH_" in processResult:
                        # significance sigma B from histogram bins (using shape too)
                        processResultNumer=processResult.split("_")[1]
                        processResultDenom=processResult.split("_")[2]
                        sig_h=dict_processMerged_histo[processResultNumer].Clone()
                        bkg_h=dict_processMerged_histo[processResultDenom].Clone()
                        if self.debug:
                            getBinValues(sig_h)
                            getBinValues(bkg_h)
                        figureOfMerit="SignificanceSigmaB"
                        a=get_dict_figureOfMerit_histo(sig_h,bkg_h,list_figureOfMerit=[figureOfMerit],debug=self.debug)
                        h=a[figureOfMerit]
                        tupleResult=add_in_quadrature_bins_of_one_histo(h,IncludeUnderflowOverflowBins=False,debug=False)
                    else:
                        # yield of one process already in processMerged
                        tupleResult=self.get_yieldTuple(dict_processMerged_histo[processResult])
                    # done if
                    text="%20s %25s %10s %15.8f %15.8f" % (variable, category, processResult, tupleResult[0], tupleResult[1])
                    if self.verbose:
                        print text
                    f.write(text+'\n')
            # done loop over category
        # done loop over variable
        f.close()
    # done function

    def read_results(self):
        if self.debug or self.verbose:
            print "Start read_results()"
        self.dict_variable_category_processResult_tupleResult={}
        suffix="_"+self.list_category[0]+"_"+self.list_variable[0]
        fileName=self.folderResults+"/results"+suffix+".txt"
        for line in open(fileName, 'r'):
            line=line.rstrip()
            if self.debug:
                print "line",line
            list_line=line.split()
            variable=list_line[0]
            category=list_line[1]
            processResult=list_line[2]
            tupleResult=(float(list_line[3]),float(list_line[4]))
            text="%20s %25s %10s %15.8f %15.8f" % (variable, category, processResult, tupleResult[0], tupleResult[1])
            if self.verbose:
                print text
            self.dict_variable_category_processResult_tupleResult[variable+"_"+category+"_"+processResult]=tupleResult
        # done loop over lines in file
        # the dictionary is filled
        # no need to result, as it is private variable of class
    # done function

    def create_yield_latex_table(self,doDocument=True):
        if self.debug or self.verbose:
            print "Start create_yield_latex_table()"
        for variable in self.list_variable:
            if self.debug:
                print "variable",variable
                   # we create the latex table
            fileName=self.folderYields+"/table_"+variable+".tex"
            # create a new file
            f = open(fileName,'w')
            if doDocument:
                f.write('\\documentclass{beamer}\n')
                f.write('\\usepackage{tabularx}\n')
                f.write('\\usepackage{adjustbox}\n')
                f.write('\\usepackage{pdflscape}\n')
                f.write('\\begin{document}\n')
            # done if
            f.write('\\begin{frame}{\\texttt{\\detokenize{'+ self.name+' '+variable+'}}}\n')
            # f.write('\\begin{center}\n')
            f.write('\\begin{landscape} \n')
            f.write('\\adjustbox{max height=\\dimexpr\\textheight-9.0cm\\relax,max width=\\textwidth}\n')
            f.write('{\n')
            text="\\begin{tabular}{|l"
            for category in self.list_category:
                text+="|l"
            text+="|}\n"
            f.write(text)
            f.write('\\hline \n')
            f.write('\\hline \n')
            text="Process vs Category"
            for category in self.list_category:
                text+=" & \\texttt{\\detokenize{"+category+"}}"
            text+=" \\\\ \n"
            f.write(text)
            f.write('\\hline \n')
            # add one processResult one at a time
            for processResult in self.list_processResult:
                # info=self.dict_processMerged_info[processMergedType]
                # doAddLineAfter=bool(info[1])
                if processResult=="qqZincH4l" or processResult=="dijet" or processResult=="stop" or processResult=="data" or processResult=="VHbb":
                    doAddLineAfter=True
                else:
                    doAddLineAfter=False
                #if self.debug:
                #    print processMergedType,info[1],type(info[1]),doAddLineAfter,type(doAddLineAfter)
                if "@" in processResult:
                    list_processResult=processResult.split("@")
                    processResult=list_processResult[0]
                    currentVariable=list_processResult[1]
                    text="\\texttt{\\detokenize{"+processResult+" "+currentVariable+"}}"
                else:
                    # regular processResult
                    currentVariable=variable
                    text="\\texttt{\\detokenize{"+processResult+"}}"
                    nrDigits="2"
                # done if
                for category in self.list_category:
                    tupleResult=self.dict_variable_category_processResult_tupleResult[currentVariable+"_"+category+"_"+processResult]
                    if tupleResult[0]>0.01:
                        if "@" in processResult:
                            text+=" & {\\color{orange}%.2f$\pm$%.2f}" % tupleResult
                        else:
                            text+=" & {\\color{orange}%.3f$\pm$%.3f}" % tupleResult
                    else:
                        text+=" & {\\color{orange}%.4f$\pm$%.4f}" % tupleResult
                # done loop over category
                text+=" \\\\ \n"
                f.write(text)
                if doAddLineAfter:
                    f.write('\\hline \n')
            # done for loop over processResult
            f.write('\\hline \n')
            f.write('\\end{tabular}\n')
            f.write('}\n')
            f.write('\\end{landscape} \n')
            # f.write('\\end{center}\n')
            f.write('\\end{frame}\n')
            if doDocument:
                f.write('\\end{document}\n')
            f.close()
        # done loop over variable
    # done function

    def create_yield_latex_table2(self):
        if self.debug or self.verbose:
            print "Start create_yield_latex_table()"
        for variable in self.list_variable:
            if self.debug:
                print "variable",variable
                   # we create the latex table
            fileName=self.folderYields+"/table_"+variable+".tex"
            # create a new file
            f = open(fileName,'w')
            f.write('\\documentclass{beamer}\n')
            f.write('\\usepackage{tabularx}\n')
            f.write('\\usepackage{adjustbox}\n')
            f.write('\\usepackage{pdflscape}\n')
            f.write('\\begin{document}\n')
            f.write('\\begin{frame}{\\texttt{\\detokenize{'+ self.name+' '+variable+'}}}\n')
            # f.write('\\begin{center}\n')
            f.write('\\begin{landscape} \n')
            f.write('\\adjustbox{max height=\\dimexpr\\textheight-7.0cm\\relax,max width=\\textwidth}\n')
            f.write('{\n')
            text="\\begin{tabular}{|l"
            for category in self.list_category:
                text+="|l"
            text+="|}\n"
            f.write(text)
            f.write('\\hline \n')
            f.write('\\hline \n')
            text="Process vs Category"
            for category in self.list_category:
                text+=" & \\texttt{\\detokenize{"+category+"}}"
            text+=" \\\\ \n"
            f.write(text)
            f.write('\\hline \n')
            # add one processResult one at a time
            print "ADRIAN ",self.list_processResult
            for processResult in self.list_processResult:
                # info=self.dict_processMerged_info[processMergedType]
                # doAddLineAfter=bool(info[1])
                if processResult=="qqZincH4l" or processResult=="dijet" or processResult=="stop" or processResult=="data" or processResult=="otherHiggs":
                    doAddLineAfter=True
                else:
                    doAddLineAfter=False
                #if self.debug:
                #    print processMergedType,info[1],type(info[1]),doAddLineAfter,type(doAddLineAfter)
                text="\\texttt{\\detokenize{"+processResult+"}}"
                for category in self.list_category:
                    tupleResult=self.dict_variable_category_processResult_tupleResult[variable+"_"+category+"_"+processResult]
                    if tupleResult[0]>0.01:
                        text+=" & {\\color{orange}%.2f$\pm$%.2f}" % tupleResult
                    else:
                        text+=" & {\\color{orange}%.4f$\pm$%.4f}" % tupleResult
                # done loop over category
                text+=" \\\\ \n"
                f.write(text)
                if doAddLineAfter:
                    f.write('\\hline \n')
            # done for loop over processResult
            f.write('\\hline \n')
            f.write('\\end{tabular}\n')
            f.write('}\n')
            f.write('\\end{landscape} \n')
            # f.write('\\end{center}\n')
            f.write('\\end{frame}\n')
            f.write('\\end{document}\n')
            f.close()
        # done loop over variable
    # done function

    def create_yield_latex_table_compare(self,ref,doDocument=True,debug=False):
        if debug:
            print "Start create_yield_latex_table_compare()"
        # the ratios will be made to the first element on the left
        list_stem=[ref.stem,self.stem]
        if debug:
            print "list_stem",list_stem
        dict_stem_analysis={
            ref.stem:ref,
            self.stem:self,
            }
        for variable in self.list_variable:
            if debug:
                print "variable",variable
            for category in self.list_category:
                if debug:
                    print "category",category
                # we create the latex table
                fileName=self.folderYields+"/table_comparison_"+variable+"_"+category+".tex"
                # create a new file
                f = open(fileName,'w')
                print "doDocument",doDocument
                if doDocument:
                    f.write('\\documentclass{beamer}\n')
                    f.write('\\usepackage{tabularx}\n')
                    f.write('\\usepackage{adjustbox}\n')
                    f.write('\\usepackage{pdflscape}\n')
                    f.write('\\begin{document}\n')
                # done if
                text='\\begin{frame}{Cat: \\texttt{\\detokenize{'+category+'}}; Var: \\texttt{\\detokenize{'+variable+'}};'
                #text+=' \\\\ Comp: \\texttt{\\detokenize{'+comparison+'}}; Stem:'
                #for i,stem in enumerate(list_stem):
                #    if i>0:
                #        text+=' vs'  
                #    text+=' {\\color{black}\\texttt{\\detokenize{'+dict_stem_analysis[stem].stem+'}}}'
                text+='.}'
                f.write(text+'\n')
                # continue
                # f.write('\\begin{center}\n')
                f.write('\\begin{landscape} \n')
                text='\\adjustbox{max height=\\dimexpr\\textheight-'
                if doDocument:
                    text+='7.0'
                else:
                    text+='8.5'
                text+='cm\\relax,max width=\\textwidth}'
                f.write(text+'\n')
                f.write('{\n')
                text="\\begin{tabular}{|l"
                for stem in list_stem:
                    text+="|l"
                text+="|l|l|}"
                f.write(text+'\n')
                f.write('\\hline \n')
                f.write('\\hline \n')
                text="Process vs Stem"
                for stem in list_stem:
                    text+=" & \\texttt{\\detokenize{"+stem+"}}"
                for i,stem in enumerate(list_stem):
                    if i==0:
                        continue
                    #text+=" & \\texttt{\\detokenize{Ratio "+stem.split("_")[-1]+" to "+list_stem[0].split("_")[-1]+"}}"
                    text+=" & Ratio right to left"
                    #text+=" & Ratio of relative error"
                text+=" \\\\"
                f.write(text+'\n')
                f.write('\\hline \n')
                # add one processResult one at a time
                for processResult in self.list_processResult:
                    # info=self.dict_processMerged_info[processMergedType]
                    # doAddLineAfter=bool(info[1])
                    if processResult=="qqZincH4l" or processResult=="dijet" or processResult=="data" or processResult=="VHbb":
                        doAddLineAfter=True
                    else:
                        doAddLineAfter=False
                    #if self.debug:
                    #    print processMergedType,info[1],type(info[1]),doAddLineAfter,type(doAddLineAfter)
                    if "@" in processResult:
                        list_processResult=processResult.split("@")
                        processResult=list_processResult[0]
                        currentVariable=list_processResult[1]
                        text="\\texttt{\\detokenize{"+processResult+" "+currentVariable+"}}"
                    else:
                        # regular processResult
                        currentVariable=variable
                        text="\\texttt{\\detokenize{"+processResult+"}}"
                        nrDigits="2"
                    # done if
                    tupleResultDenom=ref.dict_variable_category_processResult_tupleResult[currentVariable+"_"+category+"_"+processResult]
                    # a is the first one, so the reference
                    # done loop over stem
                    for stem in list_stem:
                        if False:
                            print "stem",stem
                        ana=dict_stem_analysis[stem]
                        tupleResult=ana.dict_variable_category_processResult_tupleResult[currentVariable+"_"+category+"_"+processResult]
                        if tupleResult[0]>0.01:
                            if "@" in processResult:
                                text+=" & {\\color{orange}%.2f$\pm$%.2f}" % tupleResult
                            else:
                                text+=" & {\\color{orange}%.3f$\pm$%.3f}" % tupleResult
                        else:
                            text+=" & {\\color{orange}%.4f$\pm$%.4f}" % tupleResult
                    # done loop over stem
                    # add the ratio
                    for i,stem in enumerate(list_stem):
                        if i==0:
                            continue
                        ana=dict_stem_analysis[stem]
                        tupleResultNumer=ana.dict_variable_category_processResult_tupleResult[currentVariable+"_"+category+"_"+processResult]
                        # tupleResultNumer=tupleResult # from ana, the last one, which is also the second one
                        tupleResultRatio=ratioTuple(tupleResultNumer,tupleResultDenom,debug=False) # a is the first one, ana is the last one
                        text+=" & {\\color{orange}%.3f$\pm$%.3f}" % tupleResultRatio
                    # done if
                    # add the ratio of relative errors
                    #relativeErrorDenom=ratio(tupleResultDenom[1],tupleResultDenom[0])
                    #relativeErrorNumer=ratio(tupleResultNumer[1],tupleResultNumer[0])
                    #relativeErrorRatio=ratio(relativeErrorNumer,relativeErrorDenom)
                    #text+=" & {\\color{orange}%.3f}" % relativeErrorRatio
                    # 
                    text+=" \\\\ \n"
                    f.write(text)
                    if doAddLineAfter:
                        f.write('\\hline \n')
                # done for loop over processResult
                f.write('\\hline \n')
                f.write('\\end{tabular}\n')
                f.write('}\n')
                f.write('\\end{landscape} \n')
                # f.write('\\end{center}\n')
                f.write('\\end{frame}\n')
                if doDocument:
                    f.write('\\end{document}\n')
                f.close()
                # compile to make pdf
                # os.system("pdflatex "+fileName)
            # done loop over category
        # done loop over variable
    # done function

    def create_overlaid_variable(self):
        if self.debug or self.verbose:
            print "Start create_overlaid_variable()"
        inputFileName=self.fileNameHistosProcessMerged
        #self.list_processMerged=["qqZvvHbb","qqWlvHbb","ggZvvHbb","WZ","ZZ","ggZZ","ttbar","stop","Whf","Zhf"]
        self.list_processMerged=["qqZvvHbb","qqWlvHbb","ggZvvHbb","WZ","ZZ","ggZZ"]
        self.debug=False
        for processMerged in self.list_processMerged:
            if self.debug:
                print "processMerged",processMerged
            for category in self.list_category:
                if self.debug:
                    print "category",category
                list_tuple_h1D=[]
                self.list_color=[1,4,2,8,ROOT.kOrange,ROOT.kMagenta,6,7,8,9,10]
                # list_variable=["mBBNominal","mBBOneMu20GeV","mBBOneMu10GeV","mBBOneMu4GeV","mBBAllMu","mBBPtReco"]
                # list_variable=["mBBNominal","mBBOneMu10GeV","mBBOneMu4GeV","mBBPtReco"]
                list_variable=self.list_variable
                for i,variable in enumerate(list_variable):
                    if self.debug:
                        print "variable",variable
                    if processMerged=="WZ" or processMerged=="WW" or processMerged=="ZZ" or processMerged=="ggWW" or processMerged=="ggZZ":
                        legend_info=[0.56,0.35,0.88,0.70,72,0.037,0]
                        text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; "+self.name+"}?#bf{"+category+"; "+processMerged+"}",0.04,13,0.50,0.88,0.05)
                    else:
                        legend_info=[0.12,0.35,0.40,0.70,72,0.037,0]
                        text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; "+self.name+"}?#bf{"+category+"; "+processMerged+"}",0.04,13,0.15,0.88,0.05)
                    info=self.dict_variable_info[variable]
                    # binRange=info[0]
                    debug_binRange=False
                    debug=False
                    # binRange=get_binRange(5,60,10,debug_binRange)+","+get_binRange(60,140,5,debug_binRange)+","+get_binRange(140,180,10,debug_binRange)
                    binRange=get_binRange(50,160,5,debug_binRange)
                    histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                    histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcessMerged,name="",returnDummyIfNotFound=False,debug=self.debug)
                    # rebin, collect overflows, do average
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    histo=get_histo_generic_binRange(histo,binRange=binRange,option="sum",debug=debug)
                    if "ptOneMuInJet" in variable or "dRMuonInJet" in variable or "PtRatioOneMuonInJet" in variable or "PtRatioOneElectronInJet" in variable:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=False,addOverflow=True,debug=False)
                    else:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=True, addOverflow=True,debug=False)
                    histo=get_histo_averaged_per_bin_width(histo,debug=debug)
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    # 
                    legend=processMerged
                    #histo=get_histo_generic_binRange(histo,binRange=binRange,option="average2",debug=self.debug)
                    #histo=histo.Clone()
                    #getBinValues(histo,doRescaleMeVtoGeV=False,significantDigits=2,debug=self.debug)
                    histo.SetLineColor(self.list_color[i])
                    # histo.SetXTitle(variable)
                    histo.SetXTitle("mBB [ GeV ]")
                    histo.SetYTitle("Event density per bin width")
                    bJetCorr=variable.replace("mBB","")
                    list_tuple_h1D.append((histo,bJetCorr))
                # done loop over process
                outputFileName=self.folderPlots+"/overlay_variable_"+category+"_"+processMerged
                overlayHistograms(list_tuple_h1D,fileName=outputFileName,extensions="eps,pdf,png",option="histo",doValidationPlot=False,canvasname="canvasname",addHistogramInterpolate=False,addfitinfo=True,addMedianInFitInfo=False,significantDigits=("3","3","3","3"),min_value=-1,max_value=-1,min_multiply=0.9,max_multiply=1.1,YTitleOffset=0.45,doRatioPad=False,min_value_ratio=0.5,max_value_ratio=1.5,statTitle="MC. stat uncertainty",statColor=6,ratioTitle="Ratio to data",plot_option="",plot_option_ratio="HIST",text_option=text_option,legend_info=legend_info,line_option=([0,0.5,0,0.5],2),debug=self.debug)
            # done loop over category
        # done loop over variable
    # done function

    def create_overlaid_plots(self):
        if self.debug or self.verbose:
            print "Start create_overlaid_plots()"
        inputFileName=self.fileNameHistosProcessMerged
        # default
        list_color=[8,4,2,1] # B,S,BplusS,D
        list_color=[8,4,1] # B,S,D
        min_value_ratio=0.2
        max_value_ratio=1.7
        # for BadBatman small differences expected, smaller ratio plots
        #list_color=[2,1]
        #min_value_ratio=0.9
        #max_value_ratio=1.1
        for variable in self.list_variable:
            if self.debug:
                print "variable",variable
            if "mBB" in variable or "mva" in variable: 
                # blinded, do not show data at all
                # list_processMerged="B,S,BplusS,D".split(",")
                list_processMerged="B,S,D".split(",")
            else:
                # not blinded, include data
                # list_processMerged="B,S,BplusS,D".split(",")
                list_processMerged="B,S,D".split(",")
            # done if
            if variable in self.dict_variable_info.keys():
                info=self.dict_variable_info[variable]
                binRange=info[0]
            else:
                binRange=""
            # done if
            for category in self.list_category:
                if self.debug:
                    print "category",category
                if variable=="mva":
                    if "2jet" in category:
                        binRange=self.binRange_mva2J
                    elif "3jet" in category:
                        binRange=self.binRange_mva3J
                    else:
                        binRange=self.binRange_mva3J
                    # done if
                # done if
                list_tuple_h1D=[]
                for i,processMerged in enumerate(list_processMerged):
                    if self.debug:
                        print "processMerged",processMerged
                    histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                    histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcessMerged,name="",returnDummyIfNotFound=False,debug=self.debug)
                    legend=processMerged
                    # scale the signal
                    #signalScale=5
                    #if processMerged=="S":
                    #    histo.Scale(signalScale)
                    #    legend+=" x "+str(signalScale)
                    # done if
                    # blind the data
                    if processMerged=="D" or processMerged=="data":
                        if "mBB" in variable:
                            histo=get_histo_blinded_from_binRange(histo,binRange=[80,140],debug=False)
                        elif "mva" in variable:
                            histo=get_histo_blinded_from_binRange(histo,binRange=[0.3,1.0],debug=False)
                        else:
                            None
                        # done if
                    # done if
                    # rebin, collect overflows, do average
                    debug=False
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    histo=get_histo_generic_binRange(histo,binRange=binRange,option="sum",debug=debug)
                    if "ptOneMuInJet" in variable or "dRMuonInJet" in variable or "PtRatioOneMuonInJet" in variable or "PtRatioOneElectronInJet" in variable:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=False,addOverflow=True,debug=False)
                    else:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=True, addOverflow=True,debug=False)
                    histo=get_histo_averaged_per_bin_width(histo,debug=debug)
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    # prepare histograms
                    histo.SetLineColor(list_color[i])
                    histo.SetXTitle(variable)
                    histo.SetYTitle("Event density per bin width")
                    list_tuple_h1D.append((histo,legend))
                # done loop over process
                outputFileName=self.folderPlots+"/overlay_BDS_"+variable+"_"+category
                overlayHistograms(list_tuple_h1D,fileName=outputFileName,extensions="pdf",option="histo",doValidationPlot=False,canvasname="canvasname",addHistogramInterpolate=False,addfitinfo=False,addMedianInFitInfo=False,significantDigits=("3","3","3","3"),min_value=0,max_value=-1,YTitleOffset=0.45,doRatioPad=True,min_value_ratio=min_value_ratio,max_value_ratio=max_value_ratio,statTitle="MC. stat uncertainty",statColor=6,ratioTitle="Ratio to bkg",plot_option="HIST E",plot_option_ratio="E",text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; "+self.name+"}?#bf{"+variable+"}?#bf{"+category+"}",0.04,13,0.15,0.88,0.05),legend_info=[0.70,0.70,0.88,0.88,72,0.037,0],line_option=([0,0.5,0,0.5],2),debug=False)
            # done loop over category
        # done loop over variable
        #command="$All/BuzatuBash/make_html.sh "+self.folderPlots
        #os.system(command)
    # done function

    def create_stacked_plots(self):
        if self.verbose:
            print "Start create_stacked_plots()"
        inputFileName=self.fileNameHistosProcessMerged
        self.set_dict_processMerged_stackInfo()
        for variable in self.list_variable:
            if self.debug:
                print "variable",variable
            if variable in self.dict_variable_info.keys():
                info=self.dict_variable_info[variable]
                binRange=info[0]
            elif "mBBJ" in variable:
                binRange=self.dict_variable_info["mBBJ"][0]
                print "ADRIAN mBBJ"     
                print "ADRIAN binRange",binRange
            elif "mBB" in variable:
                binRange=self.dict_variable_info["mBB"][0]
                print "ADRIAN mBB"     
                print "ADRIAN binRange",binRange
            elif "pTB1" in variable:
                binRange=self.dict_variable_info["pTB1"][0]
            elif "pTB2" in variable:
                binRange=self.dict_variable_info["pTB2"][0]
            elif "SumPtJet" in variable:
                binRange=self.dict_variable_info["SumPtJet"][0]
            elif "HT" in variable:
                binRange=self.dict_variable_info["HT"][0]
            elif "dRBB" in variable:
                binRange=self.dict_variable_info["dRBB"][0]
            elif "dEtaBB" in variable:
                binRange=self.dict_variable_info["dEtaBB"][0]
            elif "dPhiBB" in variable:
                binRange=self.dict_variable_info["dPhiBB"][0]
            elif "dPhiVBB" in variable:
                binRange=self.dict_variable_info["dPhiVBB"][0]
            elif "pTJ3" in variable:
                binRange=self.dict_variable_info["pTJ3"][0]
            elif "EtaB1" in variable:
                binRange=self.dict_variable_info["EtaB1"][0]
            elif "EtaB2" in variable:
                binRange=self.dict_variable_info["EtaB2"][0]
            elif "EtaJ3" in variable:
                binRange=self.dict_variable_info["EtaJ3"][0]
            elif "PhiB1" in variable:
                binRange=self.dict_variable_info["PhiB1"][0]
            elif "PhiB2" in variable:
                binRange=self.dict_variable_info["PhiB2"][0]
            elif "PhiJ3" in variable:
                binRange=self.dict_variable_info["PhiJ3"][0]
            elif "yBB" in variable:
                binRange=self.dict_variable_info["yBB"][0]
            elif "pTBBoverMET" in variable:
                binRange=self.dict_variable_info["pTBBoverMET"][0]
            elif "pTBBMETAsym" in variable:
                binRange=self.dict_variable_info["pTBBMETAsym"][0]
            elif "pTBB" in variable:
                binRange=self.dict_variable_info["pTBB"][0]
            else:
                binRange=""
            # done if
            for category in self.list_category:
                if True or self.debug:
                    print "category",category,"stem",self.stem,"channel",self.channel
                if variable=="mva":
                    if "2jet" in category:
                        binRange=self.binRange_mva2J
                    elif "3jet" in category:
                        binRange=self.binRange_mva3J
                    else:
                        binRange=self.binRange_mva3J
                    # done if
                # done if
                list_tuple_h1D=[]
                for i,processMerged in enumerate(self.list_processStack):
                    if self.debug:
                        print "processMerged",processMerged
                    histoNameProcessMerged=self.get_histoNameProcess(variable,category,processMerged)
                    histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcessMerged,name="",returnDummyIfNotFound=False,debug=self.debug)
                    if "mBB" in variable and variable!="mBBJ":
                        blinding=["range",[80,140]]
                    elif variable=="mva" or variable=="mvadiboson":
                        blinding=["range",[0.3,1.0]]
                    else:
                        blinding=["threshold",0.05]
                    # done if

                    # blind the data
                    #if processMerged=="data" or processMerged=="D":
                        #if "mBB" in variable:
                        #    histo=get_histo_blinded_from_binRange(histo,binRange=[80,140],debug=False)
                        #elif "mva" in variable:
                        #    histo=get_histo_blinded_from_binRange(histo,binRange=[0.3,1.0],debug=False)
                        #else:
                        #    None
                        # done if
                    # done if
                    # rebin, collect overflows, do average
                    debug=False
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    histo=get_histo_generic_binRange(histo,binRange=binRange,option="sum",debug=debug)
                    if "ptOneMuInJet" in variable or "dRMuonInJet" in variable or "PtRatioOneMuonInJet" in variable or "PtRatioOneElectronInJet" in variable:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=False,addOverflow=True,debug=False)
                    else:
                        histo=get_histo_underflows_in_edge_bins(histo,addUnderflow=True, addOverflow=True,debug=False)
                    #histo=get_histo_averaged_per_bin_width(histo,debug=debug)
                    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,doUnderflow=True,doOverflow=True,debug=debug)
                    if "TruthWZ" in variable and processMerged=="data":
                        histo.Reset()
                    # prepare histograms
                    list_info=self.dict_processMerged_stackInfo[processMerged]
                    #histo.SetLineColor(color)
                    #histo.SetFillColor(color)
                    #histo.SetXTitle(variable)
                    #histo.SetYTitle("Event density per bin width")
                    #if self.debug:
                    #    print "histo",histo,"processMerged",processMerged,"processType",processType,"SF",SF
                    list_tuple_h1D.append((histo,processMerged,list_info))
                # done loop over processMerged
                outputFileName=self.folderPlots+"/stack_"+variable.replace("_","")+"_"+category
                # stackHistograms(list_tuple_h1D,stackName="stackName",outputFileName=outputFileName,extensions="pdf",text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; "+self.name+"}?#bf{"+variable+"}?#bf{"+category+"}",0.04,13,0.15,0.88,0.05),legend_info=[0.72,0.25,0.88,0.88,72,0.037,0],debug=self.debug)
                stackHistograms(list_tuple_h1D,stackName="stackName",outputFileName=outputFileName,extensions="pdf",blinding=blinding,doAveragePerBinWidth=True,text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV}?#bf{"+self.name+"}?#bf{"+category+"}",0.04,13,0.15,0.92,0.05),xAxisTitle=variable,debug=False)
                print "outside stackHistograms"
            # done loop over category
        # done loop over variable
    # done function

    ### print

    def print_list_category(self):
        print "list_category",self.list_category

    def print_lists(self):
        print "\n Print our lists:"
        print "\n list_variable",self.list_variable
        print "\n list_category",self.list_category
        print "\n list_process",self.list_process
        print "\n list_processInitial",self.list_processInitial
        # print "\n list_all",self.list_all

    def print_all(self):
        print ""
        print "Printing all for Analysis",self.name,":"
        self.print_list_category()
        print "debug",self.debug
        print "folderInput",self.folderInput
        print "folderOutput",self.folderOutput
        print "list_processInitial",self.list_processInitial
       
    ### summary

    def do_evaluate_contents(self):
        # then evaluate the content of these files                                                                                                                              
        self.create_folderProcessInitial()
        if self.do_evaluate_list_processInitial:
            self.evaluate_list_processInitial(option="processInitial")
        self.set_evaluated_list_processInitial()
        if self.do_evaluate_content_of_all_processInitial:
            self.evaluate_content_of_all_processInitial()
        self.set_evaluated_list_process()
        self.set_evaluated_list_category()
        self.set_evaluated_list_variable()
        self.set_evaluated_list_all()
    # done function

    def do_hadd_first(self):
        if self.debug:
            print "Start do_hadd_first()"
        self.create_folderProcessInitial()
        if self.do_evaluate_list_processInitial:
            self.evaluate_list_processInitial(option="ReaderBatch")
        self.set_evaluated_list_processInitial()
        if self.do_hadd_processInitial:
            self.hadd_each_processInitial()
        # self.create_folderFitInput()
        # dict_stem_analysis[stem].set_do_hadd_all_processInitial_to_produce_fit_inputs(True)
        # re-evaluate from the folder output if you put by hand new folders, like data16B
        self.do_evaluate_contents()
    # done function

    def do_cp_second(self):
        if self.debug:
            print "Start do_cp_second()"
        self.create_folderProcessInitial()
        command="cp -r"
        if self.name.endswith("_D"):
            folder1=self.folderOutput.replace("_D","_D1")
            folder2=self.folderOutput.replace("_D","_D2")
            print "Copying D1 and D2 into D."
        elif self.name.endswith("_T"):
            folder1=self.folderOutput.replace("_T","_T1")
            folder2=self.folderOutput.replace("_T","_T2")
            print "Copying T1 and T2 into T."
        elif self.name.endswith("_TD"):
            folder1=self.folderOutput.replace("_TD","_D1")
            folder2=self.folderOutput.replace("_TD","_T2")
            print "Copying D1 and T2 into TD."
        else:
            print "name",self.name,"does not end in _D or _T, or TD. Will ABORT!!!"
            assert(False)
        # done if
        command+=" "+folder1+"/processInitial/*.root" 
        command+=" "+folder2+"/processInitial/*.root"
        command+=" "+self.folderProcessInitial+"/."
        if self.debug or self.verbose:
            print "command="+command
        os.system(command)
        if self.debug or self.verbose:
            print "Done copied the .root file in the new processInitial"
        # then evaluate the content of these files
        self.do_evaluate_contents()
    # done function

    def do_hadd_second(self):
        if self.debug:
            print "Start do_hadd_second()"
        self.create_folderHistos()
        self.set_fileNameHistosInput()
        command="hadd -f"
        command+=" "+self.folderHistos+"/input.root"
        if self.name.endswith("_D"):
            folder1=self.folderOutput.replace("_D","_D1")
            folder2=self.folderOutput.replace("_D","_D2")
        elif self.name.endswith("_T"):
            folder1=self.folderOutput.replace("_T","_D1")
            folder2=self.folderOutput.replace("_T","_T2")
        else:
            print "name",self.name,"does not end in _D or _T. Will ABORT!!!"
            assert(False)
        # done if
        command+=" "+folder1+"/processInitial/*.root"
        command+=" "+folder2+"/processInitial/*.root"
        if self.debug or self.verbose:
            print "command="+command
        os.system(command)
    # done function

    def do_all_begining_deprecated(self):
        if self.debug:
            print "Start do_all()"
        self.create_folderProcessInitial()
        if self.do_evaluate_list_processInitial:
            self.evaluate_list_processInitial(option="ReaderBatch")
        self.set_evaluated_list_processInitial()
        if self.do_hadd_processInitial:
            self.hadd_each_processInitial()
        # self.create_folderFitInput()
        # dict_stem_analysis[stem].set_do_hadd_all_processInitial_to_produce_fit_inputs(True)
        # re-evaluate from the folder output if you put by hand new folders, like data16B
        if self.do_evaluate_list_processInitial:
            self.evaluate_list_processInitial(option="processInitial")
        if self.do_evaluate_content_of_all_processInitial:
            self.evaluate_content_of_all_processInitial()
        self.set_evaluated_list_process()
        self.set_evaluated_list_category()
        self.set_evaluated_list_variable()
        self.set_evaluated_list_all()
        #if self.hadd_all_processInitial_to_produce_fit_inputs:
        #    self.hadd_all_processInitial_to_produce_fit_inputs()


    def do_all(self):
        self.create_folderHistos()
        self.set_fileNameHistosRaw()
        self.set_fileNameHistosProcess()
        self.set_fileNameHistosProcessMerged()
        self.create_folderYields()
        self.create_folderResults()
        self.create_folderPlots()
        self.set_dict_variable_info()
        self.list_color=[1,4,2,8,ROOT.kOrange]
        # self.debug=False
        
        #if self.doFirst:
        #    return

        #return

        #if True:
        #    self.create_histosRaw()

        doTTbarStudy=False
        if doTTbarStudy:
            if self.debug:
                self.print_lists()
            #self.set_list_category(["0tag2jet_150ptv_SR","0tag3jet_150ptv_SR","1tag2jet_150ptv_SR","1tag3jet_150ptv_SR","2tag2jet_150ptv_SR","2tag3jet_150ptv_SR"])
            self.set_list_category(["2tag2jet_150ptv_SR"])
            self.set_list_process(["ttbar"])
            self.set_list_processInitial(["ttbar_nonallhad_PwPy8","ttbar_allhad_PwPy8"])
            #self.set_list_process(["ttbar"])
            #self.set_list_processInitial(["ttbar_nonallhad_PwPy8","ttbar_allhad_PwPy8"])
            #ZvvZbb, ZllZbb -> ZZ_bb_Sh221
            #ZZ -> ZZ_Sh221
            if self.debug:
                self.print_lists()
            self.create_histosRaw()
            self.set_folderPlotsHistosRawByProcessInitial()
            if self.do_overlay_histosRaw_by_processInitial:
                self.overlay_histosRaw_by_processInitial()
        # done if doTTbarStudy

        doYields=True
        if doYields:
            # remove ttbar_nonallhad from our processInitial
            list_processInitial=[]
            for processInitial in self.list_processInitial:
                #if processInitial!="ttbar_nonallhad":
                #    continue
                list_processInitial.append(processInitial)
            # done for loop
            self.list_processInitial=list_processInitial
            if self.debug:
                print "self.list_processInitial",self.list_processInitial
            # remove W and Z from process
            list_process=[]
            if self.debug:
                print "list_process",self.list_process
            for process in self.list_process:
                #if process=="W" or process=="Z" or "MadZee" in process or "MadZmumu" in process or process=="ggWW":
                if process=="W" or process=="Z" or "MadZee" in process or "MadZmumu" in process:
                    print "WARNING!!! finding process",process,"will skip them!"
                    continue
                list_process.append(process)
            # done for loop
            #self.list_process=list_process
            #self.list_process=["ttbar"]
            #self.list_process=["data"]
            # reduce category
            # if self.do_later or True:
            if self.do_later and False:
                if "MVA" in self.stem:
                    # self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR","2tag4jet_150ptv_SR","2tag5pjet_150ptv_SR"])
                    self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR"])
                    # self.set_list_category(["2tag2jet_150ptv_SR"]) 
                    None
                elif "CUT" in self.stem:
                    self.set_list_category(["2tag2jet_150_200ptv_SR","2tag2jet_200ptv_SR","2tag3jet_150_200ptv_SR","2tag3jet_200ptv_SR"])
                    # self.set_list_category(["2tag2jet_150_200ptv_SR"])
                    None
                else:
                    print "Neither MVA, nor CUT are not found in stem",self.stem,". Will ABORT!!!"
                    assert(False)
                # done if
            # done if
            # self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR"]) 
            # self.set_list_category(["2tag2jet_150ptv_SR"]) 
            # self.set_list_category(["2tag3jet_150ptv_SR"]) 
            # self.set_list_category(["2tag5pjet_150ptv_SR"]) 
            # self.set_list_category(["0ptag3jet_150ptv_SR"]) 
            # self.set_list_category(["0ptag0pjet_150ptv_SR"])
            # self.set_list_category(["2tag2jet_0ptv_SR","2tag3jet_0ptv_SR"]) # with do merge ptv bins get this name convention
            # self.set_list_variable(["pTB1"])
            # self.set_list_variable(["mBB"])
            # self.set_list_variable(["mBB"])
            # self.set_list_variable(["mBB","mva"])
            # self.set_list_variable(["mBB","mva","MET","SumPtJet","EtaB2"])
            # self.set_list_variable(["EtaB1","EtaB2","EtaJ3","dEtaBB","costheta","AverageMuScaled","nTaus","MET","SumPtJet","pTB1","pTB2","pTJ3"])
            # self.set_list_variable(["EtaB2"])
            # self.set_list_variable(["pTB1","pTB2","pTJ3","EtaB1","EtaB2","EtaJ3","mBB","mva"])
            # self.list_variable=["mBBNominal","mBBOneMu","mBBPtReco"]
            # self.list_variable=["mBBNominal","mBBOneMu","mBBPtReco","SumPtJet"]
            # self.list_variable=["mva"]
            # self.list_variable=["mva","mBB"]
            # self.list_variable=["mBB","MET","pTB1"]
            # self.list_variable=["mBBRegression"]
            # self.list_variable=["MET","pTB1","mBB","pTB2","EtaB1"]
            # self.list_variable=["MET","SumPtJet","mBB"]
            # self.set_list_variable(["mBBNominal","mBBOneMu","mBBOneMu4GeV","mBBOneMu5GeV","mBBOneMu6GeV","mBBOneMu7GeV","mBBOneMu10GeV","mBBOneMu12GeV","mBBOneMu15GeV","mBBOneMu20GeV","mBBPtReco","mBB"])
            # self.set_list_variable(["njets","MV2c10_Data","btag_weight_Data","PtSigJets","EtaSigJets","NSigJets","PtFwdJets","EtaFwdJets","NFwdJets",])
            # if  self.do_later or True:
            if self.do_later and False:
                # only included at the pretag inclusive: on 0ptag2pjet or so
                string_variable_ignore="EtaFwdJets,EtaSigJets,PtFwdJets,PtSigJets,NFwdJets,NSigJets,MV2c10_B,MV2c10_C,MV2c10_Data,MV2c10_L,btag_weight_B,btag_weight_C,btag_weight_Data,btag_weight_L,eff_B,eff_C,eff_L,njets"
                string_variable_ignore+=",METSig_hard,RandomRunNumber,PileupReweight,PhiJ3,NTags,NJets,METVarT,METVarL_soft,METVarL_hard,METVarL,METSig_soft,METSig,METRho,METDirectional,METOverSqrtHT,METOverSqrtSumET,AverageMu,ActualMu,AverageMuScaled"
                list_variable_ignore=string_variable_ignore.split(",")
                list_variable=[]
                for variable in self.list_variable:
                    if variable in list_variable_ignore:
                        continue
                    #if not ("TruthWZ" in variable):
                    #    continue
                    # if not ("mBB" in variable or "mBBJ" in variable or "pTB1" in variable or "pTB2" in variable or "dPhiVBB" in variable or "HT" in variable):
                    #    continue
                    # if not ("OneMuVR0GeV_PtRecoR21InclusiveADNone" in variable or "OneMuVR0GeV_PtRecoR21SplitADNone" in variable or "OneMuVR0GeV_PtRecoR21InclusiveAorDNone" in variable or "OneMuVR0GeV_PtRecoR21SplitAorDNone" in variable):
                    # if not ("OneMuVR0GeV_PtRecoR21SplitADNone" in variable or "OneMuVR4GeV_PtRecoR21SplitADNone" in variable or "OneMuVR7GeV_PtRecoR21SplitADNone" in variable or "OneMuVR10GeV_PtRecoR21SplitADNone" in variable):
                    # if not ("OneMuVR0GeV_PtRecoR21SplitADBukin" in variable or "OneMuVR0GeV_PtRecoR21SplitADBukinMedian" in variable or "OneMuVR4GeV_PtRecoR21SplitADBukin" in variable or "OneMuVR4GeV_PtRecoR21SplitADBukinMedian" in variable or "OneMuVR7GeV_PtRecoR21SplitADBukin" in variable or "OneMuVR7GeV_PtRecoR21SplitADBukinMedian" in variable or "OneMuVR10GeV_PtRecoR21SplitADBukin" in variable or "OneMuVR10GeV_PtRecoR21SplitADBukinMedian" in variable or "Regression" in variable):
                    #if not ("mBB" in variable and "mBBJ" not in variable):
                    #   continue
                    if not (variable=="mBB"):
                        continue
                    # if not (variable.endswith("Nominal") or variable.endswith("OneMu") or variable.endswith("PtReco") or variable.endswith("OneMuVR0GeV") or variable.endswith("OneMuVR4GeV") or variable.endswith("OneMuVR7GeV") or variable.endswith("OneMuVR10GeV") or "OneMuInJet" in variable or "MuonInJet" in variable or "ElectronInJet" in variable):
                    #if not (variable.endswith("Nominal")):
                    # if not ("OneMuInJet" in variable or "MuonInJet" in variable or "ElectronInJet" in variable):
                        #continue
                    # if not "Nominal" in variable:
                    #    continue
                    # if "mBB" in variable: # temp
                    #    continue
                    list_variable.append(variable)
                # done for loop
                self.set_list_variable(list_variable)
            # done if
            # self.set_list_variable(["njets","MV2c10_Data",])
            # self.set_list_variable(["mBBNominal","mBBOneMu","mBBPtReco"])    
            # self.set_list_variable(["mBBNominal","mBBOneMu4GeV","mBBOneMu10GeV","mBBPtReco"])    
            # self.set_list_variable(["AverageMuScaled","MET","SumPtJet","EtaB1","EtaB2","EtaB3","pTB1","pTB2","pTJ3","nrMuonInJetB1","nrMuonInJetB2","nrMuonInJetB2","dRBB","])    
            # self.set_list_variable(["AverageMuScaled","MET","SumPtJet","EtaB1","EtaB2","EtaJ3","pTB1","pTB2","pTJ3","dRBB","mBB","mva"])    
            # if self.debug:
            if self.verbose:
                self.print_lists()
            if self.do_later or self.do_create_histosRaw:
                self.create_histosRaw(option="reduced")
            # return
            # now we want to sum over processInitial for a given process
            self.set_list_process_info()
            if self.do_later or self.do_create_histosProcess:
                self.create_histosProcess()
            # return
            self.set_list_processMerged()
            if self.do_later or self.do_create_histosProcessMerged:
                self.create_histosProcessMerged(doSF=True)
            # return
            self.set_list_processAnalysis()
            if False and (self.do_later or self.do_create_results):
                self.list_processResult=["VHbb","otherHiggs","diboson","Whf","Wcl","Wl","Zhf","Zcl","Zl","ttbar","ttX","stop","S","B","data"]
                self.list_processResult=self.list_processResult+["S/B","SigY_S_B","SigH_S_B"]
                if True:
                    self.create_results()
            if False and (self.do_later or self.do_create_latex_table):
                self.read_results()
                self.list_processResult=["VHbb","otherHiggs","diboson","Whf","Wcl","Wl","Zhf","Zcl","Zl","ttbar","ttX","stop","S","B","data"]
                self.list_processResult=self.list_processResult+["S/B","SigY_S_B"]
                # for bJetCorr in "Nominal,OneMu20GeV,OneMu15GeV,OneMu12GeV,OneMu10GeV,OneMu7GeV,OneMu6GeV,OneMu5GeV,OneMu4GeV,PtReco".split(","):
                # for bJetCorr in "Nominal,OneMu,PtReco".split(","):
                # for var in "mBB,mva,MET".split(","):
                # for var in "mBBNominal".split(","):
                # for var in list_variable:
                for var in []:
                    self.list_processResult=self.list_processResult+["SigH_S_B@"+var]                 
                self.create_yield_latex_table(doDocument=False)
                # self.create_overlaid_variable()
            # done if
            # return
            if self.do_later or self.do_create_stacked_plots:
                # self.set_list_variable(["pTB1","pTB2","pTJ3","EtaB1","EtaB2","EtaJ3"]) # don't look yet, as not blinded
                # self.set_list_variable(["MET"])
                # self.set_list_variable(["pTB1","pTB2","pTJ3","EtaB1","EtaB2","EtaJ3","mBB","mva"])
                # self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR","2tag4jet_150ptv_SR","2tag5pjet_150ptv_SR"])
                # self.set_list_variable(["SumPtJet"])
                # do overlay plots of D,B,BplusS,S (S is times some value)
                # self.create_overlaid_plots()
                # do stack plots of signal, background, data (S is times some value)
                self.create_stacked_plots()
                print "outside create_stacked_plots()"
        # done if doYields

        # self.set_list_processInitial(["WHlv125J_MINLO"])
        # self.set_list_processInitial(["ZeeL_v221"])
        # self.evaluate_content_of_one_processInitial("WHlv125J_MINLO","False")
        # self.print_all()
    # done function

    def set_dict_categorySF_processMerged_SF(self):
        inputFileName="./info/ICHEP2018/"+self.analysis+".txt"
        if True or self.debug:
            print "inputFileName",inputFileName
        self.dict_categorySF_processMerged_SF={}
        with open(inputFileName,'r') as f:
            for line in f:
                line=line.rstrip()
                if line=="":
                    continue
                if "-lepton" in line:
                    continue
                if "b-tag" in line:
                    continue
                if "S/B" in line:
                    continue
                if "S/sqrt(S+B)" in line:
                    continue
                if "blih" in line:
                    continue
                if self.debug:
                    print "line",line
                if "Region" in line:
                    assert(len(line.split())==1)
                    categorySF=line
                    continue
                if self.debug:
                    print "categorySF",categorySF,"line",line
                list_lineElement=line.split()
                processMerged=list_lineElement[0]
                if processMerged=="data":
                    SF=(1.0,0.0)
                else:
                    SF=(float(list_lineElement[1]),float(list_lineElement[2]))
                if self.debug:
                    print "categorySF",categorySF,"processMerged",processMerged,"SF",SF
                self.dict_categorySF_processMerged_SF[categorySF+"_"+processMerged]=SF
            # done loop over lines
        # close file
        if self.debug:
            for categorySF_processMerged in sorted(self.dict_categorySF_processMerged_SF.keys()):
                print "categorySF_processMerged",categorySF_processMerged,self.dict_categorySF_processMerged_SF[categorySF_processMerged]
        # done if
        # nothing to return as already set
    # done function

    def set_dict_analysis_channel_category_categorySF(self):
        self.dict_analysis_channel_category_categorySF={
            # #############
            # ### MVA #####
            # #############

            # 0L 150-inf SR
            "MVA_0L_2tag2jet_150ptv_SR":"Region_BMin150_Y4033_DSR_T2_L0_distmva_J2",
            "MVA_0L_2tag3jet_150ptv_SR":"Region_BMin150_Y4033_DSR_T2_L0_distmva_J3",
            # 1L 150-info SR
            "MVA_1L_2tag2jet_150ptv_WhfSR":"Region_BMin150_Y4033_DWhfSR_T2_L1_distmva_J2",
            "MVA_1L_2tag3pjet_150ptv_WhfSR":"Region_BMin150_Y4033_DWhfSR_T2_L1_distmva_J3",
            # 1L 150-inf CR
            "MVA_1L_2tag2jet_150ptv_WhfCR":"Region_BMin150_Y4033_DWhfCR_T2_L1_distmva_J2",
            "MVA_1L_2tag3pjet_150ptv_WhfCR":"Region_BMin150_Y4033_DWhfCR_T2_L1_distmva_J3",
            # 2L 150-inf SR
            "MVA_2L_2tag2jet_150ptv_SR":"Region_BMin150_Y4033_DSR_T2_L2_distmva_J2",
            "MVA_2L_2tag3pjet_150ptv_SR":"Region_BMin150_incJet1_Y4033_DSR_T2_L2_distmva_J3",
            # 2L 150-inf CR (topemucr)
            "MVA_2L_2tag2jet_150ptv_topemucr":"Region_BMin150_Y4033_Dtopemucr_T2_L2_distmBBMVA_J2",
            "MVA_2L_2tag3pjet_150ptv_topemucr":"Region_BMin150_incJet1_Y4033_Dtopemucr_T2_L2_distmBBMVA_J3",
            # 2L 75-150 SR
            "MVA_2L_2tag2jet_75_150ptv_SR":"Region_BMax150_BMin75_Y4033_DSR_T2_L2_distmva_J2",
            "MVA_2L_2tag3pjet_75_150ptv_SR":"Region_BMax150_BMin75_incJet1_Y4033_DSR_T2_L2_distmva_J3",
            # 2L 75-150 CR (topemucr)
            "MVA_2L_2tag2jet_75_150ptv_topemucr":"Region_BMax150_BMin75_Y4033_Dtopemucr_T2_L2_distmBBMVA_J2",
            "MVA_2L_2tag3pjet_75_150ptv_topemucr":"Region_BMax150_BMin75_incJet1_Y4033_Dtopemucr_T2_L2_distmBBMVA_J3",

            # #############
            # ### CUT #####
            # #############

            # 0L 200-inf SR
            "CUT_0L_2tag2jet_200ptv_SR":"Region_BMin200_Y4033_DSR_T2_L0_distmBB_J2",
            "CUT_0L_2tag3jet_200ptv_SR":"Region_BMin200_Y4033_DSR_T2_L0_distmBB_J3",
            # 0L 150-200 SR
            "CUT_0L_2tag2jet_150_200ptv_SR":"Region_BMax200_BMin150_Y4033_DSR_T2_L0_distmBB_J2",
            "CUT_0L_2tag3jet_150_200ptv_SR":"Region_BMax200_BMin150_Y4033_DSR_T2_L0_distmBB_J3",
            # 1L
            # in 1L CUT SR and CR are merged into SR at SplitInputs
            # but our inputs produced from Reader give SR and CR
            # so point both to the SR from the txt file
            # 1L 200-inf SR
            "CUT_1L_2tag2jet_200ptv_WhfSR":"Region_BMin200_Y4033_DWhfSR_T2_L1_distmBB_J2",
            "CUT_1L_2tag3pjet_200ptv_WhfSR":"Region_BMin200_Y4033_DWhfSR_T2_L1_distmBB_J3",
            # 1L 200-inf CR
            "CUT_1L_2tag2jet_200ptv_WhfCR":"Region_BMin200_Y4033_DWhfSR_T2_L1_distmBB_J2", # note CR <- SR
            "CUT_1L_2tag3pjet_200ptv_WhfCR":"Region_BMin200_Y4033_DWhfSR_T2_L1_distmBB_J3", # note CR <- SR
            # 1L 150-200 SR
            "CUT_1L_2tag2jet_150_200ptv_WhfSR":"Region_BMax200_BMin150_Y4033_DWhfSR_T2_L1_distmBB_J2",
            "CUT_1L_2tag3pjet_150_200ptv_WhfSR":"Region_BMax200_BMin150_Y4033_DWhfSR_T2_L1_distmBB_J3",
            # 1L 150-200 CR
            "CUT_1L_2tag2jet_150_200ptv_WhfCR":"Region_BMax200_BMin150_Y4033_DWhfSR_T2_L1_distmBB_J2", # note CR <- SR
            "CUT_1L_2tag3pjet_150_200ptv_WhfCR":"Region_BMax200_BMin150_Y4033_DWhfSR_T2_L1_distmBB_J3", # note CR <- SR
            # 2L
            # in 2L CUT the topemu CR 150_200ptv and 200ptv is merged into 150ptv at SplitInputs
            # 2L 200-inf SR
            "CUT_2L_2tag2jet_200ptv_SR":"Region_BMin200_Y4033_DSR_T2_L2_distmBB_J2",
            "CUT_2L_2tag3pjet_200ptv_SR":"Region_BMin200_incJet1_Y4033_DSR_T2_L2_distmBB_J3",
            # 2L 200-inf CR (topemucr)
            "CUT_2L_2tag2jet_200ptv_topemucr":"Region_BMin150_Y4033_Dtopemucr_T2_L2_distmBB_J2", # 200 <- 150
            "CUT_2L_2tag3pjet_200ptv_topemucr":"Region_BMin150_incJet1_Y4033_Dtopemucr_T2_L2_distmBB_J3", # 200 <- 150
            # 2L 150-200 SR 
            "CUT_2L_2tag2jet_150_200ptv_SR":"Region_BMax200_BMin150_Y4033_DSR_T2_L2_distmBB_J2",
            "CUT_2L_2tag3pjet_150_200ptv_SR":"Region_BMax200_BMin150_incJet1_Y4033_DSR_T2_L2_distmBB_J3",
            # 2L 150-200 CR (topemucr)
            "CUT_2L_2tag2jet_150_200ptv_topemucr":"Region_BMin150_Y4033_Dtopemucr_T2_L2_distmBB_J2", # 150_200 <- 150
            "CUT_2L_2tag3pjet_150_200ptv_topemucr":"Region_BMin150_incJet1_Y4033_Dtopemucr_T2_L2_distmBB_J3", # 150_200 <- 150
            # 2L 075-150 SR
            "CUT_2L_2tag2jet_75_150ptv_SR":"Region_BMax150_BMin75_Y4033_DSR_T2_L2_distmBB_J2",
            "CUT_2L_2tag3pjet_75_150ptv_SR":"Region_BMax150_BMin75_incJet1_Y4033_DSR_T2_L2_distmBB_J3",
            # 2L 075-150 CR (topemucr)
            "CUT_2L_2tag2jet_75_150ptv_topemucr":"Region_BMax150_BMin75_Y4033_Dtopemucr_T2_L2_distmBB_J2",
            "CUT_2L_2tag3pjet_75_150ptv_topemucr":"Region_BMax150_BMin75_incJet1_Y4033_Dtopemucr_T2_L2_distmBB_J3",
            }
    # done function

    def do_all_new(self):
        self.create_folderProcessInitial()
        self.set_dict_variable_info()
        self.set_list_processMerged_new()
        self.create_folderHistos()
        self.set_fileNameHistosProcessMerged()
        print self.fileNameHistosProcessMerged
        if True:
            self.set_dict_analysis_channel_category_categorySF()
            self.set_dict_categorySF_processMerged_SF()
        if True:
            self.create_histosProcessMerged_new(doSF=True)
        if True:
            self.create_folderPlots()
            self.list_color=[1,4,2,8,ROOT.kOrange]
            self.create_stacked_plots()
        self.create_folderResults()
        self.list_processResult=["VHbb","otherHiggs","diboson","Whf","Wcl","Wl","Zhf","Zcl","Zl","ttbar","ttX","stop","S","B","data"]
        self.list_processResult=self.list_processResult+["S/B","SigY_S_B","SigH_S_B"]
        if True:
            self.create_results()
        if True:
            self.create_folderYields()
            self.read_results()
            # self.create_yield_latex_table(doDocument=True)
            self.create_yield_latex_table2()
            if self.debug:
                print self.vtag
            # vtag_ref="32-07"
            vtag_ref="31-10"
            if self.debug:
                print "ADRIAN self",self.stem,self.folderResults
            ref=copy.copy(self)
            ref.stem=ref.stem.replace(self.vtag,vtag_ref)
            ref.folderResults=ref.folderResults.replace(self.vtag,vtag_ref)
            if self.debug:
                print "ADRIAN self",self.stem,self.folderResults
                print "ADRIAN","ref",ref.stem,ref.folderResults
            ref.read_results()
            self.create_yield_latex_table_compare(ref,doDocument=False,debug=True)
    # done function
    ### done methods



# done class
