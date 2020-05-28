#!/usr/bin/env python3

import numpy as np

def print_numpy(name,array):
  print("numpy_array: "+name)
  print(array)
  print("type",type(array),"len",len(array),"dtype",array.dtype,"shape",array.shape,"min",np.min(array),"max",np.max(array),"avg",np.mean(array))
# done function

def print_nparray(name,nparray):
  print("Start nparray: "+name)
  print(nparray)
  print("type",type(nparray),"len",len(nparray),"dtype",nparray.dtype,"shape",nparray.shape,"min",np.min(nparray),"max",np.max(nparray),"avg",np.mean(nparray))
  print("End   nparray: "+name)
# done function

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

# return a structured numpy array from a dictionary between keys and lists of values
# example:
# debug=False
# dict_key_list_value={
#     "a":[1.4,1.2,1.15,1.1,1.0,0.8,0.6,0.5],
#     "b":[10.2,10.0,9.8,8.55,6.44,6.20,5.44,3.22],
#     "c":[6,5,4.9,4.8,4.6,6.5,6.8,7.2],
# }
# numpy_structured_array=get_structured_numpy_array_from_dictionary_key_list_value(dict_key_list_value,'f8',debug)
# np.save("a.npy",numpy_structured_array)
# numpy_structured_array_2=np.load("a.npy")
# print("numpy_structured_array_2","type",type(numpy_structured_array_2),"shape",numpy_structured_array_2.shape,":")
# print(numpy_structured_array_2)
def get_structured_numpy_array_from_dictionary_key_list_value(dict_key_list_value,format="f8",debug=False):
    # first check that all the lists have the same number of elements, else crash
    # then create the list of names and formats and append each key to that
    list_name=[]
    list_format=[]
    for i,key in enumerate(sorted(dict_key_list_value.keys())):
        list_value=dict_key_list_value[key]
        len_list_value=len(list_value)
        if i==0:
            reference_key=key
            reference_len_list_value=len_list_value
        else:
            # check if the current number of elements equals that of the list
            if len_list_value != reference_len_list_value:
                print("ERROR! In dictionary key(",key,") has",len_list_value,"elements, different from first key in alphabetical order (", reference_key, "), which has ",reference_len_list_value," elements. We will ABORT!!!")
                assert(False)
            # done if
        # done if
        list_name.append(key)
        list_format.append(format)
    # done for all elements in the dictionary
    if debug:
        print("list_name","type",type(list_name),"len",len(list_name),":")
        print(list_name)
        print("list_format","type",type(list_format),"len",len(list_format),":")
        print(list_format)
    #
    # create the dtype of the dictionary
    dtype=list(zip(list_name, list_format))
    if debug:
        print("dtype","type",type(dtype),"len",len(dtype),":")
        print(dtype)
    # create the data inside, as a list of tuples, where one tuples is one row
    # meaning one value for each vertical axis, so for each name
    # use a list comprehension that inside uses a list comprehension
    list_tuple_value=[tuple([dict_key_list_value[name][i] for name in list_name]) for i in range(reference_len_list_value)]
    if debug:
        print("list_tuple_value","type",type(list_tuple_value),"len",len(list_tuple_value),":")
        print(list_tuple_value)
    nparray_structured_array=np.array(list_tuple_value,dtype=dtype)
    if debug:
        print("nparray_structured_array","type",type(nparray_structured_array),"shape",nparray_structured_array.shape,":")
        print(nparray_structured_array)
    # all done, ready to return
    return nparray_structured_array
# done function
