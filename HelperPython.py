#!/usr/bin/python
import numpy
import math
import inspect
from array import array
# this allows you to call console (bash) commands into your script
from subprocess import call
import subprocess
# help us see if a file exists
import os.path
# import operator needed to sort dictionaries in a list
import operator
# to catch the stdout from ROOT in a text file
import os,sys
from glob import glob
# for checking the itme stamps on the files
import datetime
# time measurement
from time import time
# deep copy for dictionaries
from copy import deepcopy
import copy
# named tuple
from collections import namedtuple
# to get line number
from inspect import currentframe
# regular expressions
import re
# import itertools to concatenate lists
import itertools

# get a string to be used to rebin a histogram
# 0.0, 5.0, 0.1 - from 0.0 to 5.0 with a step of 0.1
def get_binRange(initial,end,step,debug=False):
    if debug:
        print "Start get_binRange: initial",initial,"end",end,"step",step
    result=str(initial)
    i=initial
    epsilon=0.0001
    while i+step<=end+epsilon:
        i+=step
        if abs(i)<0.0001:
            i=0
        result+=","+str(i)
    if debug:
        print "binRange("+str(initial)+","+str(end)+","+str(step)+")="+result
    return result
# done function

def remove_duplicates_from_generic_binRange(binRange="150,200,400",debug=False):
    # evaluate the desired binning
    # when making the bin range from a sum of several other bin ranges
    # one ends and the other starts with the same value
    # in that case, skip one of them, as it gives incorrectly a bin of zero range
    if debug:
        print "input binRange",binRange
    binRangeOutput=""
    previousEdge=""
    list_repeatedEdge=[]
    for i,currentEdge in enumerate(binRange.split(",")):
        if False:
            print "previousEdge",previousEdge,"currentEdge",currentEdge
        if currentEdge!=previousEdge:
            if i!=0:
                binRangeOutput+=","
            binRangeOutput+=currentEdge
        # done if
        previousEdge=currentEdge
    # done for loop over bin edges
    if debug:
        print "output binRange",binRangeOutput
    return binRangeOutput
# done

#https://www.ics.uci.edu/~alspaugh/cls/shr/regularExpression.html
def match_regularExpression_in_string(regex, text):
    pattern = re.compile(regex, text)
    return pattern.search(text) is not None
# done function

def example_format_string():
    list_values=[
        ["bla", 1, 0.0, 30.0, 0.0, 0.0],
        ["bla22",5, 170.0, 190.0, 559.06, 30.65],
        ["bla333",16, 500.0, 1300.0, 7.22, 2.38],
        ]
    for text,i,binLowEdge,binHighEdge,binContent,binError in list_values:
        line="%8s bin %4.0f range [%4.0f,%4.0f] value %8.2f error %8.2f" % (text,i,binLowEdge,binHighEdge,binContent,binError)
        print line
    #     bla bin    1 range [   0,  30] value     0.00 error     0.00
    #   bla22 bin    5 range [ 170, 190] value   559.06 error    30.65
    #  bla333 bin   16 range [ 500,1300] value     7.22 error     2.38
    for text,i,binLowEdge,binHighEdge,binContent,binError in list_values:
        line="%-8s bin %-4.0f range [%-4.0f,%4.0f] value %-8.2f error %-8.2f" % (text,i,binLowEdge,binHighEdge,binContent,binError)
        print line
    # bla      bin 1    range [0   ,  30] value 0.00     error 0.00    
    # bla22    bin 5    range [170 , 190] value 559.06   error 30.65   
    # bla333   bin 16   range [500 ,1300] value 7.22     error 2.38 
    # Notice how - arranges to the left and lack of - arranges to the righ!
# done function

def get_lineNumber():
    cf = currentframe()
    return cf.f_back.f_lineno
# done function

# start functions
def percentageDifference(x,y,debug=False):
  if debug:
    print "x",x,"y",y
  if -0.0001<y<0.0001:
    result=0.0
  else:
    result=100*(x-y)/y
  return result
# done function

def listVariables(name,prefix):
  return prefix+name.replace(',',','+prefix)
# done function

def updateListVariables(prefix,name,suffix):
  return prefix+name.replace(',',suffix+','+prefix)+suffix
# done function

def getValues(event,listVariables,debug=False):
  if debug:
    print "listVariables",listVariables
  return numpy.array([getattr(event,variableName) for variableName in listVariables.split(',')])
# done function

def getFileNameStem(fileName,debug=False):
  if debug:
    print "fileName",fileName
  fileNameSplitBySlash=fileName.split("/")
  # now pick the last element, which means with path removed
  # find out how many elements are in the list
  nrElements=len(fileNameSplitBySlash)
  fileNameWithoutPath=fileNameSplitBySlash[nrElements-1]
  if debug:
    print "fileNameWithoutPath",fileNameWithoutPath
  fileNameStem=fileNameWithoutPath.split(".")[0]
  if debug:
    print "fileNameStem",fileNameStem
  # a bit hard coded, but we know the name of the root files start with
  # train_tree_ and we want to remove that, it has 11 characters
  fileNameStem=fileNameStem[12:]
  if debug:
    print "fileNameStem",fileNameStem
  return fileNameStem
# done function

def getProcessName(fileNameStem,debug=False):
  if debug:
    print "fileNameStem",fileNameStem
  fileNameStemSplitByUnderscore=fileNameStem.split("_")
  # now pick the last before last element, which means the process
  # as the last means _merged or _0
  processName=fileNameStemSplitByUnderscore[-2]
  if debug:
    print "processStem",processName
  return processName
# done function

# if based on the sample name and the index of the event (even or odd) we should skip the event, then continue
# for the train sample we use events of index 0, 2, 4, etc (even)
# for the test sample we use events of index 1, 3, 5, etc (odd)
# for the all sample we use all events
def keepEntry(sample,i,debug):
  if debug:
    print "i",i,"sample",sample
  result=False
  if sample=="train":
    # keep only even-number entries (events or jets), as they were used in the training of the NN
    if i%2==0:
      result=True
  elif sample=="test":
    # keep only odd-number entries (events or jets), as they were used in the testinging of the NN
    if i%2==1:
      result=True
  elif sample=="all":
    # keep all the entries (events or jets)
    result=True
  else:
    print "sample",sample,"not known, will abort. Need to choose between train, test and all"
    assert(False)
  # done if on sample
  return result
