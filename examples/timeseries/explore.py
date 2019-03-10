#!/usr/bin/python
# time series analysis step by step example by Adrian Buzatu (Adrian.Buzatu@cern.ch) 
# started on 10 March 2019
# not using directly pandas, but starting with simple Python to read data files
# but using numpy and matplotlib
# later pandas, DataFrame and Jupyter notebook

#################################################################
################### Configurations ##############################
#################################################################

# import basic python
import sys
# import for data analysis and plotting
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

#################################################################
################### Configurations ##############################
#################################################################

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
# list_option="A,B,C".split(",")
list_option="A".split(",")
fileNameDaily="./input/study_case_daily.txt"
fileNameMonthly="./input/study_case_monthly.txt"
doStartFromUnity=False


#################################################################
################### Functions ###################################
#################################################################

def ratio(a,b):
    result=0.0
    if b==0:
        print "WARNING, division by zero, will return 0.0!"
        result=0.0
    else:
        result=a/b
    return result
# done function

def readFile(fileName):
    # the first line gives the name of the variables, so we take it from there
    # that way we can have only one function that can read any number of data files
    # both the daily and the monthly for example
    counter=0
    f=open(fileName,"r")
    for line in f:
        line=line.rstrip()
        if debug:
            print "line",line
        list_line=line.split()
        if debug:
            print "list_line",list_line
        counter+=1
        if counter==1:
            list_name=list_line
            break
    # done loop over the file first
    if debug:
        print "list_name",list_name
    if debug:
        print ""
        print "Start loop again over the files"
    # to plot we need numpyarrays, to create them we need lists
    dict_name_list_value={}
    for name in list_name:
        dict_name_list_value[name]=[]
    f=open(fileName,"r")
    counter=0
    for line in f:
        line=line.rstrip()
        if debug:
            print "line",line
        counter+=1
        if counter==1:
            continue
        # now we are from the first line with values
        list_line=line.split()
        if debug:
            print "list_line",list_line
        dict_name_value={}
        # loop over names and fill the dictionary of values in the correct format (date and floats)
        for i,name in enumerate(list_name):
            dict_name_value[name]=list_line[i]
            if name=="Date":
                # convert from 31/02/17 to 2017-02-31 and overwrite
                list_dateElement=dict_name_value[name].split("/")
                if debug:
                    print "list_dateElement",list_dateElement
                    dict_name_value[name]="20"+list_dateElement[2]+"-"+list_dateElement[1]+"-"+list_dateElement[0]
            else:
                # convert from string to float
                dict_name_value[name]=float(dict_name_value[name])
            # done if
            if debug:
                print "counter",counter,"i",i,"name",name,"value",dict_name_value[name],"type",type(dict_name_value[name])
        # for each name, append to its list
        for name in list_name:
            if debug:
                print "name",name,"value",dict_name_value[name]
            dict_name_list_value[name].append(dict_name_value[name])
    # done for loop over all the lines
    # from lists create numpy arrays
    dict_name_nparray_value={}
    for name in list_name:
        if debug:
            print "name",name,"list_value",dict_name_list_value[name]
        if name=="Date":            
            dict_name_nparray_value[name]=np.array(dict_name_list_value[name],dtype='datetime64[D]')
        else:
            dict_name_nparray_value[name]=np.array(dict_name_list_value[name])
        if debug and name=="Date":
            print "name",name,"np.array",dict_name_nparray_value[name]
    # done loop over names
    for name in list_name:
        if debug:
            # if name=="Date":
            if True:
                print "name",name,"nparray_value",dict_name_nparray_value[name]
    # ready to return
    return dict_name_nparray_value
# done function

def testPlot():
    fig = plt.figure()  # an empty figure with no axes
    x = np.linspace(0, 2, 100)
    plt.plot(x,x,label="linear")
    plt.plot(x,x**2,label="quadratic")
    plt.plot(x,x**3,label="cubic")
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title("Simple plot")
    plt.legend()
    plt.show()
# done function

def scaleNPArrayToHaveFirstElementAtUnity(nparray):
    first=nparray[0]
    scaled_nparray=nparray*ratio(1.0,first)
    if debug:
        print "scaled_nparray",scaled_nparray
    return scaled_nparray
# done function

def doPlot(dict_name_nparray_value_daily,dict_name_nparray_value_monthly):
    fig = plt.figure()  # an empty figure with no axes
    xAxisName="Date"
    if doStartFromUnity==True:
        plt.plot(dict_name_nparray_value_daily[xAxisName],scaleNPArrayToHaveFirstElementAtUnity(dict_name_nparray_value_daily["S&P500"]),label="Test")
        plt.plot(dict_name_nparray_value_daily[xAxisName],scaleNPArrayToHaveFirstElementAtUnity(dict_name_nparray_value_daily["Soybean"]),label="Test")
    else:
        plt.plot(dict_name_nparray_value_daily[xAxisName],dict_name_nparray_value_daily["S&P500"],label="Test")
        plt.plot(dict_name_nparray_value_daily[xAxisName],dict_name_nparray_value_daily["Soybean"],label="Test")
    plt.xlabel(xAxisName)
    plt.ylabel("Value at that particular day")
    plt.title("Time series of values as a function of day")
    plt.legend()
    # plt.show() # shows in GUI, but for script we want to store in file
    plt.savefig("./output/test.png")
# done function


def doItOne(option):
    if debug:
        print "doItOne() with option",option
    dict_name_nparray_value_daily=readFile(fileNameDaily)
    dict_name_nparray_value_monthly=readFile(fileNameMonthly)
    # testPlot()
    doPlot(dict_name_nparray_value_daily,dict_name_nparray_value_monthly)
    None
# done function

def doItAll():
    for option in list_option:
        if debug:
            print "option",option
        doItOne(option)
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
