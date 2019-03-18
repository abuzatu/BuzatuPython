#!/usr/bin/python
# electric car efficiency study of battery vs milleage by Adrian Buzatu (Adrian.Buzatu@teraki.ch) 
# started on 19 March 2019
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
import pylab
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

debug=True
verbose=True
fileName="./input/data.txt"
# 0 plot their absolute values; 1 scale to first entry to compare relative performance
# list_option="0,1".split(",") 
list_option="0".split(",")
list_plot=[
    "A",
    #"B",
    #"C",
    #"D",
]
dict_plot_list_name={
    "A":["Range_City"],
    "B":["Range_City","Range_Highway"],
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
        if line.startswith("#"):
            print "Skipping line",line
            continue
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
        if line.startswith("#"):
            print "Skipping line",line
            continue
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
            if i==0:
                # the first element is the product we compare, keep it as a string, so do nothing
                None
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

def doPlot(dict_name_nparray_value,list_name,option):
    if debug or verbose:
        print "Start doPlot"
    #names = ['anne','barbara','cathy']
    #counts = [3230,2002,5456]
    doConsumption=True
    doRange=False
    if True:
        pylab.figure(1)
        x=range(len(dict_name_nparray_value["Car"]))
        pylab.xticks(x, dict_name_nparray_value["Car"])
        if doConsumption:
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Consumption_City"],option),"r",label="Consumption_City")
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Consumption_Combined"],option),"b",label="Consumption_Combined")
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Consumption_Highway"],option),"g",label="Consumption_Highway")
        if doRange:
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Range_City"],option),"r",label="Range_City")
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Range_Combined"],option),"b",label="Range_Combined")
            pylab.plot(x,scaleNPArray(dict_name_nparray_value["Range_Highway"],option),"g",label="Range_Highway")
        #pylab.plot(x,scaleNPArray(dict_name_nparray_value["Range_Combined"],option),"r",label="Range_Combined")
        #pylab.plot(x,scaleNPArray(dict_name_nparray_value["Range_Combined"],option),"g",label="Range_Combined")
        pylab.xlabel("Electric Car brand")
        if doConsumption:
            pylab.ylabel("Electrical energy used per 100 miles")
        if doRange:
            pylab.ylabel("Range in miles with a full battery charge")
        pylab.subplots_adjust(bottom=0.45)
        pylab.xticks(rotation=90)
        if doConsumption:
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value["Car"])-1, 20, 50])
            pylab.savefig("Consumption.png")
        if doRange:
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value["Car"])-1, 0, 300])
            pylab.savefig("Range.png")
        pylab.close()
        return
    #for tick in pylab.get_xticklabels():
    #    tick.set_rotation(45)
    #x = range(len(time))
    #plt.xticks(x,  time)
    #locs, labels = plt.xticks()
    #plt.setp(labels, rotation=90)
    #plt.plot(x, delay)

    xAxisName=list_name[0]
    print "xAxisName",xAxisName
    x=range(len(dict_name_nparray_value["Car"]))
    #plt.plot(dict_name_nparray_value["Car"],scaleNPArray(dict_name_nparray_value["Range_Combined"],option),label="Range_Combined")
    #plt.savefig("test.png")
    #plt.close()
    #return
    for plot in list_plot:
        plot_list_name=dict_plot_list_name[plot]
        if debug or verbose:
            print "plot",plot,"plot_list_name",plot_list_name
        #fig=plt.figure()
        pylab.figure(1)
        for i,name in enumerate(plot_list_name):
            print "i",i,"name",name
            if i==0:
                # the product we want to put on the horisontal axis
                continue
            else:
                print "i",i,"name",name
                # the values for the different products
                pylab.xticks(x, dict_name_nparray_value[xAxisName])
                pylab.plot(x,scaleNPArray(dict_name_nparray_value["Consumption_Combined"],option),"g",label="bla")
                # pylab.plot(dict_name_nparray_value[xAxisName],scaleNPArray(dict_name_nparray_value[name],option),label=name)
                #plt.plot(dict_name_nparray_value[xAxisName],scaleNPArray(dict_name_nparray_value[name],option),label=name)
                # plt.plot(scaleNPArray(dict_name_nparray_value[name],option),scaleNPArray(dict_name_nparray_value[name],option),label=name)
                #plt.plot(scaleNPArray(list_name,scaleNPArray(dict_name_nparray_value[name],option),label=name)
        # done loop over name
        pylab.subplots_adjust(bottom=0.45)
        pylab.xticks(rotation=90)
        #plt.xlabel(xAxisName)
        #plt.ylabel("Value at that particular day")
        # rotate and align the tick labels so they look better
        #fig.autofmt_xdate()
        #plt.title("Time series of values as a function of day")
        if plot=="D":
            plt.legend(loc="upper right")
        else:
            plt.legend(loc="lower left")
        # plt.show() # shows in GUI, but for script we want to store in file
        plt.savefig("./output/overlay_"+plot+"_"+option+".png",bbox_inches='tight')
        plt.close()
    # done loop over plot
# done function


def doItAll():
    if debug:
        print "doItAll()"
    list_name,dict_name_nparray_value=readFile(fileName)
    #if False:
    #    testPlot()
    for option in list_option:
        if debug:
            print "option",option
        doPlot(dict_name_nparray_value,list_name,option)
    #None
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