# done function

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)
# done function

def doesFileExist(filename, debug):

    if os.path.isfile(filename):
        if debug:
            print "DEBUG: File: %s Exisits" % (filename)

        return True
    else:
        return False
# done function

def OpenFile(filename, debug):
    
    try:
        file = open(filename,"r")
        if debug:
            print "DEBUG: Opening File: %s" % (filename)
        return file
    except IOError, (erno, sterror):
        print "IOError error(%s): %s" % (errno, strerror)
    except:
        print "Unexpected error:", system.exc_info()[0]
        raise
# done function

class XPlus1OverX:
    def __call__( self, x, par ):
        return par[0]+x[0]*par[1]+(1.0/x[0])*par[2]
    # done function
# done class

class Sigmoid:
    def __call__( self, x, par ):
        return 1.0/(1.0+par[0]*math.exp(par[1]*(x[0])))
    # done function
# done class

class Linear:
    def __call__( self, x, par ):
        return par[0]+x[0]*par[1]
    # done function
# done class

class PieceWiseLinear:
    def __call__( self, x, par ):
        if x[0]<par[2]:
            result=par[1]+((par[3]-par[1])/(par[2]-par[0]))*(x[0]-par[0])
        else:
            result=par[3]+((par[5]-par[3])/(par[4]-par[2]))*(x[0]-par[2])
        return result
    # done function
# done class

class Parabolic:
    def __call__( self, x, par ):
      return par[0]+par[1]*x[0]+par[2]*math.pow(x[0],2)
    # done function
# done class

class Parabolic2:
    def __call__( self, x, par ):
        if x[0]<par[3]:
            result=par[4]
        else:
            result=par[0]+par[1]*x[0]+par[2]*math.pow(x[0],2)
        return result
    # done function
# done class

class Polynomial3:
    def __call__( self, x, par ):
      result=0.0
      for i in xrange(4):
        result+=par[i]*math.pow(x[0],i)
      return result
    # done function
# done class

class Polynomial4:
    def __call__( self, x, par ):
      result=0.0
      for i in xrange(5):
        result+=par[i]*math.pow(x[0],i)
      return result
    # done function
# done class

class Polynomial5:
    def __call__( self, x, par ):
      result=0.0
      for i in xrange(6):
        result+=par[i]*math.pow(x[0],i)
      return result
    # done function
# done class

class Polynomial6:
    def __call__( self, x, par ):
      result=0.0
      for i in xrange(7):
        result+=par[i]*math.pow(x[0],i)
      return result
    # done function
# done class

class Gauss:
    def __call__( self, x, par ):
        if par[2]!=0:
          result=par[0]*math.exp(-0.5*math.pow((x[0]-par[1])/par[2],2))
        else:
            result=0.0
        return result
    # done function
# done class

class Bukin:
    def __call__( self, x, par ):

      debug=False

      if debug:
        print "******"
      # inputs
      xx =x[0]
      norm = par[0] # overall normalization
      x0 = par[1] # position of the peak
      sigma = par[2] # width of the core
      xi = par[3] # asymmetry
      rhoL = par[4] # size of the lower tail
      rhoR = par[5] # size of the higher tail
      if debug:
        print "xx",xx
        print "norm",norm
        print "x0",x0
        print "sigma",sigma
        print "xi",xi
        print "rhoL",rhoL
        print "rhoR",rhoR
  
      # initializations
      r1=0.0
      r2=0.0
      r3=0.0
      r4=0.0
      r5=0.0
      hp=0.0
      
      x1=0.0
      x2=0.0
      fit_result=0.0
  
      # set them other values
      consts=2*math.sqrt(2*math.log(2.0))
      hp=sigma*consts
      r3=math.log(2.0)
      r4=math.sqrt(math.pow(xi,2)+1.0)
      r1=xi/r4
      if debug:
        print "consts",consts
        print "hp",hp
        print "r3",r3
        print "r4",r4
        print "r1",r1
        print "x1",x1
        print "x2",x2
        print "x0",x0
        print "xx",xx
        print "xi",xi
        print "math.exp(-6.)",math.exp(-6.)

      if abs(xi)>math.exp(-6.):
        r5=xi/math.log(r4+xi)
      else:
        r5=1.0
      if debug:
        print "r5",r5

      x1=x0+(hp/2)*(r1-1)
      x2=x0+(hp/2)*(r1+1)
      if debug:
        print "x1",x1
        print "x2",x2
        print "x0",x0
        print "xx",xx

      if xx<x1:
        # Left Side
        r2=rhoL*math.pow((xx-x1)/(x0-x1),2)-r3+4*r3*(xx-x1)/hp*r5*r4/math.pow((r4-xi),2)
      elif xx < x2:
        # Centre
        if abs(xi)>math.exp(-6.):
          r2=math.log(1+4*xi*r4*(xx-x0)/hp)/math.log(1+2*xi*(xi-r4))
          r2=-r3*math.pow(r2,2)
        else:
          r2=-4*r3*math.pow(((xx-x0)/hp),2)
        # ended if
      else:
        # Right Side
        r2=rhoR*math.pow((xx-x2)/(x0-x2),2)-r3-4*r3*(xx-x2)/hp*r5*r4/math.pow((r4+xi),2)
      # ended if on what side
        
      if abs(r2)>100:
        fit_result=0
      else:
        # Normalize the result
        fit_result=math.exp(r2)
      # compute result
      result=norm*fit_result
      # return result
      return result
    # done function
# done class

def doesFileExist(filename, debug):

    if os.path.isfile(filename):
        if debug:
            print "DEBUG: File: %s Exisits" % (filename)

        return True
    else:
        return False
# done function

