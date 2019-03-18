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

debug=False
verbose=False
fileName="./input/data.txt"

# 0 plot their absolute values; 1 scale to first entry to compare relative performance
# list_option="0,1".split(",") 
list_option="0".split(",")
list_environment=[
    "City",
    "Highway",
    "Combined",
]

# physics parameters
dict_environment_Velocity={
    # in miles per hour 
    "City": 31.0, # ~50 km/h
    "Highway":56.0, # ~90 km/h
    "Combined":43.0, # ~70 km/h
} 
dict_environment_PowerComputing={
    # in W (Watt)
    "City": 2500.0,
    "Highway":1500.0,
    "Combined":2000.0,
} 

list_plot=[
    "Range",
    "Consumption",
    "EnergyBattery",
    "Duration",
    "EnergyComputing",
    "ComputingFraction",
]
dict_plot_list_name={
    "Range":["Range_City","Range_Combined","Range_Highway"],
    "Consumption":["Consumption_City","Consumption_Combined","Consumption_Highway"],
    "EnergyBattery":["EnergyBattery_City","EnergyBattery_Combined","EnergyBattery_Highway"],
    "Duration":["Duration_City","Duration_Combined","Duration_Highway"],
    "EnergyComputing":["EnergyComputing_City","EnergyComputing_Combined","EnergyComputing_Highway"],
    "ComputingFraction":["ComputingFraction_City","ComputingFraction_Combined","ComputingFraction_Highway"],
}

list_color=["r","b","g"]

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
            if debug or verbose:
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

def extend_dict_name_nparray_value(dict_name_nparray_value):
    for environment in list_environment:
        Velocity=dict_environment_Velocity[environment]
        PowerComputing=dict_environment_PowerComputing[environment]
        dict_name_nparray_value["EnergyBattery_"+environment]=dict_name_nparray_value["Range_"+environment]*dict_name_nparray_value["Consumption_"+environment]*ratio(1,100.0)
        dict_name_nparray_value["Duration_"+environment]=dict_name_nparray_value["Range_"+environment]*ratio(1.0,Velocity)
        dict_name_nparray_value["EnergyComputing_"+environment]=dict_name_nparray_value["Duration_"+environment]*ratio(PowerComputing,1000.0)
        dict_name_nparray_value["ComputingFraction_"+environment]=dict_name_nparray_value["EnergyComputing_"+environment]/dict_name_nparray_value["EnergyBattery_"+environment]

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
    xAxisName=list_name[0]
    if debug:
        print "xAxisName",xAxisName
    x=range(len(dict_name_nparray_value[xAxisName]))
    if debug:
        print "x",x
        print "list_plot",list_plot
    for plot in list_plot:
        plot_list_name=dict_plot_list_name[plot]
        if debug or verbose:
            print "plot",plot,"plot_list_name",plot_list_name
        pylab.figure(1)
        pylab.xticks(x, dict_name_nparray_value[xAxisName])
        pylab.xlabel("Electric Car brand")
        pylab.subplots_adjust(bottom=0.45)
        pylab.xticks(rotation=90)
        if debug:
            print "plot_list_name",plot_list_name
        for i,name in enumerate(plot_list_name):
            if debug:
                print "i",i,"name",name
            pylab.plot(x,scaleNPArray(dict_name_nparray_value[name],option),list_color[i],label=name)
        # done loop over name
        if "Consumption" in name:
            pylab.ylabel("Electrical energy / 100 miles no AD [kWh]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 20, 50])
        elif "Range" in name:
            pylab.ylabel("Range with a full battery charge no AD [mile]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 0, 300])
        elif "EnergyBattery" in name:
            pylab.ylabel("Energy of the charged battery [kWh]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 0, 100])
        elif "Duration" in name:
            pylab.ylabel("Duration full battery at typical v no AD [h]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 0, 10])
        elif "EnergyComputing" in name:
            pylab.ylabel("Energy AD at typical v and P [kWh]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 0, 30])
        elif "ComputingFraction" in name:
            pylab.ylabel("Ratio of AD to full battery at typical v and P [kWh]")
            pylab.legend(loc="upper right")
            pylab.axis([0, len(dict_name_nparray_value[xAxisName])-1, 0.00, 0.60])
        else:
            print "name", name,"does not find any of the options Consumption, Range, BatteryEnergy, Duration, BatteryComputing, ComputingFraction, so will ABORT!!!"
            assert(False)
        # done if
        pylab.savefig("./output/"+plot+".png")
        pylab.close()
    # done loop over plot
# done function


def doItAll():
    if debug:
        print "doItAll()"
    list_name,dict_name_nparray_value=readFile(fileName)
    dict_name_nparray_value=extend_dict_name_nparray_value(dict_name_nparray_value)
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
