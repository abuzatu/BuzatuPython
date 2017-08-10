# !/usr/bin/python
# Adrian Buzatu (adrian.buzatu@glasgow.ac.uk)
# 20 May 2013, Python functions to manipulate and draw histograms

from HelperPython import *#import math
import ROOT
from ROOT import TLatex,TPad,TList,TH1,TH1F,TH2F,TH1D,TH2D,TFile,TTree,TChain,TCanvas,TLegend,SetOwnership,gDirectory,TObject,gStyle,gROOT,TLorentzVector,TGraph,TMultiGraph,TColor,TAttMarker,TLine,TDatime,TGaxis,TF1,THStack,TAxis,TStyle,TPaveText,TAttFill,TCutG,TMath,TNamed

list_color=[1,2,4,3,6,ROOT.kOrange,6,7,8,9,14,29,38,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
#list_color=[7,1,4,2,3,12,9,14,29,38,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

# checks if an object exists, useful for checking of a file or tree or histogram is found in a TFile
# Warning, actually it only checks if the object exists, and not if the file exists or th tree exists
# actually this always returns true 
def exists(object,name,debug=False):
    if not not object:
        if debug:
            print "object of name",name,"does exist, will return True"
        return True
    else:
        if debug:
            print "object of name",name,"does not exist, will return False"
        return False
# ended function

# list all the objects of one type from the ROOT file, ex TH1F, TTree
# ex: getListObjectFromFile("file.root","TH1F",False)
# ex: getListObjectFromFile("file.root","TTree",False)
def getListObjectFromFile(filename,name,debug=False):
    file=TFile(filename,"READ")
    result=""
    for i,key in enumerate(file.GetListKeys()):
        if i==0:
            prefix=""
        else:
            prefix=","
        if key.GetClassName()==name:
            result+=prefix+key.GetName()
    # done for
    return result
# ended function


# create/recreate (by removing the old file) a new TFile
# ex createFile("test1.root")
def recreateFile(fileName,debug=False):
    file=TFile(fileName,"RECREATE")
    return True
# ended function

# create TTree in TFile hard coded
# ex createTree("test1.root","tree1",False)
def exCreateTree(fileName,treeName,debug):
    file=TFile(fileName,"RECREATE")
    tree=TTree(treeName,treeName)
    # will create two variables of type double (hence 'd' below)
    # in ROOT/C++ you have to give pointer (address of the variable rPt)
    # as in Python we do not have pointers, but only objects
    # where we need pointers we create an object of type array of type desired
    # double in our case of only one entry (hence "[0]") and pass that 
    rPt=array('d', [0])
    rE=array('d', [0])
    # set the branches to the tree to these two variables
    tree.Branch('rPt',rPt,"rPt/D")
    tree.Branch('rE',rE,"rE/D")
    # loop from 0 to 9 
    for i in xrange(10):
        # fill the first entry in the arrays with dummy values
        rPt[0]=12.2
        rE[0]=14.7
        # now fill the tree with these values
        tree.Fill()
        # Done, so exit the for loop
    # now write the contents of the file to the file (thus the tree as well)
    file.Write()
    # close the file
    file.Close()
    # we are done, so we can return anything so let's just return True
    return True
# ended function

# read a Tree with a style like in ROOT
# ex: exReadTreeStyle1("file1.root","tree1.root","rPt",False)
def exReadTreeStyle1(fileName,treeName,variableName,debug=False):
    # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # before the event loop, need to set the branch address
    # for the variable we want to read
    value = array('d', [0])
    tree.SetBranchAddress(variableName, value)
    # now we are ready for the event loop from 0 to the number of entries minus 1
    for i in range(0, tree.GetEntries()):
        # this command fills for the current event the values of all branches we set above
        tree.GetEntry(i)
        # now we can use the values, in this simple example simply print them
        print "current value is",value[0]
    return True
# ended function

# read a Tree with a style specific to Python
# ex: exReadTreeStyle2("file1.root","tree1.root","rPt",False)
def exReadTreeStyle2(fileName,treeName,variableName,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    for event in tree:
        value=getattr(event,variableName)
        # now we can use the values, in this simple example simply print them
        print "current value is",value
    return True
# ended function

# where you to not need to use the string of a variable name
# as in passing that as an argument to a function, but simply
# know the name to hard code inside the function
# ex: exReadTreeStyle2("file1.root","tree1.root",False)
def exReadTreeStyle3(fileName,treeName,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    for event in tree:
        value=event.rPt # to use "rPt" as a string do: value=getattr(tree,variableName)
        # now we can use the values, in this simple example simply print them
        print "current value is",value
    return True
# ended function

# read a Tree with a style specific to Python
# and get the number of the event in the list at the same time
# allowing you to run only on the odd number (train sample)
# or even number (test sample)
# ex: exReadTreeStyle4("file1.root","tree1.root","rPt",False)
def exReadTreeStyle4(fileName,treeName,variableName,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    # and you also get the number of the entry for free
    # for this you need to use "enumerate(tree)" instead of "tree"
    # this returns a tuple, i.e. a comma separated list of elements of type (number of order,event)
    # this is why we can say "for i,event in " and have both filled at the same time
    for i,event in enumerate(tree):
        value=getattr(tree,variableName)
        # now we can use the values, in this simple example simply print them
        if i%2==0:
            print "current value for i (even) is",value
        else:
            print "current value for i (odd) is",value
    return True
# ended function

# read a Tree with a style specific to Python and read several variables in an easy way
# ex: exReadTreeStyle5("WH125.root","per_jet",3,"rPt,rSumPtTrk,rWidth","2",False)
def exReadTreeStyle5(fileName,treeName,numEvents,variableNames,option,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # print the variables that we want to retrieve
    print "variableNames",variableNames
    for variableName in variableNames.split(','):
        print "variableName",variableName
    # decide the number of events we run on
    nrEntries=tree.GetEntries()
    if numEvents<0 or numEvents>nrEntries:
        numEvents=nrEntries
    for i, event in enumerate(tree):
        if i>=numEvents:
            continue
        if debug:
            print "******* new event **********"
        if option=="1":
            # this is the old way, as in exReadTreeStyle2
            values_list=[]
            for variableName in variableNames.split(','):
                print "variableName",variableName,"value",getattr(tree,variableName)
                values_list.append(getattr(tree,variableName))
        elif option=="2":
            # this is the new way, put all values in a list and print them together
            values_list=[getattr(event,variableName) for variableName in variableNames.split(',')]
            print values_list
            # we can make an array of type double ('d') values of type double out of these variables
            values_array=array('d',values_list)
            print values_array
            # if a function needs the values of these variables for this event in this order
            # we use * to get an ntuple with the values, such as a neural network object nn
            # ex: nn.value(0,*values_list) 
            # ex: nn.value(0,*values_array) instead of
            # ex: nn.value(0,event.rPt,event.rSumPtTrk,event.rWidth) or instead of
            # ex: nn.value(0,getattr(event,"rPt"),getattr(event,"rSumPtTrk"),getattr(event,"rWidth"))
    return True
# ended function

# read a Tree with a style specific to Python and then thin it
# this means keeping all the branches of the tree but only for some events
# we can select the events by asking a cut, or by throwing a random number
# either way, for each event keep all the branches without the code needing to know
# what all those branches are. it means the code can be short even for trees 
# with many many branches
# ex: exThinTree("file1.root","tree1","rPt",10.0,18.0,"thinned_file1.root",False)
def exThinTree(fileName,treeName,variableName,cut_low,cut_high,outfileName,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # create the output file
    outfile=TFile(outfileName,"RECREATE")
    # create the output tree as a clone of the initial tree
    # as we create it after the outfile is created
    # it will be owned by outfile and it will be saved to outfile when outfile will be closed
    outtree=tree.CloneTree(0)
    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    for event in tree:
        value=getattr(tree,variableName)
        # now we can use the value to apply a cut on event based on this value
        if cut_low <= value <= cut_high:
            outtree.Fill()
        if debug:
            # in this simple example simply print them
            print "current value is",value,"cut_low",cut_low,"cut_high",cut_high

    # after the event loop, save the outtree (it will be saved to the outfile)
    outtree.AutoSave()
    return True
# ended function


# read a Tree with a style specific to Python and then thin it
# based on the invariant mass of the two jets
# ex: exThinTree("file1.root","tree1",10.0,18.0,"thinned_file1.root",False)
def exThinTreeHiggsMass(fileName,treeName,cut_low,cut_high,outfileName,debug=False):
   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName
        assert(False)
    # create the output file
    outfile=TFile(outfileName,"RECREATE")
    # create the output tree as a clone of the initial tree
    # as we create it after the outfile is created
    # it will be owned by outfile and it will be saved to outfile when outfile will be closed
    outtree=tree.CloneTree(0)
    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    #
    string_4vecs="Pt,Eta,Phi,E"
    type="r"
    # start loop over events
    for event in tree:
        tlv1=TLorentzVector()
        tlv1.SetPtEtaPhiE(*getValues(event,updateListVariables("j1"+type,string_4vecs,"")))
        tlv2=TLorentzVector()
        tlv2.SetPtEtaPhiE(*getValues(event,updateListVariables("j2"+type,string_4vecs,"")))
        tlv12=tlv1+tlv2
        value=tlv12.M()
        # now we can use the value to apply a cut on event based on this value
        if cut_low <= value <= cut_high:
            outtree.Fill()
        if debug:
            # in this simple example simply print them
            print "current value is",value,"cut_low",cut_low,"cut_high",cut_high

    # after the event loop, save the outtree (it will be saved to the outfile)
    outtree.AutoSave()
    return True
# ended function


# create TTree in TFile flexible what to create inside
# list_variables=[]
# list_variables.append(['d','rPt','D',12.2])
# list_variables.append(['d','rE','D',14.7])
# ex addTree("test3.root","RECREATE","tree3",list_variables,True) if you want to add the tree to a new file
# ex addTree("test3.root","UPDATE","tree3",list_variables,True) if you want to add a tree to an existing file
def addTree(fileName,fileOpen,treeName,list_variables,debug):
    file=TFile(fileName,fileOpen)
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    tree=TTree(treeName,treeName)
    # study the list_of_lists
    nr_variables=len(list_variables)
    if debug:
        print "nr_variables",nr_variables
        for i in xrange(nr_variables):
            print list_variables[i]
    # loop over variables for each variable:
    list_values=[]
    for i in xrange(nr_variables):
        # create an array of desired type with one entry and append it to a list of values
        # ex: rPt=array('d', [0])
        list_values.append(array(list_variables[i][0], [0]))
        # add the branch to the tree with the desired name and type and passing the value from above
        # ex: tree.Branch('rPt',rPt,"rPt/D")
        tree.Branch(list_variables[i][1],list_values[i],list_variables[i][1]+"/"+list_variables[i][2])
        # done loop over variables
    # loop from 0 to 9 events
    for j in xrange(10):
        # loop over all variables for each event and fill the dummy values the user has requested
        for i in xrange(nr_variables):
            # ex: rPt[0]=12.2
            list_values[i][0]=list_variables[i][3]
        # now fill the tree with these values
        tree.Fill()
        # Done, so exit the for loop
    # now write the contents of the file to the file (thus the tree as well)
    # if we write both the tree and the file, then the tree appears twice (2 cycles)
    # tree.Write()
    file.Write()
    # close the file
    file.Close()
    # we are done, so we can return anything so let's just return True
    return True
# ended function

# list object from file
# ex: ListObjects(fileName,False)
# ex of class: TH1F, TH1D, TF1, TDirectoryFile
def listObjects(inputFileName,directoryPath="",searchClass="",list_searchName=["",""],doOption="A",doShowIntegral=False,outputFileName="a.log",debug=False):
    if debug:
        print "Start .ls of root inputFile ",inputFileName
    if outputFileName!="":
        outputFile=open(outputFileName,"w")
    inputFile=TFile(inputFileName,"READ")
    if not inputFile.IsOpen():
        print "inputFile",inputFileName,"does not exist, so will abort"
        assert(False)
    gDirectory.cd(directoryPath)
    list_key=gDirectory.GetListOfKeys()
    list_key.sort() # sort it in alphabetical order
    for key in list_key:
        if not (searchClass=="" or key.GetClassName()==searchClass):
            continue
        if not all(x in key.GetName() for x in list_searchName):
            continue
        if doOption=="A":
            text=key.GetClassName()+" "+key.GetName()
            if doShowIntegral and "TH" in searchClass:
                text+=" integral="+str(gDirectory.Get(key.GetName()).Integral())
        elif doOption=="B":
            assert(len(list_searchName)==1)
            searchName=list_searchName[0]
            text=key.GetName().replace(searchName+"_","")
        else:
            print "doOption",doOption,"not known. Choose A or B. Will ABORT!!!"
            assert(False)
        # done if
        if outputFileName=="":
            print text
        else:
            outputFile.write(text+"\n")
    if False:
        gDirectory.ls()
    if outputFileName!="":
        outputFile.close()
        print "Output written to file",outputFile
    inputFile.Close()
    if debug:
        print "End .ls of root inputFile ",inputFileName
    return True
# ended function

# remove object from file
# ex: removeObject("root1.root","tree1",";*",False)
# by adding ";*" you remove all the cycles (useful if they are more than 1)
def removeObject(fileName,objectName,objectCycle,debug=False):
    if debug:
        print "Start remove objectName",objectName,"with cycle",objectCycle,"from fileName",fileName
    # open the file in UPDATE mode 
    file=TFile(fileName,"UPDATE")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    if debug:
        print "Start .ls in the file before object removal"
        file.ls()
        print "End .ls in the file before object removal"
    if objectCycle=="":
        objectCycle=";*"
    file.Delete(objectName+objectCycle)
    if debug:
        print "Start .ls in the file after object removal"
        file.ls()
        print "End .ls in the file after object removal"
    file.Close()
    return True
    if debug:
        print "End remove objectName",objectName,"with cycle",objectCycle,"from fileName",fileName
    return True
# ended function

# remove object from file
# ex: removeObjects("root1.root",["tree1","tree2"],";*",False)
# the difference is a list of names of objects and removes all of them
# by adding ";*" you remove all the cycles (useful if they are more than 1)
def removeObjects(fileName,objectNames,objectCycle,debug=False):
    if debug:
        print "Start remove objects named",objectNames,", for each using cycle",objectCycle,"from fileName",fileName
    # open the file in UPDATE mode 
    file=TFile(fileName,"UPDATE")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    if debug:
        print "Start .ls in the file before object removal"
        file.ls()
        print "End .ls in the file before object removal"
    for objectName in objectNames:
        # only if it exists, remove the object
        # the code would not crash if we try to remove an object that does not exist
        # but it would be redundant
        if exists(file.Get(objectName),objectName,True):
            file.Delete(objectName+objectCycle)
    if debug:
        print "Start .ls in the file after object removal"
        file.ls()
        print "End .ls in the file after object removal"
    file.Close()
    return True
    if debug:
        print "Start remove objects named",objectNames,", for each using cycle",objectCycle,"from fileName",fileName
    return True
# ended function

# ex: getNrEntries("file1.root","tree1",True)
# ex: getNrEntries("WH125.root","per_jet",True)
def getNrEntries(fileName,treeName,debug=False):
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    tree=file.Get(treeName)
    if tree==None:
        print "ERROR tree",treeName,"doesn't exist in file",fileName
        #assert(False)
        return -1
    # end if
    nrEntries=tree.GetEntries()
    if debug:
        print "Number of entries in file",fileName,"in tree",treeName,"is",nrEntries
    return nrEntries
# ended function

# ex: showTreeEntries("file1.root","tree1",-1,-2,True)
def showTreeEntries(fileName,treeName,min_entry,max_entry,debug=False):
   file=TFile(fileName,"READ")
   if not file.IsOpen():
       print "File",fileName,"does not exist, so will abort"
       assert(False)
   tree=file.Get(treeName)
   if tree==None:
       print "tree",treeName,"doesn't exist in file",fileName
       assert(False)
   nrEntries=tree.GetEntries()
   if debug:
       print "Asked: nrEntries",nrEntries,"min_entry",min_entry,"max_entry",max_entry
   if min_entry<0 or min_entry>nrEntries:
       min_entry=0
   if max_entry<0 or max_entry>nrEntries:
       max_entry=nrEntries-1
   if debug:
       print "Used : nrEntries",nrEntries,"min_entry",min_entry,"max_entry",max_entry
   for i in xrange(min_entry,max_entry+1):
       tree.Show(i)
   return True
# ended function

# ex:  SumP=getSumValue("WH125.root","per_jet","rPt",True)
def getSumValue(fileName,treeName,variableName,debug=False):
   file=TFile(fileName,"READ")
   if not file.IsOpen():
       print "File",fileName,"does not exist, so will abort"
       assert(False) 
   tree=file.Get(treeName)
   if tree==None:
       print "tree",treeName,"doesn't exist in file",fileName
       assert(False)
   sumValue=0.0 
   for event in tree:
       sumValue+=getattr(event,variableName)
   if debug:
       nrEntries=tree.GetEntries()
       print "Sum of the values for variable",variableName," of all",nrEntries,"entries in file",fileName,"in tree",treeName,"is",sumValue
   return sumValue
# ended function

# ex:  print getSumAverageValue("WH125.root","per_jet","rPt",True)
def getSumAverageValue(fileName,treeName,variableName,debug=False):
   file=TFile(fileName,"READ")
   if not file.IsOpen():
       print "File",fileName,"does not exist, so will abort"
       return(False)
   tree=file.Get(treeName)
   if tree==None:
       print "tree",treeName,"doesn't exist in file",fileName
       assert(False)
   sumValue=0.0 
   for event in tree:
       sumValue+=getattr(event,variableName)
   nrEntries=tree.GetEntries()
   if nrEntries!=0:
       averageValue=sumValue/nrEntries
   else:
       averageValue=0.0
   if debug:
       print "Sum of the values for variable",variableName," of all",nrEntries,"entries in file",fileName,"in tree",treeName,"is",sumValue,",with the average value being",averageValue
   return nrEntries,sumValue,averageValue
# ended function

# func like a Bukin fit, dx is the step
def medianOfFunction(func,dx):
    min=func.GetXmin()
    max=func.GetXmax()
    x=min
    integral=0
    total=func.Integral(min,max)

    # Integrates across the function until half the total area is reached.
    while x<=max and ratio(integral,total)<0.5:
        integral=func.Integral(min,x)
        x+=dx
    return x
# ended function

def retrieveObject(fileName="",objectType="histo",objectPath="",objectName="",name="",returnDummyIfNotFound=False,debug=False):
    if debug:
        print "fileName",fileName
        print "objectPath",objectPath
        print "objectName",objectName
        print "name",name
    file=TFile(fileName,"READ")
    if debug:
        print "file",file,"type(file)",type(file)
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    #if debug:
    #    file.ls()
    gDirectory.cd(objectPath)
    if False:
        print "objectPath",objectPath
        print "gDirectory.ls()"
        gDirectory.ls()
        print "objectName",objectName
    object=gDirectory.Get(objectName)
    if debug:
        print "object",object,"type(object)",type(object)
    if object==None:
        if returnDummyIfNotFound==True:
            print "WARNING!!!! object",objectName,"doesn't exist in file",fileName,"at path",objectPath,". We will return a string called dummy!!!"
            return "dummy" # return a dummy string
        else:
            print "object",objectName,"doesn't exist in file",fileName,"at path",objectPath,". We will ABORT!!!!"
            assert(False)
    if name!="":
        object.SetName(name)
        object.SetTitle(name)
    if objectType=="histo":
        # needed so that the object is able to return a histogram
        # otherwise it will return <type 'PyROOT_NoneType'>
        object.SetDirectory(0)
    elif objectType=="function":
        None
    else:
        print "objectType",objectType,"not known. Choose histo or function. Will ABORT!!"
        assert(False)
    return object
# ended function

# retrieve histogram from file
# ex: histo=retrieveHistogram(fileName=inputFileName,histoPath=histoPath,histoName=histoName,name="",returnDummyIfNotFound=False,debug=debug)
def retrieveHistogram(fileName="",histoPath="",histoName="",name="",returnDummyIfNotFound=False,debug=False):
    histo=retrieveObject(fileName=fileName,objectType="histo",objectPath=histoPath,objectName=histoName,name=name,returnDummyIfNotFound=returnDummyIfNotFound,debug=debug)
    return histo
# ended function

# add  histogram to existing file
def writeHistogram(fileName,histo,histoPath,histoName="",histoTitle="",debug=False):
    c=inspect.currentframe();
    if debug:
        print c.f_lineno
    file=TFile(fileName,"UPDATE")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        assert(False)
    path="/"
    for folder in histoPath:
        #print folder
        path+=folder+"/"
        if debug:
            print path
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
        # if the next desired folder does not exist, then create it
        if not gDirectory.Get(folder):
            gDirectory.mkdir(folder)
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
        # either it already existed, or it was created now, cd there
        gDirectory.cd(folder)
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
    file.cd(path)
    h=histo.Clone()
    if histoName!="":
        h.SetName(histoName)
    if histoTitle!="":
        h.SetTitle(histoTitle)
    h.Write("",TObject.kOverwrite)
    #file.Write()
    file.Close()
    return True
# ended function

# add  histogram to existing file
# ex: createDirectory("file1.root",["ADI","TrigJetRec","U","Good"],False)
def createDirectory(fileName,folders,debug=False):
    c=inspect.currentframe();
    if debug:
        print c.f_lineno
    file=TFile(fileName,"UPDATE")
    path="/"
    for folder in folders:
        #print folder
        path+=folder+"/"
        if debug:
            print path
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
        # if the next desired folder does not exist, then create it
        if not gDirectory.Get(folder):
            gDirectory.mkdir(folder)
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
        # either it already existed, or it was created now, cd there
        gDirectory.cd(folder)
        if debug:
            print gDirectory.pwd()
            print gDirectory.ls()
    file.cd(path)
    file.Close()
    return True
# ended function

# plot just one histogram, either 1D or 2D
def plotHistogram(h,plot_option="",filePath="./",fileName="plot",extensions="pdf"):
    # plot one histogram, either 1D or 2D
    #h.SetLineColor(1)
    c=TCanvas()
    h.Draw(plot_option)
    # if path does not have / as the last character, add one
    if filePath=="":
        filePath="./"
    elif filePath[-1]!="/":
        filePath+="/"
    # compute the name
    if fileName=="":
        fileName=filePath+h.GetName()
    else:
        fileName=filePath+fileName
    # save the canvas in files with what extensions we want
    for extension in extensions.split(","):
        c.Print(fileName+"."+extension)
    # ended for over extensions
    return None
# ended function

# plot two histograms (numerator and denominator) and at the bottom their ratio, which is fitted
def plotHistograms(hnumer0,hdenom0,hratio0,plot_option="",filePath="./",fileName="plot",extensions="pdf",debug=False):
    hdenom=hdenom0.Clone()
    hnumer=hnumer0.Clone()
    hratio=hratio0.Clone()
    # plot one histogram, either 1D or 2D
    gStyle.SetOptStat(0) 
    c=TCanvas("c","c",600,600)
    p_main=TPad("p_main","p_main",0,0.33,1,1)
    p_ratio=TPad("p_ratio","p_ratio",0,0,1,0.33)
    p_main.Draw()
    p_ratio.Draw()
    # main pad
    p_main.cd()
    hdenom.SetLineColor(4)
    hnumer.SetLineColor(2)
    hdenom.SetMinimum(0)
    myMax=max(hdenom.GetMaximum(),hnumer.GetMaximum())
    hnumer.SetMaximum(myMax*1.30)
    hnumer.Draw(plot_option)
    hdenom.Draw(plot_option+"SAME")
    legend_info=[0.65,0.70,0.88,0.82,72,0.037,0]
    legend=get_legend(legend_info,debug)
    legend.AddEntry(hnumer,"Num: Alternative","f")
    legend.AddEntry(hdenom,"Den: Default","f")
    legend.SetBorderSize(0)
    legend.Draw("same")
    p_main.Update()
    # ratio pad
    p_ratio.cd()
    hratio.Draw(plot_option)
    # canvas
    c.Update()

    # if path does not have / as the last character, add one
    if filePath=="":
        filePath="./"
    elif filePath[-1]!="/":
        filePath+="/"
    # compute the name
    if fileName=="":
        fileName=filePath+h.GetName()
    else:
        fileName=filePath+fileName
    # save the canvas in files with what extensions we want
    for extension in extensions.split(","):
        c.Print(fileName+"."+extension)
    # ended for over extensions
    return None
# ended function

def get_string_distribution(prefix,name,height,mean,rms):
    if mean==0:
        rms_mean=0.0
    else:
        rms_mean=rms/mean
    result="%-10s %-25s %-5.1f %-4.1f %-4.1f %-5.0f" % (prefix,name,mean*100,rms*100,rms_mean*100,height)
    return result
# done function

def get_median_histogram(h,debug):
    # from here: https://root.cern.ch/phpBB3/viewtopic.php?t=7802
    numBins = h.GetXaxis().GetNbins()
    #Double_t *x = new Double_t[numBins];
    x=array("d",[])
    #Double_t* y = new Double_t[numBins];
    y=array("d",[])
    #for (int i = 0; i < numBins; i++) {
    #    x[i] = histo1->GetBinCenter(i);
    #    y[i] = histo1->GetBinContent(i);
    #double MedianOfHisto = TMath::Median(numBins, &x[], &y[])
    #
    for i in xrange(numBins):
        x.append(h.GetBinCenter(i))
        y.append(h.GetBinContent(i))
    # 
    median=TMath.Median(numBins,x,y)
    if debug:
        print "median",median
    return median
# done histogram


# ex: fit_hist(h,"None",False,"","canvasname",false)
def fit_hist(h=TH1F(),fitRange=[-1,-1],defaultFunction=TF1(),fit="None",addMedianInFitInfo=False,plot_option="",doValidationPlot=True,canvasname="canvasname",debug=False):
    if debug:
        print "Start fit_hist"
        print "h",type(h),h
        print "fitRange",fitRange
        print "fit",fit
        print "plot_option",plot_option
    if fitRange==0 or (fitRange[0]==-1 and fitRange[1]==-1) or fitRange[1]<fitRange[0]:
        fitRangeDefault=True
        xmin=h.GetBinLowEdge(0)
        NrBins=h.GetNbinsX()
        xmax=h.GetBinLowEdge(NrBins)+h.GetBinWidth(NrBins)
    else:
        fitRangeDefault=False
        xmin=fitRange[0]
        xmax=fitRange[1]
    #

    if doValidationPlot:
        ROOT.gStyle.SetOptFit(1011)
        c=TCanvas("c","c",800,600)
        h.Draw()
    #SetOwnership(h,0)
    if debug:
        print "****************** Start getBinvalues in fit ************"
        print "GetEntries",h.GetEntries()
        getBinValues(h,doRescaleMeVtoGeV=False,debug=debug)
        print "****************** End getBinvalues in fit ************"
    entries=h.GetEntries()
    height=h.GetMaximum()
    mean=h.GetMean()
    rms=h.GetRMS()
    #median=mean # todo: to update to median of histogram as per https://root.cern.ch/phpBB3/viewtopic.php?t=7802
    median=get_median_histogram(h,debug)
    if addMedianInFitInfo==True:
        result=((median,0.0),(height,0.0),(mean,0.0),(rms,0.0))
    else:
         result=((0.0,0.0),(height,0.0),(mean,0.0),(rms,0.0),(0.0,0.0),(0.0,0.0),(0.0,0.0))
    f=defaultFunction
    if debug:
        print "initially as dummy values"
        print "entries",entries
        print "result",result
        print "f",type(f),f
        print "fit",fit

    cutnentries=50
    color=h.GetLineColor()
    if fit=="None":
        None
    elif fit=="Sigmoid":
        if True:
            function=TF1("sigmoid",Sigmoid(),xmin,xmax,2)
            h.Fit("sigmoid","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("sigmoid")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(0.0,0.0))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(0.0,0.0))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Linear":
        #if entries>cutnentries and rms>0.02:
        if rms>0.02:
            if debug:
                print "we do the fit, as entries>cutnentries and rms>0.02"
            function=TF1("linear",Linear(),xmin,xmax,2)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            h.Fit("linear","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("linear")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(0.0,0.0))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(0.0,0.0))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            print "WARNING! No fit done, as entries=",entries,"rms=",rms
            None
    elif fit=="PieceWiseLinear":
        #if entries>cutnentries and rms>0.02:
        if rms>0.02:
            if debug:
                print "we do the fit, as entries>cutnentries and rms>0.02"
            if debug:
                print "xmin",xmin,"xmax",xmax
            function=TF1("piecewiselinear",PieceWiseLinear(),xmin,xmax,6)
            if debug:
                print "Done define function of type TF1"
            # y=y1+(x-x1)*(y2-y1)/(x2-x1)
            # y=y2+(x-x2)*(y3-y2)/(x3-x2)
            # set parameter name
            # notation of parameters from Eliot, 
            # may be renamed later so that the parameters come in the more natural order x1,y1,x2,y2,x3,y3
            function.SetParName(0,"p0") # x1
            function.SetParName(1,"p1") # y1
            function.SetParName(2,"p2") # x2
            function.SetParName(3,"p3") # y2
            function.SetParName(4,"p4") # x3
            function.SetParName(5,"p5") # y3
            if debug:
                print "Done function SetParName"
            # set parameter values to default values of two straight lines, both at 1
            # y1 = y2 = y3 = 1.0
            # for mcc: x1 = 30; x3 = 230; x2 = 30+(230-30)/2 = 130 (at middle)
            # for BDT: x1 = -1; x3 = +1;  x2 = -1+(1-(-1))/2 = 0   (at middle)
            function.SetParameter(0,xmin)
            function.SetParameter(1,1.0)
            function.SetParameter(2,xmin+0.5*(xmax-xmin))
            function.SetParameter(3,1.0)
            function.SetParameter(4,xmax)
            function.SetParameter(5,1.0)
            if debug:
                print "Done function SetParameter"
            h.Fit("piecewiselinear","RQ",plot_option+"same",xmin,xmax)
            if debug:
                print "Done do the fit"
            f=h.GetFunction("piecewiselinear")
            if debug:
                print "Done get the function"
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParError(2),f.GetParameter(2)),(f.GetParError(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParError(2),f.GetParameter(2)),(f.GetParError(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)))
            if debug:
                print "Done create result by getting parameters"
            f.SetLineColor(color)
            f.Draw("SAME")
            if debug:
                print "Done set color and draw the function with SAME"
        else:
            print "WARNING! No fit done, as entries=",entries,"rms=",rms
            None
    elif fit=="Parabolic":
        if True:
            function=TF1("parabolic",Parabolic(),xmin,xmax,3)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            h.Fit("parabolic","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("parabolic")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Parabolic2":
        if True:
            function=TF1("parabolic2",Parabolic2(),xmin,xmax,5)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            function.SetParName(3,"p3")
            function.SetParName(4,"p4")
            # set parameter values 
            function.SetParameter(0,1.0)
            function.SetParameter(0,1.0)
            function.SetParameter(0,1.0)
            function.SetParameter(0,-1.0)
            function.SetParameter(0,1.0)
            h.Fit("parabolic2","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("parabolic2")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif "pol" in fit:
        if True:
            h.Fit(fit,"Q",plot_option+"same",xmin,xmax)
            f=h.GetFunction(fit)
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Polynomial3":
        if True:
            function=TF1("polynomial3",Polynomial3(),xmin,xmax,4)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            function.SetParName(3,"p3")
            #
            function.SetParameter(0,1.0)
            function.SetParameter(1,1.0)
            function.SetParameter(2,1.0)
            function.SetParameter(3,1.0)
            h.Fit("polynomial3","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("polynomial3")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Polynomial4":
        if True:
            function=TF1("polynomial4",Polynomial4(),xmin,xmax,5)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            function.SetParName(3,"p3")
            function.SetParName(4,"p4")
            h.Fit("polynomial4","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("polynomial4")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)))
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Polynomial5":
        if True:
            function=TF1("polynomial5",Polynomial5(),xmin,xmax,6)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            function.SetParName(3,"p3")
            function.SetParName(4,"p4")
            function.SetParName(5,"p5")
            h.Fit("polynomial5","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("polynomial5")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5))) 
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Polynomial6":
        if True:
            function=TF1("polynomial6",Polynomial6(),xmin,xmax,7)
            function.SetParName(0,"p0")
            function.SetParName(1,"p1")
            function.SetParName(2,"p2")
            function.SetParName(3,"p3")
            function.SetParName(4,"p4")
            function.SetParName(5,"p5")
            function.SetParName(6,"p6")
            h.Fit("polynomial6","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("polynomial6")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)),(f.GetParameter(6),f.GetParError(6)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)),(f.GetParameter(6),f.GetParError(6)))      
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Gauss":
        if entries>cutnentries and rms>0.02:
            if fitRangeDefault==True:
                xmin=mean-2*rms
                xmax=mean+2*rms
            function=TF1("gauss",Gauss(),xmin,xmax,3)
            function.SetParName(0,"height")
            function.SetParName(1,"mean")
            function.SetParName(2,"width")
            function.SetParameter(0,height)
            function.SetParameter(1,mean)
            function.SetParameter(2,rms)
            h.Fit("gauss","RQ",plot_option+"same",xmin,xmax)
            f=h.GetFunction("gauss")
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)))  
            f.SetLineColor(color)
            f.Draw("SAME")
        else:
            None
    elif fit=="Bukin":
        if debug:
            print "We are starting the Bukin fit"
        if entries>cutnentries and rms>0.02:
            if debug:
                print "we do the fit, as entries>cutnentries and rms>0.02"
            if fitRangeDefault==True:
                xmin=mean-3*rms
                xmax=mean+3*rms
            # hack for Mbb mass fit like Manuel between 20 and 200
            #xmin=70.0
            #xmax=145.0
            function=TF1("bukin",Bukin(),xmin,xmax,6)
            function.SetParName(0,"height")
            function.SetParName(1,"peak") # actually the peak, as it may be asymmetric
            function.SetParName(2,"width")
            function.SetParName(3,"asymmetry")
            function.SetParName(4,"size of lower tail")
            function.SetParName(5,"size of higher tail")
            function.SetParameter(0,height)
            #function.SetParameter(0,100)
            function.SetParameter(1,mean)
            function.SetParameter(2,rms)
            #function.SetParameter(3,-0.4)
            #function.SetParameter(4,0.01)
            #function.SetParameter(5,0.005)
            if debug:
                print "we just set the function used for the fit"
            h.Fit("bukin","RQ",plot_option+"same",xmin,xmax)
            if debug:
                print "we just performed the fit"
            f=h.GetFunction("bukin")
            if debug:
                print "we just retrieved f"
            if addMedianInFitInfo==True:
                result=((medianOfFunction(f,0.01),0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)))
            else:
                result=((0.0,0.0),(f.GetParameter(0),f.GetParError(0)),(f.GetParameter(1),f.GetParError(1)),(f.GetParameter(2),f.GetParError(2)),(f.GetParameter(3),f.GetParError(3)),(f.GetParameter(4),f.GetParError(4)),(f.GetParameter(5),f.GetParError(5)))
            if debug:
                print "result of the fit",result
            # these will plot just the function
            #SetOwnership(f,0)
            f.SetLineColor(color)
            #f.Draw("SAME")
        else:
            if debug:
                print "we don't do the fit, as it fails entries>cutnentries and rms>0.02"
            None
        if debug:
            print "We just ended the Bukin fit"    
    else:
        None
        print "fit",fit,"is unknown. Choose None, Gauss, Bukin. Will return an empty function."
    # end loop over fit
    if debug:
        print "done the fit that we wanted",fit
        print "f",f,"type(f)",type(f)
        print "result",result
    if doValidationPlot:
        c.Print(canvasname+"_"+fit+".pdf")
    if debug:
        print "we now exit fit_hist(...) function"
    #SetOwnership(f,1)
    #not able to return the function
    return f,result
# done function

def get_value_error_from_result_fit(fitVar,result_fit,debug):
    if debug:
        print "result_fit (median,(height,height_error),(mean,mean_error),(sigma,sigma_error))",result_fit
    if fitVar=="Par1":
        value=result_fit[2][0] # mean or peak
        error=result_fit[2][1] 
    elif fitVar=="Par2":
        value=result_fit[3][0] # mean or peak
        error=result_fit[3][1] 
    elif fitVar=="Ratio":
        value=ratio(result_fit[3][0],result_fit[2][0]) # sigma/mean
        error=0.0 # https://en.wikipedia.org/wiki/Propagation_of_uncertainty
    else:
        print "fitVar",fitVar,"not known. Will ABORT!!!"
        assert(False)
    # done if
    return (value,error)
# done function
        
# ex: 
def update_h1D_characteristics(h,rebin,plotting,xaxis,yaxis,debug):
    if debug:
        print "rebin",rebin
        print "color for line for fill for marker",plotting[0]
        print "marker style",plotting[1]
        print "fill style",plotting[2]
        print "marker size and line width",plotting[3]
        print "xaxis title",xaxis[0]
        print "xaxis title size",xaxis[1]
        print "xaxis title offset",xaxis[2]
    h.Rebin(rebin)
    h.SetLineColor(plotting[0])
    h.SetFillColor(plotting[0])
    h.SetMarkerStyle(plotting[1])
    h.SetMarkerColor(plotting[0])
    h.SetMarkerSize(plotting[3])
    h.SetFillStyle(plotting[2])
    h.SetLineWidth(plotting[3])
    h.GetXaxis().SetTitle(xaxis[0])
    h.GetXaxis().SetTitleSize(xaxis[1])
    h.GetXaxis().SetTitleOffset(xaxis[2])
    h.GetYaxis().SetTitle(yaxis[0])
    h.GetYaxis().SetTitleSize(yaxis[1])
    h.GetYaxis().SetTitleOffset(yaxis[2])
# done function

def update_h1D_characteristics_from_another_one(new,old,debug):
    new.SetLineColor(old.GetLineColor())
    new.SetFillColor(old.GetLineColor())
    new.SetMarkerStyle(old.GetLineColor())
    new.SetMarkerColor(old.GetLineColor())
    new.SetMarkerSize(old.GetMarkerSize())
    new.SetFillStyle(old.GetFillStyle())
    new.SetLineWidth(old.GetLineWidth())
    new.GetXaxis().SetTitle(old.GetXaxis().GetTitle())
    new.GetXaxis().SetTitleSize(old.GetXaxis().GetTitleSize())
    new.GetXaxis().SetTitleOffset(old.GetXaxis().GetTitleOffset())
    new.GetYaxis().SetTitle(old.GetYaxis().GetTitle())
    new.GetYaxis().SetTitleSize(old.GetYaxis().GetTitleSize())
    new.GetYaxis().SetTitleOffset(old.GetYaxis().GetTitleOffset())
# done function

def setErrorsToZero(h,debug):
    N=h.GetNbinsX()
    for i in xrange(N+1):
        h.SetBinError(i,0.0);
# done function

def get_legend(info,debug):
    if debug:
        print "x_min",info[0]
        print "y_min",info[1]
        print "x_max",info[2]
        print "y_max",info[3]
        print "text_font",info[4]
        print "text_size",info[5]
        print "fill_color",info[6]
    legend=TLegend(info[0],info[1],info[2],info[3])
    legend.SetTextFont(info[4])
    legend.SetTextSize(info[5])
    legend.SetFillColor(info[6])
    return legend
# done function

def set_min_max_title_list_tuple_h1D(list_tuple_h1D,max_value,min_value,ignorezero,max_value_factor,min_value_factor,debug):
    # number of histograms we are overlaying
    num=len(list_tuple_h1D)
    if debug:
        print "len(list_tuple_h1D)=",len(list_tuple_h1D)
        if num>0:
            for i in range(num):
                print "type("+str(i)+")=",type(list_tuple_h1D[i][0])
    # find the minimum value of all the histograms. Pick an initial value that
    # should be biggest than all
    if min_value==-1:
        min_value=999999
        for i in range(num):
            if debug:
                print "i",i,"min_value to start with",min_value
            if ignorezero:
                current_min=list_tuple_h1D[i][0].GetMinimum(0.8)
                if debug:
                    print "we are in ignore zero, i", i, current_min
            else:
                current_min=list_tuple_h1D[i][0].GetMinimum()
                if debug:
                    print "we do not ignore zero, current_min",current_min
            if current_min <= min_value:
                min_value=current_min
        # decrease a bit to be able to see better the highest value
        min_value*=min_value_factor #0.9
        if debug:
            print "min",min_value
    # else of course it remains with the value set by the user
    # find the maximum value of all the histograms
    if max_value==-1:
        max_value=0.0
        for i in range(num):
            if list_tuple_h1D[i][0].GetMaximum() >= max_value:
                max_value=list_tuple_h1D[i][0].GetMaximum()
        # increase by a bit to be able to see better the highest value
        max_value*=max_value_factor #1.30
        if debug:
            print "max",max_value
    # else of course it remains with the value set by the user
    # as the first histogram gives the template to the entire canvas
    # tell the first histogram to use this maximum size
    list_tuple_h1D[0][0].SetMaximum(max_value)
    # tell the first histogram to use this minimum size
    list_tuple_h1D[0][0].SetMinimum(min_value)

   # For the first histogram and thus for the canvas
    # Remove title and statistics box if there is more than one histogram
    if num>1:
        list_tuple_h1D[0][0].SetTitle("")
# done function

def get_histo_normalised(h,debug=False):
    h_new=h.Clone(h.GetName()+"_normalised")
    h_new.Scale(ratio(1.0,h_new.Integral()))
    return h_new
# done function

def get_histo_values(h,i,debug=False):
    low=h.GetBinLowEdge(i)
    high=low+h.GetBinWidth(i)
    value=h.GetBinContent(i)
    error=h.GetBinError(i)
    return (low,high,value,error)
# done function

# actually coded by Root in h.Rebin(nbins,"new name",numpyArrayOfbins)
# https://root.cern.ch/doc/master/classTH1.html#aff6520fdae026334bf34fa1800946790
# so can get rid of this
# ex  h=get_histo_subRange(h,[260,340],debug)
def get_histo_subRange(h,subRange,debug=False):
    xmin=subRange[0]
    xmax=subRange[1]
    counter=0
    if debug:
        print "Looping the first time over initial histogram in get_histo_subRange()"
    for i in xrange(h.GetNbinsX()+1):
        low=h.GetBinLowEdge(i)
        high=low+h.GetBinWidth(i)
        value=h.GetBinContent(i)
        error=h.GetBinError(i)
        if high<=xmin:
            continue
        if low>=xmax:
            continue
        counter+=1
        if debug:
            print i, low,high,value,error
    # done for loop
    # make string from xrange
    stringSubRange=str(xmin)+"_"+str(xmax)
    h_subRange=TH1F(h.GetName()+"_"+stringSubRange,h.GetTitle()+"_"+stringSubRange,counter,xmin,xmax)
    #
    counter=0
    if debug:
        print "Looping the second time over initial histogram in get_histo_subRange()"
    for i in xrange(h.GetNbinsX()+1):
        low,high,value,error=get_histo_values(h,i,debug)
        if high<=xmin:
            continue
        if low>=xmax:
            continue
        counter+=1
        if debug:
            print counter,low,high,value,error
        h_subRange.SetBinContent(counter,value)
        h_subRange.SetBinError(counter,error)
        if debug:
            print counter,get_histo_values(h_subRange,counter,debug)
    # done loop
    if debug:
        print "Looping over produced histogram in get_histo_subRange()"
        print h_subRange.GetNbinsX()
        for i in xrange(h_subRange.GetNbinsX()+1):
            print i,get_histo_values(h_subRange,i,debug)
    # done loop
    #h_subRange.SetDirectory(0)
    #SetOwnership(h_subRange,0)
    return h_subRange
# done

# actually coded by Root in h.Rebin(nbins,"new name",numpyArrayOfbins)
# https://root.cern.ch/doc/master/classTH1.html#aff6520fdae026334bf34fa1800946790
# so can get rid of this
def get_histo_generic_binRange(h,binRange="150,200,400",option="sum",debug=False):
    if option!="sum" and option!="average":
        print "option",option,"not known. Choose sum, average. Will ABORT!!!"
        assert(False)
    # evaluate the desired binning
    nparray_binRange=get_numpyarray_from_listString(binRange.split(","),debug)
    if debug:
        print "nparray_binRange",nparray_binRange
    histoName=h.GetName()
    histoTitle=h.GetTitle()
    histoNrBins=len(nparray_binRange)-1
    if debug:
        print "histoName",histoName,"histoTitle",histoTitle,"histoNrBins",histoNrBins
    # create a histogram with this binning
    result=TH1F(histoName,histoTitle,histoNrBins, nparray_binRange)
    # loop over each bin of the new histogram
    for i in xrange(1,result.GetNbinsX()+1):
        low=result.GetBinLowEdge(i)
        width=result.GetBinWidth(i)
        high=low+width
        if debug:
            print "bin", i,"low",low,"high",high
        # find all the bins of the initial histogram that are between low and high
        # and then sum them together and calculate their combined statistical error
        # and set them here
        value=0.0
        error_squared=0.0
        for j in xrange(1,h.GetNbinsX()+1):
            current_low=h.GetBinLowEdge(j)
            current_width=h.GetBinWidth(j)
            current_high=current_low+current_width
            # skip the bins that not in our range
            if current_high<=low or current_low>=high:
                continue                
            current_value=h.GetBinContent(j)
            current_error=h.GetBinError(j)
            if debug:
                print "bin initial histogram", j,"current_low",current_low,"current_high",current_high,"value",current_value,"error",current_error
            value+=current_value
            # error propagation: error of on bin is the sqrt of sum of weights
            # https://root.cern.ch/doc/master/classTH1.html Associated errors Sumw2
            error_squared+=current_error*current_error
        # done loop over the bins of the initial histogram
        # we need the average value, so divide by the bin width
        error=math.sqrt(error_squared)
        if option=="average":
            value/=width
            error/=width
        elif option=="sum":
            None
        # set the value and error of our histogram
        result.SetBinContent(i,value)
        result.SetBinError(i,error)
    # all done
    getBinValues(result,doRescaleMeVtoGeV=False,debug=debug)
    return result
# done function

def get_histo_smoothed(h,debug):
    #for i in xrange(h.GetNbinsX()+1):
    result=h.Clone()
    #result.Rebin(2)
    result.Reset()
    for i in xrange(h.GetNbinsX()+1):
        value=average(h.GetBinContent(i-1),h.GetBinContent(i),h.GetBinContent(i+1))
        error=add_in_quadrature_three(h.GetBinError(i-1),h.GetBinError(i),h.GetBinContent(i+1))
        result.SetBinContent(i,value)
        result.SetBinError(i,error)
    return result
# done


def get_histo_increased_stat_error_with_equivalent_of_systematic_error(h,extraErrorFraction=0.10,debug=False):
    # adding a flat fraction of error say 10% on top of the statistical error
    new_h=h.Clone(h.GetName()+"_new_error")
    for i in xrange(new_h.GetNbinsX()+2):
        content=new_h.GetBinContent(i)
        error=new_h.GetBinError(i)
        errorExtra=content*extraErrorFraction
        new_error=add_in_quadrature(error,errorExtra)
        #new_error=0.0
        new_h.SetBinError(i,new_error)
    # done loop over bins
    if debug:
        getBinValues(h,doRescaleMeVtoGeV=False,debug=True)
    if debug:
        getBinValues(new_h,doRescaleMeVtoGeV=False,debug=True)
    # done
    return new_h
# done function

def getHistoNonZeroRange(histo,debug=False):
    if debug:
        print "Getting non-zero range for histogram of name",histo.GetName(),":"
    getBinValues(histo,significantDigits=2,doRescaleMeVtoGeV=False,debug=debug)
    minBinLowEdge=999999999
    maxHighBinEdge=-1
    nrNonZeroBins=0
    # loop over bins skipping underflow and overflow
    for i in xrange(1,histo.GetNbinsX()+1):
        if debug:
            print "bin i",
        binContent=histo.GetBinContent(i)
        if binContent<=0.0:
            continue
        nrNonZeroBins+=1
        binLowEdge=histo.GetBinLowEdge(i)
        binWidth=histo.GetBinWidth(i)
        binHighEdge=binLowEdge+binWidth
        if binLowEdge<minBinLowEdge:
            minBinLowEdge=binLowEdge
        if binHighEdge>maxHighBinEdge:
            maxHighBinEdge=binHighEdge
    nonZeroRange=[minBinLowEdge,maxHighBinEdge]
    if debug:
        print "result non-zero bin range",nonZeroRange,"with nrNonZeroBins",nrNonZeroBins
    return nonZeroRange,nrNonZeroBins
# done function

def getBinValues(histo,significantDigits=0,doRescaleMeVtoGeV=False,doUnderflow=False,doOverflow=False,debug=False):
    if debug:
        print "Printing bin values for histogram of name",histo.GetName(),":"
    list_value=[]
    list_error=[]
    list_line=[]
    list_binInfo=[]
    # loop over each bin and for each bin write the cross section on a different line
    for i in xrange(histo.GetNbinsX()+2):
        if doUnderflow==False and i==0:
            continue
        if doOverflow==False and i==histo.GetNbinsX()+1:
            continue
        binContent=histo.GetBinContent(i)
        binLowEdge=histo.GetBinLowEdge(i)
        if doRescaleMeVtoGeV:
            binLowEdge*=0.001 # MeV to GeV
        binWidth=histo.GetBinWidth(i)
        if doRescaleMeVtoGeV:
            binWidth*=0.001 # MeV to GeV
        binHighEdge=binLowEdge+binWidth
        binIntegral=binContent#*binWidth
        binError=histo.GetBinError(i)
        if binContent<=0:
            binRatio=0
        else:
            binRatio=ratio(binError,binContent)*100
        if significantDigits==0:
            line="bin %4.0f range [%6.0f,%6.0f] value %8.2f error %8.2f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        elif significantDigits==1:
            line="bin %4.0f range [%6.1f,%6.1f] value %8.2f error %8.2f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        elif significantDigits==2:
            line="bin %4.0f range [%6.2f,%6.2f] value %8.2f error %8.2f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        elif significantDigits==3:
            line="bin %4.0f range [%6.3f,%6.3f] value %8.3f error %8.2f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        elif significantDigits==4:
            line="bin %4.0f range [%6.2f,%6.2f] value %8.4f error %8.4f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        elif significantDigits==5:
            line="bin %4.0f range [%6.2f,%6.2f] value %10.8f error %10.8f (%4.2f%%)" % (i,binLowEdge,binHighEdge,binContent,binError,binRatio)
        else:
            print "number of significant digits is not known. Will ABORT!"
            assert(False)
        # done if
        if debug:
            print line
        list_line.append(line)
        binInfo=(binLowEdge,binHighEdge),(binContent,binError)
        list_binInfo.append(binInfo)
        #outputfile.write(line)
        #outputfile.write("\n")
        list_value.append(binIntegral)
        list_error.append(binError)
    # done loop over bins
    nparray_value=numpy.array(list_value)
    nparray_error=numpy.array(list_error)
    if debug:
        print "nparray_value",nparray_value
        print "nparray_error",nparray_error
    return (nparray_value,list_line,list_binInfo,nparray_error)
# done function

def getBinInfo(histo,doRescaleMeVtoGeV=False,debug=False):
    list_bin=[]
    list_content=[]
    # loop over each bin and for each bin write the cross section on a different line
    for i in xrange(histo.GetNbinsX()+2):
        binContent=histo.GetBinContent(i)
        binLowEdge=histo.GetBinLowEdge(i)
        if doRescaleMeVtoGeV:
            binLowEdge*=0.001 # MeV to GeV
        binWidth=histo.GetBinWidth(i)
        if doRescaleMeVtoGeV:
            binWidth*=0.001     # MeV to GeV
        binHighEdge=binLowEdge+binWidth
        binIntegral=binContent#*binWidth
        binError=histo.GetBinError(i)
        list_bin.append((binLowEdge,binHighEdge))
        list_content.append((binContent,binError))
    # done loop over bins
    return list_bin,list_content
# done function

def rescaleHistogramFromContentToDensity(histo,doRescaleMeVtoGeV=False,debug=False):
    # loop over each bin and divide bin content and error by the width of each bin
    # except underflow and overflow, for which there is an infinity to divide with
    for i in xrange(1,histo.GetNbinsX()+1):
        if debug:
            print "bin",i
        binContent=histo.GetBinContent(i)
        binError=histo.GetBinError(i)
        binWidth=histo.GetBinWidth(i)
        if doRescaleMeVtoGeV:
            binWidth*=0.001     # MeV to GeV
        if debug:
            print "binWidth",binWidth,"binContent",binContent,"binWidth",binWidth,"ratio(binContent,binWidth)",ratio(binContent,binWidth)
        binContentNew=ratio(binContent,binWidth)
        binErrorNew=ratio(binError,binWidth)
        histo.SetBinContent(i,binContentNew)
        histo.SetBinError(i,binErrorNew)
    # done for loop
    #return histo
# done function

# replace function with its value varied by the statistical variation
def get_histogram_with_its_statistical_variation(ho,factor,debug):
    h=ho.Clone()
    h.Reset()
    # now we have a histogram with the same properties, binning especially,
    # but all bin contents and errors set to zero
    # loop over all the bins 
    # including underflow (0) and overflow (h.GetNbinsX()+1)
    for i in xrange(0,h.GetNbinsX()+2):
        binValue=ho.GetBinContent(i)
        binError=ho.GetBinError(i)
        binValueNew=binValue+factor*binError
        binErrorNew=0 # would be strange error on the error variation, right?
        if debug:
            print "i",i,"v",binValue,"e",binError,"v new",binValueNew,"e new",binErrorNew
        h.SetBinContent(i,binValueNew)
        h.SetBinError(i,binErrorNew)
     # done loop over all the bins
    return h
# done function

def get_interpolated_graph_for_histo(h,debug):
    if debug:
        print "Start get_interpolated_graph_for_histo(h,debug)"
    xMin=20.0
    stepWidth=1.0
    nrSteps=650
    xList=[]
    yList=[]
    for i in xrange(nrSteps+1):
        #print i
        x=xMin+i*stepWidth
        y=h.Interpolate(x)
        if debug:
            print i, x, y
        xList.append(x)
        yList.append(y)
    # done loop over steps
    if False:
        print "xList",xList
        print "yList",yList
    xNumpyArray=numpy.array(xList)
    yNumpyArray=numpy.array(yList)
    result=TGraph(nrSteps,xNumpyArray,yNumpyArray)
    result.SetLineColor(h.GetLineColor())
    if debug:
        print "End  get_interpolated_graph_for_histo(h,debug)"
    return result
# done function


# for statistical error band
# code example: https://www.desy.de/~stanescu/my-tmp/plotUpDownSys.C
# its plot:https://www.desy.de/~stanescu/my-tmp/AFII/Nom-Up-Down-A500-tb050/jes1_h_ttbar_chi2_m_inc_res_mu.png
def overlayHistograms(list_tuple_h1D,fileName="overlay",extensions="pdf",option="histo",doValidationPlot=False,canvasname="canvasname",addHistogramInterpolate=False,addfitinfo=False,addMedianInFitInfo=False,significantDigits=("3","3","3","3"),min_value=-1,max_value=-1,YTitleOffset=0.45,doRatioPad=True,min_value_ratio=0,max_value_ratio=3,statTitle="MC. stat uncertainty",statColor=6,ratioTitle="Ratio each to one on top",plot_option="HIST E",plot_option_ratio="HIST",text_option=("#bf{#it{#bf{ATLAS} Simulation Internal}}?#bf{#sqrt{s}=13 TeV; Hinv analysis}?#bf{"+"category"+"}?#bf{"+"systematicStem"+"}",0.04,13,0.15,0.88,0.05),legend_info=[0.70,0.70,0.88,0.88,72,0.037,0],line_option=([0,0.5,0,0.5],2),debug=False):
    if debug:
        print "Start overlayHistograms(...)"
        print "option",option
        print "plot_option",plot_option
    # number of histograms we are overlaying
    num=len(list_tuple_h1D)
    ignorezero=False
    if debug:
        print "Start set_min_max_title_list_tuple_h1D()"
        for tuple_h1D in list_tuple_h1D:
            print "legend",tuple_h1D[1],"min",tuple_h1D[0].GetMinimum(),"max",tuple_h1D[0].GetMaximum()
    set_min_max_title_list_tuple_h1D(list_tuple_h1D,max_value,min_value,ignorezero,1.5,0.9,debug)
    if debug:
        print "End set_min_max_title_list_tuple_h1D()"
        for tuple_h1D in list_tuple_h1D:
            print "legend",tuple_h1D[1],"min",tuple_h1D[0].GetMinimum(),"max",tuple_h1D[0].GetMaximum()
    #
    gStyle.SetOptStat(0) 
    c_overlay=TCanvas("c","c",600,600)
    if doRatioPad:
        c_overlay=TCanvas("c","c",600,600)
        p_main=TPad("p_main","p_main",0,0.33,1,1)
        p_ratio=TPad("p_ratio","p_ratio",0,0,1,0.33)
    else:
        c_overlay=TCanvas("c","c",600,400)
        p_main=TPad("p_main","p_main",0,0.0,1,1)
        p_ratio=TPad("p_ratio","p_ratio",0,0,0,0.0)
    # done if
    p_main.Draw()
    p_ratio.Draw()
    p_main.cd()
    #

    if debug:
        print "Start Draw legend"
    # Draw the legend
    legend=get_legend(legend_info,debug)
    h_canvas=list_tuple_h1D[0][0].Clone()
    if debug:
        print "after h_canvas"
    h_canvas.Reset()
    if debug:
        print "after reset"
    h_canvas.Draw(plot_option)
    if debug:
        print "after draw canvas"
    if addfitinfo:
        if option=="histo":
            if addMedianInFitInfo==True:
                titleLegend="histo: median/mean/RMS/ratio"
            else:
                titleLegend="histo: mean/RMS/ratio"
        elif "Gauss" in option:
            if addMedianInFitInfo==True:
                titleLegend="Gauss: median/mean/sigma/ratio"
            else:
                titleLegend="Gauss: mean/sigma/ratio"
        elif "Bukin" in option:
            if addMedianInFitInfo==True:
                titleLegend="Bukin: median/peak/width/ratio"
            else:
                titleLegend="Bukin: peak/width/ratio"
        else:
            print "option",option,"not known in setting LegendTitle of addfitinfo is True. Will ABORT!!"
            assert(False)
        # done if option
        #legend.AddEntry(None,"#bf{"+titleLegend+"}","")
        legend.SetHeader("#bf{"+titleLegend+"}")
    # done if addfitinfo

    if debug:
        print "Done legend title, starting loop over list_tuple_h1D"

    if debug:
        print "A type(p_main)",type(p_main)
    list_g=[]
    if debug:
        print "B type(p_main)",type(p_main)
    # loop over list_tuple_h1D
    for i in range(num):
        if debug:
            print "i",i,list_tuple_h1D[i][0].GetName(),list_tuple_h1D[i][1]
        if debug:
            print "C","i",i,"type(p_main)",type(p_main)

        tuple_h1D=list_tuple_h1D[i]
        h1D=tuple_h1D[0]
        shortname=tuple_h1D[1]
        
        # set Y axis title offset
        #h1D.GetYaxis().SetTitleOffset(YTitleOffset)
        #h1D.SetTitleOffset(YTitleOffset,"Y");
        #h1D.SetTitleOffset(10.0,"Y");
        ##h1D.GetYaxis().SetLabelSize(0.001)
        #h1D.GetYaxis().SetTitleSize(0.20)
        #h1D.GetYaxis().SetTitleOffset(1.45)
        #h1D.GetYaxis().SetLabelOffset(1000)
        #h1D.GetXaxis().SetLabelSize(0.00)
        #h1D.GetYaxis().SetLabelSize(0.00)

        if debug:
            print "D","i",i,"type(p_main)",type(p_main)

        if option.find("histo")!=-1:
            if debug:
                print "B1 we want at the least the histo and maybe a fit too"
            if option=="histo":
                if debug:
                    print "B2 we want only the histo"
                h1D.Draw(plot_option+"SAME")
                result_fit=((h1D.GetMean(),0.0),(h1D.GetMaximum(),0.0),(h1D.GetMean(),0.0),(h1D.GetRMS(),0.0),(0.0,0.0),(0.0,0.0),(0.0,0.0))
            else:
                if debug: 
                    print "B3 we want both the histogram and the fit"
                temp=option.split("+")
                if debug:
                    print "temp",temp
                if len(temp)!=2:
                    print "ERROR, option",option,"should be histo+fit. As a side note, fit is known so far only for Gauss and Bukin. Will ABORT!"
                    assert(False)
                else:
                    # it means 
                    if debug:
                        print "B4 we want both the histogram"
                        print "plot_option",plot_option
                    h1D.Draw(plot_option+"SAME")
                    fit=temp[-1]
                    if debug:
                        print "fit",fit
                    #f,result_fit=fit_hist(h1D,fit,plot_option+"O",debug)
                    f,result_fit=fit_hist(h=h1D,fit=fit,addMedianInFitInfo=addMedianInFitInfo,plot_option=plot_option+"O",doValidationPlot=doValidationPlot,canvasname=canvasname+"_"+h1D.GetName(),debug=debug)
                    f.SetLineWidth(h1D.GetLineWidth())
                    f.Draw("SAME")
        else:
            if debug:
                print "B5 we want the fit without the histo"
            if debug:
                print "B5 start","i",i,"type(p_main)",type(p_main)
            # we have just a fit alone
            fit=option
            if debug:
                print "fit",fit
            #f,result_fit=fit_hist(h1D,fit,"",debug)
            plot_option="R"
            #f,result_fit=fit_hist(h1D,fit,plot_option+"O",debug)
            f,result_fit=fit_hist(h=h1D,fit=fit,addMedianInFitInfo=addMedianInFitInfo,plot_option=plot_option+"O",doValidationPlot=doValidationPlot,canvasname=canvasname+"_"+h1D.GetName(),debug=debug)
            if debug:
                print "B5 start","i",i,"type(p_main)",type(p_main)
            #f.Draw("SAME")
            #h1D.Draw(plot_option+"SAME")
            #result_fit=(0.0,0.0,0.0,0.0,0.0,0.0)
        # 

        if debug:
            print "E","i",i,"type(p_main)",type(p_main)

        # add the histogram interpolate if asked for
        if addHistogramInterpolate:
            print "i",i,"at add the histogram interpolate if asked for"
            list_g.append(get_interpolated_graph_for_histo(h1D,debug).Clone())
            list_g[i].Draw("same")

        if debug:
            print "F","i",i,"type(p_main)",type(p_main)


        #    
        legend_name="#bf{"+shortname+"}"
        # legend text median, peak, width, width/peak
        if addMedianInFitInfo==True:
            #legend_text="#bf{%-.1f/%-.1f/%-.1f/%-.3f}" % (result_fit[0][0],result_fit[2][0],result_fit[3][0],ratio(result_fit[3][0],result_fit[2][0]))
            #significantDigits=("3","3","3","3")
            if debug:
                print "tempString",tempString
            tempString="#bf{%-."+significantDigits[0]+"f/%-."+significantDigits[1]+"f/%-."+significantDigits[2]+"f/%-."+significantDigits[3]+"f}"
            legend_text= tempString % (result_fit[0][0],result_fit[2][0],result_fit[3][0],ratio(result_fit[3][0],result_fit[2][0]))
        else:
            tempString="#bf{%-."+significantDigits[1]+"f/%-."+significantDigits[2]+"f/%-."+significantDigits[3]+"f}"
            if debug:
                print "tempString",tempString
            legend_text=tempString % (result_fit[2][0],result_fit[3][0],ratio(result_fit[3][0],result_fit[2][0]))
        legend.AddEntry(h1D,legend_name,"f")
        if addfitinfo:
            legend.AddEntry(None,legend_text,"")
        legend.SetBorderSize(0)
        # add ATLAS
        # ex: setupTextOnPlot("#bf{#it{#bf{ATLAS } Simulation Internal}}",0.05,13,0.17,0.85,0.09)
        setupTextOnPlot(*text_option)
    # done loop over list_tuple_h1D
 
    if debug:
        print "type(p_main)",type(p_main)
       
    # add to the legend the statistical error on the first histogram
    # used as reference in the ratio
    # we will plot that only in the ratio plot
    hStat=list_tuple_h1D[0][0].Clone("hStat")
    hStat.SetFillColor(statColor)
    hStat.SetLineColor(statColor)
    hStat.SetFillStyle(1001)
    hStat.SetLineWidth(0)
    #legend.AddEntry(hStat,statTitle,"F")

    # legend is ready, we can draw it
    legend.Draw("SAME") 

    if debug:
        print "type(p_main)",type(p_main)
    p_main.Update()
    
    # line
    line_position=line_option[0]
    if debug:
        print "line_position",line_position
    line_color=line_option[1]
    if debug:
        print "line_color",line_color
    line=TLine(*line_position)
    line.SetLineColor(line_color)
    line.Draw("SAME")

    if debug:
        print "Ended plotting the upper pad with the main overlay"
        print "Start plotting the down pad with the ratio overlay"

    #c.Update()

    # going to the bottom pad with the ratio
    p_ratio.cd()

    #legend.Draw("SAME") 
    #h_canvas=list_tuple_h1D[0][0].Clone()
    #h_canvas.Reset()
    #h_canvas.Draw(plot_option)
    list_tuple_ratio_h1D=[]
    reference_h1D=list_tuple_h1D[0][0].Clone()
    if debug:
        print "num",num
    # loop over list_tuple_h1D
    for i in range(num):
        if debug:
            print "i",i,list_tuple_h1D[i][0].GetName(),list_tuple_h1D[i][1]
        #two lines below are standard ROOT, but statistical error is counted twice
        ratio_h1D=list_tuple_h1D[i][0].Clone()
        ratio_h1D.Divide(reference_h1D)
        getBinValues(ratio_h1D,debug=debug)
        # add ratio_h1D to list of histograms to overlay
        list_tuple_ratio_h1D.append([ratio_h1D,list_tuple_h1D[i][1]])
    # done loop over histograms

    #min_value_ratio=0.9
    #max_value_ratio=4.0
    ignorezero=True
    set_min_max_title_list_tuple_h1D(list_tuple_ratio_h1D,max_value_ratio,min_value_ratio,ignorezero,1.01,0.9,debug)
    if debug:
        print "min_value_ratio",min_value_ratio
        print "max_value_ratio",max_value_ratio



    # loop over the ratio histograms
    for i in range(num):
        ratio_h1D=list_tuple_ratio_h1D[i][0]
        if debug:
            print "i",i,"type(ratio_h1D)",type(ratio_h1D)
        #(my_nparray_value,my_list_line)=getBinValues(ratio_h1D,debug)
        if debug:
            print "plot_option",plot_option
        if i==0:
            #ratio_h1D.SetMinimum(0.95)
            #ratio_h1D.SetMaximum(1.05)
            ratio_h1D.GetYaxis().SetTitle(ratioTitle)
            ratio_h1D.GetYaxis().SetLabelSize(0.08)
            ratio_h1D.GetYaxis().SetTitleSize(0.10)
            ratio_h1D.GetYaxis().SetTitleOffset(0.45)
            # no need of an x axis label, as the same as from the pad above
            ratio_h1D.GetXaxis().SetTitle("")
            ratio_h1D.GetXaxis().SetLabelSize(0.08)
            # give the same color, style, etc as what we put in the legend
            #ratio_h1D.SetFillColor(statColor)
            #ratio_h1D.SetFillStyle(1001)
            ratio_h1D.SetLineWidth(2)
            ratio_h1D.SetMarkerStyle(0)
            #ratio_h1D.Draw(plot_option_ratio+" E4")
            ratio_h1D.Draw(plot_option_ratio)

        else:
            #if i==1:
            #    ratio_h1D.SetFillColor(statColor)
            #elif i==2:
            #    ratio_h1D.SetFillColor(0)  
            #ratio_h1D.SetFillStyle(1001)
            ratio_h1D.SetLineWidth(2)
            ratio_h1D.SetMarkerStyle(0)
            #ratio_h1D.Draw("E6 SAME") # stat errors on the ratios of systematics as curved shape
            #ratio_h1D.Draw("E1 SAME") # stat errors on the ratios of systematics as crosses
            #ratio_h1D.Draw("HIST SAME") # no errors but it draws the line also horizontally when the bins have zero value at start and vertically for the first non zero bin
            ratio_h1D.Draw(plot_option_ratio+" SAME")
            #ratio_h1D.Draw("HIST E3")
            None

    # done loop over ratio histogram

    c_overlay.Update()

    # now ready to save the canvas
    # if path does not have / as the last character, add one
    for extension in extensions.split(","):
        c_overlay.Print(fileName+"_"+option+"."+extension)
    if debug:
        print "End overlayHistograms(...)"
# done function

# plot just one histogram
def plotGraph(g,plot_option,filePath,fileName,extensions):
    # plot one graph, y function of x for N entries
    c=TCanvas("canvas","canvas",400,300)
    g.Draw(plot_option) # AP 
    # if path does not have / as the last character, add one
    if filePath[len(filePath):]!="/":
        filePath+="/"
    # compute the name
    if fileName=="":
        fileName=filePath+h.GetName()
    else:
        fileName=filePath+fileName
    # save the canvas in files with what extensions we want
    for extension in extensions.split(","):
        c.Print(fileName+"."+extension)
    # ended for over extensions
    return None
# ended function

# plot just one histogram
def plotMultiGraph(list_graphs,canvas_size,legend_position,factor_maximum,plot_option,
                   xaxis,
                   filePath,fileName,extensions):
    # plot one graph, y function of x for N entries
    # ROOT
    gStyle.SetTitle("")
    # canvas
    c=TCanvas("canvas","canvas",canvas_size[0],canvas_size[1])
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetBorderSize(1)
    c.SetFrameBorderMode(0)
    c.SetFrameBorderMode(0)
    c.SetTitle("")
    c.SetGrid()
    #
    multigraph=TMultiGraph()
    # compute minimum and maximum values
    min=+999999.0
    max=-999999.0
    # loop over the lists of graphs
    # the first element of the list is the graph
    # the second element of the list is its legend name
    for graph in list_graphs:
        multigraph.Add(graph[0])
        if graph[0].GetMaximum()>max:
            max=graph[0].GetMaximum()
        if graph[0].GetMinimum()<min:
            min=graph[0].GetMinimum()
    # set these values to the multigraph
    # print "min=",min,"max=",max
    # set it to zero for now, can se to min in the future
    multigraph.SetMinimum(0)
    # multiply with something to leave space for legend
    multigraph.SetMaximum(max*factor_maximum) 

    # options to draw the multigraph
    # A - axis
    # P - use current marker
    # * - use * as marker
    # L - draws a line between points
    # C - draws a smooth line (curve) between points
    # B - draws a bar chart
    # X+ - draws the x axis on the top (instead of down)
    # Y+ - draws the y axis on the right (instead of left)
    # 1 - starts from the correct value (instead of from zero) for bar chart
    # 
    # plot the graph
    multigraph.Draw(plot_option) # APC
    # set the title of x axis
    multigraph.GetXaxis().SetTitle(xaxis[0])
    # remove the numbers for the days from the x axis
    multigraph.GetXaxis().SetLabelSize(xaxis[1])
 
    multigraph.GetXaxis().SetTimeDisplay(xaxis[2])
    multigraph.GetXaxis().SetNdivisions(xaxis[3]) 
    multigraph.GetXaxis().SetTimeFormat(xaxis[4]) # ("%Y-%m-%d %H:%M")
    multigraph.GetXaxis().SetTimeOffset(0,"gmt") 
    multigraph.GetXaxis().LabelsOption(">")
    c.Update()

    # create the legend
    legend=TLegend(*legend_position)
    # add the text for each graph
    for graph in list_graphs:
        legend.AddEntry(graph[0],graph[1])
    # set the color of the legend
    legend.SetFillColor(TColor.kWhite)
    # draw the legend
    legend.Draw()

    # try to draw a vertical line for each month since the reference date
    lines=[]
    for i in xrange(13):
        lines.append(TLine(0*i,0,0*i,max))
    for line in lines:
        line.Draw() 

    # if path does not have / as the last character, add one
    if filePath[len(filePath):]!="/":
        filePath+="/"
    # compute the name
    if fileName=="":
        fileName=filePath+h.GetName()
    else:
        fileName=filePath+fileName
    # save the canvas in files with what extensions we want
    for extension in extensions.split(","):
        c.Print(fileName+"."+extension)
    # ended for over extensions
    return None
# ended function

def overlapHistograms(hist_1, hist_2, do_print):
    # get the standard deviation and mean of the 1st histogram
    hist_1_rms=hist_1.GetRMS()
    hist_1_mean=hist_1.GetMean()
    
    # get the range of 2 sigma around the mean of the 1st histogram
    range_i=hist_1_mean-hist_1_rms*2
    range_f=hist_1_mean+hist_1_rms*2
    
    # find the bins that correspond to the 2sigma range
    bin_i=hist_1.FindBin(range_i)
    bin_f=hist_1.FindBin(range_f)
    
    # calculate the overlap of Histogram 2 with Histogram 1 as a percentage
    overlap=hist_2.Integral(bin_i,bin_f)/hist_2.Integral()
    if do_print==True:
        overlap_percentage=overlap*100
        print "The overlap  of Histrogram 2 with Histrogram 1 is:", overlap_percentage,"%."
    return None
# ended function

def overlayDiffVars(histoList, legend_position, filePath, fileName, bin_width, Extensions, XLabel, YLabel, plot_text, hist_range, doFit, fit, debug):
    '''
    This function will overlay the different variables with or without a fit
    '''

    num = len(histoList)
    gROOT.SetBatch(1)
    c = TCanvas('c','c', 800, 600)
    gStyle.SetOptStat(0)
    c.SetTickx(1)
    c.SetTicky(1)
    c.Update()
    
    for i in xrange(num):
        sigColour = histoList[i][1]
        histogram = rebin(histoList[i][0], float(bin_width))
        histogram.GetXaxis().SetRangeUser(float(hist_range[0]), float(hist_range[1]))
        histogram.SetLineWidth(1)
        histogram.SetLineColor(int(sigColour))
        if i == 0:
            histogram.Draw()
            histogram.SetTitle("")
            histogram.GetXaxis().SetTitle(XLabel)
            histogram.GetXaxis().SetTitleSize(0.045)
            histogram.GetXaxis().SetTitleOffset(0.9)
            histogram.GetYaxis().SetTitle(YLabel)
            histogram.GetYaxis().SetTitleSize(0.045)
            histogram.GetYaxis().SetTitleOffset(0.9)
            yMax = histogram.GetMaximum() * 1.25
            histogram.SetMaximum(yMax)
            histogram.SetMinimum(0.01)
        else:
            histogram.Draw("histsame")
       
        #if doFit and fit == "BUKIN" and 'Gen' not in histoList[i][2]:
        if doFit and fit == "BUKIN":
            plotMean   = histogram.GetMean()
            plotRMS    = histogram.GetRMS()
            plotRes    = float(plotRMS)/float(plotMean)
            plotHeight = histogram.GetMaximum()

            function = TF1("bukin", Bukin(), 80, 160, 6)
            function.SetParName(0, "height")
            function.SetParName(1, "mean")
            function.SetParName(2,"width")
            function.SetParName(3,"asymmetry")
            function.SetParName(4,"size of lower tail")
            function.SetParName(5,"size of higher tail")
            function.SetParameter(0, float(plotHeight))
            function.SetParameter(1, float(plotMean))
            function.SetParameter(2, float(plotRMS))
            function.SetParameter(3, -0.2 )
            function.SetParameter(4, 0.2)
            function.SetParameter(5, 0.001)
            histogram.Fit("bukin", "Q", "histsame")
            fittedHist = histogram.GetFunction("bukin")
            fittedHist.SetLineColor(int(sigColour))
            fittedHist.Draw("histsame")
    

    text_length = len(plot_text)
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(0.035)
    t.SetTextAlign(13)
    y_value = 0.86
    for item in xrange(text_length):
        t.DrawLatex(0.15, y_value, plot_text[item])
        y_value -= 0.06

    l = TLegend(*legend_position)
    SetOwnership(l,0)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.SetTextSize(0.035)
    for i in xrange(num):
        l.AddEntry(histoList[i][0], histoList[i][1], 'l')

    l.Draw()
   
    for type in Extensions.split(","):
        c.Print(filePath+fileName+"."+type)

def overlaySigBkg(histoList, legend_position, filePath, fileName, bin_width, Extensions, XLabel, YLabel, bkgColour, plot_text, hist_range, debug):

    '''
    This function will overlay the total signal and total background on top of one another.

    This is useful for shape comparisons
    '''
    num = len(histoList)
    signalList = TList()
    bkgList    = TList()
    for i in xrange(num):
        sigColour = histoList[i][1]
        histogram = rebin(histoList[i][0], float(bin_width))
        histogram.GetXaxis().SetRangeUser(float(hist_range[0]), float(hist_range[1]))
        if histoList[i][4] == "SIGNAL":
            signalList.Add(histogram)
        elif histoList[i][4] == "BACKGROUND":
            bkgList.Add(histogram)
    
    mergeSignalHist = TH1F(histogram.Clone("mergeSignalList"))
    mergeSignalHist.Merge(signalList)
    mergeSignalHist.SetLineWidth(1)
    mergeSignalHist.SetLineColor(int(sigColour))
    mergeBkgHist    = TH1F(histogram.Clone("mergeBkgList"))
    mergeBkgHist.Merge(bkgList)
    mergeBkgHist.SetLineWidth(1)
    mergeBkgHist.SetLineColor(int(bkgColour))

    gROOT.SetBatch(1)
    c = TCanvas('c','c', 800, 600)
    gStyle.SetOptStat(0)
    mergeBkgHist.SetTitle("")
    c.SetTicky(1)
    c.SetTickx(1)
    c.Update()
    
    yMax_sig = mergeSignalHist.GetMaximum()
    yMax_bkg = mergeBkgHist.GetMaximum()

    mergeSignalHist.Scale(1/yMax_sig)
    mergeBkgHist.Scale(1/yMax_bkg)
    
    mergeBkgHist.Draw()
    mergeSignalHist.Draw("histsame")
    
    mergeBkgHist.GetXaxis().SetTitle(XLabel)
    mergeBkgHist.GetXaxis().SetTitleSize(0.045)
    mergeBkgHist.GetXaxis().SetTitleOffset(0.9)
    mergeBkgHist.GetYaxis().SetTitle(YLabel)
    mergeBkgHist.GetYaxis().SetTitleSize(0.045)
    mergeBkgHist.GetYaxis().SetTitleOffset(0.9)
    yMax = mergeBkgHist.GetMaximum() * 1.25
    mergeBkgHist.SetMaximum(yMax)
    mergeBkgHist.SetMinimum(0.01)

    l = TLegend(*legend_position)
    SetOwnership(l,0)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.SetTextSize(0.04)
    l.AddEntry(mergeSignalHist, "WH125 Signal", "l")
    l.AddEntry(mergeBkgHist, "ttbar Background", "l")

    l.Draw()

    text_length = len(plot_text)
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(0.030)
    t.SetTextAlign(13)
    y_value = 0.83
    for item in xrange(text_length):
        t.DrawLatex(0.15, y_value, plot_text[item])
        y_value -= 0.06
        
    for type in Extensions.split(","):
        c.Print(filePath+fileName+"."+type)


def StackHistograms(histoList,legend_position,filePath,fileName,Extensions,XLabel,YLabel,plot_text,bin_width,hist_range,title,save_string,doBlinding,blindingTuple,ratioPlotVars,debug):

    '''PURPOSE: Function to stack any number of histograms and save
                under the extension given
    '''
    if debug:
        print "Starting Stacking..."

    # Check the number of histograms stacking
    num = len(histoList)

    overlay_list = []
    data_list    = []
    Stack = THStack(fileName, "")
    #Stack = THStack(fileName, title)
    for i in xrange(num):
        fullPath = histoList[i][5]
        histogram = rebin(histoList[i][0], int(bin_width))
        histogram.Scale(float(histoList[i][3]))
        histogram.SetLineWidth(1)
        histogram.SetLineColor(1)
        if histoList[i][1] == "Data" and doBlinding and blindingTuple[0] in histoList[i][5]:
            histogram =  blinding(histogram, blindingTuple[1], blindingTuple[2])
        if histoList[i][4] == "STACK":
            histogram.SetFillColor(int(histoList[i][1]))
            Stack.Add(histogram)
        elif histoList[i][4] == "OVERLAY" and histoList[i][2] != "Data":
            histogram.SetLineColor(int(histoList[i][1]))
            overlay_list.append(histogram)
        elif histoList[i][4] == "OVERLAY" and histoList[i][2] == "Data":
            histogram.SetMarkerStyle(8)
            histogram.SetMarkerColor(1)
            data_list.append(histogram)
        else:
            print "\n%s Option not available\n" % (histoList[i][4])
            sys.exit(1)

    # Run Root in batch mode with no canvas displayed
    gROOT.SetBatch(1)
    c = TCanvas('c','c', 800, 600)
    if ratioPlotVars is not None:
        mainPad  = TPad("mainPad","mainPad", 0,0.30,1,1)
        ratioPad = TPad("ratioPad","ratioPad",0,0,1,0.30)
        mainPad.Draw()
        ratioPad.Draw()
        mainPad.SetTopMargin(0.05)
        mainPad.SetBottomMargin(0.02)
        ratioPad.SetTopMargin(0)
        ratioPad.SetBottomMargin(0.3)
        mainPad.cd()
        mainPad.SetTicks(1)
        mainPad.Update()

    Stack.Draw()
    over_hist = len(overlay_list)
    for i in xrange(over_hist):
        overlay_list[i].Draw("histsame")

    data_size = len(data_list)
    for i in xrange(data_size):
        data_list[i].Draw("epsame")
    
    # Setting the axis ranges, we want to have space at the top of the canvas for 
    # text and legends. Also we want the axis labels to not overlap the values on
    # the axis
    print hist_range
    Stack.GetXaxis().SetRangeUser(int(hist_range[0]), int(hist_range[1]))
    if ratioPlotVars is not None:
        Stack.GetXaxis().SetTitle("")
        Stack.GetXaxis().SetTitleOffset(0)
        Stack.GetXaxis().SetLabelOffset(999)
        Stack.GetXaxis().SetLabelSize(0)
    else:
        Stack.GetXaxis().SetTitle(XLabel)
        Stack.GetXaxis().SetTitleOffset(1.2)
    
    Stack.GetYaxis().SetTitle(YLabel)
    Stack.GetYaxis().SetTitleOffset(1.4)
    Stack.SetTitle("")
    yMax = Stack.GetMaximum()*1.25
    Stack.SetMaximum(yMax)
    Stack.SetMinimum(0.01)
    
    # Some ATLAS Style, setting ticks all round the plot
    c.SetTicky(1)
    c.SetTickx(1)
    c.Update()

    # Setting legend positions and adding the correct values 
    l = TLegend(*legend_position)
    SetOwnership( l, 0 )
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.SetTextSize(0.03)
    for i in reversed(xrange(num)):
        if histoList[i][2] == "Data":
            l.AddEntry(histoList[i][0],histoList[i][2],"p")
        else:
            l.AddEntry(histoList[i][0],histoList[i][2],"f")
    
    l.Draw()
   
    # Add some text to the plot
    if plot_text:
        if debug:
            print "DEBUG: Adding text: %s to plot" % (plot_text)
        text_length = len(plot_text) 
        t = TLatex()
        t.SetNDC()
        t.SetTextSize(0.044)
        t.SetTextAlign(13)
        y_value = 0.91
        for item in xrange(text_length):
            t.DrawLatex(0.15, float(y_value), plot_text[item])
            y_value = y_value - 0.06
    
    if ratioPlotVars is not None:
        ratioPad.cd()
        ratioPad.SetTicks(1)
        ratioPad.Update()
        sigList  = TList()
        bkgList  = TList()
        mcList   = TList()
        dataList = TList()
        for i in xrange(num):
            histogramList = rebin(histoList[i][0], int(bin_width))
            histogramList.GetXaxis().SetRangeUser(int(hist_range[0]), int(hist_range[1]))
            if histoList[i][6] == "SIGNAL":
                sigList.Add(histogramList)
                mcList.Add(histogramList)
            elif histoList[i][6] == "BACKGROUND":
                bkgList.Add(histogramList)
                mcList.Add(histogramList)
            elif histoList[i][6] == "DATA":
                dataList.Add(histogramList)
            elif histoList[i][6] == "OVERLAY":
                pass
            else:
                sys.exit(1)

        mergeSigHist  = TH1F(histogramList.Clone("mergeSigHist"))
        mergeSigHist.Merge(sigList)
        mergeBkgHist  = TH1F(histogramList.Clone("mergeBkgHist"))
        mergeBkgHist.Merge(bkgList)
        mergeMCHist   = TH1F(histogramList.Clone("mergeMCHist"))
        mergeMCHist.Merge(mcList)
        mergeDataHist = TH1F(histogramList.Clone("mergeDataHist"))
        mergeDataHist.Merge(dataList)
        if ratioPlotVars == "SIGNAL/BACKGROUND":
            histoSigBkg = getRatio(mergeMCHist, mergeBkgHist, doBlinding, blindingTuple, fullPath)
            histoSigBkg.Draw('ep')
            histoSigBkg.GetXaxis().SetTitle(XLabel)
            histoSigBkg.GetXaxis().SetTitleSize(0.08)
            histoSigBkg.GetXaxis().SetTitleOffset(1)
            histoSigBkg.GetXaxis().SetLabelSize(0.08)
            histoSigBkg.GetYaxis().SetTitle("Sig+Bkg/Bkg")
            histoSigBkg.GetYaxis().SetTitleSize(0.08)
            histoSigBkg.GetYaxis().SetLabelSize(0.08)
            histoSigBkg.GetYaxis().SetTitleOffset(0.45)
            ATLASStyle(histoSigBkg)
        elif ratioPlotVars == "DATA/MC":
            histoDataMC = getRatio(mergeDataHist, mergeBkgHist, doBlinding, blindingTuple, fullPath)
            histoDataMC.Draw('ep')
            histoDataMC.GetXaxis().SetTitle(XLabel)
            histoDataMC.GetXaxis().SetTitleSize(0.08)
            histoDataMC.GetXaxis().SetTitleOffset(1)
            histoDataMC.GetXaxis().SetLabelSize(0.08)
            histoDataMC.GetYaxis().SetTitle("Data/MC")
            histoDataMC.GetYaxis().SetTitleSize(0.08)
            histoDataMC.GetYaxis().SetLabelSize(0.08)
            histoDataMC.GetYaxis().SetTitleOffset(0.45)
            ATLASStyle(histoDataMC)
            
    # Save the plots in a range of formats
    Name = save_string + fileName
    if debug:
        print "DEBUG:The Name of the File: %s" % (Name)
    for type in Extensions.split(","):
        c.Print(filePath+"/"+Name+"."+type)
# ended function

def rebin(histogram, bin_width):

    '''PURPOSE: Function which takes in a histogram and scales it by a factor '''

    xmax  = histogram.GetXaxis().GetXmax()
    xmin  = histogram.GetXaxis().GetXmin()
    nbins = histogram.GetXaxis().GetNbins()

    width = math.fabs(xmax - xmin) / (nbins)
    factor = 0
    if width:
        factor = float(bin_width) / width
    
    if factor >= 1 or not bin_width:
        return histogram.Rebin(int(factor))
    else:
        return histogram
# ended function

def sensitivityCalc(HistoInfo,title,bin_width,debug):

    # Have to set Global values since we are altering them outside a function.
    # Python requires we do this
    sigNum = 0
    sigErr = 0
    bkgNum = 0
    bkgErr = 0
    totBkgErr = 0
    totSigErr = 0
    totSen = 0
    totSig = 0
    totBkg = 0
    totErr = 0

    num = len(HistoInfo) 
    for i in xrange(num):
         histogram = HistoInfo[i][0]
         process   = HistoInfo[i][1]
         Entries   = histogram.GetXaxis().GetNbins()
    
    for bin in xrange(1,Entries,1):
        # Resetting all the values to zero at the start of the loop
        sigNum = 0
        sigErr = 0
        bkgNum = 0
        bkgErr = 0
        totSig = 0
        totBkg = 0
        totErr = 0
        for j in xrange(num):
            if HistoInfo[j][2] == "SIGNAL":
                histogram = rebin(HistoInfo[j][0],bin_width)
                sigNum = histogram.GetBinContent(bin)
                sigErr = histogram.GetBinError(bin)
                if debug:
                    print"DEBUG: sigNum: %s \n SigErr: %s\n" % (sigNum, sigErr)
            elif HistoInfo[j][2] == "BACKGROUND":
                histogram = rebin(HistoInfo[j][0],bin_width)
                bkgNum += histogram.GetBinContent(bin)
                bkgErr += histogram.GetBinError(bin)
                if debug:
                    print "DEBUG: bkgNum: %s \n bkgErr: %s \n" % (bkgNum, bkgErr)
            elif HistoInfo[j][2] == "OVERLAY":
                pass
            else:
                print "No Signal/Background info given\n %s not a correct value" % (HistoInfo[j][2])
            totBkgErr += bkgErr * bkgErr
            totSigErr += sigErr * sigErr
            if debug:
                print "DEBUG: totBkgErr: %s \n totSigErr: %s \n" % (totBkgErr, totSigErr)

        if bkgNum > 0:
            sen = sigNum/(math.sqrt(bkgNum))
            sen_sqrd = sen * sen
            totSen += sen_sqrd
            if debug:
                print "DEBUG: sen: %s \n sen_sqrd: %s \n totSen: %s \n" % (sen, sen_sqrd, totSen)

        if bkgNum > 0 and sigNum > 0:
            senErr = sen * sen * math.sqrt(((2 * sigErr/sigNum)*(2*sigErr/sigNum)) + ((bkgErr/bkgNum)*(bkgErr/bkgNum)))
            totErr += senErr * senErr
    
    sensitivity = math.sqrt(totSen)
    if debug:
        print "DEBUG: SENSITIVITY: %s\n" % (sensitivity)
    
    return sensitivity
# ended function

def basicSensCalc(HistoInfo, title):

    global totSig
    totSig = 0
    global totBkg
    totBkg = 0

    num = len(HistoInfo)
    for i in xrange(num):
        Xmin = HistoInfo[i][0].GetXaxis().GetXmin()
        Xmax = HistoInfo[i][0].GetXaxis().GetXmax()
        if HistoInfo[i][2] == "SIGNAL":
            totSig += HistoInfo[i][0].Integral(int(Xmin),int(Xmax))
        elif HistoInfo[i][2] == "BACKGROUND":
            totBkg += HistoInfo[i][0].Integral(int(Xmin),int(Xmax))
        else:
            print "No Signal/Background info given\n %s not a correct value" % (HistoInfo[j][2])
    
    basicSen = totSig/math.sqrt(totBkg)
    
    return basicSen
# ended function

def getStackStats(HistoInfo, title, BinWidth, Fit, stat, histoLocation, Range, debug):

    num = len(HistoInfo)
    List = TList()
    for i in xrange(num):
        if "crea" in histoLocation:
            integral = HistoInfo[i][0].Integral()
            entries  = HistoInfo[i][0].GetEntries()
            return integral/entries

        histogram = rebin(HistoInfo[i][0], float(BinWidth))
        histogram.GetXaxis().SetRangeUser(float(Range[0]), float(Range[1]))
        if HistoInfo[i][1] == "STACK" and HistoInfo[i][2] == "SIGNAL":
            List.Add(histogram)
        else:
            pass
    
    mergeHist = TH1F(histogram.Clone("mergeHist"))
    mergeHist.Merge(List)
    gROOT.SetBatch(1)
    c = TCanvas('c','c', 696, 472)
    mergeHist.Draw()
    
    if Fit == "NONE":
        if stat == "mean":
            mean = mergeHist.GetMean()
            return mean

        elif stat == "rms":
            rms = mergeHist.GetRMS()
            return rms

        elif stat == "resolution":
            mean = mergeHist.GetMean()
            rms  = mergeHist.GetRMS()
            resolution = rms/mean
            return resolution

        else:
            print "\n Unknown stat variable..."
            exit()
    
    elif Fit == "GAUSS":

        mergeHist.Fit("gaus","Q","")
        fittedHist = mergeHist.GetFunction("gaus")
        fittedHist.Draw("SAME")
        if debug:
            c.Print("resolution/plots/"+title+"_GAUS.pdf")
        
        if stat == "mean":
            mean = fittedHist.GetParameter(1)
            return mean
        
        elif stat == "rms":
            rms = fittedHist.GetParameter(2)
            return rms
        
        elif stat == "resolution":
            mean = fittedHist.GetParameter(1)
            rms  = fittedHist.GetParameter(2)
            resolution = rms/mean
            return resolution
        
        else:
            print "\nUnknown stat variable..."
            exit()
    
    elif Fit == "BUKIN":
        plot_mean = mergeHist.GetMean()
        plot_height = mergeHist.GetMaximum()
        plot_RMS = mergeHist.GetRMS()
        plot_width = float(plot_mean)/float(plot_RMS)

        function = TF1("bukin", Bukin(), 80, 160, 6)
        function.SetParName(0, "height")
        function.SetParName(1, "mean")
        function.SetParName(2,"width")
        function.SetParName(3,"asymmetry")
        function.SetParName(4,"size of lower tail")
        function.SetParName(5,"size of higher tail")
        function.SetParameter(0, float(plot_height))
        function.SetParameter(1, float(plot_mean))
        function.SetParameter(2, float(plot_RMS))
        function.SetParameter(3, -0.2 )
        function.SetParameter(4, 0.2)
        function.SetParameter(5, 0.001)
        mergeHist.Fit("bukin", "Q", "")
        fittedHist = mergeHist.GetFunction("bukin")
        fittedHist.Draw("SAME")
        if debug:
            c.Print("resolution/plots/"+title+"_BUKIN.pdf")
   
        if stat == "mean":
            mean = fittedHist.GetParameter(1)
            return mean

        elif stat == "rms":
            rms = fittedHist.GetParameter(2)
            return rms

        elif stat == "resolution":
            mean = fittedHist.GetParameter(1)
            rms  = fittedHist.GetParameter(2)
            resolution = rms/mean
            return resolution
    
    else:
        print "\nUnknown fit: %s" % (Fit)
        exit()
# ended function

def blinding(hist, lowRange, highRange):
    
    Entries = hist.GetNbinsX() + 2
    for i in xrange(0, Entries, 1):
        if hist.GetBinLowEdge(i) >= int(lowRange) and hist.GetBinLowEdge(i) <= int(highRange):
            hist.SetBinContent(i,0)
            hist.SetBinContent(i,0)

    return hist
# ended function

def getRatio(histNum, histDenom, doBlinding, blindingVar, fullPath):
    
    histRatio = TH1F(histNum.Clone("histRatio"))
    histRatio.Reset()

    bins = histRatio.GetNbinsX()
    for bin in xrange(1, bins, 1):
        nNum   = histNum.GetBinContent(bin)
        eNum   = histNum.GetBinError(bin)
        nDenom = histDenom.GetBinContent(bin)

        if nNum > 1e-6 and eNum > 1e-6 and nDenom > 1e-6:
            nRatio = (nNum - nDenom)/nDenom
            eRatio = eNum/nDenom
            if histRatio.GetBinLowEdge(bin) >= int(blindingVar[1]) and histRatio.GetBinLowEdge(bin) <= int(blindingVar[2]) and doBlinding == 1 and blindingVar[0] in fullPath:
                histRatio.SetBinContent(bin, 0)
                histRatio.SetBinError(bin, 0)
            else:
                histRatio.SetBinContent(bin, nRatio)
                histRatio.SetBinError(bin, eRatio)
    
    histRatio.SetLineColor(1)
    histRatio.SetMarkerStyle(8)
    return histRatio
# ended function

def ATLASStyle(histo):

    gStyle.SetOptStat(0)
    histo.SetTitle("")
# ended function

def createMeanRMS2DPlot(t_PlotInfo, l_plotDimensions, axisLabels, legend_position, t_plotText, s_Save, l_fileType):

    len_PlotInfo = len(t_PlotInfo)
    
    x1 = float(l_plotDimensions[0])
    x2 = float(l_plotDimensions[1])
    y1 = float(l_plotDimensions[2])
    y2 = float(l_plotDimensions[3])

    DHist_EM   = TH2D("DHist_EM",     "",1000,x1,x2,1000,y1,y2)
    DHist_JES  = TH2D("DHist_JES",     "",1000,x1,x2,1000,y1,y2)
    DHist_GSC  = TH2D("DHist_GSC",     "",1000,x1,x2,1000,y1,y2)
    DHist_Mu   = TH2D("DHist_Mu",     "",1000,x1,x2,1000,y1,y2)
    DHist_Pt   = TH2D("DHist_Pt",     "",1000,x1,x2,1000,y1,y2)
    DHistNN    = TH2D("DHistNN",   "",1000,x1,x2,1000,y1,y2)
    DHistTruth = TH2D("DHistTruth","",1000,x1,x2,1000,y1,y2)
    for i in xrange(len_PlotInfo):
        if str(t_PlotInfo[i][0]) == 'EM':
            DHist_EM.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHist_EM.SetMarkerStyle(8)
            DHist_EM.SetMarkerColor(632)
        elif str(t_PlotInfo[i][0]) == 'EM+JES':
            DHist_JES.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHist_JES.SetMarkerStyle(8)
            DHist_JES.SetMarkerColor(883)
        elif str(t_PlotInfo[i][0]) == 'EM+JES+GSC':
            DHist_GSC.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHist_GSC.SetMarkerStyle(8)
            DHist_GSC.SetMarkerColor(801)
        elif str(t_PlotInfo[i][0]) == 'EM+JES+GSC+Mu':
            DHist_Mu.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHist_Mu.SetMarkerStyle(8)
            DHist_Mu.SetMarkerColor(868)
        elif str(t_PlotInfo[i][0]) == 'EM+JES+GSC+Mu+pT' or str(t_PlotInfo[i][0]) == 'reco':
            DHist_Pt.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHist_Pt.SetMarkerStyle(8)
            DHist_Pt.SetMarkerColor(824)
        elif str(t_PlotInfo[i][0]).isdigit():
            print "here"
            DHistNN.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHistNN.SetMarkerStyle(8)
            DHistNN.SetMarkerColor(862)
        elif 'truth' in str(t_PlotInfo[i][0]) or 'Truth' in str(t_PlotInfo):
            DHistTruth.Fill(float(t_PlotInfo[i][1]),float(t_PlotInfo[i][2]))
            DHistTruth.SetMarkerStyle(29)
            DHistTruth.SetMarkerColor(616)
            DHistTruth.SetMarkerSize(2.5)
    gROOT.SetBatch(1)
    c = TCanvas('c','c',800,600)
    c.SetGridx()
    c.SetGridy()
    c.SetTickx()
    c.SetTicky()
    gStyle.SetOptStat(0)
    
    DHist_EM.GetXaxis().SetTitle(axisLabels[0])
    DHist_EM.GetXaxis().SetTitleSize(0.035)
    DHist_EM.GetXaxis().SetTitleOffset(1)
    DHist_EM.GetXaxis().SetLabelSize(0.035)
    DHist_EM.GetYaxis().SetTitle(axisLabels[1])
    DHist_EM.GetYaxis().SetTitleSize(0.035)
    DHist_EM.GetYaxis().SetTitleOffset(1)
    DHist_EM.GetYaxis().SetLabelSize(0.035)
    DHist_EM.Draw('p')
    DHist_JES.Draw('same p')
    DHist_GSC.Draw('same p')
    DHist_Mu.Draw('same p')
    DHist_Pt.Draw('same p')
    DHistNN.Draw('same p')
    DHistTruth.Draw('same p')

    ATLASStyle(DHist_EM)

    l = TLegend(float(legend_position[0]),float(legend_position[1]),float(legend_position[2]),float(legend_position[3]))
    SetOwnership(l,0)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.SetTextSize(0.035)
    l.AddEntry(DHist_EM,   "EM", 'p')
    l.AddEntry(DHist_JES,  "EM+JES", 'p')
    l.AddEntry(DHist_GSC,  "EM+JES+GSC", 'p')
    l.AddEntry(DHist_Mu,   "EM+JES+GSC+Mu", 'p')
    #l.AddEntry(DHist_Pt,   "Reconstructed Level", 'p')
    l.AddEntry(DHist_Pt,   "EM+JES+GSC+Mu+Pt", 'p')
    l.AddEntry(DHistNN,    "Neural Networks", "p")
    l.AddEntry(DHistTruth, "Generator Level", "p")
    l.Draw()

    len_plotText = len(t_plotText)
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(0.035)
    t.SetTextAlign(13)
    y_value = 0.40
    for item in xrange(len_plotText):
        t.DrawLatex(0.13, float(y_value), t_plotText[item])
        y_value -= 0.06

    c.Update()

    saveName = 'resolution/plots/2D/' + s_Save
    for type in l_fileType.split(','):
        c.Print(saveName + '.' + type)

def create2DProfile(l_histoInfo):

    ##
    ## 1. Loop over the histoList
    ## 2. Save the 't' to gen level list
    ## 3. Save the rest to non 't' list
    ## 4. Loop over the contents of non 't' list
    ## 5. For each item in non 't' do the calculation needed 
    ## 6. Create a 2D Plot with correct dimensons
    ## 7. Fill the 2D plot with the calculatd value and the 't' value
    ## 8. Add the plot aesthetics
    ## 9. Save the file as required!
    ##

    len_HistoInfo = len(l_histoInfo)
    l_nonTruth = []
    for i in range(len_HistoInfo):
        if l_histoInfo[i][4] == "t":
            h_truth = l_histoInfo[i][0]
        else:
            l_nonTruth.append(l_histoInfo[i][0])
    len_nonTruth = len(l_nonTruth)
    truthXMax = h_truth.GetXaxis().GetXmax()
    truthXMin = h_truth.GetXaxis().GetXmin()
    gROOT.SetBatch(1)
    c = TCanvas('c','c',800,600)
    c.SetGridx()
    c.SetGridy()
    c.SetTickx()
    c.SetTicky()
    gStyle.SetOptStat(0)
    for i in range(len_nonTruth):
        print i


#ex: setupTextOnPlot("#it{#bf{ATLAS} Simulation Internal}",0.05, 13,0.13,0.91,0.09)
def setupTextOnPlot(plotText, t_textSize, t_alignment, t_x, t_start, t_gap):
    l_plotText = plotText.split("?")
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(float(t_textSize))
    t.SetTextAlign(int(t_alignment))
    for item in l_plotText:
        t.DrawLatex(float(t_x), float(t_start), item)
        t_start = float(t_start) - float(t_gap)
# done function

# ex: h2=resize_h1D(h,100,150,5.0,debug)
def resize_h1D(old,new_xmin,new_xmax,new_bin_width,debug):
    if debug:
        print "old",type(old),old.GetEntries(),old.Integral()
    old_Nbins=old.GetNbinsX()
    if debug:
        print "old_Nbins",old_Nbins
    old_bin_underflow=0
    old_bin_first=1
    old_bin_last=old_Nbins
    old_bin_overflow=old_Nbins+1
    if debug:
        print "old_bin_underflow",old_bin_underflow
        print "old_bin_first",old_bin_first   
        print "old_bin_last",old_bin_last
        print "old_bin_overflow",old_bin_overflow
    old_bin_width=old.GetBinWidth(old_bin_first)
    old_xmin=old.GetBinLowEdge(old_bin_first)
    old_xmax=old.GetBinLowEdge(old_bin_last)+old.GetBinWidth(old_bin_last)
    if debug:
        print "old_bin_width",old_bin_width
        print "old_xmin",old_xmin
        print "old_xmax",old_xmax
    assert(new_xmin>=old_xmin)
    assert(new_xmax<=old_xmax)
    # skip bins lower than this one
    new_bin_first=int(math.ceil((new_xmin-old_xmin)/old_bin_width))+1
    if debug:
        print "new_bin_first",new_bin_first
    # skip bins higer than this one
    new_bin_last=int(math.floor((new_xmax-old_xmin)/old_bin_width))
    if debug:
        print "new_bin_last",new_bin_last
    # if the first one is higher than the second one it means all bins are skipped
    assert(new_bin_first<=new_bin_last)
    new_title=old.GetTitle()
    new_name=old.GetName()
    new_Nbins=new_bin_last-new_bin_first+1
    new_xmin_updated=old.GetBinLowEdge(new_bin_first)
    new_xmax_updated=old.GetBinLowEdge(new_bin_last)+old.GetBinWidth(new_bin_last)
    if debug:
        print new_title,new_name,new_Nbins,new_xmin,new_xmax
    new=TH1F(new_title,new_name,new_Nbins,new_xmin,new_xmax)
    # +1 is the overflow, than +1 to include the overflow
    # that's Python works xrange [a,b)
    temp_content=0.0
    for i in xrange (0,old_Nbins+1+1):
        if i<new_bin_first:
            temp_content+=old.GetBinContent(i)
        elif i==new_bin_first:
            if debug:
                print i,"is new_bin_first"
            # set the underflow as the sum of all the bins before the first bin
            new.SetBinContent(0,temp_content)
            temp_content=0.0
            new.SetBinContent(i-new_bin_first+1,old.GetBinContent(i))
        elif i<new_bin_last:
            if debug:
                print i,"regular bin to fill one by one"
            new.SetBinContent(i-new_bin_first+1,old.GetBinContent(i))
        elif i==new_bin_last:
            if debug:
                print i,"is new_bin_last"
            new.SetBinContent(i-new_bin_first+1,old.GetBinContent(i))
        elif i>new_bin_last:
            temp_content+=old.GetBinContent(i)
        else:
            None
        # done if
    # done for
    # now we can add the remaining of the bins into the overflow of the new histogram
    new.SetBinContent(new_Nbins+1,temp_content)
    temp_content=0.0

    # rebin
    if new_bin_width<=old_bin_width:
        rebin=1
    else:
        rebin=int(math.floor(new_bin_width/old_bin_width))
    if debug:
        print "rebin",rebin
    new.Rebin(rebin)

    # change the characteristics to those of h
    update_h1D_characteristics_from_another_one(new,old,debug)

    # ready to return
    return new
# done function

def do_error_myRange(myRange):
    print "Range",myRange,"not in a good format to calculate integral with errors. Will ABORT!!!"
    assert(False)
# done function

def get_histo_integral_error(histo,myRange=0,debug=False):
    if myRange==-1:
        myRange=[0,histo.GetNbinsX()+1] # with    overflow bins
    elif myRange==0:
        myRange=[1,histo.GetNbinsX()]   # without overflow bins
    else:
        # check if it is in a good format
        if isinstance(myRange, list)==False:
            do_error_myRange(myRange)
        # if here, it means we have a list
        if len(myRange)!=2:
            do_error_myRange(myRange)
        # if here, it means lists has two elements
        if isinstance(myRange[0], int)==False:
            do_error_myRange(myRange)
        if isinstance(myRange[1], int)==False:
            do_error_myRange(myRange)
        # if here both elements behave like an int
        if myRange[0]<0 or myRange[1]>histo.GetNbinsX()+2 or myRange[0]>myRange[1]:
            do_error_myRange(myRange)
        # if here both elements are within the allowed range 0 through N+2
        # and the first is smaller or equal to the second
        # so we are good to go
        None
    # range is good and defined, we can move on
    array_error=array("d",[0])
    option=""
    integral=histo.IntegralAndError(myRange[0],myRange[1],array_error,option)
    error=array_error[0]
    if debug:
        print "integral +- error: %-.3f +- %-.3f" % (integral,error)
    return (integral,error)
# done function

def isHistoConsistentWithOne(histo,debug=False):
    result=False
    counterNonZeroBins=0
    counterNonZeroBinsConsistentWithOne=0
    # if consider consider underflow and overflow
    # for i in xrange(histo.GetNbinsX()+2):
    # do not consider underflow and overflow
    for i in xrange(1,histo.GetNbinsX()+1):
        if debug:
            print "bin ",i
        content=histo.GetBinContent(i)
        error=histo.GetBinError(i)
        if debug:
            print "bin",i,"content +/- error",content,"+/-",error
        if content<=0:
            continue
        counterNonZeroBins+=1
        if content-error<=1.0<=content+error:
            #bin consistent with one
            counterNonZeroBinsConsistentWithOne+=1
    # done loop over bins
    fractionOfBinsConsistentWithOne=ratio(float(counterNonZeroBinsConsistentWithOne),float(counterNonZeroBins))
    if fractionOfBinsConsistentWithOne>0.6666:
        result=True
    if debug:
        print "statisticallyConsistentWithOne",result,"fractionOfBinsConsistentWithOne",fractionOfBinsConsistentWithOne,"counterNonZeroBinsConsistentWithOne",counterNonZeroBinsConsistentWithOne,"counterNonZeroBins",counterNonZeroBins
    return result
# done function

def computeSB(h_S,h_B,IncludeUnderflowOverflowBins=False,AddInQuadrature=True,WhatToCompute="sensitivity",output=True,debug=False):
    if debug:
        print "Start computeSB() with IncludeUnderflowOverflowBins",IncludeUnderflowOverflowBins,"AddInQuadrature",AddInQuadrature,"WhatToCompute",WhatToCompute,"output",output
        print "h_S",type(h_S), h_S
        print "h_B",type(h_B), h_B
    NbinsX=h_S.GetNbinsX()
    # what is my range of bins I run on?
    if IncludeUnderflowOverflowBins:
        myrange=[0,NbinsX+1+1]
    else:
        # we want to run excluding the underflow (bin 0)
        # and overflow bin NbinsX+1
        myrange=[1,NbinsX+1]
    if debug:
        print "myrange",myrange
        print "AddInQuadrature",AddInQuadrature
    if AddInQuadrature:
        if debug:
            "We will AddInQuadrature"
        totalContent_squared=0.0
        totalError_squared=0.0
        # need to loop over the bins first
        # done if about my range of bins 
        for i in xrange(myrange[0],myrange[-1]):
            if debug:
                print "Starting new bin"
            #S=h_S.Integral(i,i)
            #B=h_B.Integral(i,i)
            S=h_S.GetBinContent(i)
            errS=h_S.GetBinError(i)
            B=h_B.GetBinContent(i)
            errB=h_B.GetBinError(i)
            if debug:
                print "i",i,"S +- errS","%-.5f +- %-5f" % (S,errS),"B +- errB","%-.5f +- %-.5f" % (B,errB)
            if WhatToCompute=="SignalOverBackground":
                currentContent,currentError=ratioError(S,errS,B,errB,debug=debug)
            elif WhatToCompute=="Sensitivity":
                currentContent,currentError=sensitivity(S,errS,B,errB,debug=debug)
            elif WhatToCompute=="SensitivitySigmaB":
                currentContent,currentError=sensitivitySigmaB(S,errS,B,errB,debug=debug)
            elif WhatToCompute=="Significance":
                currentContent,currentError=significance(S,errS,B,errB,debug=debug)
            elif WhatToCompute=="SignificanceSigmaB":
                currentContent,currentError=significanceSigmaB(S,errS,B,errB,debug=debug)
            else:
                print "WhatToCompute",WhatToCompute,"not known! Choose between SignalOverBackground, Sensitivity, SensitivitySigmaB, Significance, SignificanceSigmaB. Will ABORT!!!"
                assert(False)
            if debug:
                print "currentContent +/- currentError", "%-.5f +- %-.5f" % (currentContent,currentError)
            # done if on WhatToCompute
            # add in quadrature
            totalContent_squared+=currentContent*currentContent
            totalError_squared+=currentError*currentError
        # done loop over all the bins in the histogram
        if debug:
            print "totalContent_squared",totalContent_squared
            print "totalError_squared",totalError_squared
        total=math.sqrt(totalContent_squared)
        error=math.sqrt(totalError_squared)
        if debug:
            print "total",total
    else:
        # not add in quadrature
        if debug:
            print "We will not add AddInQuadrature, so add bins one by one"
        S=h_S.Integral(*myrange)
        B=h_B.Integral(*myrange)
        S,errS=get_histo_integral_error(h_S,myRange=-1,debug=debug)
        B,errB=get_histo_integral_error(h_B,myRange=-1,debug=debug)
        if WhatToCompute=="SignalOverBackground":
            total,error=ratioError(S,errS,B,errB,debug=debug)
        elif WhatToCompute=="Sensitivity":
            total,error=sensitivity(S,errS,B,errB,debug=debug)
        elif WhatToCompute=="SensitivitySigmaB":
            total,error=sensitivitySigmaB(S,errS,B,errB,debug=debug)
        elif WhatToCompute=="Significance":
            total,error=significance(S,errS,B,errB,debug=debug)
        elif WhatToCompute=="SignificanceSigmaB":
            total,error=significanceSigmaB(S,errS,B,errB,debug=debug)
        else:
            print "WhatToCompute",WhatToCompute,"not known! Choose between SignalOverBackground, Sensitivity, SensitivitySigmaB, Significance, SignificanceSigmaB. Will ABORT!!!"
            assert(False)
        # done if on WhatToCompute
    # done if AddInQuadrature, so let's write the total
    # which was able to be computed in two ways
    if output:
        print "IncludeUnderflowOverflowBins",IncludeUnderflowOverflowBins,"AddInQuadrature",AddInQuadrature,"WhatToCompute",WhatToCompute,"%-.4f +- %-.4f" % (total,error)
    return total,error
# done function


class Poisson:
    def __call__( self, x, par ):
        n=x[0] # data
        e=par[0] # expected, can be b, or s+b, or mu*s+b
        if e<10000:
            result=TMath.Poisson(n,e)
        else:
            # better to return a Gauss; so this is where the error is taken into account
            result=TMath.Gaus(n,e,math.sqrt(e),ROOT.kTrue)
        return result
    # done function
# done class

class LogLikelihood:
    def __init__(self,histo_s,histo_b,histo_d, debug=False):
        self.poisson=Poisson()
        self.histo_s=histo_s
        self.histo_b=histo_b
        self.histo_d=histo_d
        self.debug=debug

    def __call__( self, x):
        if self.debug:
            print ""
        mu=x[0] # signal parameter strength
        result=0.0
        # log of product of likelihood for each bin = 
        # sum of log of likelihood in each bin
        # prefer log as we can have very small numbers
        # log is natural logarithm
        # loop over the bins
        for i in xrange(1,self.histo_s.GetNbinsX()+1):
            s=self.histo_s.GetBinContent(i)
            b=self.histo_b.GetBinContent(i)
            d=self.histo_d.GetBinContent(i)
            n=d # data
            e=mu*s+b # expected
            if b<0:
                continue
            if e<0:
                continue
            if d<0:
                continue
            #p=Poisson()
            #result+=p.__call__([n],[e])
            #result+=Poisson().__call__([n],[e])
            #likelihood=self.poisson.__call__([n],[e])
            likelihood=TMath.Poisson(n,e)
            if self.debug:
                print "n,e,l",n,e,likelihood
            result+=TMath.Log(likelihood)
        # done loop over bins
        return result
    # done function
# done class

class F_qmu_given_muprime:
    def __call__( self, x, par ):
        qmu=x[0]
        mu=par[0]
        muprime=par[1]
        sigma=par[2]
        arg=math.sqrt(qmu)-(mu-muprime)/sigma
        result=0
        if qmu>0:
            # slide 23 of https://www.pp.rhul.ac.uk/~cowan/stat/weizmann15/cowan_weizmann15_3.pdf
            result=0.5*(1.0/math.sqrt(2.0*math.pi))*(1.0/math.sqrt(qmu))*math.exp(-0.5*arg*arg)
        else:
            # where does this come from?
            result=ROOT.Math.normal_cdf((muprime-mu)/sigma,1.0,0.0)
        return result
    # done function
# done class

class F_qmu_given_mu:
    def __call__( self, x):
        qmu=x[0]
        result=0
        if qmu>0:
            # slide 23 of https://www.pp.rhul.ac.uk/~cowan/stat/weizmann15/cowan_weizmann15_3.pdf
            result=0.5*(1.0/math.sqrt(2.0*math.pi))*(1.0/math.sqrt(qmu))*math.exp(-0.5*qmu)
        else:
            # where does this come from?
            result=0.5
        return result
    # done function
# done class