def OpenFile(filename, debug):
    
    try:
        file = open(filename,"r")
        if debug:
            print "DEBUG: Opening File: %s" % (filename)
        return file
    except IOError, (erno, sterror):
        print "IOError error(%s): %s" % (errno, strerror)
    except:
        print "Unexpected error:", system.exc_info()[0]
        raise
# done function

def dictMaker(dictObjects, debug):

    dict = {}
    for name in dictObjects.split(","):
        title = name.rstrip()
        key = ""
        value = ""
        dict[name.split(":")[0]] = name.split(":")[1]

    if debug :
        print "DEBUG: Dict: %s" % (dict)
    return dict
#done function

def tupleMaker(filename, debug):
  
  arg_list = OpenFile(filename, debug)
  
  tuple = []
  for histo_info in arg_list:
    if not histo_info.startswith("#"):
      parsed_arg = [x.strip() for x in histo_info.split(',')]
      tuple.append(parsed_arg)
      
      if debug:
        print "\nDEBUG: TUPLE OF FILE: %s\n %s\n" % (filename, tuple)
        
  return tuple
#done function

# used to run over files in step, for example a root file has 310000 events
# and we want to run on 7 files, each having 50000 events and the last one
# having 10000
# we run on all events with a step of 50000
def getListSteps(nrEntries,event_step,debug):
  if debug:
    print type(nrEntries)
    print type(event_step)
    print "event_step",event_step
  result=[]
  remainder=nrEntries%event_step
  nrSteps=(nrEntries-remainder)/event_step
  if debug:
    print "nrEntries",nrEntries,"event_step",event_step,"nrSteps",nrSteps,"plus remainder",remainder
  for i in xrange(nrSteps):
    result.append((1+i*event_step,(i+1)*event_step))
  result.append((1+nrSteps*event_step,nrEntries))
  if debug:
    print "getListSteps",result
  return result
#done function

def getModTime(file,debug):
  if debug:
    print "file name",file
   
  if os.path.exists(file):
    t = os.path.getmtime(file)
    result=datetime.datetime.fromtimestamp(t)
  else:
    result=0
  # done if
  if debug:
    print "result=",result
  return result
# done function

def find_if_we_run_given_timestamps_input_output_files(fileInputName,fileOutputName,debug):
  TimeFileInput = getModTime(fileInputName,debug)
  TimeFileOutput = getModTime(fileOutputName,debug)
  file_input_exists = TimeFileInput != 0
  file_output_exists = TimeFileOutput != 0
  file_input_newer_than_file_output = False
  if file_input_exists and file_output_exists:
    file_input_newer_than_file_output = TimeFileInput > TimeFileOutput
  # run only if the input file exists and either the output file does not exist or it is older than the input file
  shall_we_run=file_input_exists and (not file_output_exists or file_input_newer_than_file_output)
  if debug:
    print "file_input_exists", file_input_exists
    print "file_output_exists", file_output_exists
    print "file_input_newer_than_file_output", file_input_newer_than_file_output
    print "shall_we_run",shall_we_run
  # ready to return
  return shall_we_run
# done function

def testTrainRankCalc(t_train, t_test):
    
    t_rank = []
    for i in xrange(len(t_train)):
        rank = abs((t_train[i][1] - t_test[i][1])/t_train[i][1])
        l_rank = [t_train[i][0], rank]
        t_rank.append(l_rank)
    
    d_rank = {}
    for i in xrange(len(t_rank)):
        d_rank[t_rank[i][0]] = t_rank[i][1]
    
    return d_rank
# done function


#########################################################
############### Automatic binning #######################
#########################################################

def get_numpyarray_from_listString(listString,debug=False):
  if debug:
    print "listString",listString
  listFloat=[]
  for string in listString:
    listFloat.append(float(string))
  # done for loop
  numpyarray=numpy.array(listFloat)
  if debug:
    print "numpyarray",numpyarray
  return numpyarray
# done function

def get_string_from_listString(listString,debug=False):
  result=""
  for i,name in enumerate(listString):
    if i!=0:
      result+="_"
    result+=name
  # done for
  return result
# done function



# start functions used for Adrian in runAdi.py to create
# and plot histograms from the flat tree
# ex: list_values ['20', '30', '40']
# ex: returns [(-inf, 20.0), (20.0, 30.0), (30.0, 40.0), (40.0, inf)]

def get_list_intervals(string_values="",addUnderflow=False,addOverflow=False,addInclusive=False,debug=False):
    if debug:
        print "string_values",string_values
    result=[]
    if string_values=="":
      result.append((float("-inf"),float("inf")))
    else:
      list_values=string_values.split(",")
      if debug:
        print "list_values",list_values
      if addUnderflow:
        # add underflow (from minus infinity to the first element)
        result.append((float("-inf"),float(list_values[0])))
      # add all regular values
      for i in range(len(list_values)-1):
        result.append((float(list_values[i]),float(list_values[i+1])))
      if addOverflow:
        # add overflow (from the last element to infinity)
        result.append((float(list_values[-1]),float("inf")))
    # end if
    if addInclusive:
      # add the bin representing all possible values
      # the superset of the sets above
      # for inclusive studies
      result.append((float("-inf"),float("inf")))
    # check result
    if debug:
        print "get_list_intervals",result
    # return result
    return result   
# done function

# list_bin: [(-inf, 20.0), (20.0, 30.0), (30.0, 40.0), (40.0, inf)]
# value_bin: 40.0840078125
# The value_bin 40.0840078125 is in the interval (40.0, inf)
def find_bin_in_list(list_bin,value_bin,debug):
  for bin in list_bin:
    if bin[0]<=value_bin<bin[-1]:
      if debug:
        print "The value_bin",value_bin,"is in the interval",bin
      return bin
# done function



def get_array_values(string_values,debug):
    if debug:
        print "string_values",string_values
    result=[]
    list_values=string_values.split(",")
    if debug:
        print "list_values",list_values
    for i in range(len(list_values)):
        result.append((float(list_values[i])))
    # check result
    if debug:
        print "array_values",result
    # return result
    return result   
# done function

