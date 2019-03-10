#!/usr/bin/python
from HelperPython import *
# sphinx_gallery_thumbnail_number = 3
import matplotlib.pyplot as plt
import numpy as np


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

#################################################################
################### Functions ###################################
#################################################################

def readFileDaily(fileName):
    dict_date_name_values={}
    f=open(fileName,"r")
    for line in f:
        line=line.rstrip()
        if debug:
            print "line",line
        list_line=line.split()
        if debug:
            print "list_line",list_line
        dateString                  =list_line[0]
        dict_name_values={}
        dict_name_values["soybean"] =list_line[1]
        dict_name_values["corn"]    =list_line[2]
        dict_name_values["crudeOil"]=list_line[3]
        dict_name_values["DXY"]     =list_line[4]
        dict_name_values["S&P500"]  =list_line[5]
        if debug:
            print "dateString",dateString,"dict_name_values",dict_name_values
        dict_date_name_values[dateString]=dict_name_values
    # done for loop over all the lines
    if debug:
        print "List content of dictionary:"
        for date in dict_date_name_values:
            print date,dict_date_name_values[date]
# done function

def readFileMonthly(fileName):
    dict_date_name_values={}
    f=open(fileName,"r")
    for line in f:
        line=line.rstrip()
        if debug:
            print "line",line
        list_line=line.split()
        if debug:
            print "list_line",list_line
        dateString                  =list_line[0]
        dict_name_values={}
        dict_name_values["stockToUse"] =list_line[1]
        if debug:
            print "dateString",dateString,"dict_name_values",dict_name_values
        dict_date_name_values[dateString]=dict_name_values
    # done for loop over all the lines
    if debug:
        print ""
        print "List content of dictionary:"
        for date in dict_date_name_values:
            print date,dict_date_name_values[date]
# done function

def testPlot():
    fig = plt.figure()  # an empty figure with no axes
    #fig.suptitle('No axes on this figure')  # Add a title so we know which it is
    #fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
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

def doItOne(option):
    if debug:
        print "doItOne() with option",option
    # readFileDaily(fileNameDaily)
    readFileMonthly(fileNameMonthly)
    testPlot()
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
