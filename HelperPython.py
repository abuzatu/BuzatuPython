#!/usr/bin/bin python
import numpy as np
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
# shell utitiles, e.g. rmtree remove recursively in the folder
import shutil as sh
# for checking the itme stamps on the files
import datetime
# time measurement
from time import time
from timeit import default_timer as timer
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

#https://www.ics.uci.edu/~alspaugh/cls/shr/regularExpression.html
def match_regularExpression_in_string(regex, text):
    pattern = re.compile(regex, text)
    return pattern.search(text) is not None
# done function

def get_lineNumber():
    cf = currentframe()
    return cf.f_back.f_lineno
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
# done function

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
# done function

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











def concatenate_two_listString(list1,list2,debug):
  result=[]
  for i in list1:
    for j in list2:
      result.append(i+"_"+j)
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

def get_string_value(axis_name,variable_name,variable_value):
    result="%-2s  %-30s  %-.2f" % (axis_name,variable_name,variable_value)
    return result
# done function

def get_string_scale_resolution(fit_name,scale_value,resolution_value):
    result="%-7s %-.2f %-.2f" % (fit_name,scale_value,resolution_value)
    return result
# done function

# dict_A: dictionary A -> a list of B
# dict_B; dictionary B -> a list of C
# one C can appear in several of lists of C
# here we want a combined list of A where each element of A appears only once
# here we want a combined list of B where each element of B appears only once
# here we want a combined list of C where each element of C appears only once
def get_lists_with_unique_elements_from_two_nested_dictionaries(dict_A,dict_B,debug=False,verbose=False):
    list_A=dict_A.keys()
    list_B=[]
    list_C=[]
    for A in list_A:
        current_list_B=dict_A[A]
        for B in current_list_B:
            if B in list_B:
                continue
            list_B.append(B)
            current_list_C=dict_B[B]
            for C in current_list_C:
                if C in list_C:
                    continue
                list_C.append(C)
            # done loop over current_list_C
        # done for loop over current_list_B
    # done for loop over dict_A
    # sort the lists alphabetically
    list_A=sorted(list_A)
    list_B=sorted(list_B)
    list_C=sorted(list_C)
    if debug:
        print "list_A:"
        for A in list_A:
            print A
        print "list_B:"
        for B in list_B:
            print B
        print "list_C:"
        for C in list_C:
            print C
    # done if
    # all done, so return
    return list_A,list_B,list_C
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

def get_use_from_bool(option,debug=False):
    if option==True:
        result="1"
    else:
        result="0"
    if debug:
        print "option",option,"result",result
    return result
# done function

def get_today_as_string(debug=False):
    today=datetime.date.today()
    string_today=today.strftime("%d %b %Y") # e.g. 04 Aug 2019
    if debug:
        print "string_today",string_today
    return string_today
# done function

#########################################################
############### End all               ###################
#########################################################