# (0.0,90,0) -> "0_90"
# (-inf, 90) -> "inf_90"
# we want to not have dots and - in the name of a histogram
# so that we can do in TBrowswer histo_name->Draw(), etc
def get_bin_string(bin,factor,debug):
    if debug:
        print "bin",bin
    result=""
    for i,value in enumerate(bin):
        if value==float("-inf") or value==float("inf"):
            value_string="inf"
        else:
            value_string="%-.0f" % (value*factor)
        if debug:
            print "i",i,"value_string",value_string
        if i!=0:
            result+="_"
        result+=value_string
    # done for loop over the two elements in the bin
    if debug:
        print "bin_string",result
    return result
# done function

def get_listBinSelected(listBin,binValue,debug):
    result=[]
    for bin in listBin:
        if bin[0]<=binValue<bin[-1]:
            if debug:
                print "The binValue",binValue,"is in the interval",bin
            result.append(bin)
    # done for loop
    return result
# done function

# get all the bins that are included fully in that interval
# so can remain a subset of the bins not covered if the interval
# does not match perfectly
def get_listBinMerged(listBin,binMerged,debug):
    result=[]
    for bin in listBin:
        if bin[0]>=binMerged[0] and bin[1]<=binMerged[1]:
            if debug:
                print "The bin",bin,"is in the desired merged bin",binMerged
            result.append(bin)
    # done for loop
    return result
# done function

def get_listStringBin(binVariable,factor,listBin,debug):
    result=[]
    for bin in listBin:
        if debug:
            print "bin",bin
        currentString=binVariable
        if factor!=1:
          currentString+="x%-.0f" % factor
        currentString+="_"+get_bin_string(bin,factor,debug)
        result.append(currentString)
    # done for loop
    return result
# done function

def concatenate_two_listString(list1,list2,debug):
  result=[]
  for i in list1:
    for j in list2:
      result.append(i+"_"+j)
  return result
# done function

def get_listString_from_dict_binVariable_listBin(list_binVariable,dict_binVariable_listBin,dict_binVariable_factor,debug):
  result=[]
  for i,binVariable in enumerate(list_binVariable):
    if debug:
      print "binVariable",binVariable
    factor=dict_binVariable_factor[binVariable]
    if debug:
      print "factor",factor
    listBin=dict_binVariable_listBin[binVariable]
    if debug:
      print "listBin",listBin
    listStringCurrent=get_listStringBin(binVariable,factor,listBin,debug)
    if debug:
      print "listStringCurrent",listStringCurrent
    if i==0:
      result=listStringCurrent
    else:
      result=concatenate_two_listString(result,listStringCurrent,debug)
    if debug:
      print "aftr step",i,"result is",result
  # done loop over binVariable
  return result
# done function

def concatenate_two_dict_binVariable_listBin(dict1,dict2,debug):
  result=[]
  for binVariable1 in dict1:
    for binVariable2 in dict2:
      result.append(binVariable1+"_"+binVariable2)
  return result
# done function

def split_listBin(list_binVariable,dict_binVariable_listBin,debug):
  result=[]
  
  return result
# done function


#def get_list_dict_binVariable_bin(binVariable1,listBin1,binVariable2,listBin2,debug):
def get_list_dict_binVariable_bin(list_binVariable,dict_binVariable_listBin,debug):
  result=[]
  print ""
  for binVariable in list_binVariable:
    if debug:
      print "binVariable",binVariable
    dict_binVariable_bin={}
    listBin=dict_binVariable_listBin[binVariable]
    if debug:
      print "listBin",listBin
    dict_binVariable_bin[binVariable]=bin
  # 
  if debug:
    print "dict_binVariable_bin",dict_binVariable_bin
  return result
# done function

def get_list_list_dict_binVariable_bin(binVariable,dict_binVariable_listBin,debug):
  print ""
  result=[]
  for bin in dict_binVariable_listBin[binVariable]:
    result.append([{binVariable:bin}])
  # done for loop
  return result
# done function

def get_list_dict_binVariable_bin(binVariable,dict_binVariable_listBin,debug):
  print ""
  result=[]
  for bin in dict_binVariable_listBin[binVariable]:
    result.append({binVariable:bin})
  # done for loop
  return result
# done function

def concatenate_two_list_bk1(list1,list2,debug):
  if debug:
    print "list1",list1
    print "list2",list2
  result=[]
  for i1 in list1:
    temp1=[]
    temp1.append(i1)
    for i2 in list2:
      temp2=temp1[:]
      temp2.append(i2)
      result.append(temp2)
    # done loop over list2
  # done loop over list1
  return result
# done function

def concatenate_two_list(list1,list2,debug):
  if debug:
    print "list1",list1
    print "list2",list2
  result=[]
  for i2 in list2:
    temp2=list1[:]
    temp2.append(i2)
    result.append(temp2)
  # done loop over list2
  return result
# done function

def concatenate_all_list(listBig,debug):
  result=[]
  for big in listBig:
    if debug:
      print "big",big
      print "result before",result
    result=concatenate_two_list(result,big,debug)
    if debug:
      print "result after",result
  # done loop over listBig
  return result
# done function

def concatenate_2_list(list1,list2,debug):
  if debug:
    print "list1",list1
    print "list2",list2
  result=[]
  for i1 in list1:
    for i2 in list2:
      result.append([i1,i2])
    # lone loop over list2
  # done loop over list1
  return result
# done function

def concatenate_3_list(list1,list2,list3,debug):
  if debug:
    print "list1",list1
    print "list2",list2
    print "list3",list3
  result=[]
  for i1 in list1:
    for i2 in list2:
      for i3 in list3:
        result.append([i1,i2,i3])
      # lone loop over list3
    # lone loop over list2
  # done loop over list1
  return result
# done function

def concatenate_21_list(listList,list3,debug):
  if debug:
    print "listList",listList
    print "list3",list3
  result=[]
  for myList in listList:
    if debug:
      print "myList",myList
    for i3 in list3:
      if debug:
        print "i3",i3
      currentMyList=myList[:]
      currentMyList.append(i3)
      result.append(currentMyList)
    # lone loop over list2
  # done loop over list1
  return result
