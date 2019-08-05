#!/usr/bin/python
from HelperPython import *
# import for data analysis and plotting
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.gridspec as gridspec
# import pylab

# overlay two or more numpy arrays as graphs
# info_legend="best", "uppler right", "lowerleft", etc
def overlayGraphsValues(list_tupleArray,outputFileName="overlay",extensions="pdf,png",info_x=["Procent of data reduced",[0.0,1.0],"linear"],info_y=["Figure of merit of performance",[0.0,100000.0],"log"],info_legend=["best"],title="Compared performance of 3D point cloud compression",debug=False):
    if debug:
        print "Start overlayGraphsValues"
        print "outputFileName",outputFileName
        print "extensions",extensions
        print "info_x",info_x
        print "info_y",info_y
        print "info_legend",info_legend
        print "title",title
    # x axis
    x_label=info_x[0]
    x_lim=info_x[1]
    x_lim_min=x_lim[0]
    x_lim_max=x_lim[1]
    if x_lim_min==-1 and x_lim_max==-1:
        x_set_lim=False
    else:
        x_set_lim=True
    x_scale=info_x[2]
    if debug:
        print "x_label",x_label,type(x_label)
        print "x_lim_min",x_lim_min,type(x_lim_min)
        print "x_lim_max",x_lim_max,type(x_lim_max)
        print "x_set_lim",x_set_lim,type(x_set_lim)
        print "x_scale",x_scale,type(x_scale)
    # y axis
    y_label=info_y[0]
    y_lim=info_y[1]
    y_lim_min=y_lim[0]
    y_lim_max=y_lim[1]
    if y_lim_min==-1 and y_lim_max==-1:
        y_set_lim=False
    else:
        y_set_lim=True
    y_scale=info_y[2]
    if debug:
        print "y_label",y_label,type(y_label)
        print "y_lim_min",y_lim_min,type(y_lim_min)
        print "y_lim_max",y_lim_max,type(y_lim_max)
        print "y_set_lim",y_set_lim,type(y_set_lim)
        print "y_scale",y_scale,type(y_scale)
    # create empty figure
    plt.figure(1)
    # set x-axis
    plt.xlabel(x_label)
    if x_set_lim==True:
        plt.xlim(x_lim_min,x_lim_max)
    plt.xscale(x_scale)
    # set y-axis
    plt.ylabel(y_label)
    if y_set_lim==True:
        plt.ylim(y_lim_min,y_lim_max)
    plt.yscale(y_scale)
    # set title
    plt.title(title)
    # fill content of plot
    for i,tupleArray in enumerate(list_tupleArray):
        if debug:
            print "i",i,"len",len(tupleArray)
        x=tupleArray[0]
        y=tupleArray[1]
        c=tupleArray[2]
        l=tupleArray[3]
        plt.plot(x,y,c,label=l)
    # done loop over each element to plot
    # set legend
    plt.legend(loc=info_legend[0])
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print "Saving plot at",fileNameFull
        plt.savefig(fileNameFull)
    # close the figure
    plt.close()
# done function

def draw_histogram_from_nparray(nparray,outputFileName="./output_histo_from_nparray",extensions="png,pdf",nrBins=100,info_x=["x-axis","linear"],info_y=["Number of points","linear"],title="Title",debug=False,verbose=False):
    plt.hist(nparray,bins=nrBins)
    if debug:
        print "Start draw_histogram_from_nparray()"
        print "outputFileName",outputFileName
        print "extensions",extensions
        print "info_x",info_x
        print "info_y",info_y
        print "title",title
    # x_axis
    x_label,x_scale=info_x
    y_label,y_scale=info_y
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale(x_scale)
    plt.yscale(y_scale)
    # title
    plt.title(title)
    # for each extension create a plot
    for extension in extensions.split(","):
        fileNameFull=outputFileName+"."+extension
        print "Saving plot at",fileNameFull
        plt.savefig(fileNameFull)
    # close the figure
    plt.close()
# done function
