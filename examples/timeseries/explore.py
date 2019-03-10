#!/usr/bin/python
# time series analysis step by step example by Adrian Buzatu (Adrian.Buzatu@cern.ch) 
# started on 10 March 2019
# not using directly pandas, but starting with simple Python to read data files
# but using numpy and matplotlib
# later pandas, DataFrame and Jupyter notebook

#################################################################
################### Includes       ##############################
#################################################################

# import basic python
import sys
# import for data analysis and plotting
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

#################################################################
################### Command line arguemnts ######################
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

debug=False
verbose=True
fileNameDaily="./input/study_case_daily.txt"
fileNameMonthly="./input/study_case_monthly.txt"
# 0 plot their absolute values; 1 scale to first entry to compare relative performance
# list_option="0,1".split(",") 
list_option="1".split(",")
list_plot=[
    "A",
    "B",
    "C",
    "D",
]
dict_plot_list_name={
    "A":["Soybean","Corn","CrudeOil","DXY","S&P500"],
    "B":["Soybean","Corn"],
    "C":["Soybean"],
    "D":["Soybean","Corn","CrudeOil","DXY","S&P500","StockToUse"],
}


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
            dict_name_nparray_value[name]=dict_name_nparray_value[name].astype('O')
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
    return list_name,dict_name_nparray_value
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

def scaleNPArray(nparray,option="0"):
    first=nparray[0]
    if option=="0":
        # do nothing
        scaled_nparray=nparray
    elif option=="1":
        # scale all values relative to the first entry, so that the first entry is one
        scaled_nparray=nparray*ratio(1.0,first)
    else:
        print "In scaleNPArray(), option",option,"not known. Choose 0 or 1. Will ABORT!!!"
        assert(False)
    # done if
    if debug:
        print "scaled_nparray",scaled_nparray
    return scaled_nparray
# done function

def doPlot(dict_name_nparray_value_daily,list_name_daily,dict_name_nparray_value_monthly,list_name_monthly,option):
    if debug or verbose:
        print "Start doPlot"
    # 
    # Soybean has two big dips. Looking quickly through the values does not spot them. 
    # So let's use the computer to plot when the change with respect to the previous value is more than 10%, then we will tune the value
    previous_value=1.0
    for i,value in enumerate(scaleNPArray(dict_name_nparray_value_daily["Soybean"],option)):
        if debug:
            print "value",value
        if abs(value/previous_value-1)>0.30:
            print i,"previous_value",previous_value,"current_value",value
    # with this I found the two values that were 10 times lower, it seems like a typo when introducing the values
    # this gives
    # 154 previous_value 1.0 current_value 0.0976628091672
    # 905 previous_value 1.0 current_value 0.093215339233
    # then we open the input file with emacs -nw and we go to that line with M-x goto-line: 154
    # 28/07/14       107.6   428.25          88.52   81.029999       1978.910034
    # so we modify by hand 107.6 to 1076.0
    # also 
    # 20/07/17        102.7   404.75          47.34   94.269997       2473.449951
    # so we modify 102.7 to 1027.0
    #
    # and for stock to use, fill the missing data of Oct 2013 due to government showdown with the average of the periods before and after
    # and also a factor of 10 on this line 10/01/14        0.453995157, replacing with 10/01/14        0.045399516
    xAxisName="Date"
    for plot in list_plot:
        list_name=dict_plot_list_name[plot]
        if debug or verbose:
            print "list_name",list_name
        fig=plt.figure()
        for name in list_name:
            if name=="Date":
                continue
            if name=="StockToUse":
                # from the monthly
                plt.plot(dict_name_nparray_value_monthly[xAxisName],scaleNPArray(dict_name_nparray_value_monthly[name],option),label=name)
            else:
                # from the daily
                plt.plot(dict_name_nparray_value_daily[xAxisName],scaleNPArray(dict_name_nparray_value_daily[name],option),label=name)
        # done loop over name
        plt.xlabel(xAxisName)
        plt.ylabel("Value at that particular day")
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        plt.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.title("Time series of values as a function of day")
        if plot=="D":
            plt.legend(loc="upper right")
        else:
            plt.legend(loc="lower left")
        # plt.show() # shows in GUI, but for script we want to store in file
        plt.savefig("./output/overlay_daily_"+plot+"_"+option+".png",bbox_inches='tight')
        plt.close()
    # done loop over plot
# done function


def doItAll():
    if debug:
        print "doItOne() with option",option
    list_name_daily,dict_name_nparray_value_daily=readFile(fileNameDaily)
    list_name_monthly,dict_name_nparray_value_monthly=readFile(fileNameMonthly)
    if False:
        testPlot()
    for option in list_option:
        if debug:
            print "option",option
        doPlot(dict_name_nparray_value_daily,list_name_daily,dict_name_nparray_value_monthly,list_name_monthly,option)
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