# done function

def concatenate_list_to_list_of_list(myListOfList,myNewList,debug):
  if debug:
    print "myListOfList",myListOfList
    print "myNewList",myNewList
  result=[]
  for myList in myListOfList:
    if debug:
      print "myList",myList
    for element in myNewList:
      if debug:
        print "element",element
      currentMyList=myList[:]
      currentMyList.append(element)
      result.append(currentMyList)
    # lone loop over list2
  # done loop over list1
  return result
# done function

def concatenate_all(listAll,debug):
  result=[[]]
  for myNewList in listAll:
    result=concatenate_list_to_list_of_list(result,myNewList,debug)
  return result
# done function

def concatenate_two_list_dict_binVariable_bin(list1,list2,debug):
  if debug:
    print "list1",list1
    print "list2",list2
  if len(list1)==0:
    return list2
  result=[]
  for i1 in list1:
    if debug:
      print "i1",i1
    for i2 in list2:
      if debug:
        print "i2",i2
      temp1=copy.deepcopy(i1)
      print temp1.update(i2)
      result.append(temp1)
    # lone loop over list2
  # done loop over list1
  return result
# done function

def concatenate_all_list_dict_binVariable_bin(listAll,debug):
  result=[]
  for myNewList in listAll:
    result=concatenate_two_list_dict_binVariable_bin(result,myNewList,debug)
  return result
# done function

def get_string_from_dict_binVariable_bin(list_binVariable,dict_binVariable_bin,dict_binVariable_factor,debug):
  result=""
  for i,binVariable in enumerate(list_binVariable):
    bin=dict_binVariable_bin[binVariable]
    factor=dict_binVariable_factor[binVariable]
    if i!=0:
      result+="_"
    result+=binVariable
    if factor!=1:
      result+="x%-.0f" % factor
    result+="_"+get_bin_string(bin,factor,debug)
  return result
# done function


#test those above
#print ""
#variableBin="Index"
#if debug:
#    print "variableBin",variableBin
#stringBinEdge="0,1,2"
#if debug:
#    print "stringBinEdge",stringBinEdge
#listBin=get_list_intervals(string_values=stringBinEdge,addUnderflow=False,addOverflow=False,addInclusive=False,debug=debug)
#if debug:
#    print "listBin",listBin
#factor=1
#if debug:
#    print "factor",factor
#listStringBin=get_listStringBin(variableBin,factor,listBin,debug)
#if debug:
#    print "listStringBin",listStringBin
#listStringTest=["a","b"]
#if debug:
#    print "listStringTest",listStringTest
#listStringNew=concatenate_two_listString(listStringTest,listStringBin,debug)
#if debug:
#    print "listStringNew",listStringNew
#binValue=0
#listBinSelected=get_listBinSelected(listBin,binValue,debug)
#if debug:
#    print "listBinSelected",listBinSelected


#########################################################
############### End Automatic binning ###################
#########################################################

def get_string_value(axis_name,variable_name,variable_value):
    result="%-2s  %-30s  %-.2f" % (axis_name,variable_name,variable_value)
    return result
# done function

def get_string_scale_resolution(fit_name,scale_value,resolution_value):
    result="%-7s %-.2f %-.2f" % (fit_name,scale_value,resolution_value)
    return result
# done function

# http://changingminds.org/explanations/research/statistics/standard_error.htm
# https://simple.wikipedia.org/wiki/Standard_deviation#With_sample_standard_deviation
# https://simple.wikipedia.org/wiki/Standard_error

def process_sample(list_value,debug=False):
    if debug:
        print "list_value",list_value
    N=len(list_value)
    Sum=0.0
    for value in list_value:
        Sum+=value
    # done for loop
    Mean=ratio(Sum,N)
    # standard deviation (https://simple.wikipedia.org/wiki/Standard_deviation#With_sample_standard_deviation)
    # https://en.wikipedia.org/wiki/Standard_deviation#Sample_standard_deviation_of_metabolic_rate_of_Northern_Fulmars
    StdDev=0.0
    for value in list_value:
        StdDev+=(value-Mean)*(value-Mean)
    # done for loop
    StdDev=ratio(StdDev,N-1)
    StdDev=math.sqrt(StdDev)
    # standard error 
    StdErr=ratio(StdDev,math.sqrt(N))
    if debug:
        print "N=%.0f Mean=%.2f StdDev=%.2f StdErr=%.2f" % (N,Mean,StdDev,StdErr)
    return N,Mean,StdDev,StdErr
# done function

def tuple_times_scalar(myTuple,myScalar,debug=False):
    myTupleResult=(myTuple[0]*myScalar,myTuple[1]*myScalar)
    if debug:
        print "myTuple",myTuple,"myScalar",myScalar,"myTupleResult",myTupleResult
    return myTupleResult
# done function

# ratio, or s/b
def ratio(s,b,debug=False):
    if debug:
        print "ratio","s",s,"b",b
    if -0.00001<b<0.00001:
        if True:
            print "WARNING! -0.0001<b<0.0001, returning result 0! s=",str(s)," b=",str(b) 
        result=0
    else:
        result=s/b
    return result
# done function

# http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf
# https://en.wikipedia.org/wiki/Propagation_of_uncertainty

# ratio or s/b
def ratioError(s,se,b,be,debug=False):
    if debug:
        print "ratioError","s",s,"se",se,"b",b,"be",be
    if b==0:
        if True:
            print "WARNING! -0.0001<b<0.0001, returning result 0 and error 0! s=",str(s)," b=",str(b) 
        result=0.0
        error=0.0
    else:
        result=s/b
        #error1=result*math.sqrt(math.pow(se/s,2)+math.pow(be/b,2))
        dfds=1.0/b
        dfdb=-1.0*s/(b*b)
        error=math.sqrt(math.pow(dfds,2)*math.pow(se,2)+math.pow(dfdb,2)*math.pow(be,2))
    return (result,error)
# done function

# ratio of tuple, each tuple nominal and error
def ratioTuple(tupleNumer,tupleDenom,debug=False):
    return ratioError(tupleNumer[0],tupleNumer[1],tupleDenom[0],tupleDenom[1],debug=debug)
