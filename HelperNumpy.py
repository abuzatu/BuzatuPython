#!/usr/bin/env python3

import numpy as np

def getValues(event,listVariables,debug=False):
  if debug:
      print("listVariables",listVariables)
  return numpy.array([getattr(event,variableName) for variableName in listVariables.split(',')])
# done function

def get_numpyarray_from_listString(listString,debug=False):
  if debug:
    print("listString",listString)
  listFloat=[]
  for string in listString:
    listFloat.append(float(string))
  # done for loop
  numpyarray=numpy.array(listFloat)
  if debug:
    print("numpyarray",numpyarray)
  return numpyarray
# done function

def read_file_with_values_in_numpy_array(fileName,debug):
    # the first line gives the name of the variables, so we take it from there
    # that way we can have only one function that can read any number of data files
    # both the daily and the monthly for example
    counter=0
    f=open(fileName,"r")
    for line in f:
        line=line.rstrip()
        if debug:
            print("line",line)
        if line.startswith("#"):
            if debug or verbose:
                print("Skipping line",line)
            continue
        list_line=line.split()
        if debug:
            print("list_line",list_line)
        counter+=1
        if counter==1:
            list_name=list_line
            break
    # done loop over the file first
    if debug:
        print("list_name",list_name)
    if debug:
        print("")
        print("Start loop again over the files")
    # to plot we need numpyarrays, to create them we need lists
    dict_name_list_value={}
    for name in list_name:
        dict_name_list_value[name]=[]
    f=open(fileName,"r")
    counter=0
    for line in f:
        line=line.rstrip()
        if debug:
            print("line",line)
        if line.startswith("#"):
            print("Skipping line",line)
            continue
        counter+=1
        if counter==1:
            continue
        # now we are from the first line with values
        list_line=line.split()
        if debug:
            print("list_line",list_line)
        dict_name_value={}
        # loop over names and fill the dictionary of values in the correct format (date and floats)
        for i,name in enumerate(list_name):
            dict_name_value[name]=list_line[i]
            if i==0:
                # the first element is the product we compare, keep it as a string, so do nothing
                None
            else:
                # convert from string to float
                dict_name_value[name]=float(dict_name_value[name])
            # done if
            if debug:
                print("counter",counter,"i",i,"name",name,"value",dict_name_value[name],"type",type(dict_name_value[name]))
        # for each name, append to its list
        for name in list_name:
            if debug:
                print("name",name,"value",dict_name_value[name])
            dict_name_list_value[name].append(dict_name_value[name])
    # done for loop over all the lines
    # from lists create numpy arrays
    dict_name_nparray_value={}
    for name in list_name:
        if debug:
            print("name",name,"list_value",dict_name_list_value[name])
        if name=="Date":            
            dict_name_nparray_value[name]=np.array(dict_name_list_value[name],dtype='datetime64[D]')
            dict_name_nparray_value[name]=dict_name_nparray_value[name].astype('O')
        else:
            dict_name_nparray_value[name]=np.array(dict_name_list_value[name])
        if debug and name=="Date":
            print("name",name,"np.array",dict_name_nparray_value[name])
    # done loop over names
    # finished reading the file
    # print the output
    for name in list_name:
        if debug or True:
            # if name=="Date":
            if debug:
                print("name",name,"nparray_value",dict_name_nparray_value[name])
    # ready to return
    return list_name,dict_name_nparray_value
# done function
