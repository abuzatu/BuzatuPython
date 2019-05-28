#!/usr/bin/python
# electric car efficiency study of battery vs milleage by Adrian Buzatu (Adrian.Buzatu@teraki.ch) 
# started on 18 March 2019
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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec

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
list_option="".split(",")
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

# overlay based on AD off or on
list_plot=[
    "Range",
    "Duration",
]

dict_plot_info={
    "Range":[["RangeNoAD","RangeWithAD"],["Range on a full charge [mile]",[0,300]]],
    "Duration":[["DurationNoAD","DurationWithAD"],["Duration on a full charge [hour]",[0,10]]],
}

# overlay based on environment
list_plot2=[
    "RangeNoAD",
    "ConsumptionNoAD",
    "EnergyBatteryCharged",
    "DurationNoAD",
    "EnergyAD",
    "FractionADToBatteryCharged",
    "FractionBatteryDriveWithAD",
    "RangeWithAD",
    "DurationWithAD",
]
#list_plot2=[]

dict_plot2_info={
    "RangeWithAD":[[],["Range with AD on a full charge [mile]",[0,300]],["upper right"]],
    "RangeNoAD":[[],["Range no AD with a full battery charge [mile]",[0,300]],["upper right"]],
    "ConsumptionNoAD":[[],["Electrical energy / 100 miles no AD [kWh]",[20,50]],["upper right"]],
    "EnergyBatteryCharged":[[],["Energy of the charged battery [kWh]",[0,100]],["upper right"]],
    "DurationNoAD":[[],["Duration no AD full battery at typical v [h",[0,10]],["upper right"]],
    "DurationWithAD":[[],["Duration with AD full battery at typical v [h]",[0,10]],["upper right"]],
    "EnergyAD":[[],["Energy of AD at typical v and P [kWh]",[0,30]],["upper right"]],
    "FractionADToBatteryCharged":[[],["Ratio of AD energy to full battery",[0,0.60]],["upper right"]],
    "FractionBatteryDriveWithAD":[[],["Fraction of battery for drive when AD is on",[0.30,1.00]],["lower right"]],
}

list_color=["b","r","g"]

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

def extend_dict_name_nparray_value(dict_name_nparray_value):
    for environment in list_environment:
        Velocity=dict_environment_Velocity[environment]
        PowerComputing=dict_environment_PowerComputing[environment]
        dict_name_nparray_value["EnergyBatteryCharged_"+environment]=dict_name_nparray_value["RangeNoAD_"+environment]*dict_name_nparray_value["ConsumptionNoAD_"+environment]*ratio(1,100.0)
        dict_name_nparray_value["DurationNoAD_"+environment]=dict_name_nparray_value["RangeNoAD_"+environment]*ratio(1.0,Velocity)
        dict_name_nparray_value["EnergyAD_"+environment]=dict_name_nparray_value["DurationNoAD_"+environment]*ratio(PowerComputing,1000.0)
        dict_name_nparray_value["FractionADToBatteryCharged_"+environment]=dict_name_nparray_value["EnergyAD_"+environment]/dict_name_nparray_value["EnergyBatteryCharged_"+environment]
        dict_name_nparray_value["FractionBatteryDriveWithAD_"+environment]=(dict_name_nparray_value["EnergyBatteryCharged_"+environment]-dict_name_nparray_value["EnergyAD_"+environment])/dict_name_nparray_value["EnergyBatteryCharged_"+environment]
        dict_name_nparray_value["RangeWithAD_"+environment]=dict_name_nparray_value["RangeNoAD_"+environment]*dict_name_nparray_value["FractionBatteryDriveWithAD_"+environment]
        dict_name_nparray_value["DurationWithAD_"+environment]=dict_name_nparray_value["DurationNoAD_"+environment]*dict_name_nparray_value["FractionBatteryDriveWithAD_"+environment]
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

def testPlot2():
    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    
    # definitions for the axes
    left, width = 0.07, 0.65
    bottom, height = 0.1, .8
    bottom_h = left_h = left+width+0.02
    
    rect_cones = [left, bottom, width, height]
    rect_box = [left_h, bottom, 0.17, height]
    
    fig = plt.figure()
    
    cones = plt.axes(rect_cones)
    box = plt.axes(rect_box)
    
    cones.plot(x, y)
    
    box.plot(y, x)
    
    plt.show()

def testPlot4():
    # generate some data
    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    # plot it
    fig = plt.figure(figsize=(8, 6)) 
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 
    ax0 = plt.subplot(gs[0])
    ax0.plot(x, y)
    ax1 = plt.subplot(gs[1])
    ax1.plot(y, x)
    plt.tight_layout()
    plt.savefig('grid_figure.pdf')
# done function

def testPlot3():
    fig = Figure()
    canvas = FigureCanvas(fig)
    plt.subplot(211)
    plt.subplot(213)
    plt.show()
    #ax.plot([1, 2, 3])
    #ax.set_title('hi mom')
    ##ax.grid(True)
    #ax.set_xlabel('time')
    #ax.set_ylabel('volts')
    #canvas.print_figure('test')
# done function

