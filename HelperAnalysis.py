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

    def set_debug(self,debug):
        self.debug=debug

    def set_verbose(self,verbose):
        self.verbose=verbose
    
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

    def set_do_overlay_histosRaw_by_processInitial(self,do_overlay_histosRaw_by_processInitial):
        self.do_overlay_histosRaw_by_processInitial=do_overlay_histosRaw_by_processInitial
 
    ### actions

    def create_folderProcessInitial(self):
        self.folderProcessInitial=self.folderOutput+"/processInitial"
        command="mkdir -p "+self.folderProcessInitial
        if self.debug:
            print "command="+command
        os.system(command)
    # done function

    def evaluate_list_processInitial(self):
        if self.debug:
            print "Start evaluate_list_processInitial()"
        p = subprocess.Popen(
            ['ls', self.folderInput],
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
            if ".root" not in fileName:
                print "skipping non *.root file fileName",fileName
                continue
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
                # e.g. ttbar_3ptag5pjet_150ptv_SR_yBB
                list_histoNameElement=histoName.split("_")
                if "ttbar_dilep" in histoName or "stopWt_dilep" in histoName or "ggH125_bb" in histoName or "ggH125_inc" in histoName or "VBFH125_inc" in histoName or "ttbar_spin" in histoName:
                    process=list_histoNameElement[0]+"_"+list_histoNameElement[1] # e.g. "ttbar_dilep or stopWt_dilep
                    category=list_histoNameElement[2]+"_"+list_histoNameElement[3]+"_"+list_histoNameElement[4] # next three elements, eg. 3ptag5pjet_150ptv_SR
                else:
                    # only one word to define the process, e.g. ttbar
                    process=list_histoNameElement[0] # first element e.g. ttbar
                    category=list_histoNameElement[1]+"_"+list_histoNameElement[2]+"_"+list_histoNameElement[3] # next three elements, eg. 3ptag5pjet_150ptv_SR
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

    def get_histoNameRaw(self,process,category,variable,processInitial):
        if self.debug:
            print "Start get_histoNameRaw()"
        # histoNameRaw=process+"_"+category+"_"+variable+"_"+processInitial
        histoNameRaw=variable+"_"+category+"_"+process+"_"+processInitial
        if self.debug:
            print "histoNameRaw",histoNameRaw
        return histoNameRaw
    # done function

    def set_fileNameHistosRaw(self):
        self.fileNameHistosRaw=self.folderHistos+"/histosRaw.root"
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
            if self.debug or self.verbose:
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
        self.dict_variable_info={
            "EtaB1":[get_binRange(-2.5,2.5,0.1,debug_binRange)],
            "EtaB2":[get_binRange(-2.5,2.5,0.1,debug_binRange)],
            "EtaFwdJets":[get_binRange(-4.5,4.5,0.1,debug_binRange)],
            "EtaSigJets":[get_binRange(-2.5,2.5,0.1,debug_binRange)],
            "MET":[get_binRange(140,400,10,debug_binRange)+","+get_binRange(400,700,100,debug_binRange)],
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
            "MindPhiMETJet":[get_binRange(0.0315*40,3.15,0.0315*2,debug_binRange)],
            "NTags":[""],
            "Njets":[get_binRange(2,10,1,debug_binRange)],
            "njets":[get_binRange(2,10,1,debug_binRange)],
            "NFwdJets":[get_binRange(2,10,1,debug_binRange)],
            "NSigJets":[get_binRange(2,10,1,debug_binRange)],
            "SumPtJet":[get_binRange(120,400,10,debug_binRange)+","+get_binRange(400,600,20,debug_binRange)],
            "costheta":[get_binRange(0,1,0.02,debug_binRange)],
            "dEtaBB":[get_binRange(0,1.5,0.1,debug_binRange)+","+get_binRange(1.5,2.5,0.2,debug_binRange)+","+get_binRange(2.5,4.5,1,debug_binRange)],
            "dPhiBB":[get_binRange(0,3.2-20*0.032,0.032*2,debug_binRange)],
            "dPhiMETMPT":[get_binRange(0,3.15-0.0315*48,0.0315,debug_binRange)],
            "dPhiVBB":[get_binRange(3.2-10*0.032,3.2,0.032,debug_binRange)],
            "dRB1J3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "dRB2J3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "dRBB":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "mBB":[get_binRange(20,160,10,debug_binRange)+","+get_binRange(160,300,20,debug_binRange)+","+get_binRange(300,500,40,debug_binRange)],
            "mBBJ":[get_binRange(40,80,20,debug_binRange)+","+get_binRange(80,160,10,debug_binRange)+","+get_binRange(160,300,20,debug_binRange)+","+get_binRange(300,500,40,debug_binRange)+","+get_binRange(500,700,50,debug_binRange)+","+get_binRange(700,1000,100,debug_binRange)],
            "maxdRBJ3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "mindRBJ3":[get_binRange(0.4,3.4,0.1,debug_binRange)+","+get_binRange(3.4,5,0.2,debug_binRange)],
            "AverageMu":[get_binRange(0,100,1,debug_binRange)],
            "AverageMuScaled":[get_binRange(0,100,1,debug_binRange)],
            "ActualMu":[get_binRange(0,100,1,debug_binRange)],
            "ActualMuScaled":[get_binRange(0,100,1,debug_binRange)],
            "PileupReweight":[""],
            "RandomRunNumber":[""],
            "mva":[get_binRange(-1,1,0.05,debug_binRange)],
            "mvadiboson":[get_binRange(-1,1,0.05,debug_binRange)],
            "nTaus":[""],
            "pTB1":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)],
            "pTB2":[get_binRange(0,140,10,debug_binRange)+","+get_binRange(140,200,20,debug_binRange)],
            "PtFwdJets":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)],
            "PtSigJets":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,400,20,debug_binRange)+","+get_binRange(400,500,50,debug_binRange)],
            "pTBB":[get_binRange(0,300,10,debug_binRange)+","+get_binRange(300,500,20,debug_binRange)],
            "pTBBMETAsym":[get_binRange(-0.6,-0.2,0.1,debug_binRange)+","+get_binRange(-0.2,0.1,0.02,debug_binRange)+","+get_binRange(0.1,0.3,0.1,debug_binRange)],
            "pTBBoverMET":[get_binRange(0.2,0.7,0.1,debug_binRange)+","+get_binRange(0.7,1.2,0.02,debug_binRange)+","+get_binRange(1.2,1.6,0.1,debug_binRange)],
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
            "yBB":[get_binRange(0,2.5,0.05,debug_binRange)],
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
        self.fileNameHistosProcess=self.folderHistos+"/histosProcess.root"
    # done function

    def create_histosProcess(self):
        if self.debug:
            print "Start create_histosProcess()"
        # now we want to sum over processInitial for a given process
        outputFile=TFile(self.fileNameHistosProcess,"RECREATE")
        outputFile.Close()
        for variable in self.list_variable:
            if "FwdJets" in variable or "SigJets" in variable or variable=="MV2c10_B" or variable=="MV2c10_C" or variable=="MV2c10_Data" or variable=="MV2c10_L" or variable=="btag_weight_B" or variable=="btag_weight_C" or variable=="btag_weight_Data" or variable=="btag_weight_L" or variable=="eff_B" or variable=="eff_C" or variable=="eff_L" or variable=="njets":
                # they are not defined for 2tag2jet categories, as these do not have forward jets
                continue 
            counter_variable=0
            for category in self.list_category:
                for processRenamed in self.list_process:
                    #if processRenamed!="ttbar":
                    #    continue
                    counter=0
                    if self.debug:
                        print "ADRIAN1  %-10s %-10s %-10s" % (variable,category,processRenamed)
                    list_processInfo=self.dict_process_info[processRenamed]
                    #for processInitial in self.list_processInitial:
                    for processInfo in list_processInfo:
                        process=processInfo[0]
                        processInitial=processInfo[1]
                        if self.debug:
                            print "ADRIAN2 %-10s %-10s %-10s %-10s" % (variable,category,process,processInitial)
                        inputFileName=self.fileNameHistosRaw
                        histoNameRaw    =self.get_histoNameRaw    (process,category,variable,processInitial)
                        histoNameProcess=self.get_histoNameInitial(processRenamed,category,variable)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameRaw,name=histoNameProcess,returnDummyIfNotFound=True,debug=self.debug)
                        if histo=="dummy":
                            continue
                        if counter_variable==0:
                            histoReset=histo.Clone()
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
                        histoNameProcess=self.get_histoNameInitial(processRenamed,category,variable)
                        histoReset=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameRaw,name=histoNameProcess,returnDummyIfNotFound=True,debug=self.debug)
                        histoReset.Reset()
                        histoProcess=histoReset
                        histoNameProcess=self.get_histoNameInitial(processRenamed,category,variable)
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
            "ggH",
            "bbH",
            "VBF",
            "ttH",
            "WW",
            "WZ",
            "ZZ",
            "ggZZ",
            "ggWW",
            #"ZllZb",
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
            "stops",
            "stopt",
            "stopWt",
            "tZq",
            "ttV",
            "ttVV",
            "ttt",
            "tttt",
            "data",
            # "",
            ]
        
        self.dict_process_info={
            # VHbb
            "qqZvvHbb":[["qqZvvH125","qqZvvHbbJ_PwPy8MINLO"],],
            "qqWlvHbb":[["qqWlvH125","qqWlvHbbJ_PwPy8MINLO"],],
            "ggZvvHbb":[["ggZvvH125","ggZvvHbb_PwPy8"],],
            "qqZllHbb":[["qqZllH125","qqZllHbbJ_PwPy8MINLO"],],
            "ggZllHbb":[["ggZllH125","ggZllHbb_PwPy8"],],
            # VHcc
            "qqZvvHcc":[["qqZvvH125","qqZvvHccJ_PwPy8MINLO"],],
            "qqWlvHcc":[["WmH125J"  ,"qqWlvHccJ_PwPy8MINLO"],
                        ["WpH125J"  ,"qqWlvHccJ_PwPy8MINLO"],],
            "ggZvvHcc":[["ggZvvH125","ggZvvHcc_PwPy8"],],
            "qqZllHcc":[["qqZllH125","qqZllHccJ_PwPy8MINLO"],],
            "ggZllHcc":[["ggZllH125","ggZllHcc_PwPy8"],],
            # other ZH
            "qqZincH4l":[["qqZincH4l","ZincHJZZ4l_PwPy8MINLO"],],
            # non ZH signals
            "VBF":[["VBFH125_inc","VBFHinc_PwPy8"],],
            "ggHbb":[["ggH125_bb","ggHbb_PwPy8NNLOPS."],],
            "ggH":[["ggH125_inc","ggHinc_PwPy8.root"],],
            "bbH":[["bbH125","bbHinc_aMCatNLOPy8"],],
            "ttH":[["ttH","ttHinc_aMCatNLOPy8"],],
            # dibosons
            "WW":[["WW","WW_Sh221"],],
            "WZ":[["WZ","WZ_Sh221"],],
            "ZZ":[["ZZ","ZZ_Sh221"],],
            "ggZZ":[["ggZZ","ggZZ_Sh222"],],
            "ggWW":[["ggWW","ggWW_Sh222"],],
            "ZllZbb":[["ZllZbb","ZZ_bb_Sh221"],],
            "ZvvZbb":[["ZvvZbb","ZZ_bb_Sh221"],],
            "WlvZbb":[["WlvZbb","WZ_bb_Sh221"],],
            "ZllZvv":[["llvv","VV_fulllep_Sh222"],],
            # W+jets
            "Wbb":[["Wbb","WenuB_Sh221"],
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
                   ["Wbb","Wtaunu_Sh221"],],
            "Wbc":[["Wbc","WenuB_Sh221"],
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
                   ["Wbc","Wtaunu_Sh221"],],
            "Wbl":[["Wbl","WenuB_Sh221"],
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
                   ["Wbl","Wtaunu_Sh221"],],
            "Wcc":[["Wcc","WenuB_Sh221"],
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
                   ["Wcc","Wtaunu_Sh221"],],
            "Wcl":[["Wcl","WenuB_Sh221"],
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
                   ["Wcl","Wtaunu_Sh221"],],
            "Wl": [["Wl" ,"WenuB_Sh221"],
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
                   ["Wl" ,"Wtaunu_Sh221"],],
            "Zbb":[["Zbb","ZnunuB_Sh221"],
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
                   ["Zbb","Ztautau_Sh221"],],
            "Zbc":[["Zbc","ZnunuB_Sh221"],
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
                   ["Zbc","Ztautau_Sh221"],],
            "Zbl":[["Zbl","ZnunuB_Sh221"],
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
                   ["Zbl","Ztautau_Sh221"],],
            "Zcc":[["Zcc","ZnunuB_Sh221"],
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
                   ["Zcc","Ztautau_Sh221",]],
            "Zcl":[["Zcl","ZnunuB_Sh221"],
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
                   ["Zcl","Ztautau_Sh221"],],
            "Zl" :[["Zl" ,"ZnunuB_Sh221"],
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
                   ["Zl" ,"Ztautau_Sh221"],],
            "ttbar" :[["ttbar","ttbar_nonallhad_PwPy8"],],
            "stops" :[["stops","stops_PwPy"],],
            "stopt" :[["stopt","stopt_PwPy"],],
            "stopWt":[["stopWt","stopWt_PwPy"],],
            "tZq"   :[["tZq","stoptZ_MGPy8"],],
            "ttV"   :[["ttV","ttV_aMCatNLOPy8"],],
            "ttVV"  :[["ttbarWW","ttVV_MGPy8"],],
            "ttt"   :[["ttt","ttt_MGPy8"],],
            "tttt"  :[["4topSM","tttt_MGPy8"],],
            "data"  :[["data","data15"],
                      ["data","data16"],],
            # "":[[],],
            }

    # done function

    def set_list_processMerged(self):
        if self.debug:
            print "Start set_list_processMerged()"
        self.list_processMerged=[
            "qqZvvH",
            "qqZllH",
            "ggZvvH",
            "ggZllH",
            "qqWH",
            "Wl",
            "Wcl",
            "Whf",
            "Zl",
            "Zcl",
            "Zhf",
            "ttbar",
            "stop",
            "diboson",
            "data",
            "S",
            "B",
            "D",
            ]

        self.list_processMergedType=[
            "qqZvvH",
            "qqZllH",
            "ggZvvH",
            "ggZllH",
            "qqWH",
            "Wl",
            "Wcl",
            "Whf",
            "Zl",
            "Zcl",
            "Zhf",
            "ttbar",
            "stop",
            "diboson",
            "S",
            "B",
            "data",
            ]

        self.dict_processMerged_info={
            "qqZvvH" :["S",0,{"2":1.0,"3":1.0},
                       ["qqZvvH125"]],
            "qqZllH" :["S",0,{"2":1.0,"3":1.0},
                       ["qqZllH125"]],
            "ggZvvH" :["S",0,{"2":1.0,"3":1.0},
                       ["ggZvvH125"]],
            "ggZllH" :["S",0,{"2":1.0,"3":1.0},
                       ["ggZllH125"]],
            "qqWH"   :["S",1,{"2":1.0,"3":1.0},
                       ["qqWlvH125"]],
            "Wl"     :["B",0,{"2":1.0,"3":1.0},
                       ["Wl"]],
            "Wcl"    :["B",0,{"2":1.0,"3":1.0},
                       ["Wcl"]],
            "Whf"    :["B",0,{"2":1.27,"3":1.27},
                       ["Wbb","Wbc","Wbl","Wcc"]],
            "Zl"     :["B",0,{"2":1.0,"3":1.0},
                       ["Zl"]],
            "Zcl"    :["B",0,{"2":1.0,"3":1.0},
                       ["Zcl"]],
            "Zhf"    :["B",0,{"2":1.42,"3":1.31},
                       ["Zbb","Zbc","Zbl","Zcc"]],
            "ttbar"  :["B",0,{"2":0.97,"3":1.0}
                       ,["ttbar"]],
            "stop"   :["B",0,{"2":1.0,"3":1.0}
                       ,["stops","stopt","stopWt"]],
            "diboson":["B",1,{"2":1.0,"3":1.0}
                       #,["WW","WZ","ZZ","ggWW","ggZZ"]],
                       ,["WW","WZ","ZZ","ggZZ"]],
            "data"   :["D",1,{"2":1.0,"3":1.0}
                       ,["data"]],
            "S"      :["Sig",1,{"2":1.0,"3":1.0}
                       ,["qqZvvH125","qqZllH125","ggZvvH125","ggZllH125","qqWlvH125"]],
            "B"      :["Bkg",1,{"2":1.0,"3":1.0},
                       # ["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","stops","stopt","stopWt","WW","WZ","ZZ","ggWW","ggZZ"]],
                       ["Wbb","Wbc","Wbl","Wcc","Wcl","Wl","Zbb","Zbc","Zbl","Zcc","Zcl","Zl","ttbar","stops","stopt","stopWt","WW","WZ","ZZ","ggZZ"]],
            "D"      :["Dat",1,{"2":1.0,"3":1.0},
                       ["data"]],
            }

    def set_fileNameHistosProcessMerged(self):
        self.fileNameHistosProcessMerged=self.folderHistos+"/histosProcessMerged.root"
    # done function

    def create_histosProcessMerged(self):
        if self.debug:
            print "Start create_histosProcessMerged()"
        # now we want to sum over process for a given processMerged
        outputFile=TFile(self.fileNameHistosProcessMerged,"RECREATE")
        outputFile.Close()
        for variable in self.list_variable:
            for category in self.list_category:
                if "2jet" in category:
                    cat="2"
                elif "3jet" in category:
                    cat="3"
                else:
                    cat="none"   
                for processMerged in self.list_processMerged:
                    counter=0
                    if self.debug:
                        print "ADRIAN1  %-10s %-10s %-10s" % (variable,category,processMerged)
                    info=self.dict_processMerged_info[processMerged]
                    dict_cat_SF=info[2]
                    if cat in dict_cat_SF.keys():
                        SF=dict_cat_SF[cat]
                    else:
                        SF=1.0
                    if self.debug:
                        print "SF",SF,"type(SF)",type(SF)
                    list_process=info[3]
                    for process in list_process:
                        if self.debug:
                            print "ADRIAN2 %-10s %-10s %-10s %-10s" % (variable,category,processMerged,process)
                        inputFileName=self.fileNameHistosProcess
                        histoNameProcess      =self.get_histoNameInitial(process,category,variable)
                        histoNameProcessMerged=self.get_histoNameInitial(processMerged,category,variable)
                        histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcess,name=histoNameProcessMerged,returnDummyIfNotFound=True,debug=self.debug)
                        if histo=="dummy":
                            continue
                        if counter==0:
                            histoProcessMerged=histo
                        else:
                            histoProcessMerged.Add(histo)
                        counter+=1
                    # done for loop over processInitial
                    if self.debug:
                        print "counter",counter
                    # now scale the histogram with the SF
                    histoProcessMerged.Scale(SF)
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

    def set_list_processType(self):
        self.list_processType="S,B,D,Sig,Bkg,Dat".split(",")

    def create_yield_latex_table(self):
        if self.debug:
            print "Start create_yield_latex_table()"
        variable=self.list_variable[0]
        dict_category_processMerged_integralValueError={}
        for category in self.list_category:
            print "ADRIAN category",category
            dict_processType_list_tuple={}
            for processType in self.list_processType:
                if self.debug:
                    print "processType",processType
                dict_processType_list_tuple[processType]=[]
            for processMerged in self.list_processMerged:
                if self.debug:
                    print "processMerged",processMerged
                inputFileName=self.fileNameHistosProcessMerged 
                histoNameProcessMerged=self.get_histoNameInitial(processMerged,category,variable)
                histo=retrieveHistogram(fileName=inputFileName,histoPath="",histoName=histoNameProcessMerged,name="",returnDummyIfNotFound=True,debug=self.debug)
                integralValueError=get_histo_integral_error(histo,myRange=-1,option="",debug=False) # -1 to include the under/over-flow bins
                dict_category_processMerged_integralValueError[category+"_"+processMerged]=integralValueError
                info=self.dict_processMerged_info[processMerged]
                processType=info[0]
                dict_processType_list_tuple[processType].append(integralValueError)
            # done loop over processMerged
            # retrieve the sums
            for processType in self.list_processType:
                dict_category_processMerged_integralValueError[category+"_"+processType]=sum_error_list(dict_processType_list_tuple[processType],debug=False)
            if self.debug:
                print "category",category,"dict_category_processMerged_integralValueError", dict_category_processMerged_integralValueError
        # done loop over category
        # now the dictionary is filled
        

        # we create the latex table
        fileName=self.folderYields+"/table.tex"
        # create a new file
        f = open(fileName,'w')
        f.write('\\documentclass{beamer}\n')
        f.write('\\usepackage{tabularx}\n')
        f.write('\\usepackage{adjustbox}\n')
        f.write('\\usepackage{pdflscape}\n')
        f.write('\\begin{document}\n')
        f.write('\\begin{frame}{'+ self.name+'}\n')
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
        # add processes one at a time
        for processMergedType in self.list_processMergedType:
            info=self.dict_processMerged_info[processMergedType]
            doAddLineAfter=bool(info[1])
            if self.debug:
                print processMergedType,info[1],type(info[1]),doAddLineAfter,type(doAddLineAfter)
            text=processMergedType
            for category in self.list_category:
                myYield=dict_category_processMerged_integralValueError[category+"_"+processMergedType]
                text+=" & {\\color{orange}%.1f$\pm$%.1f}" % myYield
            text+=" \\\\ \n"
            f.write(text)
            if doAddLineAfter:
                f.write('\\hline \n')
        # done for loop over processMerged
        f.write('\\hline \n')
        f.write('\\end{tabular}\n')
        f.write('}\n')
        f.write('\\end{landscape} \n')
        # f.write('\\end{center}\n')
        f.write('\\end{frame}\n')
        f.write('\\end{document}\n')
        f.close()
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

    def do_all(self):
        if self.debug:
            print "Start do_all()"
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
        self.set_evaluated_list_all()
        self.create_folderHistos()
        self.set_fileNameHistosRaw()
        self.set_fileNameHistosProcess()
        self.set_fileNameHistosProcessMerged()
        self.create_folderYields()

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
            self.set_dict_variable_info()
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
                if process=="W" or process=="Z" or "MadZee" in process or "MadZmumu" in process or process=="ggWW":
                    print "WARNING!!! finding process",process,"will skip them!"
                    continue
                list_process.append(process)
            # done for loop
            #self.list_process=list_process
            #self.list_process=["ttbar"]
            #self.list_process=["data"]
            # reduce category
            #self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR","2tag4jet_150ptv_SR","2tag5pjet_150ptv_SR"])
            #self.set_list_category(["2tag2jet_150ptv_SR","2tag3jet_150ptv_SR"]) 
            self.set_list_category(["2tag2jet_150ptv_SR"]) 
            #self.set_list_category(["2tag3jet_150ptv_SR"]) 
            #self.set_list_category(["0ptag3jet_150ptv_SR"]) 
            #self.set_list_category(["0ptag0pjet_150ptv_SR"]) 
            #self.set_list_category(["2tag2jet_0ptv_SR","2tag3jet_0ptv_SR"]) # with do merge ptv bins get this name convention
            #self.set_list_variable(["pTB1"])
            #self.set_list_variable(["mBB"])
            # self.set_list_variable(["mBB","mva"])
            self.set_list_variable(["mBBJ"])
            #self.set_list_variable(["njets","MV2c10_Data","btag_weight_Data","PtSigJets","EtaSigJets","NSigJets","PtFwdJets","EtaFwdJets","NFwdJets",])
            #self.set_list_variable(["njets","MV2c10_Data",])
            #if self.debug:
            if self.verbose:
                self.print_lists()
            if True:
                self.create_histosRaw(option="reduced")
            return
            # now we want to sum over processInitial for a given process
            if True:
                self.set_list_process_info()
                self.create_histosProcess()
            return
            self.set_list_processMerged()
            if False:
                self.create_histosProcessMerged()
            self.set_list_processType()
            self.create_yield_latex_table()
        # done if doYields

        #self.set_list_processInitial(["WHlv125J_MINLO"])
        #self.set_list_processInitial(["ZeeL_v221"])
        #self.evaluate_content_of_one_processInitial("WHlv125J_MINLO","False")
        #self.print_all()

    ### done methods

# done class