# done function

# sensitivity, or s over sqrt(b)
# slide 37 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
def sensitivity(s,se,b,be,debug=False):
    if debug:
        print "sensitivity ","s",s,"se",se,"b",b,"be",be
    if b<0.0001:
        if True:
            print "WARNING! b<0.0001, returning result 0 and error 0! s=",str(s)," b=",str(b) 
        result=0
        error=0
    else:
        result=s/math.sqrt(b)
        #error=result*math.sqrt( math.pow(se/s,2)+math.pow(-0.5*be/b,2) )
        dfds=1.0/math.sqrt(b)
        if debug:
            print "dfds",dfds
        dfdb=-s/(2.0*math.pow(b,3.0/2.0))
        if debug:
            print "dfdb",dfdb
        error=math.sqrt(math.pow(dfds,2)*math.pow(se,2)+math.pow(dfdb,2)*math.pow(be,2))
    if debug:
        print "sensitivity ","content +/-error","%-.5f +/- %-.5f" % (result,error) 
    return (result,error)
# done function

# significance, or DLLR, the longer formula which becomes s/sqrt(b) in the limit when s/b -> 0
# slides 37 and 38 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
def significance(s,se,b,be,debug=False):
    if debug:
        print "significance","s",s,"se",se,"b",b,"be",be
    if b<0.001:
        result=0
        error=0
        if True:
            print "WARNING! b<0.001, returning result 0 and error 0! s=",str(s)," b=",str(b) 
    else:
        # for very low numbers, the sensitivity is a very good approximation
        # of the significance, but the code runs out of digits and approximates
        # the log(1+s/b) with zero, which makes it have negative values 
        # under the square root and then it crashes
        if s/b<0.000001:
            if True:
                print "WARNING! s/b<0.000001, returning sensitivity s=",str(s)," b=",str(b),"s/b",str(s/b) 
            (result,error)=sensitivity(s,se,b,be,debug) # sensitivity
        else:
            # slide 39 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
            # for s<<b, it reduced to s/sqrt(b)
            result=math.sqrt(2.0*((s+b)*math.log(1.0+1.0*s/b)-s))
            # error formula works only if dfds<<se and dfdb<<sb, otherwise get very large value
            # so return an error of zero
            error=0.0
            #dfds=math.log(1.0+1.0*s/b)*math.pow((s+b)*math.log(1.0+1.0*s/b)-s,3.0/2.0)
            #if debug:
            #    print "dfds",dfds
            #dfdb=(1.0*s/b+math.log(1.0+1.0*s/b))*math.pow((s+b)*math.log(1.0+1.0*s/b)-s,3.0/2.0)
            #if debug:
            #    print "dfdb",dfdb
            #error=math.sqrt(math.pow(dfds,2)*math.pow(se,2)+math.pow(dfdb,2)*math.pow(be,2))
    if debug:
        print "significance","content +/-error","%-.5f +/- %-.5f" % (result,error) 
    return (result,error)
# done function

# when there is an uncertainty on the background
# sensitivity, or s over sqrt(b+be*be)
# if s<<b, but be*be is not << b
# slide 41 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
# can be rewritten as slide 4 of Nicolas' https://indico.cern.ch/event/688766/contributions/2830787/attachments/1578214/2492928/ApproximateSignificance.pdf
def sensitivitySigmaB(s,se,b,be,debug=False):
    if debug:
        print "sensitivitySigmaB ","s",s,"se",se,"b",b,"be",be
    if b<0.0001:
        if True:
            print "WARNING! b<0.0001, returning result 0 and error 0! s=",str(s)," b=",str(b) 
        result=0
        error=0
    else:
        result=s/math.sqrt(b+be*be)
        # trial and error has shown that the signal error on the ratio is the same percentage than the signal error
        # the two formulas below are equivalent
        #error=ratio(se,math.sqrt(b+be*be),debug=False)
        error=result*ratio(se,s,debug=False)
    if debug:
        print "sensitivity ","content +/-error","%-.5f +/- %-.5f" % (result,error) 
    return (result,error)
# done function

# the most generic formula as a figure of merit
# if s/b << 1 it becomes SensitivitySigmaB
# if be*be<<b it becomes Significance 
# if be*be<<b, SensitivitySigmaB becomes Sensitivity
# if s/b <<1, Significance becomes Sensitivity
# significance the longer formula which becomes s/sqrt(b+be*be) in the limit when s/b -> 0 and when be*be/b -> 0
# slide 45 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
# is this the same as slide 5 and 6 of Nicolas' https://indico.cern.ch/event/688766/contributions/2830787/attachments/1578214/2492928/ApproximateSignificance.pdf
# in Nicolas's slides: delta is relative uncertainty, so be/b. A 10% error gives delta of 0.10.
# theta0 is the nuisance parameter that maximizes L for mu=0, it has formula on slide 5
# Nicolas uses Gaussian prior, Cowan uses Poisson, so probably the results are very similar
def significanceSigmaB(s,se,b,be,debug=False):
    if debug:
        print "significanceSigmaB","s",s,"se",se,"b",b,"be",be
    if b<0.0000001:
        result=0
        error=0
        if True:
            print "WARNING! b<0.001, returning result 0 and error 0! s=",str(s)," b=",str(b) 
    else:
        if debug:
            print "significanceSigmaB","s",s,"se",se,"b",b,"be",be,"s/b",s/b,"be*be/b",be*be/b
        # for very low numbers, the sensitivity is a very good approximation
        # of the significance, but the code runs out of digits and approximates
        # the log(1+s/b) with zero, which makes it have negative values 
        # under the square root and then it crashes
        if s/b<0.0000001:
            if True:
                print "WARNING! s/b<0.000001, returning sensitivitySigmaB s=",str(s)," b=",str(b),"s/b",str(s/b) 
            (result,error)=sensitivitySigmaB(s,se,b,be,debug) # sensitivity
        else:
            # slide 45 of https://www.pp.rhul.ac.uk/~cowan/stat/aachen/cowan_aachen14_4.pdf
            # for s<<b and be*be<<b, it reduced to s/sqrt(b+be*be)
            #result2=math.sqrt(2.0*((s+b)*math.log(((s+b)*(b+be*be))/(b*b+(s+b)*(be*be)))-((b*b)/(be*be))*math.log(1.0+(be*be*s)/(b*(b+be*be)))))
            #if debug:
            #    print "result2",result2
            # result 2 has the same shape as below, where the terms are separate
            x=s/b
            y=be*be/b
            if debug:
                print "x",x,"y",y
            alpha=(1.0+x)*math.log((1.0+x)*(1.0+y)/(1.0+(1.0+x)*y))
            if debug:
                print "alpha",alpha
            beta=(1.0/y)*math.log(1.0+x*y/(1.0+y))
            if debug:
                print "beta",beta
            result=math.sqrt(2.0*b*(alpha-beta))
            if debug:
                print "result",result
            # trial and error has shown that the signal error on the ratio is the same percentage than the signal error
            error=result*ratio(se,s)
    if debug:
        print "significance","content +/-error","%-.5f +/- %-.5f" % (result,error) 
    return (result,error)