def overlayGraphsTest(nparray_value_x,list_tuple_y,fileName="overlay",extensions="pdf,png",info_x=["Electric Car brand",0.45,90],info_y=["Range on a full charge [mile]",[0,300]],info_legend=["upper right"]):
    if debug:
        print "Start overlayGraphs"
    N=len(nparray_value_x)
    x=range(N)
    # create empty figure
    pylab.figure(1)
    # split into two
    gs = gridspec.GridSpec(4, 1, height_ratios=[1, 1]) 
    # in top bad to the regular plot
    ax1 = pylab.subplot(gs[0])
    # draw the x axis and its labels
    pylab.xticks(x,nparray_value_x)
    pylab.xlabel(info_x[0])
    pylab.subplots_adjust(bottom=info_x[1])
    pylab.xticks(rotation=info_x[2])
    # draw values on the y axis
    for i,tuple_y in enumerate(list_tuple_y):
        pylab.plot(x,tuple_y[0],list_color[i],label=tuple_y[1])
    # draw the Y axis label
    pylab.ylabel(info_y[0])
    # set the range for the Y axis
    pylab.axis([0,N-1,info_y[1][0],info_y[1][1]])
    # set position of the legend
    pylab.legend(loc=info_legend[0])
    # below
    ax2 = pylab.subplot(gs[1])
    # pylab.xticks(x,nparray_value_x)
    # pylab.xlabel(info_x[0])
    # pylab.subplots_adjust(bottom=info_x[1])
    # pylab.xticks(rotation=info_x[2])
    # draw values on the y axis
    for i,tuple_y in enumerate(list_tuple_y):
        pylab.plot(x,tuple_y[0],list_color[i],label=tuple_y[1])
    # draw the Y axis label
    # pylab.ylabel(info_y[0])
    # set the range for the Y axis
    pylab.axis([0,N-1,0.0,1.0])
    # set position of the legend
    #pylab.legend(loc=info_legend[0])
    # for each extension create a plot
    for extension in extensions.split(","):
        pylab.savefig(fileName+"."+extension)
    # close the figure
    pylab.close()
# done function

def overlayGraphs(nparray_value_x,list_tuple_y,fileName="overlay",extensions="pdf,png",info_x=["Electric Car brand",0.45,90],info_y=["Range on a full charge [mile]",[0,300]],info_legend=["upper right"]):
    if debug:
        print "Start overlayGraphs"
    N=len(nparray_value_x)
    x=range(N)
    # create empty figure
    pylab.figure(1)
    # draw the x axis and its labels
    pylab.xticks(x,nparray_value_x)
    pylab.xlabel(info_x[0])
    pylab.subplots_adjust(bottom=info_x[1])
    pylab.xticks(rotation=info_x[2])
    # draw values on the y axis
    for i,tuple_y in enumerate(list_tuple_y):
        pylab.plot(x,tuple_y[0],list_color[i],label=tuple_y[1])
    # draw the Y axis label
    pylab.ylabel(info_y[0])
    # set the range for the Y axis
    pylab.axis([0,N-1,info_y[1][0],info_y[1][1]])
    # set position of the legend
    pylab.legend(loc=info_legend[0])
    # for each extension create a plot
    for extension in extensions.split(","):
        pylab.savefig(fileName+"."+extension)
    # close the figure
    pylab.close()
# done function

def doPlot(dict_name_nparray_value,list_name,option):
    if debug or verbose:
        print "Start doPlot"
    # x axis will be the same for all types of plots
    xAxisName=list_name[0]
    if debug:
        print "xAxisName",xAxisName
    nparray_value_x=dict_name_nparray_value[xAxisName]
    if debug:
        print "x-axis:"
        print nparray_value_x
    # y axis will vary from plots to plots
    # plot - overlay witout and with AD, for each environment and variable of interest
    for environment in list_environment:
        for plot in list_plot:
            info=dict_plot_info[plot]
            list_var=info[0]
            info_y=info[1]
            list_tuple_y=[]
            for var in list_var:
                list_tuple_y.append([dict_name_nparray_value[var+"_"+environment],var+"_"+environment])
            fileName="./output/overlay_AD_"+plot+"_"+environment
            overlayGraphs(nparray_value_x,list_tuple_y,fileName=fileName,extensions="png",info_x=["Electric Car brand",0.45,90],info_y=info_y,info_legend=["upper right"])
    # plotEnvironment - overlay the three enviroments for each variable of interest
    for plot2 in list_plot2:
        var=plot2
        info=dict_plot2_info[plot2]
        info_y=info[1]
        info_legend=info[2]
        list_tuple_y=[]
        for environment in list_environment:
            list_tuple_y.append([dict_name_nparray_value[var+"_"+environment],environment])
        fileName="./output/overlay_environment_"+plot2
        overlayGraphs(nparray_value_x,list_tuple_y,fileName=fileName,extensions="png",info_x=["Electric Car brand",0.45,90],info_y=info_y,info_legend=info_legend)
# done function

def doItAll():
    if debug:
        print "doItAll()"
    list_name,dict_name_nparray_value=readFile(fileName)
    dict_name_nparray_value=extend_dict_name_nparray_value(dict_name_nparray_value)
    #if False:
    #    testPlot()
    #if True:
    #    testPlot2()
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