# done function

def get_figure_of_merit(s,se,b,be,figureOfMerit="SignificanceSigmaB",debug=False):
    result=0.0
    if figureOfMerit=="SignalOverBackground":
        result=ratioError(s,se,b,be,debug)
    elif figureOfMerit=="Sensitivity":
        result=sensitivity(s,se,b,be,debug=debug)
    elif figureOfMerit=="Significance":
        result=significance(s,se,b,be,debug=debug)
    elif figureOfMerit=="SensitivitySigmaB":
        result=sensitivitySigmaB(s,se,b,be,debug=debug)
    elif figureOfMerit=="SignificanceSigmaB":
        result=significanceSigmaB(s,se,b,be,debug=debug)
    else:
        print "figureOfMerit",figureOfMerit,"not know in get_figure_of_merit(). Will ABORT!!!"
        assert(False)
    if debug:
        print "figureOfMerit",figureOfMerit
    return result
# done function

# max(a,b) is already defined by Python

# ex (1.0,0.1,2.0,0.2)
def max_error(a,sa,b,sb):
    result=(a,sa)
    if b>result[0]:
        result=(b,sb)
    return result
# done function

# 1.0, 2.0, 3.0
def max_list(list_value):
    result=list_value[0]
    for value in list_value:
        if value>result:
            result=value
    return result
# done function

# ex [(1.0,0.1),(2.0,0.2),(3.0,0.3)]
def max_error_list(list_tuple):
    result=list_tuple[0]
    for tuple in list_tuple:
        if tuple[0]>result[0]:
            result=tuple
    return result
# done function

# abs(a) is already defined by Python

def abs_error(a,sa):
    return (abs(a),sa)
# done function

def sum(a,b):
    return a+b
# done function

def sum_error(a,sa,b,sb):
    result=a+b
    error=math.sqrt(sa*sa+sb*sb)
    return (result,error)
# done function

def sum_error_three(a,b,c):
    return a+b+c
# done function

def sum_error_three(a,sa,b,sb,c,sc):
    result=a+b+c
    error=math.sqrt(sa*sa+sb*sb+sc*sc)
    return (result,error)
# done function

def sum_list(list_value):
    result=0.0
    for value in list_value:
        result+=value
    return result
# done function

def sum_error_list(list_tuple,debug=False):
    sum=0.0
    sumErrorSquared=0.0
    for tuple in list_tuple:
        value=tuple[0]
        error=tuple[1]
        sum+=value
        sumErrorSquared+=error*error # for sum errors are added in quadrature (like at histo bins)
    # done loop over entries
    sumError=math.sqrt(sumErrorSquared)
    result=(sum,sumError)
    if debug:
        print "result",result,"input",list_tuple
    return result
# done function

def average(a,b):
    return 0.5*(a+b)
# done function

def average_error(a,sa,b,sb):
    result=0.5*(a+b)
    error=0.5*math.sqrt(sa*sa+sb*sb)
    return (result,error)
# done function

def average_error_three(a,b,c):
    return (1.0/3)*(a+b+c)
# done function

def average_error_three(a,sa,b,sb,c,sc):
    result=(1.0/3)*(a+b+c)
    error=(1.0/3)*math.sqrt(sa*sa+sb*sb+sc*sc)
    return (result,error)
# done function

def average_list(list_value):
    result=0.0
    for value in list_value:
        result+=value
    result/=len(list_value)
    return result
# done function

def average_error_list(list_tuple,debug=False):
    sum=0.0
    sumErrorSquared=0.0
    for tuple in list_tuple:
        value=tuple[0]
        error=tuple[1]
        sum+=value
        sumErrorSquared+=error*error # for sum errors are added in quadrature (like at histo bins)
    # done loop over entries
    N=len(list_tuple)
    average=sum/N
    averageError=math.sqrt(sumErrorSquared)/N
    result=(average,averageError)
    if debug:
        print "average",result,"input",list_tuple
    return result
# done function

def variance_list(list_value,average):
    result=0.0
    for value in list_value:
        diff=value-average
        result+=diff*diff
    result/=len(list_value)
    return result
# done function


# add in quadrature, taking the error from error propagation formula
# https://en.wikipedia.org/wiki/Propagation_of_uncertainty

def add_in_quadrature(a,b):
  return math.sqrt(a*a+b*b)
# done function

def add_in_quadrature_error(a,sa,b,sb):
    result=math.sqrt(a*a+b*b)
    if result==0:
        error=0.0
    else:
        # from error propagation formula
        # in other writing: (f*sf)^2=(a*sa)^2+(b*sb)^2
        error=math.sqrt(a*a*sa*sa+b*b*sb*sb)/result
    return result,error
# done function

def add_in_quadrature_three(a,b,c):
  return math.sqrt(a*a+b*b+c*c)
# done function

def add_in_quadrature_error_three(a,sa,b,sb,c,sc):
    result=math.sqrt(a*a+b*b+c*c)
    if result==0:
        error=0.0
    else:
        # from error propagation formula
        # in other writing: (f*sf)^2=(a*sa)^2+(b*sb)^2+(c*sc)^2
        error=math.sqrt(a*a*sa*sa+b*b*sb*sb+c*c*sc*sc)/result
    return result,error
# done function

def add_in_quadrature_list(list_value,debug=False):
    result=0.0
    for value in list_value:
        result+=value*value
    # done loop over entries
    result=math.sqrt(result)
    if debug:
        print "add_in_quadrature",result,"from input",list_value
    return result
# done function

def add_in_quadrature_error_list(list_tuple,debug=False):
    result=0.0
    resultError=0.0
    for tuple in list_tuple:
        value=tuple[0]
        valueError=tuple[1]
        result+=value*value
        resultError+=(value*valueError)*(value*valueError)
    # done loop over entries
    result=math.sqrt(result)
    if result==0:
        resultError=0.0
    else:
        resultError=math.sqrt(resultError)/result
    if debug:
        print "add_in_quadrature",(result,resultError),"from input",list_tuple
    return (result,resultError)
# done function

def print_figures_of_merit(s,b):
    print "s",s,"b",b,"sensitivity",sensitivity(s,b),"significance",significance(s,b)
# done function

# very much used in statistics and measurement in science
# average two or more measurements given their uncertainty
# https://physics.stackexchange.com/questions/15197/how-do-you-find-the-uncertainty-of-a-weighted-average
# http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf
# for example for two measurements
# x1+/-e1; x2+/-e2
# w1=1.0/(e1*e1); w2=1.0/(e2*e2)
# mu=x1w1+x2w2/(w1+w2)
# e=1.0/sqrt(w1+w2)
# if at least one weight is zero, return normal average
def get_average_weighted_by_uncertainties(list_tuple,debug=False):
    if debug:
        print "Calculated average weighted by their uncertainties for", list_tuple
    weightedsum=0.0
    sumofweights=0.0
    # check all weights are at least zero or positive
    for value,error in list_tuple:
        if debug:
            print "new value",value,"error",error
        if error<0:
            print "error",error,"should be zero or positive. Will ABORT!!!"
            assert(False)
    areAllWeightsPositive=True
    # check if all weights are True
    for value,error in list_tuple:
        if debug:
            print "new value",value,"error",error
        if error==0:
            areAllWeightsPositive=False
    # start if
    if areAllWeightsPositive==False:
    # if not all weights are positive, return regular average
        valueSum=0.0
        valueErrorSquared=0.0
        for value,error in list_tuple:
            if debug:
                print "new value",value,"error",error
            valueSum+=valueSum
            valueErrorSquared+=error*error
        # done for loop
        NrElements=len(list_tuple)
        average=valueSum/NrElements
        average=math.sqrt(valueErrorSquared)/NrElements
    else:
        # if all weights are positive return weighted average
        for value,error in list_tuple:
            if debug:
                print "new value",value,"error",error
            weight=1.0/(error*error)
            if debug:
                print "weight",weight
            weightedsum+=weight*value
            sumofweights+=weight
            if debug:
                print "weightedsum",weightedsum
                print "sumofweights",sumofweights
            # done loop
            average=weightedsum/sumofweights
            error=1.0/math.sqrt(sumofweights)
    # done if normal average (if at least one weight of zero) or weighted average (if all weights are larger than zero)
    if debug:
        print "average",average,"error",error
    return average,error
# done function

def get_duration_of_run(time_start,time_previous,option,debug):
  if option=="start":
    time_first=time_start
  elif option=="current":
    time_first=time_previous
  else:
    print "Option",option,"not known in get_duration_of_run(...). Choose start or current. Will ABORT!!!"
    assert(False)
  # done if
  time_current=time()
  if debug:
    print "current",time_current,"first",time_first,"previous",time_previous
  seconds=time_current-time_first
  minutes=seconds/60.0
  hours=minutes/60.0
  result="%-.0f s. %-.1f min. %-.3f h." % (seconds,minutes,hours)
  time_previous=deepcopy(time_current)
  if debug:
    print "result",result
  return time_previous,result
# done function

def get_list_fileFromFolder(inputFolderName,fileSearch="*.root",debug=False):
    result=[]
    proc = subprocess.Popen(["ls -1 "+inputFolderName+"/"+fileSearch], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if debug:
        print type(out),out
    for file in out.split():
        if debug:
            print "file",file
        result.append(file.strip('\n'))
    # the file name contains full path
    if debug:
        print "list_file:"
        for file in result:
            print file
    return result
# done function

# optionOpenFile="w" # create from scratch, "a", append to an already existing file
# in which case be sure to name the list differently
def get_python_list_filesFromFolder(inputFolderName,fileSearch="*.root",
                                    outputFileName="list.py",optionOpenFile="w",
                                    listName="list_outputFile",
                                    debug=False):
    outputFile=open(outputFileName,optionOpenFile)
    if optionOpenFile=="w":
        line="#!/usr/bin/python\n"
        outputFile.write(line)
    elif optionOpenFile=="a":
        # will append
        None
    else:
        print "optionOpenFile",optionOpenFile,"not known. Choose w (rewrite), a (append). Will ABORT!!!"
        assert(False)
    # end if
    line=" \n"
    outputFile.write(line)
    line=listName+"=[\n"
    outputFile.write(line)
    list_fileName=get_list_fileFromFolder(inputFolderName,fileSearch,debug)
    for fileName in list_fileName:
        print "fileName",fileName
        line="    \""+fileName+"\",\n"
        outputFile.write(line)
    # done loop over files
    line="]\n"
    outputFile.write(line)
    outputFile.close()
    if True:
        print "File ",outputFileName,"has been created."
# done function

def get_list_from_file(fileName,debug=False):
    # it assumes there is one element per line
    list_line=[]
    for line in open(fileName, 'r'):
        line=line.rstrip()
        if debug:
            print "line",line
        list_line.append(line)
    # done for loop over lines
    if debug:
        print "list_line",list_line
    return list_line
# done function
